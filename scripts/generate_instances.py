"""
SZDO Instance Data Generator
==============================

Generates sample RDF instance data from TEI-XML collections
for SHACL validation against the SZDO ontology.

Extracts 5 entries from each major collection:
  - SZDMSK (Werke/Manuskripte)
  - SZDKOR (Korrespondenz)
  - SZDBIB (Bibliothek)
  - SZDPER (Personen)
  - SZDBIO (Lebenskalender)

Usage:
    python scripts/generate_instances.py
"""

import sys
from pathlib import Path
from lxml import etree

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_FILE = PROJECT_ROOT / "ontology" / "sample-instances.ttl"

TEI = "http://www.tei-c.org/ns/1.0"
NS = {"t": TEI}


def parse_text(el, lang="de"):
    """Extract text from an element, preferring given language."""
    if el is None:
        return ""
    # Try lang-specific child
    for child in el:
        if child.get("{http://www.w3.org/XML/1998/namespace}lang") == lang:
            return (child.text or "").strip()
    return (el.text or "").strip()


def escape_ttl(s):
    """Escape a string for Turtle literal."""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "")


def main():
    print("SZDO Instance Data Generator")
    print("=" * 50)

    lines = [
        '@prefix szdo:    <https://gams.uni-graz.at/o:szd.ontology#> .',
        '@prefix gams:    <https://gams.uni-graz.at/> .',
        '@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .',
        '@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .',
        '@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .',
        '',
        '# =============================================================================',
        '# Sample Instance Data for SHACL Validation',
        '# Generated from TEI-XML by scripts/generate_instances.py',
        '# =============================================================================',
        '',
    ]

    # --- SZDMSK: Werke/Manuskripte ---
    print("[1/5] SZDMSK (Werke) ...")
    tree = etree.parse(str(DATA_DIR / "Work" / "SZDMSK.xml"))
    bibls = tree.xpath("//t:biblFull", namespaces=NS)[:5]

    # Nachlass (Fonds)
    lines.append("# --- Nachlass (Fonds) ---")
    lines.append("")
    lines.append("gams:context:szd a szdo:Nachlass ;")
    lines.append('    szdo:titel "Stefan Zweig Nachlass"@de , "Stefan Zweig Estate"@en ;')
    lines.append("    szdo:enthaelt gams:o:szd.werke , gams:o:szd.korrespondenzen , gams:o:szd.bibliothek .")
    lines.append("")
    lines.append("# --- Werksammlung ---")
    lines.append("")
    lines.append("gams:o:szd.werke a szdo:Werksammlung ;")
    lines.append('    szdo:titel "Werke"@de , "Works"@en .')
    lines.append("")

    for bibl in bibls:
        xml_id = bibl.get("{http://www.w3.org/XML/1998/namespace}id", "")
        title_el = bibl.find(".//t:titleStmt/t:title", NS)
        title_de = parse_text(title_el, "de") or parse_text(title_el)
        sig_el = bibl.find(".//t:msIdentifier/t:idno[@type='signature']", NS)
        sig = (sig_el.text or "").strip() if sig_el is not None else ""
        objtyp_el = bibl.find(".//t:objectDesc//t:measure[@type='leaf']", NS)

        uri = f"gams:o:szd.werke#{xml_id}"
        lines.append(f"# {xml_id}: {title_de[:60]}")
        lines.append(f"{uri} a szdo:Manuskript ;")
        lines.append(f'    szdo:titel "{escape_ttl(title_de)}"@de ;')
        if sig:
            lines.append(f'    szdo:signatur "{escape_ttl(sig)}" ;')
        lines.append(f"    szdo:istTeilVon gams:o:szd.werke .")
        lines.append("")

    print(f"       {len(bibls)} instances")

    # --- SZDKOR: Korrespondenz ---
    print("[2/5] SZDKOR (Korrespondenz) ...")
    tree = etree.parse(str(DATA_DIR / "Correspondence" / "SZDKOR.xml"))
    bibls = tree.xpath("//t:biblFull", namespaces=NS)[:5]

    lines.append("# --- Korrespondenzsammlung ---")
    lines.append("")

    for bibl in bibls:
        xml_id = bibl.get("{http://www.w3.org/XML/1998/namespace}id", "")
        titles = bibl.findall(".//t:titleStmt/t:title", NS)
        title_de = xml_id
        for tel in titles:
            lang = tel.get("{http://www.w3.org/XML/1998/namespace}lang", "")
            if lang == "de" and tel.text:
                title_de = tel.text.strip()
                break
        if title_de == xml_id and titles and titles[0].text:
            title_de = titles[0].text.strip()

        # Sender/receiver
        sent = bibl.find(".//t:correspAction[@type='sent']/t:persName", NS)
        recv = bibl.find(".//t:correspAction[@type='received']/t:persName", NS)
        sender_ref = sent.get("ref", "") if sent is not None else ""
        recv_ref = recv.get("ref", "") if recv is not None else ""

        sig_el = bibl.find(".//t:msIdentifier/t:idno[@type='signature']", NS)
        sig = (sig_el.text or "").strip() if sig_el is not None else ""

        uri = f"gams:o:szd.korrespondenzen#{xml_id}"
        lines.append(f"# {xml_id}: {title_de[:60]}")
        lines.append(f"{uri} a szdo:KorrespondenzKonvolut ;")
        lines.append(f'    szdo:titel "{escape_ttl(title_de)}"@de ;')
        if sig:
            lines.append(f'    szdo:signatur "{escape_ttl(sig)}" ;')
        if sender_ref and "#SZDPER" in sender_ref:
            per_id = sender_ref.split("#")[-1]
            lines.append(f"    szdo:hatAbsender gams:o:szd.personen#{per_id} ;")
        if recv_ref and "#SZDPER" in recv_ref:
            per_id = recv_ref.split("#")[-1]
            lines.append(f"    szdo:hatEmpfaenger gams:o:szd.personen#{per_id} ;")
        lines.append(f"    szdo:istTeilVon gams:o:szd.korrespondenzen .")
        lines.append("")

    print(f"       {len(bibls)} instances")

    # --- SZDBIB: Bibliothek ---
    print("[3/5] SZDBIB (Bibliothek) ...")
    tree = etree.parse(str(DATA_DIR / "Library" / "SZDBIB.xml"))
    bibls = tree.xpath("//t:biblFull", namespaces=NS)[:5]

    lines.append("# --- Bibliothekssammlung ---")
    lines.append("")

    for bibl in bibls:
        xml_id = bibl.get("{http://www.w3.org/XML/1998/namespace}id", "")
        title_el = bibl.find(".//t:titleStmt/t:title", NS)
        title_de = parse_text(title_el, "de") or parse_text(title_el)
        sig_el = bibl.find(".//t:msIdentifier/t:idno[@type='signature']", NS)
        sig = (sig_el.text or "").strip() if sig_el is not None else ""

        uri = f"gams:o:szd.bibliothek#{xml_id}"
        lines.append(f"# {xml_id}: {title_de[:60]}")
        lines.append(f"{uri} a szdo:Buch ;")
        lines.append(f'    szdo:titel "{escape_ttl(title_de)}"@de ;')
        if sig:
            lines.append(f'    szdo:signatur "{escape_ttl(sig)}" ;')
        lines.append(f"    szdo:istTeilVon gams:o:szd.bibliothek .")
        lines.append("")

    print(f"       {len(bibls)} instances")

    # --- SZDPER: Personen ---
    print("[4/5] SZDPER (Personen) ...")
    tree = etree.parse(str(DATA_DIR / "Index" / "Person" / "SZDPER.xml"))
    persons = tree.xpath("//t:person", namespaces=NS)[:5]

    lines.append("# --- Personen ---")
    lines.append("")

    for per in persons:
        xml_id = per.get("{http://www.w3.org/XML/1998/namespace}id", "")
        surname_el = per.find(".//t:surname", NS)
        forename_el = per.find(".//t:forename", NS)
        surname = (surname_el.text or "").strip() if surname_el is not None else ""
        forename = (forename_el.text or "").strip() if forename_el is not None else ""
        persname_el = per.find("t:persName", NS)
        gnd_ref = persname_el.get("ref", "") if persname_el is not None else ""

        uri = f"gams:o:szd.personen#{xml_id}"
        lines.append(f"# {xml_id}: {forename} {surname}")
        lines.append(f"{uri} a szdo:Person ;")
        lines.append(f'    szdo:nachname "{escape_ttl(surname)}" ;')
        if forename:
            lines.append(f'    szdo:vorname "{escape_ttl(forename)}" ;')
        if "gnd/" in gnd_ref:
            lines.append(f'    szdo:gndIdentifier "{escape_ttl(gnd_ref)}"^^xsd:anyURI ;')
        lines.append(f"    rdfs:label \"{escape_ttl(forename + ' ' + surname)}\" .")
        lines.append("")

    print(f"       {len(persons)} instances")

    # --- SZDBIO: Lebenskalender ---
    print("[5/5] SZDBIO (Lebenskalender) ...")
    tree = etree.parse(str(DATA_DIR / "Biography" / "SZDBIO.xml"))
    events = tree.xpath("//t:event", namespaces=NS)[:5]

    lines.append("# --- Biographische Ereignisse ---")
    lines.append("")

    for ev in events:
        xml_id = ev.get("{http://www.w3.org/XML/1998/namespace}id", "")
        date_el = ev.find(".//t:date", NS)
        when = date_el.get("when", "") if date_el is not None else ""

        uri = f"gams:o:szd.lebenskalender#{xml_id}"
        lines.append(f"# {xml_id}")
        lines.append(f"{uri} a szdo:BiographischesEreignis ;")
        if when:
            # Only use xsd:date for full dates (YYYY-MM-DD), otherwise xsd:string
            if len(when) == 10:  # YYYY-MM-DD
                lines.append(f'    szdo:datum "{when}"^^xsd:date ;')
            else:
                lines.append(f'    szdo:datum "{when}" ;')
        lines.append(f"    rdfs:label \"{escape_ttl(xml_id)}\" .")
        lines.append("")

    print(f"       {len(events)} instances")

    # Write
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWritten to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
