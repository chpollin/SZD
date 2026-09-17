#!/usr/bin/env python3
"""Merge the duplicate person index entries confirmed by the 2026-09 checkup verification.

The 2026-09 checkup verification (knowledge/DATA.md, Archive checkup) confirmed fourteen
index entries the archive marked as duplicates and three near-duplicate pairs the archive
did not mark. The rows classified confirmed-data are merged here; the rows classified
needs-archive (Kesten, Neumann, Pilnjak) and the rows already fixed by an earlier commit or
by the organisation migration (Geiringer, Meiler, Przeworskiego) stay untouched.

Per merge the script

    * removes the duplicate person record from data/Index/Person/SZDPER.xml,
    * rewrites every @ref under data/ that names the removed id to the surviving id,
      keeping the writing form of the reference (fragment, plain, absolute),
    * moves life dates that either record carries in its forename field, as in
      "Richard (1896-1979)", into birth/death of the survivor, but only where the survivor
      has neither element,
    * copies an authority number or a variant note from the removed record where the
      survivor has none.

Nothing else about the surviving record changes. A differing authority number on the removed
record is not copied over a number the survivor already holds, it is written to the log
instead, because two diverging numbers are an editorial question and not a merge artefact.

The reference rewrite mirrors scripts/organisationen_index/migrate_org_references.py, which
does the same job for corporate bodies.

Usage:

    python scripts/checkup_2026_09_index/merge_person_duplicates.py            # dry run
    python scripts/checkup_2026_09_index/merge_person_duplicates.py --apply
    python scripts/checkup_2026_09_index/merge_person_duplicates.py --verify

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
OUT_CSV = Path(__file__).resolve().parent / "merge_log.csv"

TEI = "{http://www.tei-c.org/ns/1.0}"
XML = "{http://www.w3.org/XML/1998/namespace}"

LOG_FIELDS = ["datei", "kontext", "zeile", "alte_referenz", "neue_referenz", "aktion"]

# surviving id -> removed ids, as decided in the verification report. The comment names the
# person and why this entry survives.
MERGES: dict[str, tuple[str, ...]] = {
    "SZDPER.92": ("SZDPER.1661", "SZDPER.1990"),  # Benaroya, only 92 carries the GND
    "SZDPER.388": ("SZDPER.2115",),  # Ferencak, 388 is the referenced entry
    "SZDPER.435": ("SZDPER.1758",),  # Friedenthal, 435 carries twenty references
    "SZDPER.616": ("SZDPER.1819",),  # Hirschfeld Georg, only 616 carries the GND
    "SZDPER.657": ("SZDPER.1971",),  # Huenich, 657 is the referenced entry
    "SZDPER.1060": ("SZDPER.1696",),  # Pange, 1060 is the referenced entry
    "SZDPER.1150": ("SZDPER.2080",),  # Reik, 1150 is referenced from SZDBIB and thema6
    "SZDPER.1221": ("SZDPER.1978",),  # Russell, 1221 is referenced and the fuller spelling
    "SZDPER.278": ("SZDPER.2105",),  # Danowski, 278 is referenced from SZDBIB
    "SZDPER.2008": ("SZDPER.1731",),  # Isenstein, only 2008 carries the GND
    "SZDPER.2064": ("SZDPER.2184",),  # Podbielski, 2064 is the correct spelling
}

# "Richard (1896-1979)" and "Mois (1896–1967)", hyphen or en dash between the years.
LIFE_DATES = re.compile(r"^(?P<name>.*?)\s*\((?P<birth>\d{4})\s*[-–]\s*(?P<death>\d{4})\)$")
REF_ATTR = re.compile(r'ref="(?P<value>[^"]*)"')
GND_NUMBER = re.compile(r"gnd/([0-9X\-]+)")
BIBL_ID = re.compile(r'<(?:biblFull|person)[^>]*xml:id="([^"]+)"')
CLOSING_PERSNAME = re.compile(r"(?m)^(?P<indent>[ \t]*)</persName>")


def read(path: Path) -> str:
    """Read without translating line terminators, so that a write reproduces them."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write_atomic(path: Path, text: str) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    temp.replace(path)


def person_block(person_id: str) -> re.Pattern[str]:
    """The whole record including its own indentation and trailing newline."""
    return re.compile(
        rf'[ \t]*<person[^>]*xml:id="{re.escape(person_id)}">.*?</person>\r?\n',
        re.DOTALL,
    )


def token_pattern(person_id: str) -> re.Pattern[str]:
    """The id as a whole id: SZDPER.105 must miss SZDPER.1056 and SZDPER.2080 miss
    SZDPER.2080a, which the index carries as a separate person."""
    return re.compile(rf"{re.escape(person_id)}(?![0-9A-Za-z_.\-])")


def facts(block: str) -> dict[str, str]:
    """Authority number, variant note, life dates and name of one person record."""
    # The extracted record has no namespace declaration of its own, so the elements are
    # read without the TEI namespace here.
    element = ET.fromstring(block.strip())
    pers_name = element.find("persName")
    result = {"gnd": "", "variants": "", "birth": "", "death": "", "name": ""}
    if pers_name is None:
        return result
    result["gnd"] = pers_name.get("ref", "") or ""
    forename = pers_name.find("forename")
    surname = pers_name.find("surname")
    parts = [(e.text or "").strip() for e in (surname, forename) if e is not None]
    result["name"] = ", ".join(p for p in parts if p)
    if forename is not None and forename.text:
        dates = LIFE_DATES.match(forename.text.strip())
        if dates:
            result["birth"] = dates.group("birth")
            result["death"] = dates.group("death")
    for note in element.findall("note"):
        if note.get("type") == "variants":
            result["variants"] = re.sub(r"\s+", " ", "".join(note.itertext())).strip()
    if element.find("birth") is not None or element.find("death") is not None:
        result["has_dates"] = "yes"
    return result


def authority_number(ref: str) -> str:
    """The bare GND number, so that http and https spellings compare as one number."""
    match = GND_NUMBER.search(ref)
    return match.group(1) if match else ref


def update_survivor(block: str, gnd: str, variants: str, birth: str, death: str) -> str:
    """Add what the merge carries over, and strip life dates from the forename field."""
    # Siblings of persName carry its indentation, which varies from record to record.
    closing = re.search(CLOSING_PERSNAME, block)
    inner = closing.group("indent") if closing else ""
    if gnd:
        block = re.sub(r"<persName(?![^>]*\bref=)", f'<persName ref="{gnd}"', block, count=1)
    if birth and death:
        # The forename field is a name field; the dates move into the elements meant for them.
        block = re.sub(
            r"(<forename[^>]*>)([^<]*)(</forename>)",
            lambda m: m.group(1) + (LIFE_DATES.sub(r"\g<name>", m.group(2).strip())) + m.group(3),
            block,
            count=1,
        )
    additions = []
    if variants:
        additions.append(f'{inner}<note type="variants">{variants}</note>')
    if birth and death:
        additions.append(f'{inner}<birth when="{birth}"/>')
        additions.append(f'{inner}<death when="{death}"/>')
    if additions:
        newline = "\r\n" if "\r\n" in block else "\n"
        anchor = block.index("</persName>") + len("</persName>")
        block = block[:anchor] + newline + newline.join(additions) + block[anchor:]
    return block


def merge_index(rows: list[dict]) -> str:
    """SZDPER with the duplicates removed and the survivors completed."""
    original = read(SZDPER_FILE)
    text = original
    for survivor, removed_ids in MERGES.items():
        survivor_match = person_block(survivor).search(text)
        if survivor_match is None:
            if person_block(removed_ids[0]).search(text):
                raise RuntimeError(f"{survivor}: surviving record missing, duplicate still there")
            continue  # already merged
        survivor_facts = facts(survivor_match.group(0))
        carried = {"gnd": "", "variants": "", "birth": "", "death": ""}
        if survivor_facts["birth"] and survivor_facts["death"]:
            carried["birth"] = survivor_facts["birth"]
            carried["death"] = survivor_facts["death"]
        for removed in removed_ids:
            match = person_block(removed).search(text)
            if match is None:
                continue
            removed_facts = facts(match.group(0))
            in_original = person_block(removed).search(original)
            line = original.count("\n", 0, in_original.start()) + 1
            note = ""
            if removed_facts["gnd"] and survivor_facts["gnd"]:
                same = authority_number(removed_facts["gnd"]) == authority_number(
                    survivor_facts["gnd"]
                )
                if not same:
                    note = f', diverging authority number {removed_facts["gnd"]} dropped'
            elif removed_facts["gnd"]:
                carried["gnd"] = removed_facts["gnd"]
            if removed_facts["variants"] and not survivor_facts["variants"]:
                carried["variants"] = removed_facts["variants"]
            if removed_facts["birth"] and not carried["birth"]:
                carried["birth"] = removed_facts["birth"]
                carried["death"] = removed_facts["death"]
            text = person_block(removed).sub("", text, count=1)
            rows.append(
                {
                    "datei": SZDPER_FILE.relative_to(REPO_ROOT).as_posix(),
                    "kontext": removed,
                    "zeile": line,
                    "alte_referenz": f'person/@xml:id="{removed}" ({removed_facts["name"]})',
                    "neue_referenz": f"{survivor} ({survivor_facts['name']}){note}",
                    "aktion": "SZDPER-Eintrag entfernt",
                }
            )
        if survivor_facts.get("has_dates"):
            carried["birth"] = carried["death"] = ""  # the survivor already has them
        if not any(carried.values()):
            continue
        survivor_match = person_block(survivor).search(text)
        block = survivor_match.group(0)
        updated = update_survivor(block, **carried)
        if updated == block:
            continue
        text = text[: survivor_match.start()] + updated + text[survivor_match.end() :]
        detail = ", ".join(f"{key}={value}" for key, value in carried.items() if value)
        rows.append(
            {
                "datei": SZDPER_FILE.relative_to(REPO_ROOT).as_posix(),
                "kontext": survivor,
                "zeile": original.count(
                    "\n", 0, person_block(survivor).search(original).start()
                )
                + 1,
                "alte_referenz": f'person/@xml:id="{survivor}"',
                "neue_referenz": detail,
                "aktion": "Angaben übernommen",
            }
        )
    return text


def rewrite_references(rows: list[dict]) -> dict[Path, str]:
    """Point every reference to a removed id at the surviving id, form preserved."""
    replacement = {
        removed: survivor for survivor, group in MERGES.items() for removed in group
    }
    changed: dict[Path, str] = {}
    for path in sorted(DATA.rglob("*.xml")):
        if path == SZDPER_FILE:
            continue
        text = read(path)
        if not any(token_pattern(removed).search(text) for removed in replacement):
            continue
        hits: list[dict] = []

        def rewrite(match: re.Match[str]) -> str:
            value = match.group("value")
            new_value = value
            for removed, survivor in replacement.items():
                new_value = token_pattern(removed).sub(survivor, new_value)
            if new_value == value:
                return match.group(0)
            hits.append(
                {
                    "datei": path.relative_to(REPO_ROOT).as_posix(),
                    "kontext": _context_id(text, match.start()),
                    "zeile": text.count("\n", 0, match.start()) + 1,
                    "alte_referenz": f'@ref="{value}"',
                    "neue_referenz": f'@ref="{new_value}"',
                    "aktion": "Verweis umgestellt",
                }
            )
            return f'ref="{new_value}"'

        result = REF_ATTR.sub(rewrite, text)
        # Trust boundary: a leftover id means a reference form this rewrite does not know.
        leftover = sorted({rid for rid in replacement if token_pattern(rid).search(result)})
        if leftover:
            raise RuntimeError(
                f"{path.relative_to(REPO_ROOT).as_posix()}: references to "
                f"{', '.join(leftover)} in a form the rewrite does not cover"
            )
        if result != text:
            changed[path] = result
            rows.extend(hits)
    return changed


def _context_id(text: str, position: int) -> str:
    matches = list(BIBL_ID.finditer(text, 0, position))
    return matches[-1].group(1) if matches else ""


def verify() -> int:
    """No removed id survives anywhere, every survivor is still there, files are well formed."""
    failures: list[str] = []
    root = ET.parse(SZDPER_FILE).getroot()
    present = {person.get(f"{XML}id") for person in root.iter(f"{TEI}person")}
    for survivor, removed_ids in MERGES.items():
        if survivor not in present:
            failures.append(f"{survivor}: surviving record missing from the index")
        for removed in removed_ids:
            if removed in present:
                failures.append(f"{removed}: duplicate record still in the index")
    for path in sorted(DATA.rglob("*.xml")):
        text = read(path)
        try:
            ET.fromstring(text)
        except ET.ParseError as error:
            failures.append(f"{path.relative_to(REPO_ROOT).as_posix()}: not well formed, {error}")
            continue
        for match in REF_ATTR.finditer(text):
            for survivor, removed_ids in MERGES.items():
                for removed in removed_ids:
                    if token_pattern(removed).search(match.group("value")):
                        failures.append(
                            f"{path.relative_to(REPO_ROOT).as_posix()}:"
                            f"{text.count(chr(10), 0, match.start()) + 1} still references "
                            f"{removed} instead of {survivor}"
                        )
    for failure in failures:
        print(f"FAIL  {failure}")
    if failures:
        return 1
    print(f"OK  {len(MERGES)} merges verified, no reference to a removed id left")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--apply", action="store_true", help="write the changes")
    parser.add_argument("--verify", action="store_true", help="check the merged state only")
    args = parser.parse_args()

    if not SZDPER_FILE.exists():
        print(f"FAIL  {SZDPER_FILE} missing", file=sys.stderr)
        return 1
    if args.verify:
        return verify()

    rows: list[dict] = []
    index_text = merge_index(rows)
    changed = rewrite_references(rows)
    ET.fromstring(index_text)  # trust boundary: never write what is not well formed
    for text in changed.values():
        ET.fromstring(text)

    for row in rows:
        print(f"OK  {row['aktion']}: {row['datei']} {row['kontext']} -> {row['neue_referenz']}")
    if not rows:
        print("SKIP  nothing to do, the merges are already in the tree")
        return 0
    if not args.apply:
        print(f"SKIP  dry run, {len(rows)} changes planned, nothing written")
        return 0

    if index_text != read(SZDPER_FILE):
        write_atomic(SZDPER_FILE, index_text)
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
