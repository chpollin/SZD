#!/usr/bin/env python3
"""Remove the certainly unreferenced persons from the person index and keep them aside.

Input is the CSV of verify_orphan_persons.py. Only rows marked sicher_unverknuepft = ja are
taken, and each one is checked again against the current repository with the same identifier
and GND tests, so a reference added since the CSV was written stops the removal of that
person. The removed <person> elements are written unchanged to removed_persons.xml next to
this script, outside data/ so that no later scan counts them as references. Their identifiers
are never assigned again. The GAMS production object o:szd.personen keeps the full index until
the next production ingest and serves as a second comparison source.

Usage:

    python scripts/checkup_2026_09_index/remove_orphan_persons.py --verified <csv>          # dry run
    python scripts/checkup_2026_09_index/remove_orphan_persons.py --verified <csv> --apply

Standard library only.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import re
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


szd_io = load("_szd_io", HERE.parent / "_szd_io.py")
verify = load("verify_orphan_persons", HERE / "verify_orphan_persons.py")
REMOVED = HERE / "removed_persons.xml"
LOG = HERE / "remove_orphan_persons_log.csv"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--verified", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    with args.verified.open(encoding="utf-8-sig") as handle:
        wanted = [row for row in csv.DictReader(handle) if row["sicher_unverknuepft"] == "ja"]
    text = szd_io.read_text(verify.PERSON_INDEX)
    newline = "\r\n" if "\r\n" in text else "\n"
    files = verify.corpus()

    removed, kept, rows = [], [], []
    for row in wanted:
        pid = row["szdper"]
        block = re.search(r'[ \t]*<person\b[^>]*xml:id="' + re.escape(pid) + r'"[^>]*>.*?</person>[ \t]*\r?\n', text, re.S)
        if not block:
            rows.append({"szdper": pid, "name": row["name"], "status": "not in index"})
            continue
        pattern = verify.id_pattern(pid)
        gnds = sorted(set(re.findall(r"d-nb\.info/gnd/([0-9X-]+)", block.group(0))) - {"placeholder"})
        others = len(pattern.findall(text)) - len(pattern.findall(block.group(0)))
        elsewhere = [label for label, content in files if pattern.search(content)]
        gnd_hits = [label for label, content in files for gnd in gnds if re.search(r"gnd/" + re.escape(gnd) + r"(?![0-9X-])", content)]
        if others or elsewhere or gnd_hits:
            kept.append(pid)
            rows.append({"szdper": pid, "name": row["name"], "status": "kept, referenced: " + "; ".join(elsewhere + gnd_hits)[:200]})
            continue
        removed.append(block.group(0))
        text = text[: block.start()] + text[block.end():]
        rows.append({"szdper": pid, "name": row["name"], "status": "removed"})

    print(f"{len(wanted)} verified, {len(removed)} to remove, {len(kept)} kept because referenced now")
    if not args.apply:
        return
    ET.fromstring(text.encode("utf-8"))  # well-formed before anything is written
    szd_io.write_atomic(verify.PERSON_INDEX, text)
    stamp = date.today().isoformat()
    previous = ""
    if REMOVED.exists():
        previous = re.sub(r"^.*?<listPerson[^>]*>|</listPerson>.*$", "", szd_io.read_text(REMOVED), flags=re.S)
    aside = (
        f'<?xml version="1.0" encoding="UTF-8"?>{newline}'
        f"<!-- Persons removed from data/Index/Person/SZDPER.xml because no reference, no GND and no{newline}"
        f"     name in any holding, konvolut or theme page reached them (last removal {stamp}).{newline}"
        f"     Their identifiers are not assigned again. -->{newline}"
        f'<listPerson xmlns="http://www.tei-c.org/ns/1.0">{newline}'
        f"{previous.strip(chr(13) + chr(10))}{newline if previous.strip() else ''}"
        + "".join(removed)
        + f"</listPerson>{newline}"
    )
    ET.fromstring(aside.encode("utf-8"))
    szd_io.write_atomic(REMOVED, aside)
    szd_io.append_log(LOG, ["date", "szdper", "name", "status"], [{"date": stamp, **r} for r in rows])
    print(f"removed {len(removed)}, kept aside in {REMOVED.name}, log {LOG.name}")


if __name__ == "__main__":
    main()
