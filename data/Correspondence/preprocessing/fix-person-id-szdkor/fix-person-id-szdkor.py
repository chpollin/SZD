#!/usr/bin/env python3
"""
fix-person-id-szdkor.py
======================

* Replaces placeholder `@ref` values in **SZDKOR.xml** using **SZDPER.xml**.
* If the matched person **has a GND** (`persName/@ref`) → write that URI.
* If the matched person **lacks** a GND → write a *local* reference to the
  person entry (`ref="#SZDPER.####"`).
* Produces namespace‑clean output (`<TEI xmlns="…">`).
"""
from __future__ import annotations

import argparse
import logging
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, NamedTuple
from xml.etree import ElementTree as ET

# ---------------------------------------------------------------------------
# Namespace handling
# ---------------------------------------------------------------------------
TEI_NS_URI = "http://www.tei-c.org/ns/1.0"
TEI_NS = {"tei": TEI_NS_URI}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
ET.register_namespace("", TEI_NS_URI)  # write default namespace

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _clean_text(el: ET.Element | None) -> str | None:
    return " ".join(el.text.split()) if el is not None and el.text else None


def _simplify(txt: str) -> str:
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(ch for ch in txt if not unicodedata.combining(ch))
    return " ".join(txt.lower().split())

# ---------------------------------------------------------------------------
# Data structure for person match
# ---------------------------------------------------------------------------
class Candidate(NamedTuple):
    ref: str | None   # the GND URI *or* None if missing
    pid: str          # SZDPER xml:id (always present)

# ---------------------------------------------------------------------------
# Build lookup tables from SZDPER.xml
# ---------------------------------------------------------------------------

def build_indexes(persons_path: Path) -> tuple[
    Dict[Tuple[str, str], List[Candidate]],
    Dict[str, List[Candidate]],
]:
    tree = ET.parse(persons_path)
    root = tree.getroot()

    pair_idx: Dict[Tuple[str, str], List[Candidate]] = defaultdict(list)
    full_idx: Dict[str, List[Candidate]] = defaultdict(list)

    for person in root.findall(".//tei:person", TEI_NS):
        pid = person.get(XML_ID)
        if not pid:
            continue  # skip malformed

        pn = person.find("tei:persName", TEI_NS)
        if pn is None:
            continue

        gnd = pn.get("ref")  # may be None or empty
        sur = _clean_text(pn.find("tei:surname", TEI_NS))
        fore = _clean_text(pn.find("tei:forename", TEI_NS))
        if not (sur and fore):
            continue

        cand = Candidate(ref=gnd or None, pid=pid)

        sur_s, fore_s = _simplify(sur), _simplify(fore)
        pair_idx[(sur_s, fore_s)].append(cand)

        full_fw = f"{fore_s} {sur_s}"
        full_bw = f"{sur_s} {fore_s}"
        full_idx[full_fw].append(cand)
        full_idx[full_bw].append(cand)

    return pair_idx, full_idx

# ---------------------------------------------------------------------------
# Main fixer
# ---------------------------------------------------------------------------

def fix_szdkor(szdkor: Path, out_path: Path, pair_idx, full_idx):
    tree = ET.parse(szdkor)
    root = tree.getroot()

    added_gnd = added_local = ambiguous = missing = 0

    for bibl in root.findall(".//tei:biblFull", TEI_NS):
        bid = bibl.get(XML_ID, "[no @xml:id]")

        for pn in bibl.findall(".//tei:persName", TEI_NS):
            ref_val = pn.get("ref")
            if ref_val and not ref_val.endswith("/placeholder"):
                continue  # already proper

            # Key strings
            sur_raw  = _clean_text(pn.find("tei:surname", TEI_NS))
            fore_raw = _clean_text(pn.find("tei:forename", TEI_NS))
            sur_s, fore_s = (_simplify(sur_raw) if sur_raw else None,
                              _simplify(fore_raw) if fore_raw else None)

            candidates: List[Candidate] = []
            if sur_s and fore_s:
                candidates = pair_idx.get((sur_s, fore_s), [])
            if not candidates:
                name_raw = _clean_text(pn.find("tei:name", TEI_NS))
                if name_raw:
                    candidates = full_idx.get(_simplify(name_raw), [])

            disp = (
                _clean_text(pn.find("tei:name", TEI_NS)) or
                f"{fore_raw or ''} {sur_raw or ''}".strip() or "[unknown name]"
            )

            if len(candidates) == 1:
                cand = candidates[0]
                if cand.ref:  # has GND URI
                    pn.set("ref", cand.ref)
                    added_gnd += 1
                    logging.info("Set GND for '%s' in %s -> %s", disp, bid, cand.ref)
                else:  # no GND, use local SZDPER id
                    pn.set("ref", f"#{cand.pid}")
                    added_local += 1
                    logging.info("Set local ref for '%s' in %s -> #%s", disp, bid, cand.pid)
            elif len(candidates) == 0:
                missing += 1
                logging.warning("No match for '%s' in %s", disp, bid)
            else:
                ambiguous += 1
                logging.warning(
                    "Ambiguous match for '%s' in %s (candidates: %s)",
                    disp, bid, ", ".join(c.pid for c in candidates)
                )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(out_path, encoding="utf-8", xml_declaration=True)

    logging.info(
        "Finished. %d GND refs added, %d local refs added, %d ambiguous, %d unmatched.",
        added_gnd, added_local, ambiguous, missing
    )

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    base = Path(__file__).resolve().parents[2]
    argp = argparse.ArgumentParser(description="Fix person @ref placeholders in SZDKOR.xml")
    argp.add_argument("--szdkor", type=Path, default=base / "SZDKOR.xml")
    argp.add_argument("--persons", type=Path, default=Path(r"C:\Users\Chrisi\Documents\GitHub\SZD\data\Index\Person\SZDPER.xml"))
    argp.add_argument("--out", type=Path, default=base / "SZDKOR-fixed.xml")
    args = argp.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    if not args.szdkor.exists():
        argp.error(f"SZDKOR file not found: {args.szdkor}")
    if not args.persons.exists():
        argp.error(f"SZDPER file not found: {args.persons}")

    pair_idx, full_idx = build_indexes(args.persons)
    logging.info("Index built: %d pair keys, %d full-name keys", len(pair_idx), len(full_idx))

    fix_szdkor(args.szdkor, args.out, pair_idx, full_idx)

if __name__ == "__main__":
    main()
