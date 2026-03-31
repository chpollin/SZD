"""
SZDO Instance Data Generator -- generates sample RDF instance data from
TEI-XML collections for SHACL validation.  Usage: python scripts/generate_instances.py
"""
import sys
from pathlib import Path
from lxml import etree

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_FILE = PROJECT_ROOT / "ontology" / "sample-instances.ttl"
SAMPLE_SIZE = 5

TEI = "http://www.tei-c.org/ns/1.0"
NS = {"t": TEI}
XID = "{http://www.w3.org/XML/1998/namespace}id"
XLANG = "{http://www.w3.org/XML/1998/namespace}lang"


def parse_text(el, lang="de"):
    """Extract text from an element, preferring given language."""
    if el is None:
        return ""
    for child in el:
        if child.get(XLANG) == lang:
            return (child.text or "").strip()
    return (el.text or "").strip()


def escape_ttl(s):
    """Escape a string for Turtle literal."""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "")


def _sig(el):
    s = el.find(".//t:msIdentifier/t:idno[@type='signature']", NS)
    return (s.text or "").strip() if s is not None else ""


def _title_triples(title_de, sig):
    t = [f'    szdo:titel "{escape_ttl(title_de)}"@de ;']
    if sig:
        t.append(f'    szdo:signatur "{escape_ttl(sig)}" ;')
    return t


# -- Extractors: each returns (comment_str, list_of_triple_lines) -----------

def _extract_standard(bibl):
    title_el = bibl.find(".//t:titleStmt/t:title", NS)
    title_de = parse_text(title_el, "de") or parse_text(title_el)
    xid = bibl.get(XID, "")
    return f"{xid}: {title_de[:60]}", _title_triples(title_de, _sig(bibl))


def _extract_kor(bibl):
    xid = bibl.get(XID, "")
    titles = bibl.findall(".//t:titleStmt/t:title", NS)
    title_de = xid
    for tel in titles:
        if tel.get(XLANG, "") == "de" and tel.text:
            title_de = tel.text.strip(); break
    if title_de == xid and titles and titles[0].text:
        title_de = titles[0].text.strip()
    triples = _title_triples(title_de, _sig(bibl))
    for role, prop in [("sent", "hatAbsender"), ("received", "hatEmpfaenger")]:
        pn = bibl.find(f".//t:correspAction[@type='{role}']/t:persName", NS)
        ref = pn.get("ref", "") if pn is not None else ""
        if ref and "#SZDPER" in ref:
            triples.append(f"    szdo:{prop} gams:o:szd.personen#{ref.split('#')[-1]} ;")
    return f"{xid}: {title_de[:60]}", triples


def _extract_per(per):
    xid = per.get(XID, "")
    sn = (per.findtext(".//t:surname", "", NS) or "").strip()
    fn = (per.findtext(".//t:forename", "", NS) or "").strip()
    pn_el = per.find("t:persName", NS)
    gnd = pn_el.get("ref", "") if pn_el is not None else ""
    triples = [f'    szdo:nachname "{escape_ttl(sn)}" ;']
    if fn:
        triples.append(f'    szdo:vorname "{escape_ttl(fn)}" ;')
    if "gnd/" in gnd:
        triples.append(f'    szdo:gndIdentifier "{escape_ttl(gnd)}"^^xsd:anyURI ;')
    triples.append(f'    rdfs:label "{escape_ttl(fn + " " + sn)}" .')
    return f"{xid}: {fn} {sn}", triples


def _extract_bio(ev):
    xid = ev.get(XID, "")
    date_el = ev.find(".//t:date", NS)
    when = date_el.get("when", "") if date_el is not None else ""
    triples = []
    if when:
        suffix = "^^xsd:date" if len(when) == 10 else ""
        triples.append(f'    szdo:datum "{when}"{suffix} ;')
    triples.append(f'    rdfs:label "{escape_ttl(xid)}" .')
    return xid, triples


# -- Collection configs: (name, label, xml_path, xpath, rdf_class,
#    uri_base, section_header, parent_prop, extract_fn)
COLLECTIONS = [
    ("SZDMSK", "Werke", "Work/SZDMSK.xml", "//t:biblFull",
     "szdo:Manuskript", "gams:o:szd.werke", None, "szdo:istTeilVon", _extract_standard),
    ("SZDKOR", "Korrespondenz", "Correspondence/SZDKOR.xml", "//t:biblFull",
     "szdo:KorrespondenzKonvolut", "gams:o:szd.korrespondenzen",
     "# --- Korrespondenzsammlung ---", "szdo:istTeilVon", _extract_kor),
    ("SZDBIB", "Bibliothek", "Library/SZDBIB.xml", "//t:biblFull",
     "szdo:Buch", "gams:o:szd.bibliothek",
     "# --- Bibliothekssammlung ---", "szdo:istTeilVon", _extract_standard),
    ("SZDPER", "Personen", "Index/Person/SZDPER.xml", "//t:person",
     "szdo:Person", "gams:o:szd.personen", "# --- Personen ---", None, _extract_per),
    ("SZDBIO", "Lebenskalender", "Biography/SZDBIO.xml", "//t:event",
     "szdo:BiographischesEreignis", "gams:o:szd.lebenskalender",
     "# --- Biographische Ereignisse ---", None, _extract_bio),
]


def process_collection(step, total, name, label, xml_path, xpath,
                       rdf_class, uri_base, header, parent_prop, extract, lines):
    """Parse one XML collection and append Turtle triples to *lines*."""
    print(f"[{step}/{total}] {name} ({label}) ...")
    entries = etree.parse(str(DATA_DIR / xml_path)).xpath(xpath, namespaces=NS)[:SAMPLE_SIZE]
    if header:
        lines += [header, ""]
    for entry in entries:
        xid = entry.get(XID, "")
        comment, triples = extract(entry)
        lines.append(f"# {comment}")
        lines.append(f"{uri_base}#{xid} a {rdf_class} ;")
        lines.extend(triples)
        if parent_prop:
            lines.append(f"    {parent_prop} {uri_base} .")
        lines.append("")
    print(f"       {len(entries)} instances")


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
        '# --- Nachlass (Fonds) ---', '',
        'gams:context:szd a szdo:Nachlass ;',
        '    szdo:titel "Stefan Zweig Nachlass"@de , "Stefan Zweig Estate"@en ;',
        '    szdo:enthaelt gams:o:szd.werke , gams:o:szd.korrespondenzen , gams:o:szd.bibliothek .', '',
        '# --- Werksammlung ---', '',
        'gams:o:szd.werke a szdo:Werksammlung ;',
        '    szdo:titel "Werke"@de , "Works"@en .', '',
    ]
    total = len(COLLECTIONS)
    for i, (name, label, path, xp, cls, uri, hdr, parent, fn) in enumerate(COLLECTIONS, 1):
        process_collection(i, total, name, label, path, xp, cls, uri, hdr, parent, fn, lines)
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWritten to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
