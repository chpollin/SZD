---
title: "Task Briefing: SZDO Data Modelling"
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD.git
method:
  name: Promptotyping
  url: https://dhcraft.org/promptotyping
status: archived
created: 2026-03-29
updated: 2026-09-23
---

# Task Briefing: SZDO Data Modelling

Archived briefing of the four data modelling tasks that were carried out with SZDO v1.1.0 in March 2026. File and class names are those of v1.1.0.

## Outcome

- Task 1, `szdo:datumEvidenz` implemented as a SKOS vocabulary with four concepts in `szdg:DatumEvidenz`.
- Task 2, `szdo:hatBeteiligtenAkteur` as superproperty of ten role properties with RiC alignment.
- Task 3, Klawiter reconciliation checked, eight type corrections (historical-study to `hatManifestation`).
- Task 4, validation pipeline extended (CQ16, CQ17, SHACL shape 14).

## Context

SZDO v1.0.0 was published at the time with 72 classes and 130 properties. It integrates RiC-O, IFLA LRM and CIDOC-CRM in a layered architecture. Documentation `knowledge/ONTOLOGY.md`, OWL file `ontology/szd-ontology.ttl`, validation pipeline `ontology/validate.py`.

## Tasks

### 1. Evidence source model

SZDO then had only `szdo:sicherheitsgrad` (low, medium, high) for date uncertainty. A property `szdo:datumEvidenz` was to qualify the source of a dating.

- `aus-dokument`, the date stands in the document itself
- `aus-kontext`, inferred from context such as neighbouring letters
- `aus-externer-quelle`, taken from an external source such as a catalogue or secondary literature
- `unbekannt`, evidence source not documented

It complements the degree of certainty and was to be implemented as a SKOS vocabulary in the SZD glossary (analogous to `szdg:ProvenanceFeature`), with updated SHACL shapes. The M³GIM project uses `m3gim:dateEvidence` for the same concept.

### 2. Person roles

SZDO did not distinguish persons actively involved (author, addressee, scribe) from persons only mentioned. To be added:

- `szdo:hatBeteiligtenAkteur` (⊂ `rico:hasOrHadContributor`) for active involvement
- `rico:hasOrHadSubject` for thematic mention, already present in RiC-O

The existing properties `szdo:hatAutor`, `szdo:hatSchreiberhand` and `szdo:hatAdressat` imply active involvement and were to be declared `rdfs:subPropertyOf szdo:hatBeteiligtenAkteur`. A new competency question was to distinguish active involvement from mention, as needed for network analyses of the correspondence.

### 3. Klawiter reconciliation mapping

Part of the Klawiter entries was reconciled with the work index. The task checked whether the links through `szdo:hatManifestation` (work to Klawiter entry) are typed correctly (first editions as `szdo:Manifestation`, translations as `szdo:WerkExpression`, secondary literature as `szdo:Sekundaerliteratur`) and whether the Klawiter JSON-LD types and the SZDO classes are consistent. Klawiter data in `../klawiter-rescue/data/output/klawiter.jsonld`, vocabulary in `../klawiter-rescue/pipeline/lib/vocabulary.py`.

### 4. Validation pipeline

`ontology/validate.py` was to receive tests for the new properties (`datumEvidenz`, `hatBeteiligtenAkteur`), a competency question on persons actively involved in a document versus only mentioned, and SHACL shapes for the evidence sources.

## Scope

Frontend work belonged to another agent session. The correspondence date gaps had been closed separately in March 2026, see [DATA.md](../DATA.md#dates).

## Files

| File | Purpose |
|------|---------|
| `ontology/szd-ontology.ttl` | Main file, edited here |
| `ontology/szd-shapes.ttl` | SHACL shapes, extended |
| `ontology/validate.py` | Validation pipeline, extended |
| `knowledge/ONTOLOGY.md` | Design document, updated |
| `knowledge/DATA_MODEL.md` | Data model documentation, updated where needed |
