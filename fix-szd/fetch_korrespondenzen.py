#!/usr/bin/env python3
"""
fetch_korrespondenzen.py  v0.3 (2025‑04‑22)

•  Download the Korrespondenzen SPARQL result (1 201 rows)
•  Analyse tag structure
•  Build ASCII‑only slugs (NFD → strip diacritics, ß→ss, etc.)
•  Fetch every partner’s TEI_SOURCE
•  Extract every  <idno type="signature">  inside the TEI
•  Log for each partner which signatures (convolutes) occur
•  Everything in ONE file: fetch_korrespondenzen.log
"""

from __future__ import annotations

import collections
import logging
import re
import sys
import unicodedata
from pathlib import Path
from typing import Dict, List, Set, Tuple
from urllib.parse import quote

import requests
import xml.etree.ElementTree as ET

# --------------------------------------------------------------------------- #
#  Config                                                                     #
# --------------------------------------------------------------------------- #
SPARQL_URL = (
    "https://gams.uni-graz.at/archive/risearch?"
    "type=tuples&lang=sparql&format=Sparql&"
    "query=http://fedora:8380/archive/get/context:szd.facsimiles.korrespondenzen/QUERY"
)
LOG_FILE = Path(__file__).with_suffix(".log")
TIMEOUT   = 60      # seconds


# --------------------------------------------------------------------------- #
#  Slug utilities                                                             #
# --------------------------------------------------------------------------- #
_SPACE_COMMA = str.maketrans(" ,", "--")           # space & comma → hyphen

def _strip_diacritics(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if not unicodedata.combining(c))

def slugify(person: str) -> str:
    s = person.strip().lower().translate(_SPACE_COMMA)
    s = _strip_diacritics(s).replace("ß", "ss")
    s = re.sub(r"-{2,}", "-", s)            # collapse “--”
    s = re.sub(r"[^a-z0-9.\-]", "", s)      # keep safe ASCII only
    return f"szd.korrespondenzen.{s}"


# --------------------------------------------------------------------------- #
#  XML helpers                                                                #
# --------------------------------------------------------------------------- #
def traverse(node: ET.Element,
             depth: int,
             tag_counter: collections.Counter,
             tag_attrs: Dict[str, Set[str]],
             max_depth: Tuple[int],
             paths: Set[str],
             cur_path: str) -> None:
    tag_counter[node.tag] += 1
    tag_attrs[node.tag].update(node.attrib.keys())
    paths.add(cur_path)
    max_depth[0] = max(max_depth[0], depth)
    for child in node:
        traverse(child, depth + 1, tag_counter, tag_attrs,
                 max_depth, paths, f"{cur_path}/{child.tag}")

def get_person_names(root: ET.Element) -> Set[str]:
    ns = {"s": "http://www.w3.org/2001/sw/DataAccess/rf1/result"}
    names: Set[str] = set()
    for r in root.findall(".//s:result", ns):
        creator = r.find("s:creator", ns)
        if creator is not None and creator.text and creator.text != "Zweig, Stefan":
            names.add(creator.text)
        contrib = r.find("s:contributor", ns)
        if contrib is not None and contrib.text and contrib.get("bound") != "false":
            names.add(contrib.text)
    return names

def extract_signatures(tei_xml: str) -> List[str]:
    try:
        root = ET.fromstring(tei_xml)
    except ET.ParseError:
        return []
    sigs = {el.text.strip() for el in
            root.findall(".//{*}idno[@type='signature']") if el.text}
    return sorted(sigs)


# --------------------------------------------------------------------------- #
#  Main                                                                       #
# --------------------------------------------------------------------------- #
def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    # 1  download SPARQL result ------------------------------------------------
    logging.info("Fetching SPARQL XML …")
    xml_text = requests.get(SPARQL_URL, timeout=TIMEOUT).text
    root = ET.fromstring(xml_text)

    # 2  basic structure statistics -------------------------------------------
    tag_counter: collections.Counter = collections.Counter()
    tag_attrs: Dict[str, Set[str]] = collections.defaultdict(set)
    max_depth = [0]
    paths: Set[str] = set()
    traverse(root, 0, tag_counter, tag_attrs, max_depth, paths, root.tag)
    logging.info("Root tag: %s  —  total elements: %d  —  max depth: %d",
                 root.tag, sum(tag_counter.values()), max_depth[0])

    logging.info("\n---- Tag statistics ----")
    for tag, cnt in tag_counter.most_common():
        attrs = ", ".join(sorted(tag_attrs[tag])) or "—"
        logging.info("• %-25s  count=%-6d  attrs=[%s]", tag, cnt, attrs)

    # 3  TEI phase -------------------------------------------------------------
    names = sorted(get_person_names(root))
    logging.info("\n---- TEI fetch phase ----")
    logging.info("Unique persons: %d", len(names))

    tei_found, tei_missing = 0, 0
    convolute_map: Dict[str, List[str]] = {}

    for person in names:
        slug = slugify(person)
        url  = f"https://stefanzweig.digital/o:{quote(slug, safe='.:')}/TEI_SOURCE"
        try:
            r = requests.get(url, timeout=TIMEOUT)
            if r.status_code == 200:
                tei_found += 1
                sigs = extract_signatures(r.text)
                convolute_map[person] = sigs
                logging.info("✓ %s", url)
            else:
                tei_missing += 1
                logging.info("✗ %s", url)
        except requests.RequestException:
            tei_missing += 1
            logging.info("✗ %s  (request error)", url)

    # 4  grouping log ----------------------------------------------------------
    logging.info("\n---- Convolutes per partner ----")
    for person in sorted(convolute_map):
        sigs = convolute_map[person]
        if sigs:
            logging.info("%s :", person)
            for s in sigs:
                logging.info("  * %s", s)

    # 5  summary ---------------------------------------------------------------
    logging.info("\nSummary: TEI found=%d  missing=%d", tei_found, tei_missing)
    print(f"\nAll details written to {LOG_FILE.resolve()}")


if __name__ == "__main__":
    main()
