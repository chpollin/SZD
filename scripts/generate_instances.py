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
GAMS_BASE = "https://gams.uni-graz.at/"

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


def gams_iri(pid, xid):
    """Full IRI of an entry inside a GAMS object. A prefixed name such as
    gams:o:szd.werke#SZDMSK.2 is not valid here, because Turtle reads the
    '#' as the start of a comment and drops the fragment."""
    return f"<{GAMS_BASE}{pid}#{xid}>"


def _sig(el):
    # SZDMSK and SZDKOR type the shelfmark as @type='signature', SZDBIB leaves
    # the only idno of msIdentifier untyped.
    s = el.xpath(".//t:msIdentifier/t:idno[@type='signature' or not(@type)]", namespaces=NS)
    return (s[0].text or "").strip() if s else ""


def _title_triples(title_de, sig):
    t = [f'    szdo:title "{escape_ttl(title_de)}"@de ;']
    if sig:
        t.append(f'    szdo:signature "{escape_ttl(sig)}" ;')
    return t


# -- Extractors: each returns (comment_str, list_of_triple_lines) and may add
#    a third element, a list of statement blocks about further nodes --------

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
    persons = []
    for role, prop in [("sent", "sender"), ("received", "receiver")]:
        pn = bibl.find(f".//t:correspAction[@type='{role}']/t:persName", NS)
        ref = (pn.get("ref", "") if pn is not None else "").strip()
        # Correspondents are referenced by GND URI, a few by SZDPER id.
        if "#SZDPER" in ref:
            person = gams_iri("o:szd.personen", ref.split("#")[-1])
        elif ref.startswith("http"):
            person = f"<{ref}>"
        else:
            continue
        triples.append(f"    szdo:{prop} {person} ;")
        sn = (pn.findtext("t:surname", "", NS) or "").strip()
        fn = (pn.findtext("t:forename", "", NS) or "").strip()
        if sn:
            block = [f'{person} a szdo:Person ;']
            if fn:
                block.append(f'    szdo:forename "{escape_ttl(fn)}" ;')
            block.append(f'    szdo:surname "{escape_ttl(sn)}" .')
            persons.append(block)
    return f"{xid}: {title_de[:60]}", triples, persons


def _extract_per(per):
    xid = per.get(XID, "")
    sn = (per.findtext(".//t:surname", "", NS) or "").strip()
    fn = (per.findtext(".//t:forename", "", NS) or "").strip()
    pn_el = per.find("t:persName", NS)
    gnd = pn_el.get("ref", "") if pn_el is not None else ""
    triples = [f'    szdo:surname "{escape_ttl(sn)}" ;']
    if fn:
        triples.append(f'    szdo:forename "{escape_ttl(fn)}" ;')
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
        triples.append(f'    szdo:when "{when}"{suffix} ;')
    triples.append(f'    rdfs:label "{escape_ttl(xid)}" .')
    return xid, triples


# -- Collection configs: (name, label, xml_path, xpath, rdf_class,
#    uri_base, section_header, parent_prop, extract_fn)
COLLECTIONS = [
    ("SZDMSK", "Werke", "Work/SZDMSK.xml", "//t:biblFull",
     "szdo:Manuscript", "gams:o:szd.werke", None, "szdo:isPartOf", _extract_standard),
    ("SZDKOR", "Korrespondenz", "Correspondence/SZDKOR.xml", "//t:biblFull",
     "szdo:BundleOfCorrespondence", "gams:o:szd.korrespondenzen",
     "# --- Correspondence collection ---", "szdo:isPartOf", _extract_kor),
    ("SZDBIB", "Bibliothek", "Library/SZDBIB.xml", "//t:biblFull",
     "szdo:Book", "gams:o:szd.bibliothek",
     "# --- Library collection ---", "szdo:isPartOf", _extract_standard),
    ("SZDPER", "Personen", "Index/Person/SZDPER.xml", "//t:person",
     "szdo:Person", "gams:o:szd.personen", "# --- Persons ---", None, _extract_per),
    ("SZDBIO", "Lebenskalender", "Biography/SZDBIO.xml", "//t:event",
     "szdo:BiographicalEvent", "gams:o:szd.lebenskalender",
     "# --- Biographical events ---", None, _extract_bio),
]


def process_collection(step, total, name, label, xml_path, xpath,
                       rdf_class, uri_base, header, parent_prop, extract, lines):
    """Parse one XML collection and append Turtle triples to *lines*."""
    print(f"[{step}/{total}] {name} ({label}) ...")
    entries = etree.parse(str(DATA_DIR / xml_path)).xpath(xpath, namespaces=NS)[:SAMPLE_SIZE]
    if header:
        lines += [header, ""]
    seen = set()
    for entry in entries:
        xid = entry.get(XID, "")
        comment, triples, *extra = extract(entry)
        lines.append(f"# {comment}")
        lines.append(f"{gams_iri(uri_base.removeprefix('gams:'), xid)} a {rdf_class} ;")
        lines.extend(triples)
        if parent_prop:
            lines.append(f"    {parent_prop} {uri_base} .")
        for block in (extra[0] if extra else []):
            if block[0] not in seen:
                seen.add(block[0])
                lines.extend(block)
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
        '# --- Estate (fonds) ---', '',
        'gams:context:szd a szdo:Estate ;',
        '    szdo:title "Stefan Zweig Nachlass"@de , "Stefan Zweig Estate"@en ;',
        '    szdo:contains gams:o:szd.werke , gams:o:szd.korrespondenzen , gams:o:szd.bibliothek .', '',
        '# --- Works collection ---', '',
        'gams:o:szd.werke a szdo:WorksCollection ;',
        '    szdo:title "Werke"@de , "Works"@en .', '',
    ]
    total = len(COLLECTIONS)
    for i, (name, label, path, xp, cls, uri, hdr, parent, fn) in enumerate(COLLECTIONS, 1):
        process_collection(i, total, name, label, path, xp, cls, uri, hdr, parent, fn, lines)
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWritten to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
