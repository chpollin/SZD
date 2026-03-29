# Knowledge Vault -- Stefan Zweig Digital

Zentrale Dokumentation fuer das SZD-Projekt. Jedes Thema hat genau eine Datei.

## Dokumentation

| Datei | Inhalt |
|-------|--------|
| [PROJECT.md](PROJECT.md) | Forschungsprojekt: Kontext, Methodik, Sammlungen, FAIR-Compliance, Chronologie |
| [ONTOLOGY.md](ONTOLOGY.md) | Nachlass-Ontologie (SZDO v1.2.0): Zwei-Schichten-Architektur, Designprinzipien, Alignments, Kompetenzfragen |
| [COLLECTIONS.md](COLLECTIONS.md) | Alle Sammlungen im Detail: Struktur, Inhalt, TEI-Encoding |
| [DATA.md](DATA.md) | Datenbestand-Statistiken: 9 TEI-Dateien, 311k Zeilen, 15 MB, Datumsqualitaet |
| [DATA_MODEL.md](DATA_MODEL.md) | TEI-XML Encoding-Muster, bilinguale Architektur |
| [MAPPING.md](MAPPING.md) | TEI-CSV Schema-Mapping (Referenzdokument) |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Systemarchitektur, Datenfluss, Plattform-Integration |

## Ontologie-Dateien

| Datei | Zweck |
|-------|-------|
| [nachlass-ontology.ttl](../ontology/nachlass-ontology.ttl) | Generische Nachlass-Ontologie (`https://w3id.org/nachlass#`) -- nachnutzbar |
| [szd-ontology.ttl](../ontology/szd-ontology.ttl) | SZD-spezifische Ontologie (importiert `nachlass:`) |
| [szd-shapes.ttl](../ontology/szd-shapes.ttl) | SHACL-Shapes fuer Strukturvalidierung |
| [validate.py](../ontology/validate.py) | 6-Stufen-Pipeline: Syntax, SHACL, OWL, OntoClean, 22 CQs |
| [generate_docs.py](../ontology/generate_docs.py) | HTML-Dokumentationsgenerator |
| [sample-instances.ttl](../ontology/sample-instances.ttl) | 25 Beispielinstanzen aus 5 Sammlungen |
| [reconciliation.ttl](../ontology/reconciliation.ttl) | Klawiter-Reconciliation-Triples |

## Scripts

| Datei | Zweck |
|-------|-------|
| [reconcile_klawiter.py](../scripts/reconcile_klawiter.py) | Klawiter-Bibliographie Reconciliation (105 Werke, 119 Verknuepfungen) |
| [generate_instances.py](../scripts/generate_instances.py) | Instanzdaten-Generierung aus TEI-XML |

## Externe Dokumentation

- [szd-zenodo-backup/README.md](../szd-zenodo-backup/README.md) -- Zenodo-Archivierung
- [Live-Dokumentation](https://chpollin.github.io/SZD/ontology/) -- GitHub Pages

## Standards

- [Records in Context (RiC-O)](https://www.ica.org/standards/RiC/ontology) -- Archivische Modellierung
- [IFLA LRM](https://www.ifla.org/publications/ifla-library-reference-model) -- Werkmodellierung
- [CIDOC-CRM](https://www.cidoc-crm.org/) -- Ereignisse, Provenienz
- [TEI P5](https://tei-c.org/guidelines/) -- Textencoding

---

_Stand: 29. Maerz 2026_
