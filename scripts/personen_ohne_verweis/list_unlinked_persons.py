#!/usr/bin/env python3
"""List the entries of the person authority file data/Index/Person/SZDPER.xml that no
other TEI file under data/ refers to, as a candidate list for the project.

The list is a candidate list, nothing more. Whether an entry is removed, kept for a future
delivery or linked from somewhere is an editorial decision; this script only writes the
CSV. It changes no TEI file.

Reference patterns actually used in the corpus, all on @ref, all resolved here:

    ref="#SZDPER.42"                                        (the ordinary case)
    ref="SZDPER.42"                                         (without the fragment marker)
    ref="https://gams.uni-graz.at/o:szd.personen#SZDPER.42" (absolute, in some files)
    ref="#SZDPER.42 SZDPER.43"                              (several ids in one attribute)

References inside SZDPER.xml itself do not count as a link from another file, but the CSV
says whether one exists, and likewise whether the entry's GND appears elsewhere in the
data even though the SZDPER id does not -- such a person is in use and only linked by
authority number.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252
    sys.stdout.reconfigure(errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA = REPO_ROOT / "data"
SZDPER = DATA / "Index" / "Person" / "SZDPER.xml"
DEFAULT_CSV = Path(__file__).resolve().parent / "unlinked_persons.csv"

TEI = "{http://www.tei-c.org/ns/1.0}"
XML = "{http://www.w3.org/XML/1998/namespace}"

PERSON_ID = re.compile(r"SZDPER\.[A-Za-z0-9_.\-]*")
GND = re.compile(r"gnd/([0-9X\-]+)")


def text_of(elem: ET.Element) -> str:
    return re.sub(r"\s+", " ", "".join(elem.itertext())).strip()


def display_name(person: ET.Element) -> str:
    """The name as the file writes it: 'Nachname, Vorname', else the persName text."""
    pers_name = person.find(f"{TEI}persName")
    if pers_name is None:
        return ""
    surname = pers_name.find(f"{TEI}surname")
    forename = pers_name.find(f"{TEI}forename")
    if surname is not None or forename is not None:
        parts = [text_of(e) for e in (surname, forename) if e is not None and text_of(e)]
        return ", ".join(parts)
    return text_of(pers_name)


def authority_links(person: ET.Element) -> str:
    """GND from persName/@ref, plus Wikidata/Wikipedia identifiers, space separated."""
    links: list[str] = []
    pers_name = person.find(f"{TEI}persName")
    if pers_name is not None and pers_name.get("ref"):
        links.append(pers_name.get("ref", ""))
    for idno in person.iter(f"{TEI}idno"):
        value = text_of(idno)
        if value:
            links.append(value)
    if person.get("corresp"):
        links.append(person.get("corresp", ""))
    return " ".join(links)


def scan_references(data_dir: Path, authority_file: Path) -> tuple[Counter, Counter, set]:
    """(references from other files, references inside SZDPER, GNDs used elsewhere)."""
    external: Counter = Counter()
    internal: Counter = Counter()
    external_gnd: set[str] = set()
    for path in sorted(data_dir.rglob("*.xml")):
        text = path.read_text(encoding="utf-8")
        is_authority = path.resolve() == authority_file.resolve()
        target = internal if is_authority else external
        for match in re.finditer(r'\b(?:ref|key|corresp|target|sameAs)="([^"]*)"', text):
            value = match.group(1)
            for person_id in PERSON_ID.findall(value):
                target[person_id] += 1
            if not is_authority:
                for gnd in GND.findall(value):
                    external_gnd.add(gnd)
    return external, internal, external_gnd


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--szdper", type=Path, default=SZDPER)
    parser.add_argument("--data", type=Path, default=DATA)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--dry-run", action="store_true",
                        help="nur zählen und die ersten Zeilen zeigen, keine CSV schreiben")
    args = parser.parse_args()

    persons = list(ET.parse(args.szdper).getroot().iter(f"{TEI}person"))
    known = {p.get(XML + "id") for p in persons}
    external, internal, external_gnd = scan_references(args.data, args.szdper)

    dangling = sorted((set(external) | set(internal)) - known)
    rows = []
    for person in persons:
        xml_id = person.get(XML + "id") or ""
        if external.get(xml_id):
            continue
        links = authority_links(person)
        gnds = GND.findall(links)
        rows.append({
            "id": xml_id,
            "name": display_name(person),
            "normdaten": links,
            "gnd_sonst_verwendet": "ja" if any(g in external_gnd for g in gnds) else "nein",
            "verweis_innerhalb_szdper": "ja" if internal.get(xml_id) else "nein",
        })

    print(f"Personeneinträge insgesamt: {len(persons)}")
    print(f"Ohne Verweis aus einer anderen Datei unter {args.data.name}/: {len(rows)}")
    print(f"  davon mit anderweitig verwendeter GND: "
          f"{sum(1 for r in rows if r['gnd_sonst_verwendet'] == 'ja')}")
    print(f"  davon ohne jeden Normdaten-Verweis: "
          f"{sum(1 for r in rows if not r['normdaten'])}")
    print(f"Verweise auf nicht vorhandene Kennungen: {len(dangling)}")
    for person_id in dangling:
        origin = "SZDPER-intern" if person_id in internal else "andere Datei"
        print(f"  {person_id} ({origin})")

    if args.dry_run:
        for row in rows[:10]:
            print("  " + " | ".join(row.values()))
        print("\nTrockenlauf -- keine CSV geschrieben.")
        return 0

    with open(args.csv, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\ngeschrieben: {args.csv.relative_to(REPO_ROOT)} ({len(rows)} Zeilen)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
