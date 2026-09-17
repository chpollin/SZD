#!/usr/bin/env python3
"""Move the corporate bodies out of the person index and point the holdings at the
organisation index instead.

The script runs after build_org_index.py, which mints the SZDORG ids this one uses, and it
carries out the editorial decision of 2026-09-11: an entry that SZDORG lists as a corporate
body leaves data/Index/Person/SZDPER.xml, and every reference the holdings make to its
SZDPER id is rewritten.

Two reference forms are written, both of them forms the holdings already use for corporate
bodies.

    * the name element becomes <orgName ref="http://d-nb.info/gnd/<number>"> where SZDORG
      has an authority number, which is the form SZDLEB and SZDKOR use throughout;
    * without an authority number it becomes
      <orgName ref="https://gams.uni-graz.at/o:szd.organisation#SZDORG.<n>">, mirroring the
      "https://gams.uni-graz.at/o:szd.standorte#SZDSTA.<n>" that SZDAUT and SZDBIB use for a
      repository without a GND. szd-TORDF.xsl passes such a value through unchanged.

The @ref of the wrapping author or editor element is rewritten to the SZDORG form as well,
not dropped: szd-Bibliothek.xsl groups and sorts the library browse list by that attribute,
so an empty one would collapse several titles under one heading.

Every rewrite is protocolled in migration_log.csv. The run is idempotent, a second run on
the same tree finds nothing to do and leaves the protocol alone.

Usage:

    python scripts/organisationen_index/migrate_org_references.py
    python scripts/organisationen_index/migrate_org_references.py --dry-run

Regime: script pipeline in the shape the other scripts of this repo use, standard library
only, no dependency manifest, run with plain python.
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
SZDORG_FILE = DATA / "Index" / "Organisation" / "SZDORG.xml"
OUT_CSV = Path(__file__).resolve().parent / "migration_log.csv"

TEI = "{http://www.tei-c.org/ns/1.0}"
XML = "{http://www.w3.org/XML/1998/namespace}"

ORG_OBJECT_URI = "https://gams.uni-graz.at/o:szd.organisation#"

# The wrapping element that carries the index reference, with the name element inside it.
WRAPPER = re.compile(
    r'<(?P<tag>author|editor)(?P<head>[^>]*?)\bref="#?(?P<pid>SZDPER\.\d+)"(?P<tail>[^>]*?)>'
    r"(?P<inner>.*?)"
    r"</(?P=tag)>",
    re.DOTALL,
)
PERS_NAME = re.compile(
    r"<persName(?P<attrs>[^>]*)>\s*<name>(?P<text>[^<]*)</name>\s*</persName>",
    re.DOTALL,
)
REF_ATTR = re.compile(r'\s+ref="[^"]*"')
BIBL_ID = re.compile(r'<biblFull[^>]*xml:id="([^"]+)"')


def _mentions(person_id: str, text: str) -> bool:
    """Whether the id occurs as a whole id, so that SZDPER.105 misses SZDPER.1056."""
    return re.search(rf"{re.escape(person_id)}(?![0-9])", text) is not None


def _person_block(person_id: str) -> re.Pattern[str]:
    return re.compile(
        rf'[ \t]*<person xml:id="{re.escape(person_id)}">.*?</person>\r?\n',
        re.DOTALL,
    )


def read_index() -> dict[str, dict[str, str]]:
    """SZDPER id -> the SZDORG entry that replaces it, with the reference to write.

    A body merged from two person entries carries both idno back-references, so both ids
    map onto the same target.
    """
    root = ET.parse(SZDORG_FILE).getroot()
    targets: dict[str, dict[str, str]] = {}
    for org in root.iter(f"{TEI}org"):
        org_id = org.get(f"{XML}id", "")
        org_name = org.find(f"{TEI}orgName")
        gnd_ref = org_name.get("ref", "") if org_name is not None else ""
        name = "".join(org_name.itertext()).strip() if org_name is not None else ""
        for idno in org.findall(f"{TEI}idno"):
            if idno.get("type") != "SZDPER":
                continue
            targets[(idno.text or "").strip()] = {
                "szdorg": org_id,
                "name": name,
                "wrapper_ref": f"{ORG_OBJECT_URI}{org_id}",
                "name_ref": gnd_ref or f"{ORG_OBJECT_URI}{org_id}",
            }
    return targets


def _context_id(text: str, position: int) -> str:
    """The xml:id of the biblFull the match sits in, as the anchor of the protocol row."""
    matches = list(BIBL_ID.finditer(text, 0, position))
    return matches[-1].group(1) if matches else ""


def _rewrite_wrapper(match: re.Match[str], target: dict[str, str]) -> tuple[str, str, str]:
    """The rewritten element, plus the old and new reference for the protocol."""
    inner, count = PERS_NAME.subn(
        lambda name: '<orgName{attrs} ref="{ref}">{text}</orgName>'.format(
            attrs=REF_ATTR.sub("", name.group("attrs")),
            ref=target["name_ref"],
            text=re.sub(r"\s+", " ", name.group("text")).strip(),
        ),
        match.group("inner"),
        count=1,
    )
    if count != 1:
        raise RuntimeError(
            f"{match.group('pid')}: kein <persName><name> im "
            f"<{match.group('tag')}>, Form nicht vorgesehen"
        )
    element = (
        f"<{match.group('tag')}{match.group('head')}"
        f'ref="{target["wrapper_ref"]}"{match.group("tail")}>{inner}</{match.group("tag")}>'
    )
    old = f'{match.group("tag")}/@ref="#{match.group("pid")}"'
    new = (
        f'{match.group("tag")}/@ref="{target["wrapper_ref"]}", orgName/@ref="{target["name_ref"]}"'
    )
    return element, old, new


def migrate_holdings(targets: dict[str, dict[str, str]]) -> tuple[dict[Path, str], list[dict]]:
    """The rewritten text per file and the protocol rows, without touching the disk."""
    changed: dict[Path, str] = {}
    rows: list[dict] = []
    for path in sorted(DATA.rglob("*.xml")):
        if path in (SZDPER_FILE, SZDORG_FILE):
            continue
        text = path.read_text(encoding="utf-8")
        if not any(_mentions(person_id, text) for person_id in targets):
            continue
        pieces: list[str] = []
        cursor = 0
        for match in WRAPPER.finditer(text):
            target = targets.get(match.group("pid"))
            if target is None:
                continue
            element, old, new = _rewrite_wrapper(match, target)
            pieces.append(text[cursor : match.start()])
            pieces.append(element)
            cursor = match.end()
            rows.append(
                {
                    "datei": path.relative_to(REPO_ROOT).as_posix(),
                    "kontext": _context_id(text, match.start()),
                    "zeile": text.count("\n", 0, match.start()) + 1,
                    "alte_referenz": old,
                    "neue_referenz": new,
                    "aktion": "Verweis umgestellt",
                }
            )
        pieces.append(text[cursor:])
        result = "".join(pieces)
        # Trust boundary: an id left over means a reference form the rewrite does not know.
        leftover = sorted({pid for pid in targets if _mentions(pid, result)})
        if leftover:
            raise RuntimeError(
                f"{path.relative_to(REPO_ROOT).as_posix()}: Verweise auf "
                f"{', '.join(leftover)} in einer nicht vorgesehenen Form"
            )
        if result != text:
            changed[path] = result
    return changed, rows


def remove_person_entries(targets: dict[str, dict[str, str]]) -> tuple[str, list[dict]]:
    """SZDPER without the corporate bodies, plus one protocol row per removed entry."""
    original = SZDPER_FILE.read_text(encoding="utf-8")
    text = original
    rows: list[dict] = []
    for person_id in sorted(targets, key=lambda pid: int(pid.split(".")[1])):
        match = _person_block(person_id).search(original)
        if match is None or not _person_block(person_id).search(text):
            continue
        # The name of the entry being removed, not of the index record it joins: a merged
        # record leads under the other name, and the protocol has to stay readable against
        # the file as it was.
        name = " ".join(" ".join(ET.fromstring(match.group(0).strip()).itertext()).split())
        text = _person_block(person_id).sub("", text, count=1)
        rows.append(
            {
                "datei": SZDPER_FILE.relative_to(REPO_ROOT).as_posix(),
                "kontext": person_id,
                "zeile": original.count("\n", 0, match.start()) + 1,
                "alte_referenz": f"person/@xml:id={person_id} ({name})",
                "neue_referenz": targets[person_id]["szdorg"],
                "aktion": "SZDPER-Eintrag entfernt",
            }
        )
    return text, rows


def _write_atomic(path: Path, text: str) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text, encoding="utf-8")
    temp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--dry-run", action="store_true", help="nur berichten, nichts schreiben")
    args = parser.parse_args()

    for required in (SZDPER_FILE, SZDORG_FILE):
        if not required.exists():
            print(f"FEHLER: {required} fehlt", file=sys.stderr)
            return 1

    targets = read_index()
    if not targets:
        print("FEHLER: SZDORG trägt keinen idno type='SZDPER'", file=sys.stderr)
        return 1

    changed, rows = migrate_holdings(targets)
    person_text, person_rows = remove_person_entries(targets)
    rows.extend(person_rows)

    for text in changed.values():
        ET.fromstring(text)  # trust boundary: never write something that is not well-formed
    ET.fromstring(person_text)

    for row in rows:
        print(f"OK  {row['aktion']}: {row['datei']} {row['kontext']} -> {row['neue_referenz']}")
    if not rows:
        print("SKIP  keine Verweise und keine Einträge offen, nichts zu tun")
        return 0
    if args.dry_run:
        print("SKIP  dry-run, nichts geschrieben")
        return 0

    for path, text in changed.items():
        _write_atomic(path, text)
    if person_rows:
        _write_atomic(SZDPER_FILE, person_text)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["datei", "kontext", "zeile", "alte_referenz", "neue_referenz", "aktion"],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"OK  {OUT_CSV.relative_to(REPO_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
