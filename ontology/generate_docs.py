"""
SZDO Ontology Documentation Generator
======================================

Generates a complete HTML documentation site from szd-ontology.ttl.
No external dependencies beyond rdflib (pyLODE-free approach for maximum control).

Usage:
    python ontology/generate_docs.py
"""

import sys
import os
import shutil
from pathlib import Path
from collections import defaultdict
from html import escape

from rdflib import Graph, Namespace, RDF, RDFS, OWL, XSD, URIRef, Literal, BNode
from rdflib.namespace import SKOS, DCTERMS

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.parent
ONTOLOGY_FILE = Path(__file__).parent / "szd-ontology.ttl"
DOCS_DIR = PROJECT_ROOT / "docs"
ONTO_DOCS_DIR = DOCS_DIR / "ontology"

# ---------------------------------------------------------------------------
# Namespaces
# ---------------------------------------------------------------------------
SZDO = Namespace("https://gams.uni-graz.at/o:szd.ontology#")
SZDG = Namespace("https://gams.uni-graz.at/o:szd.glossar#")
RICO = Namespace("https://www.ica.org/standards/RiC/ontology#")
LRM  = Namespace("http://iflastandards.info/ns/lrm/lrmer/")
CRM  = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
SCHEMA = Namespace("https://schema.org/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

BADGE_MAP = {
    str(RICO): ("RiC-O", "badge-rico"),
    str(LRM): ("LRM", "badge-lrm"),
    str(CRM): ("CRM", "badge-crm"),
    str(SKOS): ("SKOS", "badge-skos"),
    str(FOAF): ("FOAF", "badge-foaf"),
    str(SCHEMA): ("Schema", "badge-schema"),
    str(DCTERMS): ("DC", "badge-dc"),
    "http://purl.org/dc/elements/1.1/": ("DC", "badge-dc"),
}

WELLKNOWN_NS = {
    "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
    "http://www.w3.org/2002/07/owl#": "owl",
    "http://www.w3.org/2001/XMLSchema#": "xsd",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def local_name(uri):
    s = str(uri)
    return s.split("#")[-1] if "#" in s else s.split("/")[-1]

def is_szdo(uri):
    return str(uri).startswith(str(SZDO))

def get_lang_values(g, uri, predicate):
    """Return {lang: value} dict for a predicate."""
    values = {}
    for obj in g.objects(uri, predicate):
        if hasattr(obj, "language") and obj.language:
            values[obj.language] = str(obj)
        else:
            values[""] = str(obj)
    return values

def get_labels(g, uri):
    """Return {lang: label} dict."""
    return get_lang_values(g, uri, RDFS.label)

def get_comments(g, uri):
    """Return {lang: comment} dict."""
    return get_lang_values(g, uri, RDFS.comment)

def uri_to_link(g, uri):
    """Create an HTML link for a URI -- internal anchor for szdo:, external otherwise."""
    if isinstance(uri, BNode):
        return "<em>(blank node)</em>"
    s = str(uri)
    name = local_name(uri)
    if is_szdo(uri):
        return f'<a href="#{escape(name)}"><code>szdo:{escape(name)}</code></a>'
    # Check known prefixes from BADGE_MAP
    for ns_str, (prefix, badge_cls) in BADGE_MAP.items():
        if s.startswith(ns_str):
            return f'<code>{escape(prefix)}:{escape(name)}</code> <span class="badge {badge_cls}">{escape(prefix)}</span>'
    # Check well-known W3C namespaces via dict lookup
    for ns_str, prefix in WELLKNOWN_NS.items():
        if s.startswith(ns_str):
            return f'<code>{escape(prefix)}:{escape(name)}</code>'
    return f'<a href="{escape(s)}" target="_blank"><code>{escape(name)}</code></a>'

def render_labels_html(labels):
    parts = []
    if "de" in labels:
        parts.append(f'<span class="label-de">DE: {escape(labels["de"])}</span>')
    if "en" in labels:
        parts.append(f'<span class="label-en">EN: {escape(labels["en"])}</span>')
    return " ".join(parts)

def render_comments_html(comments):
    parts = []
    if "de" in comments:
        parts.append(f'<span class="de-only">{escape(comments["de"])}</span>')
    if "en" in comments:
        parts.append(f'<span class="en-only comment-en">{escape(comments["en"])}</span>')
    if not parts and "" in comments:
        parts.append(escape(comments[""]))
    return " ".join(parts)

def _render_metadata_table(rows):
    """Render a list of (label, value) tuples as an HTML prop-table string."""
    if not rows:
        return ""
    html = '  <table class="prop-table">\n'
    for label, val in rows:
        html += f'    <tr><th>{label}</th><td>{val}</td></tr>\n'
    html += '  </table>\n'
    return html


# ---------------------------------------------------------------------------
# Ontology Sections (matching Turtle structure)
# ---------------------------------------------------------------------------

SECTIONS = [
    ("archiv", "Archivschicht", "Archival Layer", [
        "Nachlass", "Sammlung", "Werksammlung", "Korrespondenzsammlung",
        "Autographensammlung", "Bibliothekssammlung", "Lebensdokumentesammlung",
        "Aufsatzsammlung", "ThematischeSammlung",
        "NachlassObjekt", "Manuskript", "Typoskript", "Typoskriptdurchschlag",
        "Notizbuch", "Konvolut", "Korrekturfahne", "KorrespondenzKonvolut",
        "Autograph", "Buch", "Lebensdokument",
        "DigitalesObjekt", "METSObjekt", "IIIFManifest", "Faksimile",
        "Umfang", "Beilage",
    ]),
    ("werk", "Werkschicht", "Work Layer", [
        "Werk", "WerkExpression", "Manifestation", "Exemplar",
        "BelletristischesWerk", "EssayistischesWerk", "BiographischesWerk",
        "HistorischesWerk", "DramatischesWerk", "LyrischesWerk",
        "SammelWerk", "Uebersetzungswerk", "VorwortNachwort",
        "Sekundaerliteratur",
    ]),
    ("akteur", "Akteure", "Agents", [
        "Akteur", "Person", "Organisation",
    ]),
    ("biographie", "Biographie & Ereignisse", "Biography & Events", [
        "BiographischesEreignis", "Geburt", "Tod", "Reise",
        "Publikationsereignis", "Begegnung", "InstitutionellesEreignis",
        "Exilereignis", "WissenschaftlichesEreignis",
    ]),
    ("ort", "Orte", "Places", [
        "Ort", "GeographischerOrt", "Aufbewahrungsort", "Entstehungsort",
    ]),
    ("provenienz", "Provenienz", "Provenance", [
        "Provenienzereignis", "ProvenienzmerkmalInstanz",
    ]),
]


# ---------------------------------------------------------------------------
# HTML Generation
# ---------------------------------------------------------------------------

def generate_class_card(g, cls_uri):
    name = local_name(cls_uri)
    labels = get_labels(g, cls_uri)
    comments = get_comments(g, cls_uri)

    # Superclasses
    parents = []
    for p in g.objects(cls_uri, RDFS.subClassOf):
        if not isinstance(p, BNode):
            parents.append(uri_to_link(g, p))

    # Equivalent classes
    equivs = []
    for e in g.objects(cls_uri, OWL.equivalentClass):
        if not isinstance(e, BNode):
            equivs.append(uri_to_link(g, e))

    # Disjoint
    disjoints = []
    for d in g.objects(cls_uri, OWL.disjointWith):
        if not isinstance(d, BNode):
            disjoints.append(uri_to_link(g, d))

    # Properties with this class as domain
    props_with_domain = []
    all_props = set(g.subjects(RDF.type, OWL.ObjectProperty)) | set(g.subjects(RDF.type, OWL.DatatypeProperty))
    for prop in all_props:
        for dom in g.objects(prop, RDFS.domain):
            if dom == cls_uri:
                prop_labels = get_labels(g, prop)
                prop_name = local_name(prop)
                ranges = [uri_to_link(g, r) for r in g.objects(prop, RDFS.range) if not isinstance(r, BNode)]
                label_de = prop_labels.get("de", prop_name)
                props_with_domain.append((prop_name, label_de, ranges))

    html = f'<div class="entity-card" id="{escape(name)}">\n'
    html += f'  <div class="entity-name">szdo:{escape(name)}</div>\n'
    html += f'  <div class="entity-uri">{escape(str(cls_uri))}</div>\n'
    html += f'  <div class="entity-labels">{render_labels_html(labels)}</div>\n'
    if comments:
        html += f'  <div class="entity-comment">{render_comments_html(comments)}</div>\n'

    # Metadata table
    rows = []
    if parents:
        rows.append(("Subclass of", " , ".join(parents)))
    if equivs:
        rows.append(("Equivalent to", " , ".join(equivs)))
    if disjoints:
        rows.append(("Disjoint with", " , ".join(disjoints)))

    html += _render_metadata_table(rows)

    # Properties
    if props_with_domain:
        html += '  <h4 class="properties-heading">Properties</h4>\n'
        html += '  <table class="prop-table">\n'
        html += '    <tr><th>Property</th><th>Label</th><th>Range</th></tr>\n'
        for pname, plabel, pranges in sorted(props_with_domain):
            range_str = " , ".join(pranges) if pranges else "—"
            html += f'    <tr><td><a href="#{escape(pname)}"><code>{escape(pname)}</code></a></td><td>{escape(plabel)}</td><td>{range_str}</td></tr>\n'
        html += '  </table>\n'

    html += '</div>\n'
    return html


def generate_property_card(g, prop_uri, prop_type="Object"):
    name = local_name(prop_uri)
    labels = get_labels(g, prop_uri)
    comments = get_comments(g, prop_uri)

    domains = [uri_to_link(g, d) for d in g.objects(prop_uri, RDFS.domain) if not isinstance(d, BNode)]
    ranges = [uri_to_link(g, r) for r in g.objects(prop_uri, RDFS.range) if not isinstance(r, BNode)]
    inverses = [uri_to_link(g, i) for i in g.objects(prop_uri, OWL.inverseOf) if not isinstance(i, BNode)]
    equivs = [uri_to_link(g, e) for e in g.objects(prop_uri, OWL.equivalentProperty) if not isinstance(e, BNode)]

    # Check special property types
    is_symmetric = (prop_uri, RDF.type, OWL.SymmetricProperty) in g
    is_transitive = (prop_uri, RDF.type, OWL.TransitiveProperty) in g

    html = f'<div class="entity-card" id="{escape(name)}">\n'
    html += f'  <div class="entity-name">szdo:{escape(name)}</div>\n'
    html += f'  <div class="entity-uri">{escape(str(prop_uri))}</div>\n'
    html += f'  <div class="entity-labels">{render_labels_html(labels)}</div>\n'
    if comments:
        html += f'  <div class="entity-comment">{render_comments_html(comments)}</div>\n'

    rows = []
    rows.append(("Type", f"{prop_type} Property" + (" · Symmetric" if is_symmetric else "") + (" · Transitive" if is_transitive else "")))
    if domains:
        rows.append(("Domain", " , ".join(domains)))
    if ranges:
        rows.append(("Range", " , ".join(ranges)))
    if inverses:
        rows.append(("Inverse of", " , ".join(inverses)))
    if equivs:
        rows.append(("Equivalent to", " , ".join(equivs)))

    html += _render_metadata_table(rows)
    html += '</div>\n'
    return html


def generate_prose_section():
    """Return an HTML prose overview of the ontology (bilingual DE/EN)."""
    return '''<section class="onto-prose" id="overview">

  <h2><span class="de-only">Überblick</span><span class="en-only">Overview</span></h2>

  <p class="en-only">
    The Stefan Zweig Digital Ontology (SZDO) provides a formal OWL 2 data model
    for describing the digital estate (<em>Nachlass</em>) of Stefan Zweig, held
    primarily at the Literaturarchiv Salzburg. It bridges archival science,
    library cataloguing, and cultural-heritage modelling into a single,
    interoperable vocabulary that can be queried, linked, and extended.
  </p>
  <p class="de-only">
    Die Stefan Zweig Digital Ontology (SZDO) stellt ein formales OWL-2-Datenmodell
    zur Beschreibung des digitalen Nachlasses von Stefan Zweig bereit, der
    vorwiegend im Literaturarchiv Salzburg verwahrt wird. Sie verbindet
    Archivwissenschaft, bibliothekarische Erschließung und
    Kulturerbe-Modellierung in einem einzigen, interoperablen Vokabular.
  </p>

  <h3><span class="en-only">Design Principles</span><span class="de-only">Entwurfsprinzipien</span></h3>

  <p class="en-only">
    SZDO follows an archive-first approach: its backbone is aligned with
    Records in Contexts (RiC-O), ensuring that the hierarchical structure of a
    literary estate&mdash;from <em>Nachlass</em> down to individual items&mdash;is
    captured faithfully. For the description of intellectual works the model
    adopts the FRBR/IFLA-LRM Work&ndash;Expression&ndash;Manifestation&ndash;Item
    hierarchy, while events and temporal phenomena are modelled in accordance
    with CIDOC-CRM. All classes and properties carry bilingual labels (German
    and English), and the design is deliberately extensible so that new
    sub-collections or scholarly projects can add domain-specific refinements
    without breaking the core schema.
  </p>
  <p class="de-only">
    SZDO verfolgt einen archivzentrierten Ansatz: Das Rückgrat orientiert sich
    an Records in Contexts (RiC-O), sodass die hierarchische Struktur eines
    literarischen Nachlasses&mdash;vom Gesamtbestand bis zum Einzelstück&mdash;originalgetreu
    abgebildet wird. Für die Beschreibung intellektueller Werke übernimmt das
    Modell die FRBR/IFLA-LRM-Hierarchie (Werk&ndash;Expression&ndash;Manifestation&ndash;Exemplar),
    während Ereignisse und zeitliche Phänomene gemäß CIDOC-CRM modelliert werden.
    Alle Klassen und Properties tragen zweisprachige Labels (Deutsch und Englisch),
    und das Design ist bewusst erweiterbar.
  </p>

  <h3><span class="en-only">Layer Architecture</span><span class="de-only">Schichtenarchitektur</span></h3>

  <p class="en-only">
    The ontology is organised into seven interconnected layers.
    The <strong>Archival Layer</strong> models the <em>Nachlass</em> structure
    (collections, sub-collections, and individual archival objects such as
    manuscripts, typescripts, and notebooks).
    The <strong>Digital Objects Layer</strong> represents their digital
    surrogates (METS objects, IIIF manifests, facsimiles).
    The <strong>Work Layer</strong> maps intellectual creations through the
    WEMI hierarchy (Work&ndash;Expression&ndash;Manifestation&ndash;Item).
    The <strong>Agents Layer</strong> covers persons and organisations.
    The <strong>Biography &amp; Events Layer</strong> captures life-timeline
    events such as births, deaths, journeys, and encounters.
    The <strong>Places Layer</strong> distinguishes geographic locations from
    repositories and places of origin.
    Finally, the <strong>Provenance Layer</strong> traces the ownership chain
    of archival objects. These layers are connected through shared properties
    so that, for example, a manuscript (Archival) can be linked to the work it
    witnesses (Work), the person who authored it (Agents), the place where it
    was written (Places), and the event through which it changed hands
    (Provenance).
  </p>
  <p class="de-only">
    Die Ontologie ist in sieben miteinander verbundene Schichten gegliedert.
    Die <strong>Archivschicht</strong> bildet die Nachlassstruktur ab
    (Sammlungen, Teilsammlungen und Einzelobjekte wie Manuskripte, Typoskripte
    und Notizbücher).
    Die <strong>Schicht der digitalen Objekte</strong> repräsentiert deren
    digitale Surrogate (METS-Objekte, IIIF-Manifeste, Faksimiles).
    Die <strong>Werkschicht</strong> beschreibt intellektuelle Schöpfungen über
    die WEMI-Hierarchie (Werk&ndash;Expression&ndash;Manifestation&ndash;Exemplar).
    Die <strong>Akteursschicht</strong> umfasst Personen und Organisationen.
    Die <strong>Biographie- und Ereignisschicht</strong> erfasst Lebensereignisse
    wie Geburt, Tod, Reisen und Begegnungen.
    Die <strong>Ortsschicht</strong> unterscheidet geographische Orte von
    Aufbewahrungsorten und Entstehungsorten.
    Die <strong>Provenienzschicht</strong> zeichnet die Besitzkette von
    Archivalien nach. Die Schichten sind über gemeinsame Properties verbunden.
  </p>

  <h3><span class="en-only">Integration</span><span class="de-only">Integration</span></h3>

  <p class="en-only">
    SZDO connects to the
    <a href="https://chpollin.github.io/klawiter-rescue/" target="_blank" rel="noopener">Klawiter Bibliography</a>
    (6,296 entries) via the Work/Manifestation layer, enabling scholars to
    navigate from a physical manuscript in the Nachlass to its published
    editions and translations. The ontology also links to external authority
    files&mdash;GND, Wikidata, VIAF for persons and organisations, and
    GeoNames for places&mdash;ensuring that every entity can be reconciled
    with the wider Linked-Data ecosystem.
  </p>
  <p class="de-only">
    SZDO ist über die Werk-/Manifestationsschicht mit der
    <a href="https://chpollin.github.io/klawiter-rescue/" target="_blank" rel="noopener">Klawiter-Bibliographie</a>
    (6.296 Einträge) verbunden, sodass von einem physischen Manuskript im
    Nachlass zu seinen publizierten Ausgaben und Übersetzungen navigiert werden
    kann. Darüber hinaus verknüpft die Ontologie mit externen Normdateien&mdash;GND,
    Wikidata, VIAF für Personen und Organisationen sowie GeoNames für
    Orte&mdash;und gewährleistet so die Anschlussfähigkeit an das
    Linked-Data-Ökosystem.
  </p>

</section>
'''


def _build_sidebar(g, all_classes, all_obj_props, all_dat_props):
    """Build the sidebar navigation HTML."""
    class_map = {local_name(c): c for c in all_classes}

    sidebar = '<nav class="onto-sidebar">\n'
    sidebar += '  <a href="#overview" style="font-weight:600;"><span class="de-only">Überblick</span><span class="en-only">Overview</span></a>\n'
    for sec_id, sec_de, sec_en, _ in SECTIONS:
        sidebar += f'  <h3><span class="de-only">{escape(sec_de)}</span><span class="en-only">{escape(sec_en)}</span></h3>\n'
        for cls_name in [c for _, _, _, classes in SECTIONS if _ == sec_id for c in classes]:
            if cls_name in class_map:
                labels = get_labels(g, class_map[cls_name])
                display = labels.get("de", cls_name)
                sidebar += f'  <a href="#{escape(cls_name)}">{escape(display)}</a>\n'
    # Properties sections
    sidebar += '  <h3>Object Properties</h3>\n'
    for p in all_obj_props[:10]:
        n = local_name(p)
        sidebar += f'  <a href="#{escape(n)}">{escape(n)}</a>\n'
    if len(all_obj_props) > 10:
        sidebar += f'  <a href="#object-properties">... ({len(all_obj_props)} total)</a>\n'
    sidebar += '  <h3>Datatype Properties</h3>\n'
    for p in all_dat_props[:8]:
        n = local_name(p)
        sidebar += f'  <a href="#{escape(n)}">{escape(n)}</a>\n'
    if len(all_dat_props) > 8:
        sidebar += f'  <a href="#datatype-properties">... ({len(all_dat_props)} total)</a>\n'

    sidebar += '  <div class="download-links">\n'
    sidebar += '    <h3>Download</h3>\n'
    sidebar += '    <a href="szd-ontology.ttl">Turtle (.ttl)</a>\n'
    sidebar += '    <a href="szd-ontology.jsonld">JSON-LD</a>\n'
    sidebar += '  </div>\n'
    sidebar += '</nav>\n'
    return sidebar


def _build_content(g, all_classes, all_obj_props, all_dat_props, version):
    """Build the main content area HTML."""
    class_map = {local_name(c): c for c in all_classes}

    content = '<div class="onto-content">\n'
    content += f'  <h1>Stefan Zweig Digital Nachlass-Ontologie</h1>\n'
    content += f'  <div class="onto-version">Version {escape(version)} · Namespace: <code>https://gams.uni-graz.at/o:szd.ontology#</code></div>\n'
    content += f'  <p>{len(all_classes)} Klassen · {len(all_obj_props)} Object Properties · {len(all_dat_props)} Datatype Properties · <a href="visualize.html">Interaktive Visualisierung</a></p>\n'

    # External vocabularies
    content += '  <div class="badge-row">\n'
    content += '    <span class="badge badge-rico">RiC-O</span> '
    content += '    <span class="badge badge-lrm">LRM</span> '
    content += '    <span class="badge badge-crm">CRM</span> '
    content += '    <span class="badge badge-skos">SKOS</span> '
    content += '    <span class="badge badge-foaf">FOAF</span> '
    content += '    <span class="badge badge-schema">Schema.org</span> '
    content += '    <span class="badge badge-dc">Dublin Core</span>\n'
    content += '  </div>\n'

    # Prose overview section
    content += generate_prose_section()

    # Classes by section
    for sec_id, sec_de, sec_en, cls_names in SECTIONS:
        content += f'  <h2 id="section-{escape(sec_id)}"><span class="de-only">{escape(sec_de)}</span><span class="en-only">{escape(sec_en)}</span></h2>\n'
        for cls_name in cls_names:
            if cls_name in class_map:
                content += generate_class_card(g, class_map[cls_name])

    # Object Properties
    content += '  <h2 id="object-properties">Object Properties</h2>\n'
    for prop in all_obj_props:
        content += generate_property_card(g, prop, "Object")

    # Datatype Properties
    content += '  <h2 id="datatype-properties">Datatype Properties</h2>\n'
    for prop in all_dat_props:
        content += generate_property_card(g, prop, "Datatype")

    content += '</div>\n'
    return content


def _build_page(sidebar, content, version):
    """Assemble the full HTML page from sidebar, content, and version."""
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SZDO — Stefan Zweig Digital Nachlass-Ontologie</title>
  <meta name="description" content="Formale OWL-Ontologie fuer den digitalen Nachlass Stefan Zweigs. 72 Klassen, 130 Properties, basierend auf RiC-O, IFLA LRM und CIDOC-CRM.">
  <link rel="alternate" type="text/turtle" href="szd-ontology.ttl">
  <link rel="alternate" type="application/ld+json" href="szd-ontology.jsonld">
  <link rel="stylesheet" href="../css/szd-ontology.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "DefinedTermSet",
    "name": "Stefan Zweig Digital Nachlass-Ontologie",
    "description": "OWL ontology for the digital estate of Stefan Zweig",
    "url": "https://chpollin.github.io/SZD/ontology/",
    "version": "{version}",
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "creator": {{
      "@type": "Organization",
      "name": "Digital Humanities Craft OG"
    }}
  }}
  </script>
</head>
<body class="lang-de">
  <header class="site-header">
    <div class="header-inner">
      <a href="../" class="header-brand">
        <img src="../img/SZlogo.png" alt="SZD Logo" class="header-logo">
        <span class="header-title">Stefan Zweig Digital</span>
      </a>
      <nav class="header-nav">
        <a href="../project/">Projekt</a>
        <a href=".">Ontologie</a>
        <a href="../downloads/">Downloads</a>
        <a href="https://stefanzweig.digital" target="_blank" rel="noopener">Website</a>
        <a href="https://github.com/chpollin/SZD" target="_blank" rel="noopener">GitHub</a>
        <div class="lang-toggle" role="group" aria-label="Language selection">
          <button data-lang="de" class="active" aria-pressed="true" aria-label="Deutsch">DE</button>
          <button data-lang="en" aria-pressed="false" aria-label="English">EN</button>
        </div>
      </nav>
    </div>
  </header>

  <div class="onto-layout">
    {sidebar}
    {content}
  </div>

  <footer class="site-footer">
    <div class="footer-inner">
      <p>&copy; 2026 Stefan Zweig Digital · <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC-BY 4.0</a> · Generated from <a href="szd-ontology.ttl">szd-ontology.ttl</a></p>
    </div>
  </footer>
  <script>
    document.querySelectorAll('.lang-toggle [data-lang]').forEach(function(btn) {{
      btn.addEventListener('click', function() {{
        document.body.className = 'lang-' + this.dataset.lang;
        document.querySelectorAll('.lang-toggle [data-lang]').forEach(function(b) {{
          b.classList.remove('active');
          b.setAttribute('aria-pressed', 'false');
        }});
        this.classList.add('active');
        this.setAttribute('aria-pressed', 'true');
      }});
    }});
  </script>
</body>
</html>'''


def generate_html(g):
    """Generate the complete ontology documentation HTML."""

    # Gather all entities
    all_classes = sorted([c for c in g.subjects(RDF.type, OWL.Class) if is_szdo(c)], key=lambda x: local_name(x))
    all_obj_props = sorted([p for p in g.subjects(RDF.type, OWL.ObjectProperty) if is_szdo(p)], key=lambda x: local_name(x))
    all_dat_props = sorted([p for p in g.subjects(RDF.type, OWL.DatatypeProperty) if is_szdo(p)], key=lambda x: local_name(x))

    # Get ontology metadata
    onto_uri = URIRef("https://gams.uni-graz.at/o:szd.ontology")
    version = str(list(g.objects(onto_uri, OWL.versionInfo))[0]) if list(g.objects(onto_uri, OWL.versionInfo)) else "?"

    sidebar = _build_sidebar(g, all_classes, all_obj_props, all_dat_props)
    content = _build_content(g, all_classes, all_obj_props, all_dat_props, version)
    return _build_page(sidebar, content, version)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("SZDO Documentation Generator")
    print("=" * 40)

    # 1. Parse ontology
    print(f"[1/4] Parsing {ONTOLOGY_FILE.name} ...")
    g = Graph()
    g.parse(str(ONTOLOGY_FILE), format="turtle")
    print(f"       {len(g)} triples loaded.")

    # 2. Generate HTML
    print("[2/4] Generating HTML documentation ...")
    html = generate_html(g)
    ONTO_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (ONTO_DOCS_DIR / "index.html").write_text(html, encoding="utf-8")
    print(f"       Written to {ONTO_DOCS_DIR / 'index.html'}")

    # 3. Copy Turtle file
    print("[3/4] Copying Turtle file ...")
    shutil.copy2(str(ONTOLOGY_FILE), str(ONTO_DOCS_DIR / "szd-ontology.ttl"))
    print(f"       Copied to {ONTO_DOCS_DIR / 'szd-ontology.ttl'}")

    # 4. Generate graph data for D3.js visualization
    print("[4/5] Generating graph data ...")
    import subprocess
    subprocess.run([sys.executable, str(Path(__file__).parent / "generate_graph.py")], check=True)

    # 5. Generate JSON-LD
    print("[5/5] Generating JSON-LD ...")
    jsonld_str = g.serialize(format="json-ld", indent=2)
    (ONTO_DOCS_DIR / "szd-ontology.jsonld").write_text(jsonld_str, encoding="utf-8")
    print(f"       Written to {ONTO_DOCS_DIR / 'szd-ontology.jsonld'}")

    print("\nDone! Preview with: python -m http.server -d docs 8000")


if __name__ == "__main__":
    main()
