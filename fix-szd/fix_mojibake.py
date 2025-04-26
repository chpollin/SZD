#!/usr/bin/env python3
"""
fix_mojibake.py   v1.2   (2025-04-27)

Repairs every TEI XML in ./tei/ and writes the cleaned version to
./tei-hudriwduri/ (same basename) **only if** any of these fixes apply:

  1. Undo UTF-8 mojibake (Ãsterreich → Österreich)
     • uses `ftfy` if installed, else a safe Latin-1⇆UTF-8 round-trip
  2. Remove trailing ", SZ-…/…" from every <title xml:lang="de|en">
     • tolerant of any whitespace / newlines before the comma
  3. Delete empty <altIdentifier><idno type="context"/> blocks
"""

from __future__ import annotations
import logging, re
from pathlib import Path
import xml.etree.ElementTree as ET

# ── folders ──────────────────────────────────────────────────────────────
SRC_DIR = Path("tei")
OUT_DIR = Path("tei-hudriwduri")
OUT_DIR.mkdir(exist_ok=True)

# ── logging ───────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("fix")

# ── 1. mojibake repair ────────────────────────────────────────────────────
try:
    from ftfy import fix_text  # type: ignore

    def de_mojibake(s: str) -> str:
        return fix_text(s)

    log.info("ftfy found – robust encoding repair enabled")

except ModuleNotFoundError:
    log.info("ftfy not installed – using basic Latin-1⇆UTF-8 round-trip")

    def de_mojibake(s: str) -> str:
        try:
            repaired = s.encode("latin-1").decode("utf-8")
            if "Ã" in repaired or "Â" in repaired or "\uFFFD" in repaired:
                return s   # still broken → keep original
            return repaired
        except UnicodeEncodeError:
            return s       # couldn’t encode in Latin-1 → leave unchanged

# ── 2. structural tidy helpers ────────────────────────────────────────────
TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}
ET.register_namespace("", TEI_NS["tei"])        # write default ns w/o prefix

# regex now tolerates whitespace / newlines before & after comma
TITLE_SIG_RE = re.compile(r",\s*SZ-[A-Z]+/[A-Za-z0-9.\-]+\s*$")

def tidy_titles(root: ET.Element) -> bool:
    changed = False
    for tit in root.findall(".//tei:titleStmt/tei:title", TEI_NS):
        if tit.text and TITLE_SIG_RE.search(tit.text):
            tit.text = TITLE_SIG_RE.sub("", tit.text)
            changed = True
    return changed

def drop_empty_context(root: ET.Element) -> bool:
    removed = False
    for ms_id in root.findall(".//tei:msIdentifier", TEI_NS):
        for alt in list(ms_id.findall("tei:altIdentifier", TEI_NS)):
            idn = alt.find("tei:idno[@type='context']", TEI_NS)
            if idn is not None and (idn.text is None or not idn.text.strip()):
                ms_id.remove(alt)
                removed = True
    return removed

# ── 3. main loop ──────────────────────────────────────────────────────────
fixed = skipped = 0

for xml_path in SRC_DIR.glob("*.xml"):
    raw = xml_path.read_text(encoding="utf-8", errors="ignore")
    text_fixed = de_mojibake(raw)

    try:
        tree = ET.ElementTree(ET.fromstring(text_fixed))
    except ET.ParseError as err:
        log.warning("parse error in %s – skipped (%s)", xml_path.name, err)
        continue

    root = tree.getroot()
    changed = (text_fixed != raw)

    # structural fixes
    if tidy_titles(root):
        changed = True
    if drop_empty_context(root):
        changed = True

    if changed:
        tree.write(OUT_DIR / xml_path.name, encoding="utf-8", xml_declaration=True)
        fixed += 1
        log.info("✓ %s – repaired & saved", xml_path.name)
    else:
        skipped += 1
        log.info("· %s – no change", xml_path.name)

log.info("--- summary ---")
log.info("processed: %d   repaired: %d   unchanged: %d",
         fixed + skipped, fixed, skipped)
print(f"\nCleaned files: {fixed}  →  {OUT_DIR.resolve()}")
