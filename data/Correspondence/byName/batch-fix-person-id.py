#!/usr/bin/env python3
"""
batch-fix-person-id.py (reporting)
=================================

Batch-process TEI XML files, patch `<persName>@ref`, **and** write 2 CSV
reports:

* **refs_added.csv** – every place where a GND URI *or* a local `#SZDPER…`
  reference was inserted. Columns: *file, name, new_ref*.
* **refs_not_changed.csv** – every `<persName>` that still lacks an `@ref`
  afterwards (unmatched or ambiguous).  Columns: *file, name, reason*.

Both reports are created in the destination directory (next to the fixed XML).

Zero-flag invocation still works; defaults are identical to the previous
version.
"""
from __future__ import annotations

import argparse
import csv
import logging
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, NamedTuple
from xml.etree import ElementTree as ET

# ---------------------------------------------------------------------------
# Namespace
# ---------------------------------------------------------------------------
TEI_NS_URI = "http://www.tei-c.org/ns/1.0"
TEI_NS = {"tei": TEI_NS_URI}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
ET.register_namespace("", TEI_NS_URI)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clean(el):
    return " ".join(el.text.split()) if el is not None and el.text else None

def _simplify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(text.lower().split())

class Candidate(NamedTuple):
    ref: str | None  # GND or None
    pid: str         # SZDPER xml:id

# ---------------------------------------------------------------------------
# Build lookup tables
# ---------------------------------------------------------------------------

def build_indexes(persons_xml: Path):
    tree = ET.parse(persons_xml)
    root = tree.getroot()

    pair_idx: Dict[Tuple[str, str], List[Candidate]] = defaultdict(list)
    full_idx: Dict[str, List[Candidate]] = defaultdict(list)

    for person in root.findall(".//tei:person", TEI_NS):
        pid = person.get(XML_ID)
        if not pid:
            continue
        pn = person.find("tei:persName", TEI_NS)
        if pn is None:
            continue
        gnd = pn.get("ref") or None
        sur = _clean(pn.find("tei:surname", TEI_NS))
        fore = _clean(pn.find("tei:forename", TEI_NS))
        if not (sur and fore):
            continue
        cand = Candidate(ref=gnd, pid=pid)
        sur_s, fore_s = _simplify(sur), _simplify(fore)
        pair_idx[(sur_s, fore_s)].append(cand)
        full_idx[f"{fore_s} {sur_s}"].append(cand)
        full_idx[f"{sur_s} {fore_s}"].append(cand)

    return pair_idx, full_idx

# ---------------------------------------------------------------------------
# Fix single file, recording row lists
# ---------------------------------------------------------------------------

def fix_file(src: Path, dest: Path, pair_idx, full_idx, added_rows, unchanged_rows):
    try:
        tree = ET.parse(src)
    except ET.ParseError as e:
        logging.warning("SKIP (malformed XML): %s – %s", src, e)
        return False

    root = tree.getroot()

    for pn in root.findall(".//tei:persName", TEI_NS):
        ref_val = pn.get("ref")
        if ref_val and not ref_val.endswith("/placeholder"):
            # already contains a valid ref – no action, no report
            continue

        sur_raw  = _clean(pn.find("tei:surname", TEI_NS))
        fore_raw = _clean(pn.find("tei:forename", TEI_NS))
        name_raw = _clean(pn.find("tei:name", TEI_NS))
        display_name = name_raw or f"{fore_raw or ''} {sur_raw or ''}".strip() or "[unknown]"

        sur_s, fore_s = (_simplify(sur_raw) if sur_raw else None,
                          _simplify(fore_raw) if fore_raw else None)
        candidates: List[Candidate] = []
        if sur_s and fore_s:
            candidates = pair_idx.get((sur_s, fore_s), [])
        if not candidates and name_raw:
            candidates = full_idx.get(_simplify(name_raw), [])

        if len(candidates) == 1:
            cand = candidates[0]
            new_ref = cand.ref if cand.ref else f"#{cand.pid}"
            pn.set("ref", new_ref)
            added_rows.append((str(src), display_name, new_ref))
        else:
            reason = "no match" if len(candidates)==0 else "ambiguous"
            unchanged_rows.append((str(src), display_name, reason))

    dest.parent.mkdir(parents=True, exist_ok=True)
    tree.write(dest, encoding="utf-8", xml_declaration=True)
    return True

# ---------------------------------------------------------------------------
# Batch processing
# ---------------------------------------------------------------------------

def batch_process(src_dir: Path, dest_dir: Path, persons_xml: Path):
    pair_idx, full_idx = build_indexes(persons_xml)
    logging.info("Index: %d pair keys, %d full-name keys", len(pair_idx), len(full_idx))

    added_rows: List[tuple] = []
    unchanged_rows: List[tuple] = []
    processed_files = 0

    for xml_file in sorted(src_dir.rglob("*.xml")):
        rel = xml_file.relative_to(src_dir)
        ok = fix_file(xml_file, dest_dir / rel, pair_idx, full_idx, added_rows, unchanged_rows)
        if ok:
            processed_files += 1

    # Write CSV reports
    dest_dir.mkdir(parents=True, exist_ok=True)
    added_csv = dest_dir / "refs_added.csv"
    unchanged_csv = dest_dir / "refs_not_changed.csv"

    with added_csv.open("w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "name", "new_ref"])
        writer.writerows(added_rows)

    with unchanged_csv.open("w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "name", "reason"])
        writer.writerows(unchanged_rows)

    logging.info("Processed %d XML files", processed_files)
    logging.info("%d refs added → %s", len(added_rows), added_csv)
    logging.info("%d persNames unchanged → %s", len(unchanged_rows), unchanged_csv)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    script_dir = Path(__file__).resolve()
    default_src  = script_dir.parents[2] / "Correspondence"
    default_dest = default_src.with_name(f"{default_src.name}-fixed")
    default_per  = script_dir.parents[2].parent / "data" / "Index" / "Person" / "SZDPER.xml"

    p = argparse.ArgumentParser(description="Batch-fix @ref attributes and generate CSV reports; defaults let you run with no flags.")
    p.add_argument("--src", type=Path, default=default_src, help="Source directory (default: %(default)s)")
    p.add_argument("--dest", type=Path, default=default_dest, help="Destination directory (default: %(default)s)")
    p.add_argument("--persons", type=Path, default=default_per, help="Path to SZDPER.xml (default: %(default)s)")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    if not args.src.is_dir():
        p.error(f"Source directory not found: {args.src}")
    if not args.persons.exists():
        p.error(f"SZDPER.xml not found: {args.persons}")

    batch_process(args.src, args.dest, args.persons)

if __name__ == "__main__":
    main()
