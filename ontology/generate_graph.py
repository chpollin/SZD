"""
SZDO Ontology Graph Data Generator
====================================

Extracts nodes (classes) and edges (properties, subClassOf) from
szd-ontology.ttl and outputs a JSON file for D3.js visualization.

Usage:
    python ontology/generate_graph.py
"""

import sys
import os
import json
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef, Literal, BNode

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ONTOLOGY_FILE = Path(__file__).parent / "szd-ontology.ttl"
OUTPUT_FILE = Path(__file__).parent.parent / "docs" / "ontology" / "szd-graph.json"

SZDO = Namespace("https://gams.uni-graz.at/o:szd.ontology#")
RICO = Namespace("https://www.ica.org/standards/RiC/ontology#")
LRM  = Namespace("http://iflastandards.info/ns/lrm/lrmer/")
CRM  = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

def local_name(uri):
    s = str(uri)
    return s.split("#")[-1] if "#" in s else s.split("/")[-1]

def is_szdo(uri):
    return str(uri).startswith(str(SZDO))

def is_deprecated(g, uri):
    return (uri, OWL.deprecated, Literal(True)) in g

# Layer assignment based on class hierarchy
LAYER_MAP = {
    "Nachlass": "archiv", "Sammlung": "archiv", "Werksammlung": "archiv",
    "Korrespondenzsammlung": "archiv", "Autographensammlung": "archiv",
    "Bibliothekssammlung": "archiv", "Lebensdokumentesammlung": "archiv",
    "Aufsatzsammlung": "archiv", "ThematischeSammlung": "archiv",
    "NachlassObjekt": "archiv", "Manuskript": "archiv", "Typoskript": "archiv",
    "Typoskriptdurchschlag": "archiv", "Notizbuch": "archiv", "Konvolut": "archiv",
    "Korrekturfahne": "archiv", "KorrespondenzKonvolut": "archiv",
    "Autograph": "archiv", "Buch": "archiv", "Lebensdokument": "archiv",
    "Umfang": "archiv", "Beilage": "archiv",
    "DigitalesObjekt": "digital", "METSObjekt": "digital",
    "IIIFManifest": "digital", "Faksimile": "digital",
    "Werk": "werk", "WerkExpression": "werk", "Manifestation": "werk",
    "Exemplar": "werk", "BelletristischesWerk": "werk",
    "EssayistischesWerk": "werk", "BiographischesWerk": "werk",
    "HistorischesWerk": "werk", "DramatischesWerk": "werk",
    "LyrischesWerk": "werk", "SammelWerk": "werk",
    "Uebersetzungswerk": "werk", "VorwortNachwort": "werk",
    "Sekundaerliteratur": "werk",
    "Akteur": "akteur", "Person": "akteur", "Organisation": "akteur",
    "BiographischesEreignis": "biographie", "Geburt": "biographie",
    "Tod": "biographie", "Reise": "biographie",
    "Publikationsereignis": "biographie", "Begegnung": "biographie",
    "InstitutionellesEreignis": "biographie", "Exilereignis": "biographie",
    "WissenschaftlichesEreignis": "biographie",
    "Ort": "ort", "GeographischerOrt": "ort",
    "Aufbewahrungsort": "ort", "Entstehungsort": "ort",
    "Provenienzereignis": "provenienz",
    "ProvenienzmerkmalInstanz": "provenienz",
}

LAYER_COLORS = {
    "archiv": "#1a6b47",
    "digital": "#2c7da0",
    "werk": "#2c5aa0",
    "akteur": "#e67e22",
    "biographie": "#8b5e3c",
    "ort": "#6a5acd",
    "provenienz": "#9b3a4e",
}

LAYER_LABELS = {
    "archiv": "Archivschicht",
    "digital": "Digitale Objekte",
    "werk": "Werkschicht",
    "akteur": "Akteure",
    "biographie": "Biographie & Ereignisse",
    "ort": "Orte",
    "provenienz": "Provenienz",
}


def main():
    print("SZDO Graph Data Generator")
    print("=" * 40)

    g = Graph()
    g.parse(str(ONTOLOGY_FILE), format="turtle")
    print(f"Loaded {len(g)} triples.")

    nodes = []
    node_ids = set()
    edges = []

    # Collect non-deprecated SZDO classes
    for cls in g.subjects(RDF.type, OWL.Class):
        if not is_szdo(cls) or is_deprecated(g, cls):
            continue
        name = local_name(cls)
        labels = {}
        for obj in g.objects(cls, RDFS.label):
            if hasattr(obj, "language") and obj.language:
                labels[obj.language] = str(obj)
        comments = {}
        for obj in g.objects(cls, RDFS.comment):
            if hasattr(obj, "language") and obj.language:
                comments[obj.language] = str(obj)

        layer = LAYER_MAP.get(name, "other")

        # Count properties where this class is domain
        prop_count = 0
        for prop in set(g.subjects(RDF.type, OWL.ObjectProperty)) | set(g.subjects(RDF.type, OWL.DatatypeProperty)):
            if is_deprecated(g, prop):
                continue
            for dom in g.objects(prop, RDFS.domain):
                if dom == cls:
                    prop_count += 1

        nodes.append({
            "id": name,
            "uri": str(cls),
            "label_de": labels.get("de", name),
            "label_en": labels.get("en", name),
            "comment_de": comments.get("de", ""),
            "comment_en": comments.get("en", ""),
            "layer": layer,
            "color": LAYER_COLORS.get(layer, "#999"),
            "properties": prop_count,
        })
        node_ids.add(name)

    # SubClassOf edges
    for cls in g.subjects(RDF.type, OWL.Class):
        if not is_szdo(cls) or is_deprecated(g, cls):
            continue
        src = local_name(cls)
        for parent in g.objects(cls, RDFS.subClassOf):
            if is_szdo(parent) and not is_deprecated(g, parent):
                tgt = local_name(parent)
                if src in node_ids and tgt in node_ids:
                    edges.append({
                        "source": src,
                        "target": tgt,
                        "type": "subClassOf",
                        "label": "subClassOf",
                        "color": "#999",
                    })

    # Object Property edges (domain → range)
    for prop in g.subjects(RDF.type, OWL.ObjectProperty):
        if not is_szdo(prop) or is_deprecated(g, prop):
            continue
        pname = local_name(prop)
        labels = {}
        for obj in g.objects(prop, RDFS.label):
            if hasattr(obj, "language") and obj.language:
                labels[obj.language] = str(obj)

        domains = [local_name(d) for d in g.objects(prop, RDFS.domain)
                   if is_szdo(d) and not isinstance(d, BNode) and local_name(d) in node_ids]
        ranges = [local_name(r) for r in g.objects(prop, RDFS.range)
                  if is_szdo(r) and not isinstance(r, BNode) and local_name(r) in node_ids]

        for d in domains:
            for r in ranges:
                edges.append({
                    "source": d,
                    "target": r,
                    "type": "property",
                    "label": pname,
                    "label_de": labels.get("de", pname),
                    "color": LAYER_COLORS.get(LAYER_MAP.get(d, "other"), "#7A1B2D"),
                })

    graph_data = {
        "nodes": nodes,
        "edges": edges,
        "layers": LAYER_LABELS,
        "layerColors": LAYER_COLORS,
        "meta": {
            "title": "Stefan Zweig Digital Nachlass-Ontologie",
            "version": "1.0.0",
            "nodeCount": len(nodes),
            "edgeCount": len(edges),
        }
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(graph_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Written {len(nodes)} nodes, {len(edges)} edges to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
