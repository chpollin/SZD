#!/usr/bin/env python3
"""
Vollständige Verifizierung: Prüft für jeden Eintrag in SZDLEB.xml, dass
1. Die PID per HTTP erreichbar ist (kein 404)
2. Die PID zur richtigen Signatur in der GAMS-METADATA passt
3. Keine PIDs in der XML fehlen, die in METADATA vorhanden sind
"""

import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
import re
import os
import time

METADATA_URL = (
    "https://gams.uni-graz.at/archive/objects/"
    "context:szd.facsimiles.lebensdokumente/datastreams/METADATA/content"
)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XML_PATH = os.path.normpath(os.path.join(SCRIPT_DIR, "../data/PersonalDocument/SZDLEB.xml"))

TEI_NS = "{http://www.tei-c.org/ns/1.0}"
SPARQL_NS = "{http://www.w3.org/2001/sw/DataAccess/rf1/result}"
GAMS_BASE = "https://gams.uni-graz.at"


def fetch_metadata() -> dict[str, dict]:
    """Returns {signature: {pid, title, signature}} from GAMS METADATA."""
    print("  Lade METADATA von GAMS...")
    req = urllib.request.Request(METADATA_URL)
    req.add_header("User-Agent", "SZD-Verifier/1.0")
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read().decode("utf-8")

    root = ET.fromstring(content)
    sig_pattern = re.compile(r'(SZ-[A-Z0-9]+/L[\w\-\.]+)')

    by_sig = {}
    by_pid = {}
    seen = set()

    for result in root.iter(f"{SPARQL_NS}result"):
        ident = result.find(f"{SPARQL_NS}identifier")
        title_el = result.find(f"{SPARQL_NS}title")
        if ident is None or ident.text is None:
            continue
        pid = ident.text.strip()
        if pid in seen:
            continue
        seen.add(pid)

        title = (title_el.text or "").strip() if title_el is not None else ""
        sig_match = sig_pattern.search(title)
        sig = sig_match.group(1) if sig_match else ""

        entry = {"pid": pid, "title": title, "signature": sig}
        if sig:
            by_sig[sig] = entry
        by_pid[pid] = entry

    print(f"  -> {len(by_sig)} Einträge mit Signatur, {len(by_pid)} gesamt\n")
    return by_sig, by_pid


def extract_xml_entries(xml_path: str) -> list[dict]:
    """Extract all biblFull entries from XML."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    entries = []

    for biblfull in root.iter(f"{TEI_NS}biblFull"):
        xml_id = biblfull.get("{http://www.w3.org/XML/1998/namespace}id", "")

        title_de = ""
        for t in biblfull.iter(f"{TEI_NS}title"):
            ana = t.get("ana", "")
            lang = t.get("{http://www.w3.org/XML/1998/namespace}lang", "")
            if ana in ("assigned", "original") and lang in ("de", ""):
                title_de = (t.text or "").strip()
                if title_de:
                    break

        signature = ""
        for idno in biblfull.iter(f"{TEI_NS}idno"):
            if idno.get("type") == "signature":
                signature = (idno.text or "").strip()
                break

        pid = ""
        for idno in biblfull.iter(f"{TEI_NS}idno"):
            if idno.get("type") == "PID":
                pid = (idno.text or "").strip()
                break

        if pid and pid != "o:szd.lebensdokumente":
            entries.append({
                "xml_id": xml_id,
                "title": title_de,
                "signature": signature,
                "pid": pid,
            })

    return entries


def check_url(pid: str) -> int:
    """HTTP HEAD check, returns status code."""
    url = f"{GAMS_BASE}/{pid}"
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "SZD-Verifier/1.0")
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def main():
    print("=" * 100)
    print("  VOLLSTÄNDIGE VERIFIZIERUNG - SZDLEB.xml PIDs")
    print("=" * 100 + "\n")

    # 1) Load both sources
    print("1) Datenquellen laden...")
    meta_by_sig, meta_by_pid = fetch_metadata()
    xml_entries = extract_xml_entries(XML_PATH)
    print(f"  XML-Einträge: {len(xml_entries)}\n")

    # 2) Cross-check: XML signature+PID vs METADATA signature+PID
    print("2) Signatur-PID-Abgleich (XML vs. METADATA)...")
    print("-" * 100)
    print(f"  {'XML-ID':<12} {'Signatur':<20} {'XML-PID':<16} {'META-PID':<16} {'Status'}")
    print("-" * 100)

    mismatch_count = 0
    match_count = 0
    no_meta_count = 0

    for entry in xml_entries:
        sig = entry["signature"]
        xml_pid = entry["pid"]

        meta = meta_by_sig.get(sig)
        if meta:
            meta_pid = meta["pid"]
            if xml_pid == meta_pid:
                status = "OK"
                match_count += 1
            else:
                status = "MISMATCH!"
                mismatch_count += 1
        else:
            meta_pid = "---"
            status = "NICHT IN METADATA"
            no_meta_count += 1

        marker = "  " if status == "OK" else ">>"
        print(f"{marker}{entry['xml_id']:<12} {sig:<20} {xml_pid:<16} {meta_pid:<16} {status}")

    print("-" * 100)
    print(f"\n  Übereinstimmend:    {match_count}")
    print(f"  Abweichend:         {mismatch_count}")
    print(f"  Nicht in METADATA:  {no_meta_count}\n")

    # 3) HTTP-Check for all PIDs
    print("3) HTTP-Erreichbarkeit prüfen...")
    http_ok = 0
    http_fail = 0
    for i, entry in enumerate(xml_entries, 1):
        status = check_url(entry["pid"])
        symbol = "OK" if status == 200 else f"FEHLER ({status})"
        if status == 200:
            http_ok += 1
        else:
            http_fail += 1
            print(f"  >> [{i:3d}] {entry['pid']:<16} -> {symbol}  ({entry['signature']})")
        time.sleep(0.2)

    print(f"\n  HTTP OK:     {http_ok}")
    print(f"  HTTP Fehler: {http_fail}\n")

    # 4) Check if METADATA has entries not in XML
    print("4) Prüfe ob METADATA-Einträge in XML fehlen...")
    xml_sigs = {e["signature"] for e in xml_entries}
    missing_in_xml = []
    for sig, meta in meta_by_sig.items():
        if sig not in xml_sigs:
            missing_in_xml.append(meta)

    if missing_in_xml:
        print(f"  >> {len(missing_in_xml)} METADATA-Einträge fehlen in XML:")
        for m in missing_in_xml:
            print(f"     {m['pid']:<16} {m['signature']:<20} {m['title']}")
    else:
        print("  Alle METADATA-Einträge sind in XML vorhanden.")

    # Summary
    print("\n" + "=" * 100)
    print("  GESAMTERGEBNIS")
    print("=" * 100)
    all_ok = mismatch_count == 0 and http_fail == 0
    if all_ok and not missing_in_xml:
        print("  ALLES KORREKT! Alle PIDs stimmen mit METADATA überein und sind erreichbar.")
    else:
        if mismatch_count > 0:
            print(f"  WARNUNG: {mismatch_count} PID-Abweichungen zwischen XML und METADATA")
        if http_fail > 0:
            print(f"  WARNUNG: {http_fail} PIDs nicht erreichbar (404 o.ä.)")
        if missing_in_xml:
            print(f"  INFO: {len(missing_in_xml)} METADATA-Einträge fehlen in XML")
    print("=" * 100)


if __name__ == "__main__":
    main()
