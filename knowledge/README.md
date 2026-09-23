---
title: Knowledge Base -- Stefan Zweig Digital
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

# Knowledge Base -- Stefan Zweig Digital

Index of the project knowledge of the Stefan Zweig Digital data repository. Each subject has one canonical document, and the others link to it.

## Documents

| File | Subject |
|------|---------|
| [PROJECT.md](PROJECT.md) | Research project, context, methodology, FAIR, chronology |
| [COLLECTIONS.md](COLLECTIONS.md) | Collections and indices with files and PIDs, collection-specific encoding, the organisation index, the rendering contracts of the presentation layer |
| [DATA_MODEL.md](DATA_MODEL.md) | Encoding patterns shared by all TEI files, bilingual encoding, authority references, identifiers, dates |
| [DATA.md](DATA.md) | Counting conventions, date coverage, documented data gaps, results and open points of the archive checkups of September 2026 |
| [MAPPING.md](MAPPING.md) | TEI-CSV schema mapping of the correspondence catalogue |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Two-repository topography, publication workflow, derived assets, Zenodo, GitHub Pages |
| [ONTOLOGY.md](ONTOLOGY.md) | Nachlass-Ontologie SZDO, two-layer architecture, alignments, competency questions |
| [Lebenskalender-Lanes.md](Lebenskalender-Lanes.md) | Timeline lanes of the Lebenskalender, event schema, dating rules, generation, delivery state |
| [journal.md](journal.md) | Work diary, one entry per substantive session with changes, decisions and open points (German) |
| [archive/TASK-BRIEFING-v1.1.0.md](archive/TASK-BRIEFING-v1.1.0.md) | Archived task briefing of SZDO v1.1.0 |

## Ontology Files

| File | Purpose |
|------|---------|
| [nachlass-ontology.ttl](../ontology/nachlass-ontology.ttl) | Generic Nachlass-Ontologie (`https://w3id.org/nachlass#`), reusable for other estates |
| [szd-ontology.ttl](../ontology/szd-ontology.ttl) | SZD-specific ontology, imports `nachlass:` |
| [szd-shapes.ttl](../ontology/szd-shapes.ttl) | SHACL shapes for structural validation |
| [validate.py](../ontology/validate.py) | Validation pipeline with syntax, SHACL, OWL, OntoClean and competency questions |
| [generate_docs.py](../ontology/generate_docs.py) | HTML documentation generator |
| [sample-instances.ttl](../ontology/sample-instances.ttl) | Sample instances from several collections |
| [reconciliation.ttl](../ontology/reconciliation.ttl) | Klawiter reconciliation triples |

## Scripts

| Path | Purpose |
|------|---------|
| [reconcile_klawiter.py](../scripts/reconcile_klawiter.py) | Klawiter bibliography reconciliation by title matching, report in [reconciliation_report.md](../scripts/reconciliation_report.md) |
| [generate_instances.py](../scripts/generate_instances.py) | Instance data generation from TEI |
| [szaal_lebensdokumente/](../scripts/szaal_lebensdokumente/README.md) | SZ-AAL Personal Documents CSV to SZDLEB.xml |
| [korrespondenz_titel/](../scripts/korrespondenz_titel/README.md) | Entry titles of the konvolut objects after the title and date convention |
| [essay_klassifikation/](../scripts/essay_klassifikation/README.md) | Grouping keys of the Aufsatzablage and survey of the grouped lists |
| [personen_ohne_verweis/](../scripts/personen_ohne_verweis/README.md) | Candidate list of person entries the RDF mapping finds no reference to |
| [lebenskalender_lanes/](../scripts/lebenskalender_lanes/README.md) | Timeline lanes of the Lebenskalender from the TEI sources |
| [organisationen_index/](../scripts/organisationen_index/README.md) | Build of the organisation index and migration of the corporate-body references |
| [checkup_2026_09_korrespondenz/](../scripts/checkup_2026_09_korrespondenz/README.md) | Bundle signatures of signature-less correspondence index entries |
| [checkup_2026_09_index/](../scripts/checkup_2026_09_index/README.md) | Person duplicates, reference form, essay author references, further IIIF label repairs, survey of unlinked persons |
| [iiif_structure_labels/](../scripts/iiif_structure_labels/README.md) | Prepared book sources without straight quotes in structure labels |
| [Mets Import QA Pipeline/](../scripts/Mets%20Import%20QA%20Pipeline/README.md) | Pre-ingest validation of book sources |

## Further Documentation

- [szd-zenodo-backup/README.md](../szd-zenodo-backup/README.md) — Zenodo archiving pipeline
- [ontology/README.md](../ontology/README.md) — ontology files and versions
- [docs/lebenskalender/README.md](../docs/lebenskalender/README.md) — Lebenskalender prototype in the SZD design
- https://chpollin.github.io/SZD/ontology/ — live ontology documentation

## Standards

- [Records in Context (RiC-O)](https://www.ica.org/standards/RiC/ontology) — archival modelling
- [IFLA LRM](https://www.ifla.org/publications/ifla-library-reference-model) — work modelling
- [CIDOC-CRM](https://www.cidoc-crm.org/) — events, provenance
- [TEI P5](https://tei-c.org/guidelines/) — text encoding
