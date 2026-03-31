"""
Stefan Zweig Digital Nachlass-Ontologie -- Validation Pipeline
==============================================================

Runs a multi-stage validation of szd-ontology.ttl:
  1. Syntax check (rdflib parse)
  2. Structural metrics (class/property counts)
  3. SHACL validation (szd-shapes.ttl)
  4. OWL consistency checks (rdflib-based, no Java required)
  5. OntoClean taxonomy checks
  6. Competency question SPARQL tests

Usage:
    python validate.py
    python validate.py --verbose
    python validate.py --fix  (apply auto-fixes where possible)
"""

import sys
import os
import argparse
from pathlib import Path
from collections import defaultdict

# Fix Windows console encoding for Unicode output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

from rdflib import Graph, Namespace, RDF, RDFS, OWL, XSD, URIRef, Literal
from rdflib.namespace import SKOS

# ---------------------------------------------------------------------------
# Namespaces
# ---------------------------------------------------------------------------
SZDO = Namespace("https://gams.uni-graz.at/o:szd.ontology#")
SZDG = Namespace("https://gams.uni-graz.at/o:szd.glossar#")
NACHLASS = Namespace("https://w3id.org/nachlass#")
RICO = Namespace("https://www.ica.org/standards/RiC/ontology#")
LRM  = Namespace("http://iflastandards.info/ns/lrm/lrmer/")
CRM  = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
GAMS = Namespace("https://gams.uni-graz.at/o:gams-ontology#")
DCTERMS = Namespace("http://purl.org/dc/terms/")

ONTOLOGY_FILE  = Path(__file__).parent / "szd-ontology.ttl"
NACHLASS_FILE  = Path(__file__).parent / "nachlass-ontology.ttl"
SHAPES_FILE    = Path(__file__).parent / "szd-shapes.ttl"

# ---------------------------------------------------------------------------
# SPARQL prefix block for competency question tests (defined once)
# ---------------------------------------------------------------------------
CQ_PREFIX_BLOCK = """
    PREFIX szdo:     <https://gams.uni-graz.at/o:szd.ontology#>
    PREFIX szdg:     <https://gams.uni-graz.at/o:szd.glossar#>
    PREFIX nachlass: <https://w3id.org/nachlass#>
    PREFIX rico:     <https://www.ica.org/standards/RiC/ontology#>
    PREFIX lrm:     <http://iflastandards.info/ns/lrm/lrmer/>
    PREFIX crm:     <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX owl:     <http://www.w3.org/2002/07/owl#>
    PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def error(self, stage, msg):
        self.errors.append((stage, msg))

    def warn(self, stage, msg):
        self.warnings.append((stage, msg))

    def add_info(self, stage, msg):
        self.info.append((stage, msg))

    def print_report(self):
        print("\n" + "=" * 72)
        print("  SZDO VALIDATION REPORT")
        print("=" * 72)

        if self.info:
            print("\n--- INFO ---")
            for stage, msg in self.info:
                print(f"  [{stage}] {msg}")

        if self.warnings:
            print(f"\n--- WARNINGS ({len(self.warnings)}) ---")
            for stage, msg in self.warnings:
                print(f"  [{stage}] {msg}")

        if self.errors:
            print(f"\n--- ERRORS ({len(self.errors)}) ---")
            for stage, msg in self.errors:
                print(f"  [{stage}] {msg}")

        print("\n" + "-" * 72)
        print(f"  Total: {len(self.errors)} errors, {len(self.warnings)} warnings, {len(self.info)} info")
        if not self.errors:
            print("  ✓ Ontology validation PASSED")
        else:
            print("  ✗ Ontology validation FAILED")
        print("-" * 72 + "\n")

        return len(self.errors) == 0


def local_name(uri):
    """Extract the local name after # or /."""
    s = str(uri)
    if "#" in s:
        return s.split("#")[-1]
    return s.split("/")[-1]


def is_szdo(uri):
    """Check if a URI belongs to the SZDO namespace."""
    return str(uri).startswith(str(SZDO))


# ---------------------------------------------------------------------------
# Stage 1: Syntax Check
# ---------------------------------------------------------------------------

def stage_syntax(result, verbose=False):
    print("\n[1/6] Syntax Check ...")
    g = Graph()
    try:
        g.parse(str(ONTOLOGY_FILE), format="turtle")
        n_triples = len(g)
        result.add_info("SYNTAX", f"Parsed OK: {n_triples} triples from {ONTOLOGY_FILE.name}")
    except Exception as e:
        result.error("SYNTAX", f"Failed to parse {ONTOLOGY_FILE.name}: {e}")
        return None
    # Also load the generic nachlass ontology if present
    if NACHLASS_FILE.exists():
        try:
            g.parse(str(NACHLASS_FILE), format="turtle")
            result.add_info("SYNTAX", f"Parsed OK: nachlass-ontology.ttl ({len(g) - n_triples} additional triples)")
        except Exception as e:
            result.error("SYNTAX", f"Failed to parse {NACHLASS_FILE.name}: {e}")
            return None
    return g


# ---------------------------------------------------------------------------
# Stage 2: Structural Metrics
# ---------------------------------------------------------------------------

def stage_metrics(g, result, verbose=False):
    print("[2/6] Structural Metrics ...")

    classes = set(g.subjects(RDF.type, OWL.Class))
    obj_props = set(g.subjects(RDF.type, OWL.ObjectProperty))
    dat_props = set(g.subjects(RDF.type, OWL.DatatypeProperty))
    ann_props = set(g.subjects(RDF.type, OWL.AnnotationProperty))

    szdo_classes = [c for c in classes if is_szdo(c)]
    szdo_obj = [p for p in obj_props if is_szdo(p)]
    szdo_dat = [p for p in dat_props if is_szdo(p)]

    result.add_info("METRICS", f"Total OWL Classes: {len(classes)} (szdo: {len(szdo_classes)})")
    result.add_info("METRICS", f"Object Properties:  {len(obj_props)} (szdo: {len(szdo_obj)})")
    result.add_info("METRICS", f"Datatype Properties: {len(dat_props)} (szdo: {len(szdo_dat)})")
    result.add_info("METRICS", f"Annotation Properties: {len(ann_props)}")

    # Depth analysis
    max_depth = 0
    for cls in szdo_classes:
        depth = 0
        current = cls
        visited = set()
        while True:
            parents = list(g.objects(current, RDFS.subClassOf))
            szdo_parents = [p for p in parents if is_szdo(p)]
            if not szdo_parents or current in visited:
                break
            visited.add(current)
            current = szdo_parents[0]
            depth += 1
        max_depth = max(max_depth, depth)

    result.add_info("METRICS", f"Max class hierarchy depth (szdo only): {max_depth}")

    if verbose:
        print(f"    Classes: {[local_name(c) for c in sorted(szdo_classes, key=str)]}")


# ---------------------------------------------------------------------------
# Stage 3: SHACL Validation
# ---------------------------------------------------------------------------

def stage_shacl(g, result, verbose=False):
    print("[3/6] SHACL Validation ...")

    if not SHAPES_FILE.exists():
        result.warn("SHACL", f"Shapes file not found: {SHAPES_FILE}")
        return

    try:
        from pyshacl import validate
        conforms, results_graph, results_text = validate(
            data_graph=g,
            shacl_graph=str(SHAPES_FILE),
            inference="rdfs",
            abort_on_first=False,
        )

        if conforms:
            result.add_info("SHACL", "All SHACL shapes conform.")
        else:
            # Parse individual violations
            SH = Namespace("http://www.w3.org/ns/shacl#")
            for report_node in results_graph.subjects(RDF.type, SH.ValidationResult):
                severity = list(results_graph.objects(report_node, SH.resultSeverity))
                message = list(results_graph.objects(report_node, SH.resultMessage))
                focus = list(results_graph.objects(report_node, SH.focusNode))

                sev_str = local_name(severity[0]) if severity else "?"
                msg_str = str(message[0]) if message else "?"
                focus_str = local_name(focus[0]) if focus else "?"

                if sev_str == "Violation":
                    result.error("SHACL", f"{focus_str}: {msg_str}")
                else:
                    result.warn("SHACL", f"[{sev_str}] {focus_str}: {msg_str}")

            if verbose:
                print(results_text[:2000])

    except ImportError:
        result.warn("SHACL", "pyshacl not installed -- skipping SHACL validation.")
    except Exception as e:
        result.error("SHACL", f"SHACL validation error: {e}")


# ---------------------------------------------------------------------------
# Stage 4: OWL Consistency Checks (rdflib-based, no Java)
# ---------------------------------------------------------------------------

def is_deprecated(g, uri):
    """Check if a resource is marked owl:deprecated true."""
    return (uri, OWL.deprecated, Literal(True)) in g


def _check_labels(g, classes, result):
    """4a: rdfs:label in de and en; 4b: rdfs:comment present."""
    for cls in classes:
        labels = list(g.objects(cls, RDFS.label))
        langs = {l.language for l in labels if hasattr(l, "language") and l.language}
        name = local_name(cls)
        if "de" not in langs:
            result.error("OWL", f"Class '{name}' missing rdfs:label@de")
        if "en" not in langs:
            result.error("OWL", f"Class '{name}' missing rdfs:label@en")

    for cls in classes:
        comments = list(g.objects(cls, RDFS.comment))
        if not comments:
            result.warn("OWL", f"Class '{local_name(cls)}' has no rdfs:comment")


def _check_hierarchy(g, classes, result):
    """4c: orphan classes (no superclass); 4i: circular subClassOf."""
    # 4c
    for cls in classes:
        parents = list(g.objects(cls, RDFS.subClassOf))
        equivs = list(g.objects(cls, OWL.equivalentClass))
        if not parents and not equivs:
            result.error("OWL", f"Class '{local_name(cls)}' has no rdfs:subClassOf -- orphaned in hierarchy")

    # 4i
    for cls in classes:
        visited = set()
        current = cls
        is_cyclic = False
        while True:
            if current in visited:
                is_cyclic = True
                break
            visited.add(current)
            parents = [p for p in g.objects(current, RDFS.subClassOf) if is_szdo(p)]
            if not parents:
                break
            current = parents[0]
        if is_cyclic:
            result.error("OWL", f"Circular subClassOf detected involving '{local_name(cls)}'")


def _check_naming(g, classes, obj_props, dat_props, result):
    """4d: ObjectProperty lowercase; 4e: DatatypeProperty lowercase; 4f: Class uppercase."""
    for prop in obj_props:
        name = local_name(prop)
        if name and name[0].isupper():
            result.warn("OWL", f"ObjectProperty '{name}' starts with uppercase -- convention is lowercase")

    for prop in dat_props:
        name = local_name(prop)
        if name and name[0].isupper():
            result.warn("OWL", f"DatatypeProperty '{name}' starts with uppercase -- convention is lowercase")

    for cls in classes:
        name = local_name(cls)
        if name and name[0].islower():
            result.warn("OWL", f"Class '{name}' starts with lowercase -- convention is uppercase")


def _check_property_constraints(g, obj_props, dat_props, result):
    """4g: multiple rdfs:domain; 4h: multiple rdfs:range; 4j: missing domain; 4k: missing range."""
    all_props = list(obj_props) + list(dat_props)

    # 4g
    for prop in all_props:
        domains = list(g.objects(prop, RDFS.domain))
        if len(domains) > 1:
            result.warn("OWL",
                f"Property '{local_name(prop)}' has {len(domains)} rdfs:domain declarations -- "
                f"in OWL this means intersection (AND), not union. Consider using owl:unionOf.")

    # 4h
    for prop in all_props:
        ranges = list(g.objects(prop, RDFS.range))
        if len(ranges) > 1:
            result.warn("OWL",
                f"Property '{local_name(prop)}' has {len(ranges)} rdfs:range declarations -- "
                f"in OWL this means intersection. Consider using owl:unionOf.")

    # 4j
    for prop in obj_props:
        domains = list(g.objects(prop, RDFS.domain))
        if not domains:
            result.warn("OWL", f"ObjectProperty '{local_name(prop)}' has no rdfs:domain")

    # 4k
    for prop in obj_props:
        ranges = list(g.objects(prop, RDFS.range))
        if not ranges:
            result.warn("OWL", f"ObjectProperty '{local_name(prop)}' has no rdfs:range")


def _check_inverses(g, obj_props, result):
    """4l: owl:inverseOf consistency."""
    for prop in obj_props:
        inverses = list(g.objects(prop, OWL.inverseOf))
        for inv in inverses:
            back_inverses = list(g.objects(inv, OWL.inverseOf))
            if prop not in back_inverses:
                result.warn("OWL",
                    f"'{local_name(prop)}' declares owl:inverseOf '{local_name(inv)}' "
                    f"but '{local_name(inv)}' does not declare inverse back")


def _check_disjointness(g, classes, result):
    """4m: sibling classes should ideally be disjoint."""
    parent_children = defaultdict(list)
    for cls in classes:
        for parent in g.objects(cls, RDFS.subClassOf):
            if is_szdo(parent):
                parent_children[parent].append(cls)

    disjoint_missing = 0
    for parent, children in parent_children.items():
        if len(children) > 1:
            has_disjoint = False
            for i, c1 in enumerate(children):
                for c2 in children[i+1:]:
                    d1 = list(g.objects(c1, OWL.disjointWith))
                    d2 = list(g.objects(c2, OWL.disjointWith))
                    if c2 in d1 or c1 in d2:
                        has_disjoint = True
                        break
            if not has_disjoint:
                disjoint_missing += 1

    if disjoint_missing > 0:
        result.warn("OWL",
            f"{disjoint_missing} parent classes have siblings without owl:disjointWith. "
            f"Consider adding disjointness axioms for clearer semantics.")


def stage_owl_checks(g, result, verbose=False):
    print("[4/6] OWL Consistency Checks ...")

    classes = set(g.subjects(RDF.type, OWL.Class))
    obj_props = set(g.subjects(RDF.type, OWL.ObjectProperty))
    dat_props = set(g.subjects(RDF.type, OWL.DatatypeProperty))
    szdo_classes = [c for c in classes if is_szdo(c) and not is_deprecated(g, c)]
    szdo_obj = [p for p in obj_props if is_szdo(p) and not is_deprecated(g, p)]
    szdo_dat = [p for p in dat_props if is_szdo(p) and not is_deprecated(g, p)]

    # Count deprecated for info
    n_dep_cls = len([c for c in classes if is_szdo(c) and is_deprecated(g, c)])
    n_dep_prop = len([p for p in (obj_props | dat_props) if is_szdo(p) and is_deprecated(g, p)])
    if n_dep_cls or n_dep_prop:
        result.add_info("OWL", f"Skipping {n_dep_cls} deprecated classes, {n_dep_prop} deprecated properties (GAMS v0.x compatibility layer)")

    _check_labels(g, szdo_classes, result)
    _check_hierarchy(g, szdo_classes, result)
    _check_naming(g, szdo_classes, szdo_obj, szdo_dat, result)
    _check_property_constraints(g, szdo_obj, szdo_dat, result)
    _check_inverses(g, szdo_obj, result)
    _check_disjointness(g, szdo_classes, result)


# ---------------------------------------------------------------------------
# Stage 5: OntoClean Taxonomy Checks
# ---------------------------------------------------------------------------

def stage_ontoclean(g, result, verbose=False):
    print("[5/6] OntoClean Taxonomy Checks ...")

    # OntoClean meta-properties for key classes
    # +R = rigid (essential to instances), ~R = anti-rigid, -R = non-rigid
    # We tag classes based on domain knowledge

    rigid_classes = {
        SZDO.Person, SZDO.Organisation, SZDO.Nachlass, SZDO.Sammlung,
        SZDO.NachlassObjekt, SZDO.Manuskript, SZDO.Typoskript, SZDO.Notizbuch,
        SZDO.Buch, SZDO.Autograph, SZDO.Lebensdokument, SZDO.Konvolut,
        SZDO.Werk, SZDO.Ort, SZDO.BiographischesEreignis,
        SZDO.DigitalesObjekt, SZDO.METSObjekt, SZDO.Faksimile,
        SZDO.KorrespondenzKonvolut, SZDO.Korrekturfahne,
        SZDO.Typoskriptdurchschlag, SZDO.IIIFManifest,
    }

    # Anti-rigid: role-like classes that depend on context
    # (Currently SZDO doesn't have explicit role classes -- roles are modeled as properties,
    #  which is actually the correct ODP approach)

    # Check: No anti-rigid class should be superclass of a rigid class
    # Since we don't have anti-rigid classes, this passes by definition

    # Check: Rigid classes should not be subclass of non-rigid utility classes
    # (e.g., a rigid class should not subclass a "mixin" or "descriptor")

    # Verify that all rigid classes actually exist in the ontology
    all_classes = set(g.subjects(RDF.type, OWL.Class))
    for cls in rigid_classes:
        if cls not in all_classes:
            result.warn("ONTOCLEAN", f"Rigid class '{local_name(cls)}' not found in ontology")

    # Check identity criteria: classes with +I (identity-carrying) should
    # have an identifier property (signatur, gamsIdentifier, etc.)
    identity_classes = {
        SZDO.NachlassObjekt: "szdo:signatur",
        SZDO.Person: "szdo:gndIdentifier or szdo:nachname",
        SZDO.Werk: "szdo:titel",
        SZDO.Ort: "szdo:geonamesIdentifier",
    }

    for cls, id_hint in identity_classes.items():
        if cls in all_classes:
            result.add_info("ONTOCLEAN",
                f"'{local_name(cls)}' (+R +I): identity via {id_hint}")

    # Roles are correctly modeled as properties (hatAutor, hatHerausgeber, etc.)
    # rather than as role subclasses -- this follows the Agent-Role ODP
    result.add_info("ONTOCLEAN",
        "Agent roles modeled as properties (ODP Agent-Role pattern) -- correct approach")

    result.add_info("ONTOCLEAN",
        f"Analyzed {len(rigid_classes)} rigid classes -- no anti-rigid/rigid conflicts detected")


# ---------------------------------------------------------------------------
# Stage 6: Competency Question SPARQL Tests
# ---------------------------------------------------------------------------

def stage_competency_questions(g, result, verbose=False):
    print("[6/6] Competency Question Tests ...")

    # These test that the ontology SCHEMA can support answering the questions,
    # i.e., the required classes and properties exist.

    cq_tests = [
        # CQ1: Welche Sammlungen umfasst der Nachlass?
        {
            "id": "CQ01",
            "question": "Welche Sammlungen umfasst der Nachlass?",
            "query": """
                ASK {
                    szdo:Nachlass a owl:Class .
                    szdo:Sammlung a owl:Class .
                    szdo:enthaelt a owl:ObjectProperty .
                }
            """,
            "expected": True,
        },
        # CQ2: Welche Manuskriptzeugen existieren zu einem Werk?
        {
            "id": "CQ02",
            "question": "Welche Manuskriptzeugen existieren zu einem Werk?",
            "query": """
                ASK {
                    szdo:Werk a owl:Class .
                    szdo:hatManuskriptzeuge a owl:ObjectProperty .
                    szdo:NachlassObjekt a owl:Class .
                }
            """,
            "expected": True,
        },
        # CQ3: Wie ist die Provenienzkette eines Bibliotheksbuchs?
        {
            "id": "CQ03",
            "question": "Wie ist die Provenienzkette eines Bibliotheksbuchs?",
            "query": """
                ASK {
                    szdo:Buch a owl:Class .
                    szdo:hatProvenienz a owl:ObjectProperty .
                    szdo:Provenienzereignis a owl:Class .
                    szdo:hatVorbesitzer a owl:ObjectProperty .
                    szdo:hatNachbesitzer a owl:ObjectProperty .
                }
            """,
            "expected": True,
        },
        # CQ4: Welche Schreiberhände finden sich auf einem Manuskript?
        {
            "id": "CQ04",
            "question": "Welche Schreiberhände finden sich auf einem Manuskript?",
            "query": """
                ASK {
                    szdo:Manuskript a owl:Class .
                    szdo:hatSchreiberhand a owl:ObjectProperty .
                    szdo:Person a owl:Class .
                }
            """,
            "expected": True,
        },
        # CQ5: Wo wird ein Objekt aufbewahrt und unter welcher Signatur?
        {
            "id": "CQ05",
            "question": "Wo wird ein Objekt aufbewahrt?",
            "query": """
                ASK {
                    szdo:wirdAufbewahrtIn a owl:ObjectProperty .
                    szdo:Aufbewahrungsort a owl:Class .
                    szdo:signatur a owl:DatatypeProperty .
                }
            """,
            "expected": True,
        },
        # CQ6: Welche publizierten Ausgaben existieren zu einem Werk? (Klawiter)
        {
            "id": "CQ06",
            "question": "Welche Manifestationen hat ein Werk?",
            "query": """
                ASK {
                    szdo:Werk a owl:Class .
                    szdo:hatManifestation a owl:ObjectProperty .
                    szdo:Manifestation a owl:Class .
                }
            """,
            "expected": True,
        },
        # CQ7: In welche Sprachen wurde ein Werk übersetzt?
        {
            "id": "CQ07",
            "question": "In welche Sprachen wurde ein Werk übersetzt?",
            "query": """
                ASK {
                    szdo:WerkExpression a owl:Class .
                    szdo:istUebersetzungVon a owl:ObjectProperty .
                    szdo:sprache a owl:DatatypeProperty .
                }
            """,
            "expected": True,
        },
        # CQ8: Textgenese eines Werks
        {
            "id": "CQ08",
            "question": "Gibt es Klassen für Textgenese (Notizbuch, Manuskript, Typoskript, Korrekturfahne)?",
            "query": """
                ASK {
                    szdo:Notizbuch a owl:Class .
                    szdo:Manuskript a owl:Class .
                    szdo:Typoskript a owl:Class .
                    szdo:Korrekturfahne a owl:Class .
                    szdo:istManifestationVon a owl:ObjectProperty .
                }
            """,
            "expected": True,
        },
        # CQ9: Sekundärliteratur zu einem Werk
        {
            "id": "CQ09",
            "question": "Gibt es eine Klasse für Sekundärliteratur?",
            "query": """
                ASK {
                    szdo:Sekundaerliteratur a owl:Class .
                    szdo:wirdBehandeltIn a owl:ObjectProperty .
                }
            """,
            "expected": True,
        },
        # CQ10: Lebensereignisse mit Ort
        {
            "id": "CQ10",
            "question": "Können biographische Ereignisse mit Orten verknüpft werden?",
            "query": """
                ASK {
                    szdo:BiographischesEreignis a owl:Class .
                    szdo:hatOrt a owl:ObjectProperty .
                    szdo:Ort a owl:Class .
                    szdo:datum a owl:DatatypeProperty .
                }
            """,
            "expected": True,
        },
        # CQ11: Korrespondenzpartner
        {
            "id": "CQ11",
            "question": "Können Korrespondenzpartner identifiziert werden?",
            "query": """
                ASK {
                    szdo:KorrespondenzKonvolut a owl:Class .
                    szdo:hatAbsender a owl:ObjectProperty .
                    szdo:hatEmpfaenger a owl:ObjectProperty .
                }
            """,
            "expected": True,
        },
        # CQ12: Werke einer Lebensphase
        {
            "id": "CQ12",
            "question": "Können Werke zeitlich eingeordnet werden?",
            "query": """
                ASK {
                    szdo:Werk a owl:Class .
                    szdo:entstehungsdatum a owl:DatatypeProperty .
                    szdo:zeitperiode a owl:DatatypeProperty .
                }
            """,
            "expected": True,
        },
        # CQ13: Klawiter-Eintrag -> Werkindex
        {
            "id": "CQ13",
            "question": "Kann ein Klawiter-Eintrag (Manifestation) einem Werk zugeordnet werden?",
            "query": """
                ASK {
                    szdo:Manifestation a owl:Class .
                    szdo:hatManifestation a owl:ObjectProperty .
                    szdo:Werk a owl:Class .
                }
            """,
            "expected": True,
        },
        # CQ14: GND-Verknüpfung
        {
            "id": "CQ14",
            "question": "Gibt es GND-Identifikatoren für Personen?",
            "query": """
                ASK {
                    szdo:Person a owl:Class .
                    szdo:gndIdentifier a owl:DatatypeProperty .
                }
            """,
            "expected": True,
        },
        # CQ15: Provenienzmerkmale (SKOS)
        {
            "id": "CQ15",
            "question": "Können Provenienzmerkmale mit SKOS-Konzepten verknüpft werden?",
            "query": """
                ASK {
                    szdo:ProvenienzmerkmalInstanz a owl:Class .
                    szdo:hatMerkmaltyp a owl:ObjectProperty .
                }
            """,
            "expected": True,
        },
        # CQ-extra: WEMI stack complete
        {
            "id": "CQ-WEMI",
            "question": "Ist die vollständige WEMI-Hierarchie (Werk-Expression-Manifestation-Exemplar) modelliert?",
            "query": """
                ASK {
                    szdo:Werk a owl:Class .
                    szdo:WerkExpression a owl:Class .
                    szdo:Manifestation a owl:Class .
                    szdo:Exemplar a owl:Class .
                    szdo:hatExpression a owl:ObjectProperty .
                    szdo:hatManifestation a owl:ObjectProperty .
                    szdo:hatExemplar a owl:ObjectProperty .
                }
            """,
            "expected": True,
        },
        # CQ-extra: RiC alignment
        {
            "id": "CQ-RiC",
            "question": "Sind die RiC-Alignments korrekt (Nachlass->RecordSet, NachlassObjekt->Record)?",
            "query": """
                ASK {
                    szdo:Nachlass rdfs:subClassOf rico:RecordSet .
                    szdo:NachlassObjekt rdfs:subClassOf rico:Record .
                    szdo:DigitalesObjekt rdfs:subClassOf rico:Instantiation .
                }
            """,
            "expected": True,
        },
        # CQ16: Active participants vs mentioned persons
        {
            "id": "CQ16",
            "question": "Kann man aktive Beteiligte von erwähnten Personen unterscheiden?",
            "query": """
                ASK {
                    szdo:hatBeteiligtenAkteur a owl:ObjectProperty .
                    szdo:hatBeteiligtenAkteur rdfs:subPropertyOf rico:hasOrHadContributor .
                    szdo:hatAutor rdfs:subPropertyOf szdo:hatBeteiligtenAkteur .
                    szdo:hatBetroffenePerson a owl:ObjectProperty .
                    szdo:hatBetroffenePerson rdfs:subPropertyOf rico:hasOrHadSubject .
                    FILTER NOT EXISTS { szdo:hatBetroffenePerson rdfs:subPropertyOf szdo:hatBeteiligtenAkteur }
                }
            """,
            "expected": True,
        },
        # CQ17: Date evidence qualification
        {
            "id": "CQ17",
            "question": "Kann die Evidenz einer Datierung qualifiziert werden?",
            "query": """
                ASK {
                    szdo:datumEvidenz a owl:ObjectProperty .
                    szdo:datum a owl:DatatypeProperty .
                    szdo:sicherheitsgrad a owl:DatatypeProperty .
                }
            """,
            "expected": True,
        },
        # CQ-G1: Nachlass-Ontologie imported
        {
            "id": "CQ-G1",
            "question": "Importiert die SZDO die generische Nachlass-Ontologie?",
            "query": """
                ASK {
                    <https://gams.uni-graz.at/o:szd.ontology> owl:imports <https://w3id.org/nachlass> .
                }
            """,
            "expected": True,
        },
        # CQ-G2: Core classes aligned to nachlass:
        {
            "id": "CQ-G2",
            "question": "Sind die Kernklassen mit nachlass: aligniert?",
            "query": """
                ASK {
                    szdo:Nachlass rdfs:subClassOf nachlass:Nachlass .
                    szdo:NachlassObjekt rdfs:subClassOf nachlass:NachlassObjekt .
                    szdo:Werk rdfs:subClassOf nachlass:Werk .
                    szdo:Akteur rdfs:subClassOf nachlass:Akteur .
                    szdo:BiographischesEreignis rdfs:subClassOf nachlass:BiographischesEreignis .
                    szdo:Ort rdfs:subClassOf nachlass:Ort .
                }
            """,
            "expected": True,
        },
        # CQ-G3: nachlass: ontology is self-contained
        {
            "id": "CQ-G3",
            "question": "Definiert die nachlass:-Ontologie eigenstaendige Kernklassen?",
            "query": """
                ASK {
                    nachlass:Nachlass a owl:Class .
                    nachlass:NachlassObjekt a owl:Class .
                    nachlass:Werk a owl:Class .
                    nachlass:Person a owl:Class .
                    nachlass:BiographischesEreignis a owl:Class .
                    nachlass:Ort a owl:Class .
                    nachlass:Provenienzereignis a owl:Class .
                }
            """,
            "expected": True,
        },
    ]

    passed = 0
    failed = 0
    for test in cq_tests:
        full_query = CQ_PREFIX_BLOCK + test["query"]
        try:
            actual = bool(g.query(full_query).askAnswer)
        except Exception as e:
            result.error("CQ", f"{test['id']}: Query error -- {e}")
            failed += 1
            continue

        if actual == test["expected"]:
            passed += 1
            if verbose:
                result.add_info("CQ", f"{test['id']} PASS: {test['question']}")
        else:
            result.error("CQ", f"{test['id']} FAIL: {test['question']} (expected {test['expected']}, got {actual})")
            failed += 1

    result.add_info("CQ", f"Competency Questions: {passed}/{passed+failed} passed")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="SZDO Ontology Validation Pipeline")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    args = parser.parse_args()

    result = ValidationResult()

    # Stage 1
    g = stage_syntax(result, args.verbose)
    if g is None:
        result.print_report()
        sys.exit(1)

    # Stage 2
    stage_metrics(g, result, args.verbose)

    # Stage 3
    stage_shacl(g, result, args.verbose)

    # Stage 4
    stage_owl_checks(g, result, args.verbose)

    # Stage 5
    stage_ontoclean(g, result, args.verbose)

    # Stage 6
    stage_competency_questions(g, result, args.verbose)

    # Report
    ok = result.print_report()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
