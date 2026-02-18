#!/usr/bin/env python3
"""
Korrigiert alle fehlerhaften PIDs in SZDLEB.xml anhand der METADATA-Liste von GAMS.
Matching erfolgt über die Signatur (z.B. SZ-SAH/L1).
"""

import xml.etree.ElementTree as ET
import urllib.request
import re
import os
import time

METADATA_URL = (
    "https://gams.uni-graz.at/archive/objects/"
    "context:szd.facsimiles.lebensdokumente/datastreams/METADATA/content"
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XML_PATH = os.path.normpath(os.path.join(SCRIPT_DIR, "../data/PersonalDocument/SZDLEB.xml"))


def fetch_signature_to_pid_map() -> dict[str, str]:
    """Fetch METADATA from GAMS and build signature -> correct PID mapping."""
    print("Lade METADATA von GAMS...")
    req = urllib.request.Request(METADATA_URL)
    req.add_header("User-Agent", "SZD-PID-Fixer/1.0")

    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read().decode("utf-8")

    root = ET.fromstring(content)
    ns = "{http://www.w3.org/2001/sw/DataAccess/rf1/result}"
    sig_pattern = re.compile(r'(SZ-[A-Z0-9]+/L[\w\-\.]+)')

    sig_to_pid = {}
    seen = set()

    for result in root.iter(f"{ns}result"):
        identifier_el = result.find(f"{ns}identifier")
        title_el = result.find(f"{ns}title")

        if identifier_el is None or identifier_el.text is None:
            continue

        pid = identifier_el.text.strip()
        if pid in seen:
            continue
        seen.add(pid)

        title = (title_el.text or "").strip() if title_el is not None else ""
        sig_match = sig_pattern.search(title)
        if sig_match:
            sig_to_pid[sig_match.group(1)] = pid

    print(f"  -> {len(sig_to_pid)} Signatur-PID-Zuordnungen gefunden\n")
    return sig_to_pid


def fix_pids_in_xml(xml_path: str, sig_to_pid: dict[str, str]) -> int:
    """Replace wrong PIDs in the XML file using simple text replacement."""
    print(f"Lese XML: {xml_path}")

    with open(xml_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # Parse XML to extract signature -> old PID mapping
    tei_ns = "{http://www.tei-c.org/ns/1.0}"
    root = ET.fromstring(content)

    replacements = []

    for biblfull in root.iter(f"{tei_ns}biblFull"):
        xml_id = biblfull.get("{http://www.w3.org/XML/1998/namespace}id", "")

        # Find signature
        signature = ""
        for idno in biblfull.iter(f"{tei_ns}idno"):
            if idno.get("type") == "signature":
                signature = (idno.text or "").strip()
                break

        # Find current PID
        old_pid = ""
        for idno in biblfull.iter(f"{tei_ns}idno"):
            if idno.get("type") == "PID":
                old_pid = (idno.text or "").strip()
                break

        if not old_pid or old_pid == "o:szd.lebensdokumente":
            continue

        # Look up correct PID
        correct_pid = sig_to_pid.get(signature)
        if correct_pid and correct_pid != old_pid:
            replacements.append((xml_id, signature, old_pid, correct_pid))

    # Now do the replacements in the raw XML text
    # We need to be careful to only replace PIDs inside their <idno type="PID"> context
    fixed = 0
    for xml_id, signature, old_pid, new_pid in replacements:
        # Match the exact PID value within an idno element
        # Pattern: >o:szd.XXXX< inside an idno type="PID" context
        old_text = f">{old_pid}<"
        new_text = f">{new_pid}<"

        if old_text in content:
            content = content.replace(old_text, new_text, 1)
            fixed += 1
            print(f"  {xml_id:<12} {signature:<20} {old_pid:<20} -> {new_pid}")

    if fixed > 0:
        # Write back
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\n  {fixed} PIDs korrigiert und gespeichert.")
    else:
        print("\n  Keine Korrekturen nötig.")

    return fixed


def main():
    print("=== SZD Lebensdokumente PID-Korrektur ===\n")

    sig_to_pid = fetch_signature_to_pid_map()
    fixed = fix_pids_in_xml(XML_PATH, sig_to_pid)

    print(f"\nFertig! {fixed} PIDs wurden korrigiert.")


if __name__ == "__main__":
    main()
