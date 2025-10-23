#!/usr/bin/env python3
"""
validate_tei_csv.py  v0.9  (2025-04-27)

Offline validator for the Zweig correspondence corpus.
"""

from __future__ import annotations

import csv
import logging
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import xml.etree.ElementTree as ET

# --------------------------------------------------------------------------- #
#  Paths & logging                                                            #
# --------------------------------------------------------------------------- #
BASE     = Path(__file__).parent
DATA_DIR = BASE / "data"
TEI_DIR  = BASE / "tei"
LOG_FILE = BASE / "validate_tei_csv.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, "w", "utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

NS = {
    "tei": "http://www.tei-c.org/ns/1.0",
    "xml": "http://www.w3.org/XML/1998/namespace",        # <-- fix
}
STRIP_RE = re.compile(r"\s+")

# --------------------------------------------------------------------------- #
#  Helpers                                                                    #
# --------------------------------------------------------------------------- #
def norm(txt: str) -> str:
    return STRIP_RE.sub(" ", (txt or "").strip())


def split_multi(cell: str) -> List[str]:
    return [norm(p) for p in cell.split(";") if p.strip()]


def join_forename_surname(pers: ET.Element | None) -> str:
    if pers is None:
        return ""
    fn  = pers.find("tei:forename", NS)
    sur = pers.find("tei:surname", NS)
    parts = []
    if fn is not None and fn.text:
        parts.append(fn.text)
    if sur is not None and sur.text:
        parts.append(sur.text)
    return norm(" ".join(parts)) or norm(pers.text or "")


def lang_iso(val: str) -> str:
    return val.lower()


def clark(attr: str) -> str:
    """Translate 'xml:lang' → '{uri}lang' if namespaced, else return unchanged."""
    if ":" not in attr:
        return attr
    prefix, local = attr.split(":", 1)
    uri = NS.get(prefix)
    return f"{{{uri}}}{local}" if uri else attr

# --------------------------------------------------------------------------- #
#  Mapping rules (excerpt – extend as needed)                                 #
# --------------------------------------------------------------------------- #
Rule = Dict[str, object]

M: Dict[str, Rule] = {
    # --- identifiers ----------------------------------------------------- #
    "PID": {
        "xpath": ".//tei:idno[@type='PID']",
        "attr": None, "card": "0-1",
    },
    "Context": {
        "xpath": ".//tei:idno[@type='context']",
        "attr": None, "card": "0-1",
    },
    "Signatur": {
        "xpath": ".//tei:idno[@type='signature']",
        "attr": None, "card": "1",
    },

    # --- agents: sender (sent) ------------------------------------------- #
    "Verfasser*in": {
        "custom": lambda b: [join_forename_surname(
            b.find(".//tei:correspAction[@type='sent']/tei:persName", NS))],
        "split": False, "card": "1",
    },
    "Verfasser*in GND": {
        "xpath": ".//tei:correspAction[@type='sent']/tei:persName",
        "attr": "ref", "card": "0-1",
    },
    "Körperschaft Verfasser*in": {
        "xpath": ".//tei:correspAction[@type='sent']/tei:orgName",
        "attr": None, "card": "0-n",
    },
    "Körperschaft Verfasser*in GND": {
        "xpath": ".//tei:correspAction[@type='sent']/tei:orgName",
        "attr": "ref", "card": "0-n",
    },

    # --- agents: receiver (received) ------------------------------------- #
    "Adressat*in": {
        "custom": lambda b: [join_forename_surname(
            b.find(".//tei:correspAction[@type='received']/tei:persName", NS))],
        "split": False, "card": "1",
    },
    "Adressat*in GND": {
        "xpath": ".//tei:correspAction[@type='received']/tei:persName",
        "attr": "ref", "card": "0-1",
    },
    "Körperschaft Adressat*in": {
        "xpath": ".//tei:correspAction[@type='received']/tei:orgName",
        "attr": None, "card": "0-n",
    },
    "Körperschaft Adressat*in GND": {
        "xpath": ".//tei:correspAction[@type='received']/tei:orgName",
        "attr": "ref", "card": "0-n",
    },

    # --- material & extent ------------------------------------------------ #
    "Art/Umfang": {
        "xpath": ".//tei:extent/tei:span[@xml:lang='de']",
        "attr": None, "card": "1",
    },
    "Physical Description": {
        "xpath": ".//tei:extent/tei:span[@xml:lang='en']",
        "attr": None, "card": "1",
    },
    "Beilagen": {
        "xpath": ".//tei:additional/tei:list[@type='enclosure']/tei:item[@xml:lang='de']",
        "attr": None, "card": "0-n",
    },
    "Enclosures": {
        "xpath": ".//tei:additional/tei:list[@type='enclosure']/tei:item[@xml:lang='en']",
        "attr": None, "card": "0-n",
    },

    # --- dates ------------------------------------------------------------ #
    "Datierung Original": {
        "xpath": ".//tei:correspAction[@type='sent']/tei:date[@xml:lang='de']",
        "attr": None, "card": "1",
    },
    "Date original": {
        "xpath": ".//tei:correspAction[@type='sent']/tei:date[@xml:lang='en']",
        "attr": None, "card": "1",
    },
    "Datierung erschlossen": {
        "xpath": ".//tei:correspAction[@type='sent']/tei:date[@type='supplied'][@xml:lang='de']",
        "attr": None, "card": "0-1",
    },
    "Date supplied/verified": {
        "xpath": ".//tei:correspAction[@type='sent']/tei:date[@type='supplied'][@xml:lang='en']",
        "attr": None, "card": "0-1",
    },
    "Datierung normalisiert": {
        "xpath": ".//tei:correspAction[@type='sent']/tei:date",
        "attr": "when", "card": "1",
    },

    # --- places & addresses ---------------------------------------------- #
    "Poststempel": {
        "xpath": ".//tei:correspAction[@type='sent']/tei:placeName[@type='postmark']",
        "attr": None, "card": "0-1",
    },
    "Entstehungsort Original": {
        "xpath": ".//tei:correspAction[@type='sent']/tei:placeName[@xml:lang='de']",
        "attr": None, "card": "0-1",
    },
    "Entstehungsort erschlossen": {
        "xpath": ".//tei:correspAction[@type='sent']/tei:placeName[@xml:lang='en']",
        "attr": None, "card": "0-1",
    },
    "Postanschrift (original)": {
        "xpath": ".//tei:correspAction[@type='sent']/tei:address/tei:addrLine[@xml:lang='de']",
        "attr": None, "card": "0-n",
    },
    "Postanschrift normalisiert": {
        "xpath": ".//tei:correspAction[@type='sent']/tei:address/tei:addrLine[@type='normalized']",
        "attr": None, "card": "0-n",
    },

    # --- language --------------------------------------------------------- #
    "Sprache": {
        "xpath": ".//tei:msContents/tei:textLang/tei:lang",
        "attr": "xml:lang",
        "transform": lang_iso, "card": "1",
    },

    # --- physical description -------------------------------------------- #
    "Beschreibstoff": {
        "xpath": ".//tei:material[@ana='szdg:WritingMaterial'][@xml:lang='de']",
        "attr": None, "card": "1",
    },
    "Writing Material": {
        "xpath": ".//tei:material[@ana='szdg:WritingMaterial'][@xml:lang='en']",
        "attr": None, "card": "1",
    },
    "Schreibstoff": {
        "xpath": ".//tei:material[@ana='szdg:WritingInstrument'][@xml:lang='de']",
        "attr": None, "card": "1",
    },
    "Writing Instrument": {
        "xpath": ".//tei:material[@ana='szdg:WritingInstrument'][@xml:lang='en']",
        "attr": None, "card": "1",
    },
    "Schreiberhand": {
        "xpath": ".//tei:handDesc/tei:handNote",
        "attr": None, "card": "0-1",
    },
    "Maße": {
        "xpath": ".//tei:measureGrp/tei:measure",
        "attr": None, "card": "0-n",
    },

    # --- repository & provenance ----------------------------------------- #
    "Standort GND": {
        "xpath": ".//tei:repository",
        "attr": "ref", "card": "1",
    },
    "Provenienz": {
        "xpath": ".//tei:history/tei:provenance/tei:ab[@xml:lang='de']",
        "attr": None, "card": "0-1",
    },
    "Erwerbung": {
        "xpath": ".//tei:history/tei:acquisition/tei:ab[@xml:lang='de']",
        "attr": None, "card": "0-1",
    },
    "Acquired": {
        "xpath": ".//tei:history/tei:acquisition/tei:ab[@xml:lang='en']",
        "attr": None, "card": "0-1",
    },

    # --- notes & participants -------------------------------------------- #
    "Beteiligte": {
        "xpath": ".//tei:note[@type='participants'][@xml:lang='de']",
        "attr": None, "card": "0-1",
    },
    "Beteiligte (GND)": {
        "xpath": ".//tei:note[@type='participants']/tei:name",
        "attr": "ref", "card": "0-n",
    },
    "Hinweis": {
        "xpath": ".//tei:note[@type='hint'][@xml:lang='de']",
        "attr": None, "card": "0-1",
    },
    "Note(s)": {
        "xpath": ".//tei:note[@type='hint'][@xml:lang='en']",
        "attr": None, "card": "0-1",
    },
    "Anmerkungen": {
        "xpath": ".//tei:note[@type='comment'][@xml:lang='de']",
        "attr": None, "card": "0-n",
    },
}
# --------------------------------------------------------------------------- #
#  Build TEI signature index                                                  #
# --------------------------------------------------------------------------- #
sig_index: Dict[str, Tuple[Path, ET.Element]] = {}
parse_errors = 0

for xml_path in TEI_DIR.glob("*.xml"):
    try:
        root = ET.parse(xml_path).getroot()
    except ET.ParseError as exc:
        parse_errors += 1
        logging.error("XML parse error %s – %s", xml_path.name, exc)
        continue

    for bibl in root.findall(".//tei:biblFull", NS):
        id_el = bibl.find(".//tei:idno[@type='signature']", NS)
        if id_el is not None and id_el.text:
            sig_index[id_el.text.strip()] = (xml_path, bibl)

logging.info("[IDX] %d TEI files, %d signatures indexed, %d parse errors",
             len(list(TEI_DIR.glob('*.xml'))), len(sig_index), parse_errors)

# --------------------------------------------------------------------------- #
#  Validation loop                                                            #
# --------------------------------------------------------------------------- #
total_rows = ok_rows = err_rows = 0

for csv_file in sorted(DATA_DIR.glob("*.csv")):
    with csv_file.open(encoding="utf-8-sig", newline="") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            total_rows += 1
            sig = row.get("Signatur", "").strip()
            if not sig or sig not in sig_index:
                err_rows += 1
                logging.error("Signature %s not found in TEI (CSV %s row %d)",
                              sig or "<empty>", csv_file.name, total_rows)
                continue

            tei_path, bibl = sig_index[sig]
            errors: List[str] = []

            for col, val in row.items():
                if not val or col not in M:
                    continue
                rule = M[col]

                # Obtain TEI values
                if "custom" in rule:
                    tei_vals = rule["custom"](bibl)
                else:
                    nodes = bibl.findall(rule["xpath"], NS)
                    attr = rule.get("attr")
                    if attr:
                        akey = clark(attr)
                        tei_vals = [norm(n.get(akey) or "") for n in nodes if n.get(akey)]
                    else:
                        tei_vals = [norm(n.text or "") for n in nodes if n.text and n.text.strip()]

                # Apply transforms
                val_cmp = rule.get("transform", lambda x: x)(val)
                tei_vals = [rule.get("transform", lambda x: x)(t) for t in tei_vals]

                csv_vals = split_multi(val_cmp) if rule.get("split", True) else [norm(val_cmp)]

                # Cardinality
                card = rule.get("card")
                if card == "1" and len(tei_vals) != 1:
                    errors.append(f"{col}: expected 1, got {len(tei_vals)}")
                elif card == "0-1" and len(tei_vals) > 1:
                    errors.append(f"{col}: expected ≤1, got {len(tei_vals)}")

                # Value equality (set, order-insensitive)
                if set(csv_vals) != set(tei_vals):
                    errors.append(f"{col}: CSV {csv_vals} ≠ TEI {tei_vals}")

            if errors:
                err_rows += 1
                logging.error("FAIL %s ↔ %s: %s",
                              sig, tei_path.name, "; ".join(errors))
            else:
                ok_rows += 1
                logging.info("OK   %s ↔ %s", sig, tei_path.name)

# --------------------------------------------------------------------------- #
#  Summary                                                                    #
# --------------------------------------------------------------------------- #
logging.info("[SUM] rows=%d  ok=%d  errors=%d  xmlParseErrors=%d",
             total_rows, ok_rows, err_rows, parse_errors)
print(f"\nValidation finished – see {LOG_FILE}")
