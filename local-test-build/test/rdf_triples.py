"""Triple difference of two RDF/XML files, for rdf-triples.mjs and rdf-staging.mjs.

Prints JSON with the triples only in the first and only in the second graph, each as an
N-Triples line. Blank nodes are compared through rdflib's canonical isomorphic form.
rdflib is not a harness dependency, the Node callers report the check as not run when
it is missing.
"""
import json
import sys

from rdflib import Graph
from rdflib.compare import graph_diff, to_isomorphic


def load(path):
    graph = Graph()
    # The theme pages emit relative URIs such as #SZDLEB.2 (rdf-mapping, Theme pages). Both
    # files resolve them against one base, so the file paths do not count as a difference.
    graph.parse(path, format="xml", publicID="urn:szd:base")
    return to_isomorphic(graph)


def lines(graph):
    return sorted(f"{s.n3()} {p.n3()} {o.n3()} ." for s, p, o in graph)


def main():
    # the Windows console encoding cannot hold every character of the data
    sys.stdout.reconfigure(encoding="utf-8")
    first, second = load(sys.argv[1]), load(sys.argv[2])
    _, only_first, only_second = graph_diff(first, second)
    json.dump({"triples": [len(first), len(second)], "onlyFirst": lines(only_first), "onlySecond": lines(only_second)},
              sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
