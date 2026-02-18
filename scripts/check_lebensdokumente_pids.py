#!/usr/bin/env python3
"""
Prüft alle PIDs in SZDLEB.xml auf 404-Fehler und gleicht sie mit der
METADATA-Liste von GAMS ab, um korrekte PIDs zu finden.

Ablauf:
1. Alle PIDs + Signaturen + Titel aus SZDLEB.xml extrahieren
2. Jede PID als URL https://gams.uni-graz.at/{PID} per HTTP HEAD prüfen
3. METADATA-Liste von GAMS abrufen (korrekte PIDs mit Signaturen)
4. Für 404-PIDs: anhand der Signatur die korrekte PID aus METADATA finden
5. Report ausgeben
"""

import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
import json
import re
import sys
import time

TEI_NS = "{http://www.tei-c.org/ns/1.0}"
GAMS_BASE = "https://gams.uni-graz.at"
METADATA_URL = (
    "https://gams.uni-graz.at/archive/objects/"
    "context:szd.facsimiles.lebensdokumente/datastreams/METADATA/content"
)
XML_PATH = "../data/PersonalDocument/SZDLEB.xml"


def extract_pids_from_xml(xml_path: str) -> list[dict]:
    """Extract all biblFull entries with PID, signature, and title."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    entries = []

    for biblfull in root.iter(f"{TEI_NS}biblFull"):
        xml_id = biblfull.get("{http://www.w3.org/XML/1998/namespace}id", "")

        # Find title (first ana="assigned" or ana="original" title in German)
        title_de = ""
        for title_el in biblfull.iter(f"{TEI_NS}title"):
            ana = title_el.get("ana", "")
            lang = title_el.get("{http://www.w3.org/XML/1998/namespace}lang", "")
            if ana in ("assigned", "original") and lang in ("de", ""):
                title_de = (title_el.text or "").strip()
                if title_de:
                    break

        # Find signature
        signature = ""
        for idno in biblfull.iter(f"{TEI_NS}idno"):
            if idno.get("type") == "signature":
                signature = (idno.text or "").strip()
                break

        # Find PID
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


def check_pid_url(pid: str) -> tuple[int, str]:
    """Check if a PID URL returns 200 or 404. Returns (status_code, redirect_url)."""
    url = f"{GAMS_BASE}/{pid}"
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "SZD-PID-Checker/1.0")
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.url
    except urllib.error.HTTPError as e:
        return e.code, ""
    except urllib.error.URLError as e:
        return 0, str(e)
    except Exception as e:
        return -1, str(e)


def fetch_metadata() -> list[dict]:
    """Fetch the METADATA list from GAMS and parse it (SPARQL XML format)."""
    print(f"Fetching METADATA from GAMS...")
    req = urllib.request.Request(METADATA_URL)
    req.add_header("User-Agent", "SZD-PID-Checker/1.0")

    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read().decode("utf-8")

    # The METADATA endpoint returns SPARQL XML results.
    # Each <result> contains <identifier>o:szd.XXX</identifier>,
    # <title>Title, SZ-XXX/LYY</title>, <pid uri="info:fedora/o:szd.XXX"/>
    metadata_entries = []
    seen_pids = set()

    root = ET.fromstring(content)
    # Handle namespace - SPARQL result format
    # Find all result elements (try with and without namespace)
    ns_sparql = "{http://www.w3.org/2001/sw/DataAccess/rf1/result}"

    for result in root.iter(f"{ns_sparql}result"):
        identifier_el = result.find(f"{ns_sparql}identifier")
        title_el = result.find(f"{ns_sparql}title")

        if identifier_el is None or identifier_el.text is None:
            continue

        pid = identifier_el.text.strip()
        if pid in seen_pids:
            continue  # Skip duplicates
        seen_pids.add(pid)

        title = (title_el.text or "").strip() if title_el is not None else ""

        # Extract signature from title (format: "Title, SZ-XXX/LYY" or "Title, SZ-XXX/L-SYY.ZZ")
        sig_pattern = re.compile(r'(SZ-[A-Z0-9]+/L[\w\-\.]+)')
        sig_match = sig_pattern.search(title)
        signature = sig_match.group(1) if sig_match else ""

        metadata_entries.append({
            "pid": pid,
            "signature": signature,
            "title": title,
        })

    return metadata_entries


def build_signature_to_pid_map(metadata: list[dict]) -> dict[str, dict]:
    """Build a lookup from signature to metadata entry."""
    sig_map = {}
    for entry in metadata:
        if entry["signature"]:
            sig_map[entry["signature"]] = entry
    return sig_map


def main():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    xml_path = os.path.normpath(os.path.join(script_dir, XML_PATH))

    print(f"=== SZD Lebensdokumente PID-Checker ===\n")
    print(f"XML-Datei: {xml_path}\n")

    # Step 1: Extract PIDs from XML
    print("1) Extrahiere PIDs aus SZDLEB.xml...")
    entries = extract_pids_from_xml(xml_path)
    print(f"   -> {len(entries)} Einträge gefunden\n")

    # Step 2: Check each PID
    print("2) Prüfe jede PID-URL auf Erreichbarkeit...")
    ok_entries = []
    error_entries = []

    for i, entry in enumerate(entries, 1):
        status, redirect = check_pid_url(entry["pid"])
        entry["status"] = status
        entry["redirect"] = redirect

        symbol = "OK" if status == 200 else f"FEHLER ({status})"
        print(f"   [{i:3d}/{len(entries)}] {entry['pid']:20s} -> {symbol}  ({entry['signature']})")

        if status == 200:
            ok_entries.append(entry)
        else:
            error_entries.append(entry)

        # Be polite to the server
        time.sleep(0.3)

    print(f"\n   Ergebnis: {len(ok_entries)} OK, {len(error_entries)} Fehler\n")

    # Step 3: Fetch METADATA for correct PIDs
    if error_entries:
        print("3) Lade METADATA-Liste von GAMS...")
        try:
            metadata = fetch_metadata()
            print(f"   -> {len(metadata)} Einträge in METADATA gefunden\n")
            sig_map = build_signature_to_pid_map(metadata)

            # Also build a PID-based lookup
            pid_map = {e["pid"]: e for e in metadata}
        except Exception as e:
            print(f"   FEHLER beim Laden der METADATA: {e}\n")
            metadata = []
            sig_map = {}
            pid_map = {}

        # Step 4: Match errors with correct PIDs
        print("4) Suche korrekte PIDs für fehlerhafte Einträge...\n")
        print("=" * 120)
        print(f"{'XML-ID':<12} {'Signatur':<20} {'Alte PID (404)':<20} {'Korrekte PID':<20} {'Titel'}")
        print("=" * 120)

        fixed = 0
        unfixed = 0
        for entry in error_entries:
            correct = sig_map.get(entry["signature"])
            if correct:
                correct_pid = correct["pid"]
                fixed += 1
            else:
                correct_pid = "??? (nicht gefunden)"
                unfixed += 1

            print(
                f"{entry['xml_id']:<12} "
                f"{entry['signature']:<20} "
                f"{entry['pid']:<20} "
                f"{correct_pid:<20} "
                f"{entry['title']}"
            )

        print("=" * 120)
        print(f"\nZusammenfassung:")
        print(f"  Gesamt geprüft:       {len(entries)}")
        print(f"  OK (200):             {len(ok_entries)}")
        print(f"  Fehler (404 etc.):    {len(error_entries)}")
        print(f"  Korrektur gefunden:   {fixed}")
        print(f"  Keine Korrektur:      {unfixed}")
    else:
        print("3) Keine Fehler gefunden - alle PIDs sind erreichbar!\n")

    # Save detailed report
    report_path = os.path.join(script_dir, "lebensdokumente_pid_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("SZD Lebensdokumente - PID-Prüfbericht\n")
        f.write(f"Datum: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Gesamt geprüft: {len(entries)}\n")
        f.write(f"OK: {len(ok_entries)}\n")
        f.write(f"Fehler: {len(error_entries)}\n\n")

        if error_entries:
            f.write("FEHLERHAFTE PIDs:\n")
            f.write("-" * 120 + "\n")
            for entry in error_entries:
                correct = sig_map.get(entry["signature"], {})
                correct_pid = correct.get("pid", "???")
                f.write(
                    f"XML-ID: {entry['xml_id']}\n"
                    f"  Titel:      {entry['title']}\n"
                    f"  Signatur:   {entry['signature']}\n"
                    f"  Alte PID:   {entry['pid']} (HTTP {entry['status']})\n"
                    f"  Neue PID:   {correct_pid}\n"
                    f"  Alte URL:   {GAMS_BASE}/{entry['pid']}\n"
                    f"  Neue URL:   {GAMS_BASE}/{correct_pid}\n\n"
                )

    print(f"\nReport gespeichert: {report_path}")


if __name__ == "__main__":
    main()
