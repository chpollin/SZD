---
title: Governance
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD  # the served files it describes are in https://zimlab.uni-graz.at/gams/projects/szd/gams-www
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: complete
language: en
created: 2026-10-09
updated: 2026-10-28
authors: [Christopher Pollin]
generated-with: Claude Code (Claude Opus 5.5)
related: [project, deployment-architecture, testing, plan, handoff]
---

# Governance

Who may decide and change what in the SZD presentation layer in gams-www and in this data repository, which sources count as authoritative, and how a state reaches the public site. The agent instructions in [CLAUDE.md](../CLAUDE.md) bind agents to these rules.

## Roles

The operator works at DHCraft, see the open question on the project lead in the [plan](plan.md#data-questions). The operator decides open questions, holds every action on the GAMS servers and publishes.

The project partners at the Literaturarchiv Salzburg approve a state before it is published in production. The archive staff curate the catalogue data in the data repository, carry out the regular data ingests in Cirilo and supply curated texts such as the Konvolut titles.

The ZIM GAMS team at the University of Graz operates the GAMS instances and the server configuration on which the updater and the gamsdev mirror run.

Agents are LLM coding agents working in a checkout of gams-www or of the data repository on behalf of the operator. They change code and documentation and check their changes locally.

## Who does what

| Action | Who |
|---|---|
| Change code on `develop` of gams-www and documentation in this knowledge base | agents and operator, checked as [testing](testing.md#rule) requires |
| Commit | in gams-www agents on explicit request of the operator, in the data repository agents after each finished and checked unit as its `CLAUDE.md` states |
| Push gams-www to `origin/develop` and synchronise the gamsdev mirror, push the data repository | on explicit request of the operator |
| Merge into `main`, push `main` | operator only |
| GAMS update of production | operator only, after approval by the project partners |
| Cirilo settings (`STYLESHEET`, `TORDF`, `QUERY`, context membership) | operator only |
| Ingest of objects on staging or production | operator, regular data ingests also the archive staff |
| Deletion of GAMS objects | operator only |
| Corrections of TEI sources | data repository, never in gams-www |

Agents document the target values of Cirilo settings in [deployment-architecture](deployment-architecture.md#cirilo-references) and check them read-only through the datastream URLs. They never edit the gamsdev mirror on the server, whose only allowed change is the synchronisation with `origin/develop`.

## Authoritative sources

- The stylesheets, scripts and styles in gams-www are the source of truth for the presentation layer. The copies of `szd-TOMETS.xsl`, `szd-MODStoDC_MAPPING.xsl` and `szd-tei-hssf.xsl` in [gams/](../gams/) of this repository document what the operator copies into Cirilo, `szd-TOMETS.xsl` as copy of the inline production value, and which value each instance runs is recorded in [deployment-architecture](deployment-architecture.md#ingest-stylesheets-in-cirilo). The gamsdev mirror and the production checkout are copies of `develop` and `main`.
- The TEI sources in the data repository are the source of truth for the catalogue. GAMS holds their ingested copies.
- A document that carries both a catalogue description and a transcription is authoritative by part (operator decision of 2026-10-30): this repository for the header and the catalogue description, szd-teiCrafter for the transcription body. Both parts are merged into one document and validated together against the project ODD, which lives in this repository and whose generated RELAX NG the editor pins.
- The Klawiter bibliography (`data/Klawiter/`) is a delivery of klawiter-rescue, which is authoritative for it; this repository holds the delivered copy, and its profile and schema are klawiter-rescue's (`knowledge/tei-profile.md` there).
- The `QUERY` datastreams of the query and context objects are what GAMS executes. The templates in [gams/query/](../gams/query/README.md) are the target state, and a difference between the two is an open finding until the operator copies the template into Cirilo.
- Datastreams on staging and production are read without login and never written by agents. A reading is recorded with its date, because the servers change with every ingest.
- Within the knowledge base the declarative documents hold the current state, [plan](plan.md) the accepted open work and the operator questions, [handoff](handoff.md) unprocessed input from elsewhere and [journal](journal.md) the provenance of changes.

## Publication

The production instance serves the checkout of gams-www `main` at `https://gams.uni-graz.at/szd/`, which until the split of October 2026 included the knowledge base of the presentation layer and its agent instructions. Everything merged into gams-www `main` is therefore public. This knowledge base now lies in the data repository on GitHub, whose `docs/` folder GitHub Pages serves publicly, and the same care applies to it. Documentation names third parties by role and institution and carries no e-mail addresses, telephone numbers, monetary amounts or credentials.

A release merges `develop` into `main` after the project partners have approved the state, and `main` is never rewritten. The mechanics are described in [deployment-architecture](deployment-architecture.md#release-flow).

## Language

Documentation and code comments are English. Commit messages of gams-www are English since 2026-10-09 ([specification](specification.md#documentation)), and the language of commit messages in the data repository is set in [CLAUDE.md](../CLAUDE.md). German project terms stay where the [glossary](INDEX.md#glossary) defines them, and German user-facing texts of the site stay German.

## Open questions and incoming points

A question that only the operator can decide is recorded in [plan](plan.md#operator-questions) with the evidence it rests on. A point handed over from another session, lane or repository enters [handoff](handoff.md) and leaves it once it is integrated or rejected, with a record in the [journal](journal.md).
