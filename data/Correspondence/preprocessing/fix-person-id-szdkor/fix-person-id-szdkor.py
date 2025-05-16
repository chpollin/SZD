#!/usr/bin/env python3
"""
fix-person-id-szdkor.py
======================

Enhanced version — **2025-05-16**
--------------------------------
* Replaces `@ref` placeholders with the correct **GND URI** from *SZDPER.xml*.
* Removes the placeholder when the person is present in SZDPER but has **no** GND.
* Handles:
  * split `<surname>/<forename>` pairs (case and diacritic insensitive),
  * single `<name>` corporate bodies,
  * abbreviations like **"Richard M." ⇄ "Richard M"** (trailing dots ignored).
* Treats a candidate list as **unambiguous** when every value is identical or
  when it contains exactly **one non-empty** GND plus any number of empty
  strings (variants without GND).
* Output stays namespace-clean (`<TEI xmlns="…">`) → **SZDKOR-fixed.xml**.

Usage:
```bash
python fix-person-id-szdkor.py   # defaults inferred from script location
```
"""
from __future__ import annotations

import argparse
import logging
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple
from xml.etree import ElementTree as ET
import re

# ---------------------------------------------------------------------------
# Namespace handling – default TEI namespace, no ns0 prefixes
# ---------------------------------------------------------------------------
TEI_NS_URI = "http://www.tei-c.org/ns/1.0"
TEI_NS = {"tei": TEI_NS_URI}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
ET.register_namespace("", TEI_NS_URI)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
DOT_RE = re.compile(r"\.+$")  # trailing dots


def _clean_text(el: ET.Element | None) -> str | None:
    if el is not None and el.text:
        return " ".join(el.text.split())  # collapse whitespace
    return None


def _simplify(txt: str) -> str:
    """Lower-case, remove diacritics, collapse whitespace, strip trailing dots."""
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(c for c in txt if not unicodedata.combining(c))
    tokens = [DOT_RE.sub("", t) for t in txt.lower().split()]
    return " ".join(tokens)


def _is_unambiguous(cands: List[str]) -> tuple[bool, str | None]:
    """Return (True, chosen_value) if candidate list is unambiguous."""
    if not cands:
        return False, None
    # Deduplicate while preserving order
    uniq = []
    for c in cands:
        if c not in uniq:
            uniq.append(c)
    if len(uniq) == 1:
        return True, uniq[0]
    # Exactly one non-empty + rest empty → treat as unambiguous non-empty
    non_empty = [c for c in uniq if c]
    if len(non_empty) == 1:
        return True, non_empty[0]
    return False, None

# ---------------------------------------------------------------------------
# Build lookup tables from SZDPER
# ---------------------------------------------------------------------------

def build_indexes(persons_path: Path):
    pair_idx: Dict[Tuple[str, str], List[str]] = defaultdict(list)
    full_idx: Dict[str, List[str]] = defaultdict(list)

    root = ET.parse(persons_path).getroot()

    for person in root.findall(".//tei:person", TEI_NS):
        pn = person.find("tei:persName", TEI_NS)
        if pn is None:
            continue

        gnd = pn.get("ref", "")  # empty string → no GND

        sur = _clean_text(pn.find("tei:surname", TEI_NS))
        fore = _clean_text(pn.find("tei:forename", TEI_NS))
        if sur and fore:
            sur_s, fore_s = _simplify(sur), _simplify(fore)
            pair_idx[(sur_s, fore_s)].append(gnd)
            full_idx[f"{fore_s} {sur_s}"].append(gnd)
            full_idx[f"{sur_s} {fore_s}"].append(gnd)

        name_raw = _clean_text(pn.find("tei:name", TEI_NS))
        if name_raw:
            full_idx[_simplify(name_raw)].append(gnd)

    return pair_idx, full_idx

# ---------------------------------------------------------------------------
# Main fix routine
# ---------------------------------------------------------------------------

def fix_szdkor(szdkor: Path, out_path: Path, pair_idx, full_idx):
    tree = ET.parse(szdkor)
    root = tree.getroot()

    added = removed = ambiguous = missing = 0

    for bibl in root.findall(".//tei:biblFull", TEI_NS):
        bid = bibl.get(XML_ID, "[no @xml:id]")

        for pn in bibl.findall(".//tei:persName", TEI_NS):
            ref_val = pn.get("ref")
            if ref_val and not ref_val.endswith("/placeholder"):
                continue

            sur_raw  = _clean_text(pn.find("tei:surname", TEI_NS))
            fore_raw = _clean_text(pn.find("tei:forename", TEI_NS))
            sur_s    = _simplify(sur_raw) if sur_raw else None
            fore_s   = _simplify(fore_raw) if fore_raw else None

            cands: List[str] = []
            if sur_s and fore_s:
                cands = pair_idx.get((sur_s, fore_s), [])

            if not cands:
                name_raw = _clean_text(pn.find("tei:name", TEI_NS))
                if name_raw:
                    cands = full_idx.get(_simplify(name_raw), [])

            if not cands and sur_raw and fore_raw:
                cands = (full_idx.get(_simplify(f"{fore_raw} {sur_raw}"), []) or
                         full_idx.get(_simplify(f"{sur_raw} {fore_raw}"), []))

            disp = (_clean_text(pn.find("tei:name", TEI_NS)) or
                    f"{fore_raw or ''} {sur_raw or ''}".strip() or "[unknown]")

            ok, chosen = _is_unambiguous(cands)
            if ok:
                if chosen:  # non-empty GND
                    pn.set("ref", chosen)
                    added += 1
                    logging.info("Added GND for '%s' in %s -> %s", disp, bid, chosen)
                else:       # empty → known but no GND yet
                    pn.attrib.pop("ref", None)
                    removed += 1
                    logging.info("Removed placeholder for '%s' in %s (no GND)", disp, bid)
            elif not cands:
                missing += 1
                logging.warning("No match for '%s' in %s", disp, bid)
            else:
                ambiguous += 1
                logging.warning("Ambiguous match for '%s' in %s (%s)", disp, bid, ", ".join(set(cands)))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(out_path, encoding="utf-8", xml_declaration=True)

    logging.info(
        "Finished. %d added, %d placeholders removed, %d ambiguous, %d unmatched.",
        added, removed, ambiguous, missing,
    )

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    base = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="Fix @ref placeholders in SZDKOR.xml using SZDPER.xml")
    parser.add_argument("--szdkor", type=Path, default=base / "SZDKOR.xml")
    parser.add_argument("--persons", type=Path, default=Path(r"C:\Users\Chrisi\Documents\GitHub\SZD\data\Index\Person\SZDPER.xml"))
    parser.add_argument("--out", type=Path, default=base / "SZDKOR-fixed.xml")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    if not args.szdkor.exists():
        parser.error(f"SZDKOR file not found: {args.szdkor}")
    if not args.persons.exists():
        parser.error(f"SZDPER file not found: {args.persons}")

    pair_idx, full_idx = build_indexes(args.persons)
    logging.info("Index loaded: %d pair keys, %d full-name keys", len(pair_idx), len(full_idx))

    fix_szdkor(args.szdkor, args.out, pair_idx, full_idx)

if __name__ == "__main__":
    main()
