#!/usr/bin/env python3
"""Write every person reference under data/ in the form the RDF mapping reads.

The 2026-09 checkup verification (knowledge/DATA.md, Archive checkup) shows why this matters.
GetPersonlist in szd-TORDF.xsl emits a triple only for a value that contains "#SZDPER." or
a GND, so a reference written as ref="SZDPER.1315" is silently dropped and the person looks
unlinked in the person view although the holdings name her.

Two repairs, both mechanical:

    * every SZDPER token in an @ref gets the fragment marker, so that ref="SZDPER.1315"
      becomes ref="#SZDPER.1315" and the trailing ids of a multi-id attribute are written
      the same way as the leading one;
    * a term[@type='person'] that carries no reference of its own gets the one its inner
      persName already holds, because Work_RDF reads the term attribute and not the inner
      name.

Only the first token of an @ref reaches the RDF: GetPersonlist takes substring-before the
first space. Normalising the trailing tokens therefore changes no triple, it only makes the
writing uniform, and the ids behind the first token stay invisible to the mapping either
way.

A term reference is only lifted where the inner persName resolves to exactly one index
entry, by its own SZDPER id or through its GND. Everything else is left alone and listed:
a name with no reference at all, a GND that several index entries share, and a reference
that sits on a nested name element rather than on the persName.

Usage:

    python scripts/checkup_2026_09_index/normalize_person_refs.py            # dry run
    python scripts/checkup_2026_09_index/normalize_person_refs.py --apply
    python scripts/checkup_2026_09_index/normalize_person_refs.py --verify

Regime: script pipeline in the shape the other scripts of this repo use, standard library
only, run with plain python.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252
    sys.stdout.reconfigure(errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA = REPO_ROOT / "data"
SZDPER_FILE = DATA / "Index" / "Person" / "SZDPER.xml"
OUT_CSV = Path(__file__).resolve().parent / "normalize_log.csv"

TEI = "{http://www.tei-c.org/ns/1.0}"
XML = "{http://www.w3.org/XML/1998/namespace}"

LOG_FIELDS = ["datei", "kontext", "zeile", "alte_referenz", "neue_referenz", "aktion"]

REF_ATTR = re.compile(r'ref="(?P<value>[^"]*)"')
PLAIN_ID = re.compile(r"^SZDPER\.[0-9][0-9A-Za-z_.\-]*$")
GND_NUMBER = re.compile(r"gnd/([0-9X\-]+)")
FRAGMENT_ID = re.compile(r"#(SZDPER\.[0-9][0-9A-Za-z_.\-]*)")
BIBL_ID = re.compile(r'<(?:biblFull|person)[^>]*xml:id="([^"]+)"')
# A term element with its content; term elements do not nest.
TERM = re.compile(
    r"<term(?P<attrs>[^>]*)>(?P<inner>.*?)</term>",
    re.DOTALL,
)
TERM_TYPE = re.compile(r'type="(person|person_affected)"')
PERSNAME_REF = re.compile(r"<persName[^>]*\bref=\"(?P<value>[^\"]*)\"")


def read(path: Path) -> str:
    """Read without translating line terminators, so that a write reproduces them."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write_atomic(path: Path, text: str) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    temp.replace(path)


def person_ids_by_gnd() -> dict[str, list[str]]:
    """GND number -> the index entries that carry it, several where the index is unclean."""
    index: dict[str, list[str]] = {}
    root = ET.parse(SZDPER_FILE).getroot()
    for person in root.iter(f"{TEI}person"):
        person_id = person.get(f"{XML}id") or ""
        for pers_name in person.findall(f"{TEI}persName"):
            number = GND_NUMBER.search(pers_name.get("ref") or "")
            if number:
                index.setdefault(number.group(1), []).append(person_id)
    return index


def known_person_ids() -> set[str]:
    root = ET.parse(SZDPER_FILE).getroot()
    return {person.get(f"{XML}id") for person in root.iter(f"{TEI}person")}


def _context_id(text: str, position: int) -> str:
    matches = list(BIBL_ID.finditer(text, 0, position))
    return matches[-1].group(1) if matches else ""


def add_fragment_marker(text: str, path: Path, rows: list[dict]) -> str:
    """ref="SZDPER.42 SZDPER.43" -> ref="#SZDPER.42 #SZDPER.43"."""

    def rewrite(match: re.Match[str]) -> str:
        value = match.group("value")
        tokens = value.split()
        if not any(PLAIN_ID.match(token) for token in tokens):
            return match.group(0)
        new_value = " ".join(
            f"#{token}" if PLAIN_ID.match(token) else token for token in tokens
        )
        rows.append(
            {
                "datei": path.relative_to(REPO_ROOT).as_posix(),
                "kontext": _context_id(text, match.start()),
                "zeile": text.count("\n", 0, match.start()) + 1,
                "alte_referenz": f'@ref="{value}"',
                "neue_referenz": f'@ref="{new_value}"',
                "aktion": "Fragmentmarke ergänzt",
            }
        )
        return f'ref="{new_value}"'

    return REF_ATTR.sub(rewrite, text)


def lift_term_refs(
    text: str,
    path: Path,
    rows: list[dict],
    by_gnd: dict[str, list[str]],
    known: set[str],
    skipped: list[str],
) -> str:
    """Give a person term the reference its inner persName already carries."""

    def rewrite(match: re.Match[str]) -> str:
        attrs = match.group("attrs")
        if not TERM_TYPE.search(attrs) or re.search(r'\bref="', attrs):
            return match.group(0)
        inner = match.group("inner")
        line = text.count("\n", 0, match.start()) + 1
        where = f"{path.relative_to(REPO_ROOT).as_posix()}:{line}"
        inner_ref = PERSNAME_REF.search(inner)
        if inner_ref is None:
            name = " ".join(re.sub(r"<[^>]*>", " ", inner).split())
            skipped.append(f"{where} no reference on the inner name: {name}")
            return match.group(0)
        value = inner_ref.group("value")
        fragment = FRAGMENT_ID.search(value)
        if fragment is not None:
            person_id = fragment.group(1)
        elif PLAIN_ID.match(value):
            person_id = value
        else:
            number = GND_NUMBER.search(value)
            candidates = by_gnd.get(number.group(1), []) if number else []
            if len(candidates) != 1:
                reason = "several index entries" if candidates else "no index entry"
                skipped.append(f"{where} {reason} for {value}")
                return match.group(0)
            person_id = candidates[0]
        if person_id not in known:
            skipped.append(f"{where} {person_id} is not an index entry")
            return match.group(0)
        rows.append(
            {
                "datei": path.relative_to(REPO_ROOT).as_posix(),
                "kontext": _context_id(text, match.start()),
                "zeile": line,
                "alte_referenz": f'term/@ref fehlt, persName/@ref="{value}"',
                "neue_referenz": f'term/@ref="#{person_id}"',
                "aktion": "Verweis auf den Term gehoben",
            }
        )
        return f'<term{attrs} ref="#{person_id}">{inner}</term>'

    return TERM.sub(rewrite, text)


def process(rows: list[dict], skipped: list[str]) -> dict[Path, str]:
    by_gnd = person_ids_by_gnd()
    known = known_person_ids()
    changed: dict[Path, str] = {}
    for path in sorted(DATA.rglob("*.xml")):
        if path == SZDPER_FILE:
            continue  # the index describes persons, it does not reference the holdings
        original = read(path)
        text = add_fragment_marker(original, path, rows)
        text = lift_term_refs(text, path, rows, by_gnd, known, skipped)
        if text != original:
            ET.fromstring(text)  # trust boundary: never write what is not well formed
            changed[path] = text
    return changed


def verify() -> int:
    failures: list[str] = []
    for path in sorted(DATA.rglob("*.xml")):
        if path == SZDPER_FILE:
            continue
        text = read(path)
        try:
            ET.fromstring(text)
        except ET.ParseError as error:
            failures.append(f"{path.relative_to(REPO_ROOT).as_posix()}: not well formed, {error}")
            continue
        for match in REF_ATTR.finditer(text):
            for token in match.group("value").split():
                if PLAIN_ID.match(token):
                    line = text.count("\n", 0, match.start()) + 1
                    failures.append(
                        f"{path.relative_to(REPO_ROOT).as_posix()}:{line} "
                        f"{token} still written without the fragment marker"
                    )
    # Closure: a second pass must find nothing left to lift and nothing left to mark.
    rows: list[dict] = []
    skipped: list[str] = []
    changed = process(rows, skipped)
    for row in rows:
        failures.append(f"{row['datei']}:{row['zeile']} still open, {row['neue_referenz']}")
    if changed:
        failures.append(f"{len(changed)} files would still change")
    for note in skipped:
        print(f"NOTE  left alone by design: {note}")
    for failure in failures:
        print(f"FAIL  {failure}")
    if failures:
        return 1
    print("OK  every person reference under data/ carries the fragment marker and resolves")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--apply", action="store_true", help="write the changes")
    parser.add_argument("--verify", action="store_true", help="check the normalised state only")
    args = parser.parse_args()

    if not SZDPER_FILE.exists():
        print(f"FAIL  {SZDPER_FILE} missing", file=sys.stderr)
        return 1
    if args.verify:
        return verify()

    rows: list[dict] = []
    skipped: list[str] = []
    changed = process(rows, skipped)

    for row in rows:
        print(
            f"OK  {row['aktion']}: {row['datei']}:{row['zeile']} "
            f"{row['alte_referenz']} -> {row['neue_referenz']}"
        )
    for note in skipped:
        print(f"SKIP  {note}")
    if not rows:
        print("SKIP  nothing to do, every reference already carries the fragment marker")
        return 0
    if not args.apply:
        print(f"SKIP  dry run, {len(rows)} changes planned in {len(changed)} files")
        return 0

    for path, text in changed.items():
        write_atomic(path, text)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOG_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"OK  {OUT_CSV.relative_to(REPO_ROOT).as_posix()} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
