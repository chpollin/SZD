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
CONFIG_FILE = Path(__file__).parent / "graph-config.json"

SZDO = Namespace("https://gams.uni-graz.at/o:szd.ontology#")
RICO = Namespace("https://www.ica.org/standards/RiC/ontology#")
LRM  = Namespace("http://iflastandards.info/ns/lrm/lrmer/")
CRM  = Namespace("http://www.cidoc-crm.org/cidoc-crm/")


def load_config():
    """Load layer configuration from graph-config.json."""
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

    layer_colors = {key: val["color"] for key, val in config["layers"].items()}
    layer_labels = {key: val["label"] for key, val in config["layers"].items()}
    class_to_layer = config["classToLayer"]
    default_color = config.get("defaultColor", "#7A1B2D")

    return class_to_layer, layer_colors, layer_labels, default_color


def local_name(uri):
    s = str(uri)
    return s.split("#")[-1] if "#" in s else s.split("/")[-1]


def is_szdo(uri):
    return str(uri).startswith(str(SZDO))


def is_deprecated(g, uri):
    return (uri, OWL.deprecated, Literal(True)) in g


def _get_lang_dict(g, uri, predicate):
    """Extract a {language: text} dict for a given predicate on uri."""
    result = {}
    for obj in g.objects(uri, predicate):
        if hasattr(obj, "language") and obj.language:
            result[obj.language] = str(obj)
    return result


def read_ontology_version(g):
    """Read owl:versionInfo from the ontology URI in the graph."""
    onto_uri = URIRef("https://gams.uni-graz.at/o:szd.ontology")
    version_info = list(g.objects(onto_uri, OWL.versionInfo))
    return str(version_info[0]) if version_info else "unknown"


def collect_nodes(g, class_to_layer, layer_colors):
    """Collect non-deprecated SZDO classes as node dicts.

    Returns a tuple (nodes, node_ids) where nodes is a list of dicts
    and node_ids is a set of local names.
    """
    nodes = []
    node_ids = set()

    for cls in g.subjects(RDF.type, OWL.Class):
        if not is_szdo(cls) or is_deprecated(g, cls):
            continue
        name = local_name(cls)
        labels = _get_lang_dict(g, cls, RDFS.label)
        comments = _get_lang_dict(g, cls, RDFS.comment)

        layer = class_to_layer.get(name, "other")

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
            "color": layer_colors.get(layer, "#999"),
            "properties": prop_count,
        })
        node_ids.add(name)

    return nodes, node_ids


def collect_edges(g, node_ids, class_to_layer, layer_colors, default_color):
    """Collect subClassOf and ObjectProperty edges.

    Returns a list of edge dicts.
    """
    edges = []

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

    # Object Property edges (domain -> range)
    for prop in g.subjects(RDF.type, OWL.ObjectProperty):
        if not is_szdo(prop) or is_deprecated(g, prop):
            continue
        pname = local_name(prop)
        labels = _get_lang_dict(g, prop, RDFS.label)

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
                    "color": layer_colors.get(class_to_layer.get(d, "other"), default_color),
                })

    return edges


def main():
    print("SZDO Graph Data Generator")
    print("=" * 40)

    class_to_layer, layer_colors, layer_labels, default_color = load_config()

    g = Graph()
    g.parse(str(ONTOLOGY_FILE), format="turtle")
    print(f"Loaded {len(g)} triples.")

    version = read_ontology_version(g)
    print(f"Ontology version: {version}")

    nodes, node_ids = collect_nodes(g, class_to_layer, layer_colors)
    edges = collect_edges(g, node_ids, class_to_layer, layer_colors, default_color)

    graph_data = {
        "nodes": nodes,
        "edges": edges,
        "layers": layer_labels,
        "layerColors": layer_colors,
        "meta": {
            "title": "Stefan Zweig Digital Nachlass-Ontologie",
            "version": version,
            "nodeCount": len(nodes),
            "edgeCount": len(edges),
        }
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(graph_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Written {len(nodes)} nodes, {len(edges)} edges to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
