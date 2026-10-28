---
title: Index
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: complete
language: en
version: 1.1
created: 2025-10-23
updated: 2026-10-28
authors: [Christopher Pollin]
generated-with: Claude Code (Claude Opus 5.5)
related: [project, specification, architecture, governance, plan, journal, handoff]
---

# Index

Entry point to the project knowledge of Stefan Zweig Digital, for scholars and developers who want to understand how the portal and its data are built and for the coding agents that work on them. The knowledge describes both repositories. The data repository [chpollin/SZD](https://github.com/chpollin/SZD) holds the TEI sources, the estate ontology SZDO, the scripts that prepare, repair and reconcile the catalogue data, the local harness of the presentation layer, the SPARQL query templates, copies of three ingest stylesheets and this knowledge base. The ZimLab repository gams-www (https://zimlab.uni-graz.at/gams/projects/szd/gams-www, local checkout `ZIMLAB/szd`) holds only what GAMS serves, the page XSLT, the RDF transformation `szd-TORDF.xsl`, JavaScript, CSS, fonts, icons, images and the lane copies of the timeline ([architecture](architecture.md#two-repositories)). Until October 2026 gams-www kept a knowledge base of its own, which this one now contains. Read the [README](../README.md) first, then this index, the [plan](plan.md) and the [journal](journal.md), then the document the task needs. All knowledge documents are English, German project terms stay where the glossary below defines them.

## Documents

| Document | Function | Question it answers |
|---|---|---|
| [project](project.md) | Charter | What is Stefan Zweig Digital, who runs it, with which context, method, standards, material, licences, participants and chronology? |
| [specification](specification.md) | Specification | What must the presentation layer do, under which constraints, and which decisions stand? |
| [governance](governance.md) | Governance | Who may change, deploy, ingest and publish what? |
| [architecture](architecture.md) | Architecture | How do the two repositories, GAMS with its concepts and layers, the derived timeline assets, Zenodo and GitHub Pages fit together, and which debt is known? |
| [deployment-architecture](deployment-architecture.md) | Architecture | How do a commit of gams-www and a data change reach staging and production, which ingest stylesheets does Cirilo run, and which Cirilo references must be set? |
| [rendering-architecture](rendering-architecture.md) | Architecture | Which stylesheet renders which page, and how do templates, languages, scripts and styles work? |
| [search-architecture](search-architecture.md) | Architecture | How do the search queries and their result page work? |
| [correspondence-gallery-architecture](correspondence-gallery-architecture.md) | Architecture | How does the correspondence gallery group by person and Konvolut? |
| [data](data.md) | Material | Which GAMS objects and derived datastreams exist, and where do their sources live? |
| [collections](collections.md) | Material | Which collections and indexes exist, with which files and PIDs and which collection-specific encoding, and which rendering contracts does the presentation layer impose on them? |
| [data-model](data-model.md) | Material | Which encoding patterns do all TEI files share, from header and bilingual encoding to authority references, identifiers and dates? |
| [data-quality](data-quality.md) | Material | How are entries counted, how far do machine-readable dates reach, which data gaps are documented and what did the archive checkups of September 2026 find and correct? |
| [konvolut-csv-mapping](konvolut-csv-mapping.md) | Material | How does each column of the correspondence catalogue CSV map to the TEI of the Konvolut files? |
| [konvolut-title-curation](konvolut-title-curation.md) | Material (snapshot of 2026-09-10) | Which B shelfmark groups need a curated title? |
| [lebenskalender-lanes](lebenskalender-lanes.md) | Material | How are the timeline lanes derived from the TEI, with which event schema and dating rules, and where are they delivered? |
| [ontology](ontology.md) | Domain knowledge | How is SZDO built, with its two layers, alignments, validation and competency questions? |
| [rdf-mapping](rdf-mapping.md) | Domain knowledge | How does TEI map to the `szd:` RDF of the search, and which findings are open? |
| [testing](testing.md) | Quality assurance | What is checked locally, what only on staging, and which rule applies before a push? |
| [plan](plan.md) | Planning | Which work and which operator and archive questions are open, on the data side and on the presentation side? |
| [journal](journal.md) | Provenance | What changed and was decided, integrated, rejected or corrected, and when? |
| [handoff](handoff.md) | Handoff | Which points from elsewhere wait for integration? |
| [archive/task-briefing-v1.1.0](archive/task-briefing-v1.1.0.md) | Archive | Which task briefing produced SZDO v1.1.0? Kept as a historical record. |

Further documentation sits beside the material it describes, [ontology/README.md](../ontology/README.md) for the ontology files and versions, [szd-zenodo-backup/README.md](../szd-zenodo-backup/README.md) for the Zenodo pipeline, [docs/lebenskalender/README.md](../docs/lebenskalender/README.md) for the timeline prototype and [webpage/README.md](../webpage/README.md) for the static page content. The live ontology documentation is https://chpollin.github.io/SZD/ontology/. Operational guides of the presentation layer are the harness README [local-test-build/README.md](../local-test-build/README.md), the prototype README [local-test-build/proto/README.md](../local-test-build/proto/README.md) and the SPARQL template README [gams/query/README.md](../gams/query/README.md). The agent instructions are [CLAUDE.md](../CLAUDE.md), into which the former `AGENTS.md` of gams-www is merged.

## Reading paths

- An agent starts with [CLAUDE.md](../CLAUDE.md), this index, [handoff](handoff.md) and [plan](plan.md), then reads the document of its task.
- A reader who wants to understand the portal reads [project](project.md), [architecture](architecture.md), [data](data.md) and [rendering-architecture](rendering-architecture.md).
- A change to a page needs [specification](specification.md), [rendering-architecture](rendering-architecture.md), [testing](testing.md) and [deployment-architecture](deployment-architecture.md).
- A change to the RDF or the search needs [rdf-mapping](rdf-mapping.md), [search-architecture](search-architecture.md) and [testing](testing.md#rule).
- A change to TEI lists and indexes needs [collections](collections.md) first, then [data-model](data-model.md) and [data-quality](data-quality.md), and its ingest follows [deployment-architecture](deployment-architecture.md#data-ingest).
- Work on SZDO needs [ontology](ontology.md) and [ontology/README.md](../ontology/README.md).

## Conventions

The knowledge base follows the Promptotyping convention for knowledge documents (<https://dhcraft.org/Promptotyping/>). File names are lowercase kebab-case, with a canonical name for a single carrier of a function and `<subject>-<function>.md` or a descriptive `<subject>-<aspect>.md` for a specialisation. The entry point keeps the conventional name `INDEX.md`. The document schema version is kept here in the field `version` and holds for every document of this folder. It changes when the shared frontmatter or the set of functions changes, and a content correction leaves it unchanged. Every document carries `title`, `project`, `method`, `status`, `created` and `updated`, and its first paragraph states its purpose. Documents about the presentation layer note in their frontmatter that the served files they describe lie in gams-www, and they name such files in code formatting without a link.

## Scripts

Every script folder has a README with procedure, options and log format. Scripts that rewrite files under `data/` read and write through [scripts/_szd_io.py](../scripts/_szd_io.py), which keeps each file's line endings and writes only after a well-formedness check, and they append every change to a CSV log beside them. The same module holds the TEI namespaces, the person id and GND patterns, the UTF-8 console setup and the reads from `HEAD` that the newer scripts share. The finished `checkup_2026_09_*` scripts keep their own copies as the record of the changes they made.

| Path | Purpose |
|---|---|
| [konvolute_import/](../scripts/konvolute_import/README.md) | Import of every correspondence Konvolut from GAMS production into `data/Correspondence/konvolute/`, with the known defective production objects |
| [check_data.py](../scripts/check_data.py) | Read-only checks of all TEI files with an exit code, from well-formedness and double-encoded umlauts to dangling references, GND form, dates and the Konvolut PIDs, with the open findings frozen as documented exceptions |
| [staging_package/build_staging_package.py](../scripts/staging_package/build_staging_package.py) | Staging ingest package from `HEAD` outside the repository, in ingest order, with checksums and the Cirilo references still to set, after `check_data.py` |
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

`python -m pytest -q scripts` runs the tests of the script folders and of the shared file helpers. The tests of the presentation layer run in [local-test-build/](../local-test-build/README.md), see [testing](testing.md).

## Glossary

### Aufsatzablage

Zweig's essay filing (essay files), the collection `o:szd.aufsatzablage` in `data/Aufsatzablage/SZDESS.xml`, rendered by `szd-Essays.xsl`.

### B shelfmark

The part `B<nr>` after the `/` of a correspondence shelfmark, for instance `SZ-SAM/B7`, the physical bundle within a holding.

### Bestand (holding)

One collection of the estate with its own TEI file, for instance works, autographs, correspondence or library. In shelfmarks, among them correspondence shelfmarks, it is the prefix before the `/`.

### Blazegraph

The triplestore of GAMS that holds the `szd:` RDF of the ingest and answers the content search.

### Cirilo

The GAMS client with which objects are ingested and their datastreams and stylesheet references are set. The operator ingests with it and holds its settings, see [governance](governance.md#who-does-what).

### Datenkorb (data basket)

The bookmark list of catalogue objects kept in the browser's `localStorage`, shown at `mode=databasket`.

### Einheitssachtitel

The uniform document-type title of a catalogue entry, `title[@type="Einheitssachtitel"]`, which the grouped lists use as their inner grouping key.

### GAMS

Geisteswissenschaftliches Asset Management System, the Fedora-based repository infrastructure and asset management system of the University of Graz on which Stefan Zweig Digital runs, with a production instance at `gams.uni-graz.at` and a staging instance at `gams-staging.uni-graz.at`.

### gams-www

The ZimLab repository https://zimlab.uni-graz.at/gams/projects/szd/gams-www with the files GAMS serves for SZD, checked out locally as `ZIMLAB/szd`. Older documents call it the presentation repository or `ZIMLAB/szd`.

### gamsdev mirror

The checkout of the presentation layer at `origin/develop` of gams-www on the staging server, from which staging serves the stylesheets and assets. The staging references `STYLESHEET` and `TORDF` point into it.

### Konvolut

In SZD the curated correspondence with one person or partner, also called Personen-Konvolut. It is the TEI object `o:szd.korrespondenzen.<slug>`, one `biblFull` per letter, stored as `data/Correspondence/konvolute/szd.korrespondenzen.<slug>.xml`. The correspondence index `SZDKOR.xml` points to it from each archival bundle. The Konvolut mode of the correspondence gallery groups by B shelfmark, the physical bundle, which is coarser than the curated Konvolut.

### Lebensdokumente (personal documents)

Diaries, contracts, official documents and ephemera, the collection `o:szd.lebensdokumente` in `data/PersonalDocument/SZDLEB.xml`.

### Lebenskalender

The biography object `o:szd.lebenskalender`, shown as a vertical list of dated events. By extension also its timeline view (Zeitleiste) with the lanes derived in this repository, which is switched off on the site.

### Mulgara

The Fedora resource index of GAMS with the Dublin Core and membership metadata of every object, from which the galleries are filled.

### Operator

The person at DHCraft who decides open questions, holds the Cirilo settings, ingests into GAMS, pushes and publishes releases.

### PID

The persistent identifier of a GAMS object, for instance `o:szd.werke`, `context:szd` or `query:szd.fulltext`.

### Register (index)

The index pages of persons, repositories, organisations and works, rendered by `szd-Index.xsl`.

### Staging package

A folder outside the repository, written by `scripts/staging_package/build_staging_package.py`, that holds the TEI files to ingest in ingest order together with the references each object needs.

### Standort (repository)

An institution that holds material of the estate, recorded in the location index `o:szd.standorte`.

### Themenseite (theme page)

A curated essay page `o:szd.thema.<n>` in `data/Issue/`, rendered by `szd-Thema.xsl`.

### TORDF

The datastream that names the RDF stylesheet an object runs at ingest, and by extension `szd-TORDF.xsl` in gams-www itself.

### Zeitleiste (timeline)

The multi-holding view of the Lebenskalender at `mode=timeline`, with the holdings as switchable lanes on a shared year scale. It is implemented and switched off by `timelineView` in `szd-static.xsl`.
