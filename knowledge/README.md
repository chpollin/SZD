---
title: Knowledge Vault -- Stefan Zweig Digital
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD.git
method:
  name: Promptotyping
  url: https://dhcraft.org/promptotyping
status: complete
created: 2025-10-23
updated: 2026-09-23
---

# Knowledge Vault -- Stefan Zweig Digital

Zentrale Dokumentation fuer das SZD-Projekt. Jedes Thema hat genau eine Datei.

## Dokumentation

| Datei | Inhalt |
|-------|--------|
| [PROJECT.md](PROJECT.md) | Forschungsprojekt: Kontext, Methodik, Sammlungen, FAIR-Compliance, Chronologie |
| [ONTOLOGY.md](ONTOLOGY.md) | Nachlass-Ontologie (SZDO v1.2.0): Zwei-Schichten-Architektur, Designprinzipien, Alignments, Kompetenzfragen |
| [COLLECTIONS.md](COLLECTIONS.md) | Alle Sammlungen im Detail: Struktur, Inhalt, TEI-Encoding |
| [DATA.md](DATA.md) | Datenbestand-Statistiken der Hauptsammlungen und Korrespondenz-Konvolute, Datumsqualitaet, Organisationenindex SZDORG, Archiv-Checkup September 2026 |
| [DATA_MODEL.md](DATA_MODEL.md) | TEI-XML Encoding-Muster, bilinguale Architektur |
| [MAPPING.md](MAPPING.md) | TEI-CSV Schema-Mapping (Referenzdokument) |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Systemarchitektur, Datenfluss, Plattform-Integration |
| [journal.md](journal.md) | Arbeitstagebuch, ein Eintrag je substanzieller Session: Änderungen, Entscheidungen, Offenes |
| [Lebenskalender-Lanes.md](Lebenskalender-Lanes.md) | Zeitleisten-Lanes des Lebenskalenders: Ereignisschema, Quellenbewahrung, Datierungsregeln, Erzeugung, Auslieferungsstand |

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
| [szaal_lebensdokumente/csv_to_szdleb.py](../scripts/szaal_lebensdokumente/csv_to_szdleb.py) | SZ-AAL Lebensdokumente CSV -> SZDLEB.xml ([README](../scripts/szaal_lebensdokumente/README.md)) |
| [korrespondenz_titel/fix_titles.py](../scripts/korrespondenz_titel/fix_titles.py) | Eintragstitel der Korrespondenz-Konvolute auf die Titel- und Datumskonvention ziehen ([README](../scripts/korrespondenz_titel/README.md)) |
| [essay_klassifikation/fix_classification.py](../scripts/essay_klassifikation/fix_classification.py) | Gruppierungsschluessel der Aufsatzablage vervollstaendigen und die gruppierten Listen erheben ([README](../scripts/essay_klassifikation/README.md)) |
| [personen_ohne_verweis/list_unlinked_persons.py](../scripts/personen_ohne_verweis/list_unlinked_persons.py) | Kandidatenliste der unverknuepften Personeneintraege als CSV ([README](../scripts/personen_ohne_verweis/README.md)) |
| [lebenskalender_lanes/build_lanes.py](../scripts/lebenskalender_lanes/build_lanes.py) | Zeitleisten-Lanes des Lebenskalenders aus den TEI-Quellen ableiten ([README](../scripts/lebenskalender_lanes/README.md)) |
| [organisationen_index/](../scripts/organisationen_index/README.md) | Organisationenindex SZDORG erzeugen und die Koerperschaftsverweise des Bestands vom Personenindex darauf umstellen ([README](../scripts/organisationen_index/README.md)) |
| [checkup_2026_09_korrespondenz/add_bundle_signatures.py](../scripts/checkup_2026_09_korrespondenz/add_bundle_signatures.py) | Buendelsignaturen der signaturlosen Indexeintraege aus dem Konvolut ableiten ([README](../scripts/checkup_2026_09_korrespondenz/README.md)) |
| [checkup_2026_09_index/](../scripts/checkup_2026_09_index/README.md) | Dublettenzusammenfuehrung im Personenregister, Referenzform der Personenverweise, Autorreferenzen der Aufsatzablage, weitere IIIF-Label-Reparaturen ([README](../scripts/checkup_2026_09_index/README.md)) |
| [iiif_structure_labels/](../scripts/iiif_structure_labels/README.md) | Vorbereitete Buchquellen ohne Anfuehrungszeichen in Strukturlabels, Ingest offen ([README](../scripts/iiif_structure_labels/README.md)) |

## Externe Dokumentation

- [szd-zenodo-backup/README.md](../szd-zenodo-backup/README.md) -- Zenodo-Archivierung
- [Live-Dokumentation](https://chpollin.github.io/SZD/ontology/) -- GitHub Pages
- [docs/lebenskalender/README.md](../docs/lebenskalender/README.md) -- Lebenskalender-Prototyp im SZD-Design, erzeugt aus SZDBIO.xml durch den Generator im gams-www-Harness

## Standards

- [Records in Context (RiC-O)](https://www.ica.org/standards/RiC/ontology) -- Archivische Modellierung
- [IFLA LRM](https://www.ifla.org/publications/ifla-library-reference-model) -- Werkmodellierung
- [CIDOC-CRM](https://www.cidoc-crm.org/) -- Ereignisse, Provenienz
- [TEI P5](https://tei-c.org/guidelines/) -- Textencoding

---

_Stand: 23. September 2026_
