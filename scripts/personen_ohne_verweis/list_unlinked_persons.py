#!/usr/bin/env python3
"""List the entries of the person authority file data/Index/Person/SZDPER.xml that no
other TEI file under data/ refers to, as a candidate list for the project.

The list is a candidate list, nothing more. Whether an entry is removed, kept for a future
delivery or linked from somewhere is an editorial decision; this script only writes the
CSV. It changes no TEI file.

A reference counts here when the RDF mapping reads it, not when it merely looks like one.
GetPersonlist in szd-TORDF.xsl emits a triple for two kinds of value and for nothing else,
so the same two kinds count as a link:

    ref="#SZDPER.42"                                        (the fragment form)
    ref="https://gams.uni-graz.at/o:szd.personen#SZDPER.42" (absolute, same fragment)
    ref="http://d-nb.info/gnd/118637479" on a persName       (resolved through the index)

Three consequences of reading it this way, each of them a correction of an earlier count.

A reference written without the fragment marker, ref="SZDPER.42", does not count. The
mapping drops it, the person view stays empty, and the entry belongs on this list until the
writing is unified; scripts/checkup_2026_09_index/normalize_person_refs.py does that.

An authority number on a persName does count, wherever under data/ it stands. Such a person
is linked in the person view through the index lookup, so she is not a candidate at all.
The number has to sit on a persName: the same number on a repository or an orgName names an
institution, not the person.

In data/Aufsatzablage/SZDESS.xml the author/@ref is ignored where the inner persName carries
a reference of its own, because the essay template of szd-TORDF.xsl reads the persName first
and falls back to the author attribute only where the persName has none. Without this rule
the sequence numbers that file carried as author references made 84 persons look linked.

References inside SZDPER.xml itself do not count as a link from the holdings, but the CSV
says whether one exists.
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
FRAGMENT_ID = re.compile(r"#(SZDPER\.[A-Za-z0-9_.\-]*)")
GND = re.compile(r"gnd/([0-9X\-]+)")
ESSAYS = DATA / "Aufsatzablage" / "SZDESS.xml"


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


def local_name(elem: ET.Element) -> str:
    return elem.tag.rsplit("}", 1)[-1]


def reads_wrapper(elem: ET.Element, is_essays: bool) -> bool:
    """Whether the mapping reads this element's own @ref.

    For an essay author it does not, as long as the inner persName carries a reference: the
    essay template passes that one and never reaches the attribute on the author element.
    """
    if not is_essays or local_name(elem) != "author":
        return True
    return not any(child.get("ref") for child in elem if local_name(child) == "persName")


def scan_references(data_dir: Path, authority_file: Path) -> tuple[Counter, Counter, set, set]:
    """(links from the holdings, references inside SZDPER, GNDs on a persName, trailing ids).

    The fourth value holds the ids that only ever appear behind the first token of a
    multi-id attribute. GetPersonlist takes substring-before the first space, so the mapping
    never sees them; they are reported, not silently counted as links.
    """
    external: Counter = Counter()
    internal: Counter = Counter()
    persname_gnd: set[str] = set()
    leading: set[str] = set()
    trailing: set[str] = set()
    for path in sorted(data_dir.rglob("*.xml")):
        is_authority = path.resolve() == authority_file.resolve()
        is_essays = path.resolve() == ESSAYS.resolve()
        target = internal if is_authority else external
        for elem in ET.parse(path).getroot().iter():
            value = elem.get("ref")
            if not value or not reads_wrapper(elem, is_essays):
                continue
            tokens = value.split()
            for position, token in enumerate(tokens):
                for person_id in FRAGMENT_ID.findall(token):
                    (leading if position == 0 else trailing).add(person_id)
                    if position == 0:
                        target[person_id] += 1
            if not is_authority and local_name(elem) == "persName" and tokens:
                persname_gnd.update(GND.findall(tokens[0]))
    return external, internal, persname_gnd, trailing - leading


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
    external, internal, persname_gnd, trailing_only = scan_references(args.data, args.szdper)

    dangling = sorted((set(external) | set(internal)) - known)
    rows = []
    for person in persons:
        xml_id = person.get(XML + "id") or ""
        links = authority_links(person)
        gnds = GND.findall(links)
        # Either writing is a link: the id in fragment form, or the authority number on a
        # persName in the holdings, which the mapping resolves through the index.
        if external.get(xml_id) or any(gnd in persname_gnd for gnd in gnds):
            continue
        rows.append({
            "id": xml_id,
            "name": display_name(person),
            "normdaten": links,
            "verweis_innerhalb_szdper": "ja" if internal.get(xml_id) else "nein",
        })

    print(f"Personeneinträge insgesamt: {len(persons)}")
    print(f"Ohne Verweis aus einer anderen Datei unter {args.data.name}/: {len(rows)}")
    print(f"  davon ohne jeden Normdaten-Verweis: "
          f"{sum(1 for r in rows if not r['normdaten'])}")
    print(f"Verweise auf nicht vorhandene Kennungen: {len(dangling)}")
    for person_id in dangling:
        origin = "SZDPER-intern" if person_id in internal else "andere Datei"
        print(f"  {person_id} ({origin})")
    print(f"Nur hinter dem ersten Token eines Mehrfachverweises genannt: {len(trailing_only)}")
    for person_id in sorted(trailing_only):
        print(f"  {person_id}")

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
