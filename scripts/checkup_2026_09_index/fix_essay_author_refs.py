#!/usr/bin/env python3
"""Point the author reference of every Aufsatzablage entry at the author, not at the entry.

The 2026-09 checkup verification (knowledge/DATA.md, Archive checkup) found the defect. All 403
author/@ref values in data/Aufsatzablage/SZDESS.xml repeat the sequence number of the entry
they sit in, so SZDESS.28 carries ref="#SZDPER.28", which is Hanns Arens, while the author
element names Stefan Zweig, SZDPER.1560. The wrong number does not reach the published page,
because the essay template of szd-TORDF.xsl reads the inner persName/@ref first and only
falls back to the author attribute where the persName carries none, but it makes 84 persons
look referenced in our own candidate lists when they are not.

The repair resolves the person from the inner persName: through the GND against
data/Index/Person/SZDPER.xml, or, for the two entries whose persName carries the name
"Zweig, Stefan" in the attribute meant for an identifier, through that name. Those two also
get the authority number the index entry holds, so that the persName says what the other 401
say.

Where a GND resolves to more than one index entry the author element is left as it is and
listed. Merging such duplicates is the job of merge_person_duplicates.py, and running that
script first removes the ambiguity here.

Usage:

    python scripts/checkup_2026_09_index/fix_essay_author_refs.py            # dry run
    python scripts/checkup_2026_09_index/fix_essay_author_refs.py --apply
    python scripts/checkup_2026_09_index/fix_essay_author_refs.py --verify

An applied run appends its rows to essay_author_log.csv and never rewrites it, because the log is
provenance committed with the data. The columns stay those of the existing log, without
a run date, since the commit that carries a run dates its rows.

Regime: script pipeline in the shape the other scripts of this repo use, standard library
only, run with plain python.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252
    sys.stdout.reconfigure(errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]

# Shared file helpers, loaded by path because the scripts run as plain files.
_spec = importlib.util.spec_from_file_location("_szd_io", REPO_ROOT / "scripts" / "_szd_io.py")
szd_io = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(szd_io)

DATA = REPO_ROOT / "data"
SZDESS_FILE = DATA / "Aufsatzablage" / "SZDESS.xml"
SZDPER_FILE = DATA / "Index" / "Person" / "SZDPER.xml"
OUT_CSV = Path(__file__).resolve().parent / "essay_author_log.csv"

TEI = "{http://www.tei-c.org/ns/1.0}"
XML = "{http://www.w3.org/XML/1998/namespace}"

LOG_FIELDS = ["datei", "kontext", "zeile", "alte_referenz", "neue_referenz", "aktion"]

AUTHOR = re.compile(
    r'<author(?P<head>[^>]*?)\bref="(?P<ref>[^"]*)"(?P<tail>[^>]*)>(?P<inner>.*?)</author>',
    re.DOTALL,
)
PERSNAME = re.compile(r'<persName(?P<head>[^>]*?)\bref="(?P<ref>[^"]*)"(?P<tail>[^>]*)>')
SURNAME = re.compile(r"<surname>(?P<text>[^<]*)</surname>")
FORENAME = re.compile(r"<forename>(?P<text>[^<]*)</forename>")
GND_NUMBER = re.compile(r"gnd/([0-9X\-]+)")
BIBL_ID = re.compile(r'<biblFull[^>]*xml:id="([^"]+)"')


class PersonIndex:
    """The two lookups this repair needs, both required to be unambiguous."""

    def __init__(self, path: Path) -> None:
        self.by_gnd: dict[str, list[str]] = {}
        self.by_name: dict[str, list[str]] = {}
        self.gnd_of: dict[str, str] = {}
        for person in ET.parse(path).getroot().iter(f"{TEI}person"):
            person_id = person.get(f"{XML}id") or ""
            pers_name = person.find(f"{TEI}persName")
            if pers_name is None:
                continue
            reference = pers_name.get("ref") or ""
            number = GND_NUMBER.search(reference)
            if number:
                self.by_gnd.setdefault(number.group(1), []).append(person_id)
                self.gnd_of[person_id] = reference
            surname = (pers_name.findtext(f"{TEI}surname") or "").strip()
            forename = (pers_name.findtext(f"{TEI}forename") or "").strip()
            if surname and forename:
                self.by_name.setdefault(f"{surname}, {forename}", []).append(person_id)

    def by_reference(self, value: str) -> tuple[str, str]:
        """(person id, reason it failed). Exactly one of the two is filled."""
        number = GND_NUMBER.search(value)
        if number:
            candidates = self.by_gnd.get(number.group(1), [])
        else:
            candidates = self.by_name.get(value.strip(), [])
        if len(candidates) == 1:
            return candidates[0], ""
        if not candidates:
            return "", f"no index entry for {value}"
        return "", f"{len(candidates)} index entries for {value}: {', '.join(candidates)}"


def plan(text: str, index: PersonIndex) -> tuple[str, list[dict], list[str]]:
    rows: list[dict] = []
    skipped: list[str] = []

    def rewrite(match: re.Match[str]) -> str:
        inner = match.group("inner")
        pers_name = PERSNAME.search(inner)
        line = text.count("\n", 0, match.start()) + 1
        context = _context_id(text, match.start())
        if pers_name is None:
            return match.group(0)
        value = pers_name.group("ref")
        person_id, problem = index.by_reference(value)
        if problem:
            skipped.append(f"{context} (line {line}): {problem}")
            return match.group(0)
        wanted = f"#{person_id}"
        new_inner = inner
        old_parts = [f'author/@ref="{match.group("ref")}"']
        new_parts = [f'author/@ref="{wanted}"']
        if not GND_NUMBER.search(value):
            # A name in the attribute meant for an identifier: write the index entry's number.
            gnd = index.gnd_of.get(person_id, "")
            if not gnd:
                skipped.append(f"{context} (line {line}): {person_id} has no authority number")
                return match.group(0)
            new_inner = (
                inner[: pers_name.start()]
                + f'<persName{pers_name.group("head")}ref="{gnd}"{pers_name.group("tail")}>'
                + inner[pers_name.end() :]
            )
            old_parts.append(f'persName/@ref="{value}"')
            new_parts.append(f'persName/@ref="{gnd}"')
        if match.group("ref") == wanted and new_inner == inner:
            return match.group(0)
        rows.append(
            {
                "datei": SZDESS_FILE.relative_to(REPO_ROOT).as_posix(),
                "kontext": context,
                "zeile": line,
                "alte_referenz": ", ".join(old_parts),
                "neue_referenz": ", ".join(new_parts),
                "aktion": "Autorenverweis korrigiert",
            }
        )
        return (
            f'<author{match.group("head")}ref="{wanted}"{match.group("tail")}>'
            f"{new_inner}</author>"
        )

    return AUTHOR.sub(rewrite, text), rows, skipped


def _context_id(text: str, position: int) -> str:
    matches = list(BIBL_ID.finditer(text, 0, position))
    return matches[-1].group(1) if matches else ""


def verify() -> int:
    index = PersonIndex(SZDPER_FILE)
    text = szd_io.read_text(SZDESS_FILE)
    try:
        ET.fromstring(text)
    except ET.ParseError as error:
        print(f"FAIL  {SZDESS_FILE.name} not well formed, {error}")
        return 1
    _, rows, skipped = plan(text, index)
    for note in skipped:
        print(f"NOTE  left alone, needs a ruling: {note}")
    for row in rows:
        print(f"FAIL  {row['kontext']} line {row['zeile']}: {row['alte_referenz']} still open")
    if rows:
        return 1
    print(
        f"OK  every author reference resolved from its persName, "
        f"{len(skipped)} left to an editorial ruling"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--apply", action="store_true", help="write the changes")
    parser.add_argument("--verify", action="store_true", help="check the corrected state only")
    args = parser.parse_args()

    for required in (SZDESS_FILE, SZDPER_FILE):
        if not required.exists():
            print(f"FAIL  {required} missing", file=sys.stderr)
            return 1
    if args.verify:
        return verify()

    index = PersonIndex(SZDPER_FILE)
    text = szd_io.read_text(SZDESS_FILE)
    result, rows, skipped = plan(text, index)
    ET.fromstring(result)  # trust boundary: never write what is not well formed

    for row in rows:
        print(
            f"OK  {row['kontext']} line {row['zeile']}: "
            f"{row['alte_referenz']} -> {row['neue_referenz']}"
        )
    for note in skipped:
        print(f"SKIP  {note}")
    if not rows:
        print("SKIP  nothing to do, every author reference already names its author")
        return 0
    if not args.apply:
        print(f"SKIP  dry run, {len(rows)} changes planned, nothing written")
        return 0

    szd_io.write_atomic(SZDESS_FILE, result)
    szd_io.append_log(OUT_CSV, LOG_FIELDS, rows)
    print(f"OK  {OUT_CSV.relative_to(REPO_ROOT).as_posix()} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
