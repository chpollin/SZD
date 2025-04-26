#!/usr/bin/env python3
"""
fetch_korrespondenzen.py  v0.7  (2025-04-27)

Offline version:
• reads all TEI XMLs from ./tei/
• extracts signatures and links them to CSV records in ./data/
• concise one-line logs, no network calls
"""

from __future__ import annotations

import collections
import csv
import logging
import re
import sys
import unicodedata
from pathlib import Path
from typing import Dict, List, Set

import xml.etree.ElementTree as ET

# --------------------------------------------------------------------------- #
#  Paths                                                                      #
# --------------------------------------------------------------------------- #
BASE     = Path(__file__).parent
DATA_DIR = BASE / "data"
TEI_DIR  = BASE / "tei"
LOG_FILE = BASE / "fetch_korrespondenzen.log"

# --------------------------------------------------------------------------- #
#  Helpers                                                                    #
# --------------------------------------------------------------------------- #
_SPACE_COMMA = str.maketrans(" ,", "--")

def _strip_diacritics(txt: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", txt)
                   if not unicodedata.combining(c))

def slugify_name(name: str) -> str:
    """(still available but not used now; kept for completeness)."""
    s = name.strip().lower().translate(_SPACE_COMMA)
    s = _strip_diacritics(s).replace("ß", "ss")
    s = re.sub(r"-{2,}", "-", s)
    s = re.sub(r"[^a-z0-9.\-]", "", s)
    return f"szd.korrespondenzen.{s}"

def extract_signatures(xml_txt: str) -> List[str]:
    try:
        root = ET.fromstring(xml_txt)
    except ET.ParseError:
        return []
    return sorted(
        {el.text.strip() for el in root.findall(".//{*}idno[@type='signature']") if el.text}
    )

def load_csv_signatures(folder: Path) -> Dict[str, List[str]]:
    """Return { signature → [csv filename, …] }."""
    sig_map: Dict[str, List[str]] = collections.defaultdict(list)
    for csv_file in folder.glob("*.csv"):
        try:
            with csv_file.open(encoding="utf-8-sig", newline="") as f:
                rdr = csv.DictReader(f)
                for row in rdr:
                    sig = (row.get("Signatur") or "").strip()
                    if sig:
                        sig_map[sig].append(csv_file.name)
        except Exception as exc:  # noqa: BLE001
            logging.error("CSV read error %s – %s", csv_file.name, exc)
    return sig_map


# --------------------------------------------------------------------------- #
#  Main                                                                       #
# --------------------------------------------------------------------------- #
def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, "w", "utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    # ------------------------------------------------------------------ #
    # 0  CSV index                                                       #
    # ------------------------------------------------------------------ #
    csv_sig_map = load_csv_signatures(DATA_DIR)
    logging.info("[CSV] %d files, %d unique signatures indexed",
                 len(list(DATA_DIR.glob('*.csv'))), len(csv_sig_map))

    # ------------------------------------------------------------------ #
    # 1  TEI loop (local files)                                          #
    # ------------------------------------------------------------------ #
    tei_files = sorted(TEI_DIR.glob("*.xml"))
    if not tei_files:
        logging.warning("No TEI files found in %s", TEI_DIR)
        sys.exit(1)

    logging.info("[TEI] %d files to process", len(tei_files))

    total_sigs = total_csv_hits = parse_errors = 0

    for tei_path in tei_files:
        slug = f"szd.korrespondenzen.{tei_path.stem}"

        try:
            xml_text = tei_path.read_text(encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            parse_errors += 1
            logging.error("File read error %s – %s", tei_path.name, exc)
            continue

        sigs = extract_signatures(xml_text)
        total_sigs += len(sigs)

        sig_hits = [s for s in sigs if s in csv_sig_map]
        total_csv_hits += len(sig_hits)

        logging.info("+ %s | sigs=%d | csv=%d | %s",
                     slug, len(sigs), len(sig_hits),
                     ",".join(sig_hits) if sig_hits else "-")

    # ------------------------------------------------------------------ #
    # 2  summary                                                         #
    # ------------------------------------------------------------------ #
    logging.info("[SUM] TEI processed=%d  read_errors=%d  signatures=%d  CSV links=%d",
                 len(tei_files), parse_errors, total_sigs, total_csv_hits)
    print(f"\nLog written to {LOG_FILE.resolve()}")


if __name__ == "__main__":
    main()
