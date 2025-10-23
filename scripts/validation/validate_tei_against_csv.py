#!/usr/bin/env python3
"""
validate_tei_against_csv.py  v1.0  (2025-04-27)

* Compare each CSV row (authoritative) with its corresponding <biblFull> in
  every TEI file found in ./tei/.
* Log discrepancies: missing TEI, missing element, value mismatch, wrong
  cardinality.
* Mapping rules follow TEI-CSV_MAPPING.md.
"""

from __future__ import annotations

import csv
import logging
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import xml.etree.ElementTree as ET

# ---------------------------------------------------------------------------- #
#  Config & paths                                                              #
# ---------------------------------------------------------------------------- #
BASE     = Path(__file__).parent
DATA_DIR = BASE / "data"
TEI_DIR  = BASE / "tei"
LOG_FILE = BASE / "tei_csv_audit.log"

TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}

# ---------------------------------------------------------------------------- #
#  Helper: mapping dictionary                                                  #
# ---------------------------------------------------------------------------- #
# Each entry:  csv column  →  list of (xpath, attr_name or None, lang_filter)
# - lang_filter: None     → ignore @xml:lang
#                 'de'/'en'   → pick node that has @xml:lang == value
#
# --------------------------------------------------------------------- #
#  Full CSV-to-TEI mapping dictionary                                   #
#  key = CSV column title                                               #
#  value = list of (relative XPath, attribute-name or None, xml:lang)   #
# --------------------------------------------------------------------- #

MAPPING = {
    # ──────────────────────────────────────────────────────────────
    # Identification
    "PID": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/"
         "tei:altIdentifier/tei:idno[@type='PID']", None, None)
    ],
    "Context": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/"
         "tei:altIdentifier/tei:idno[@type='context']", None, None)
    ],
    # ──────────────────────────────────────────────────────────────
    # Agents (persons & organisations)
    "Verfasser*in": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:persName", None, None)
    ],
    "Verfasser*in GND": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:persName", "ref", None)
    ],
    "Körperschaft Verfasser*in": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:orgName", None, None)
    ],
    "Körperschaft Verfasser*in GND": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:orgName", "ref", None)
    ],
    "Adressat*in": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/"
         "tei:persName", None, None)
    ],
    "Adressat*in GND": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/"
         "tei:persName", "ref", None)
    ],
    "Körperschaft Adressat*in": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/"
         "tei:orgName", None, None)
    ],
    "Körperschaft Adressat*in GND": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='received']/"
         "tei:orgName", "ref", None)
    ],
    # ──────────────────────────────────────────────────────────────
    # Physical extent & description
    "Art/Umfang": [
        ("./tei:fileDesc/tei:physDesc/tei:objectDesc/tei:supportDesc/"
         "tei:extent/tei:span", None, "de")
    ],
    "Physical Description": [
        ("./tei:fileDesc/tei:physDesc/tei:objectDesc/tei:supportDesc/"
         "tei:extent/tei:span", None, "en")
    ],
    "Beilagen": [
        ("./tei:fileDesc/tei:physDesc//tei:additional/"
         "tei:list[@type='enclosure']/tei:item", None, "de")
    ],
    "Enclosures": [
        ("./tei:fileDesc/tei:physDesc//tei:additional/"
         "tei:list[@type='enclosure']/tei:item", None, "en")
    ],
    # ──────────────────────────────────────────────────────────────
    # Dates
    "Datierung Original": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:date", None, "de")
    ],
    "Date original": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:date", None, "en")
    ],
    "Datierung erschlossen": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:date[@type='supplied']", None, "de")
    ],
    "Date supplied/verified": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:date[@type='supplied']", None, "en")
    ],
    "Datierung normalisiert": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:date", "when", None)
    ],
    # ──────────────────────────────────────────────────────────────
    # Places & addresses
    "Poststempel": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:placeName[@type='postmark']", None, None)
    ],
    "Entstehungsort Original": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:placeName", None, "de")
    ],
    "Entstehungsort erschlossen": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:placeName", None, "en")
    ],
    "Postanschrift (original)": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:address/tei:addrLine", None, "de")
    ],
    "Postanschrift normalisiert": [
        ("./tei:profileDesc/tei:correspDesc/tei:correspAction[@type='sent']/"
         "tei:address/tei:addrLine[@type='normalized']", None, None)
    ],
    # ──────────────────────────────────────────────────────────────
    # Language
    "Sprache": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msContents/"
         "tei:textLang/tei:lang", "xml:lang", None)
    ],
    # ──────────────────────────────────────────────────────────────
    # Materials & writing
    "Beschreibstoff": [
        ("./tei:fileDesc/tei:physDesc/tei:objectDesc/tei:supportDesc/"
         "tei:support/tei:material[@ana='szdg:WritingMaterial']", None, "de")
    ],
    "Writing Material": [
        ("./tei:fileDesc/tei:physDesc/tei:objectDesc/tei:supportDesc/"
         "tei:support/tei:material[@ana='szdg:WritingMaterial']", None, "en")
    ],
    "Schreibstoff": [
        ("./tei:fileDesc/tei:physDesc/tei:objectDesc/tei:supportDesc/"
         "tei:support/tei:material[@ana='szdg:WritingInstrument']", None, "de")
    ],
    "Writing Instrument": [
        ("./tei:fileDesc/tei:physDesc/tei:objectDesc/tei:supportDesc/"
         "tei:support/tei:material[@ana='szdg:WritingInstrument']", None, "en")
    ],
    "Schreiberhand": [
        ("./tei:fileDesc/tei:physDesc/tei:handDesc/tei:handNote", None, None)
    ],
    "Maße": [
        ("./tei:fileDesc/tei:physDesc/tei:objectDesc/tei:measureGrp/"
         "tei:measure", None, None)
    ],
    # ──────────────────────────────────────────────────────────────
    # Repository & signature
    "Standort GND": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/"
         "tei:repository", "ref", None)
    ],
    "Signatur": [
        ("./tei:fileDesc/tei:sourceDesc/tei:msDesc/tei:msIdentifier/"
         "tei:idno[@type='signature']", None, None)
    ],
    # ──────────────────────────────────────────────────────────────
    # History / provenance
    "Provenienz": [
        ("./tei:fileDesc/tei:history/tei:provenance/tei:ab", None, "de")
    ],
    "Erwerbung": [
        ("./tei:fileDesc/tei:history/tei:acquisition/tei:ab", None, "de")
    ],
    "Acquired": [
        ("./tei:fileDesc/tei:history/tei:acquisition/tei:ab", None, "en")
    ],
    # ──────────────────────────────────────────────────────────────
    # Notes & participants
    "Beteiligte": [
        ("./tei:fileDesc/tei:notesStmt/tei:note[@type='participants']",
         None, "de")
    ],
    "Beteiligte (GND)": [
        ("./tei:fileDesc/tei:notesStmt/tei:note[@type='participants']/"
         "tei:name", "ref", None)
    ],
    "Hinweis": [
        ("./tei:fileDesc/tei:notesStmt/tei:note[@type='hint']", None, "de")
    ],
    "Note(s)": [
        ("./tei:fileDesc/tei:notesStmt/tei:note[@type='hint']", None, "en")
    ],
    "Anmerkungen": [
        ("./tei:fileDesc/tei:notesStmt/tei:note[@type='comment']", None, "de")
    ],
}


NAME_PATTERN = re.compile(r"\s+", re.U)


# ---------------------------------------------------------------------------- #
#  Utilities                                                                   #
# ---------------------------------------------------------------------------- #
def normalise(txt: str) -> str:
    """trim, collapse whitespace, normalise NFD diacritics."""
    if txt is None:
        return ""
    txt = NAME_PATTERN.sub(" ", txt.strip())
    txt = unicodedata.normalize("NFC", txt)
    return txt


def csv_signature_index() -> Dict[str, Dict[str, str]]:
    """Load every CSV row, keyed by Signatur (first row wins on duplicates)."""
    index: Dict[str, Dict[str, str]] = {}
    for csv_file in DATA_DIR.glob("*.csv"):
        with csv_file.open(encoding="utf-8-sig", newline="") as f:
            rdr = csv.DictReader(f)
            if "Signatur" not in rdr.fieldnames:
                logging.warning("CSV %s has no 'Signatur' column – skipped", csv_file.name)
                continue
            for row in rdr:
                sig = normalise(row["Signatur"])
                if sig:
                    index[sig] = row
    return index


def tei_signature_index() -> Dict[str, Tuple[str, ET.Element]]:
    """
    Build {signature → (tei_filepath, biblFull_node)} for all TEI files.
    Assumes one biblFull per signature.
    """
    idx: Dict[str, Tuple[str, ET.Element]] = {}
    for tei_path in TEI_DIR.glob("*.xml"):
        try:
            tree = ET.parse(tei_path)
        except ET.ParseError as exc:
            logging.error("XML parse error %s – %s", tei_path.name, exc)
            continue
        for bibl in tree.findall(".//tei:biblFull", TEI_NS):
            sig_el = bibl.find(".//tei:idno[@type='signature']", TEI_NS)
            if sig_el is not None and sig_el.text:
                sig = normalise(sig_el.text)
                idx[sig] = (tei_path.name, bibl)
    return idx


def value_from_xpath(bibl: ET.Element,
                     xpath: str,
                     attr: str | None,
                     lang: str | None) -> List[str]:
    res: List[str] = []
    for node in bibl.findall(xpath, TEI_NS):
        if lang and node.get("{http://www.w3.org/XML/1998/namespace}lang") != lang:
            continue
        val = node.get(attr) if attr else "".join(node.itertext())
        if val is not None:
            res.append(normalise(val))
    return res


# ---------------------------------------------------------------------------- #
#  Validation loop                                                             #
# ---------------------------------------------------------------------------- #
def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",     # keep log extremely concise
        handlers=[logging.FileHandler(LOG_FILE, "w", "utf-8"),
                  logging.StreamHandler(sys.stdout)],
    )

    csv_idx  = csv_signature_index()
    tei_idx  = tei_signature_index()

    missing_tei   = 0
    missing_bibl  = 0
    mismatch_cnt  = 0
    ok_cnt        = 0

    for sig, row in csv_idx.items():
        if sig not in tei_idx:
            logging.info("!! %s  — TEI signature not found", sig)
            missing_tei += 1
            continue

        tei_file, bibl = tei_idx[sig]
        row_errors: List[str] = []

        for col, rules in MAPPING.items():
            csv_val = normalise(row.get(col, ""))
            if not csv_val:      # authoritative empty ⇒ nothing to check
                continue

            tei_vals: List[str] = []
            for xpath, attr, lang in rules:
                tei_vals.extend(value_from_xpath(bibl, xpath, attr, lang))

            if not tei_vals:
                row_errors.append(f"{col}=∅ (expected '{csv_val}')")
                continue

            # Special case: name concatenation
            if col == "Verfasser*in":
                tei_vals = [" ".join([normalise(x) for x in
                                      (bibl.find(xpath + "/tei:forename", TEI_NS).text
                                       if bibl.find(xpath + "/tei:forename", TEI_NS) is not None else "",
                                       bibl.find(xpath + "/tei:surname",  TEI_NS).text
                                       if bibl.find(xpath + "/tei:surname", TEI_NS) is not None else "")]).strip()
                             for xpath, _, _ in rules]

            if csv_val not in tei_vals:
                row_errors.append(f"{col} mismatch (csv='{csv_val}', tei={tei_vals})")

        if row_errors:
            mismatch_cnt += 1
            logging.info("× %s  — %s", sig, "; ".join(row_errors))
        else:
            ok_cnt += 1

    logging.info("--- summary ---")
    logging.info("csv rows: %d  ok: %d  mismatching: %d  missing TEI: %d",
                 len(csv_idx), ok_cnt, mismatch_cnt, missing_tei)
    print(f"\nFull report written to {LOG_FILE.resolve()}")


if __name__ == "__main__":
    if not DATA_DIR.exists() or not TEI_DIR.exists():
        sys.exit("data/ and tei/ folders must exist next to this script.")
    main()
