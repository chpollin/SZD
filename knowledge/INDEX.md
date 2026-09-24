---
title: Index
project:
  name: Stefan Zweig Digital, data repository
  repository: https://github.com/chpollin/SZD
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: complete
created: 2025-10-23
updated: 2026-09-24
---

# Index

Entry point to the project knowledge of the Stefan Zweig Digital data repository, which holds the TEI sources, the estate ontology SZDO and the scripts that prepare, repair and reconcile the catalogue data. Read the [README](../README.md) first, then this index, the [plan](plan.md) and the [journal](journal.md), then the document the task needs. All knowledge documents are English, German project terms stay where the glossary below defines them. The presentation layer (XSLT, JavaScript, CSS, the RDF transformation) lives in the repository `ZIMLAB/szd` with a knowledge base of its own that starts at its `knowledge/INDEX.md`.

## Documents

| Document | Question it answers |
|---|---|
| [PROJECT](PROJECT.md) | What is the research project, with which context, method, standards, participants and chronology? |
| [COLLECTIONS](COLLECTIONS.md) | Which collections and indexes exist, with which files and PIDs and which collection-specific encoding, and which rendering contracts does the presentation layer impose on them? |
| [DATA_MODEL](DATA_MODEL.md) | Which encoding patterns do all TEI files share, from header and bilingual encoding to authority references, identifiers and dates? |
| [DATA](DATA.md) | How are entries counted, how far do machine-readable dates reach, which data gaps are documented and what did the archive checkups of September 2026 find and correct? |
| [MAPPING](MAPPING.md) | How does each column of the correspondence catalogue CSV map to the TEI of the Konvolut files? |
| [ARCHITECTURE](ARCHITECTURE.md) | How do the two repositories, the staging and production ingest, the derived timeline assets, Zenodo and GitHub Pages fit together? |
| [ONTOLOGY](ONTOLOGY.md) | How is SZDO built, with its two layers, alignments, validation and competency questions? |
| [Lebenskalender-Lanes](Lebenskalender-Lanes.md) | How are the timeline lanes derived from the TEI, with which event schema and dating rules, and where are they delivered? |
| [plan](plan.md) | Which technical work and which operator and archive questions are open on the data side? |
| [journal](journal.md) | What changed and was decided in which session? |
| [handoff](handoff.md) | Which handoff points from other sessions or repositories wait for integration? |
| [archive/TASK-BRIEFING-v1.1.0](archive/TASK-BRIEFING-v1.1.0.md) | Which task briefing produced SZDO v1.1.0? Kept as a historical record. |

Further documentation sits beside the material it describes, [ontology/README.md](../ontology/README.md) for the ontology files and versions, [szd-zenodo-backup/README.md](../szd-zenodo-backup/README.md) for the Zenodo pipeline, [docs/lebenskalender/README.md](../docs/lebenskalender/README.md) for the timeline prototype and [webpage/README.md](../webpage/README.md) for the static page content. The live ontology documentation is https://chpollin.github.io/SZD/ontology/.

## Scripts

Every script folder has a README with procedure, options and log format. Scripts that rewrite files under `data/` read and write through [scripts/_szd_io.py](../scripts/_szd_io.py), which keeps each file's line endings and writes only after a well-formedness check, and they append every change to a CSV log beside them.

| Path | Purpose |
|---|---|
| [konvolute_import/](../scripts/konvolute_import/README.md) | Import of every correspondence Konvolut from GAMS production into `data/Correspondence/konvolute/`, with the known defective production objects |
| [staging_package/build_staging_package.py](../scripts/staging_package/build_staging_package.py) | Staging ingest package outside the repository, in ingest order, with checksums and the Cirilo references still to set |
| [checkup_2026_09_konvolute/](../scripts/checkup_2026_09_konvolute/README.md) | Evidenced corrections of the Konvolut files from the archive checkup of September 2026 |
| [checkup_2026_09_korrespondenz/](../scripts/checkup_2026_09_korrespondenz/README.md) | Bundle signatures of correspondence index entries without signature |
| [checkup_2026_09_index/](../scripts/checkup_2026_09_index/README.md) | Person duplicates, reference form, essay author references and further IIIF label repairs, the survey of unlinked persons (`find_unlinked_persons.py`), and the check and removal of certainly unreferenced persons (`verify_orphan_persons.py`, `remove_orphan_persons.py`, removed entries kept in `removed_persons.xml`) |
| [organisationen_index/](../scripts/organisationen_index/README.md) | Build (historical) and maintenance of the organisation index, country and place from the GND (`reconcile_org_places.py`) |
| [personen_ohne_verweis/](../scripts/personen_ohne_verweis/README.md) | Person entries the RDF mapping finds no reference to |
| [korrespondenz_titel/](../scripts/korrespondenz_titel/README.md) | Entry titles of the Konvolut files after the title and date convention |
| [essay_klassifikation/](../scripts/essay_klassifikation/README.md) | Grouping keys of the Aufsatzablage and survey of the grouped lists |
| [lebenskalender_lanes/](../scripts/lebenskalender_lanes/README.md) | Timeline lanes of the Lebenskalender from the TEI sources |
| [iiif_structure_labels/](../scripts/iiif_structure_labels/README.md) | Prepared book sources without straight quotes in structure labels |
| [szaal_lebensdokumente/](../scripts/szaal_lebensdokumente/README.md) | SZ-AAL personal documents CSV to `SZDLEB.xml` |
| [Mets Import QA Pipeline/](../scripts/Mets%20Import%20QA%20Pipeline/README.md) | Pre-ingest validation of book sources |
| [Processing Pipeline/](../scripts/Processing%20Pipeline/README.md) | Scan exports to METS viewer XML for GAMS |
| [reconcile_klawiter.py](../scripts/reconcile_klawiter.py) | Klawiter links in `ontology/reconciliation.ttl` by title matching, with [reconciliation_report.md](../scripts/reconciliation_report.md) and `reconciliation_results.json` |
| [generate_instances.py](../scripts/generate_instances.py) | Sample instances `ontology/sample-instances.ttl` from the TEI for the SHACL validation |

`python -m pytest -q scripts` runs the tests of the script folders and of the shared file helpers.

## Glossary

Aufsatzablage

Zweig's essay filing, the collection `o:szd.aufsatzablage` in `data/Aufsatzablage/SZDESS.xml`.

Bestand (holding)

One collection of the estate with its own TEI file, for instance works, correspondence or library. In shelfmarks it is the prefix before the `/`.

Cirilo

The GAMS client with which the operator ingests objects and sets their datastreams and stylesheet references.

Einheitssachtitel

The uniform document-type title of a catalogue entry, `title[@type="Einheitssachtitel"]`, which the grouped lists use as their inner grouping key.

GAMS

The asset management system of the University of Graz on which Stefan Zweig Digital runs, with a production instance at `gams.uni-graz.at` and a staging instance at `gams-staging.uni-graz.at`.

gamsdev mirror

The checkout of the presentation layer on the staging server, from which staging serves stylesheets and assets. The staging references `STYLESHEET` and `TORDF` point into it.

Konvolut

The TEI object `o:szd.korrespondenzen.<slug>` that holds the correspondence with one partner, one `biblFull` per letter, stored as `data/Correspondence/konvolute/szd.korrespondenzen.<slug>.xml`. The correspondence index `SZDKOR.xml` points to it from each archival bundle.

Lebensdokumente (personal documents)

Diaries, contracts, official documents and ephemera, the collection `o:szd.lebensdokumente` in `data/PersonalDocument/SZDLEB.xml`.

Lebenskalender

The biography object `o:szd.lebenskalender` and, by extension, its timeline view with the lanes derived in this repository.

Operator

The project lead, who decides open questions, ingests into GAMS and pushes.

Staging package

A folder outside the repository, written by `scripts/staging_package/build_staging_package.py`, that holds the TEI files to ingest in ingest order together with the references each object needs.

Standort (repository)

An institution that holds material of the estate, recorded in the location index `o:szd.standorte`.

Themenseite (theme page)

A curated page `o:szd.thema.<n>` in `data/Issue/`.

TORDF

The datastream that names the RDF stylesheet an object uses at ingest, and by extension `szd-TORDF.xsl` in the presentation layer.
