---
title: Journal
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: active
language: en
created: 2026-09-18
updated: 2026-10-28
authors: [Christopher Pollin]
generated-with: Claude Code (Claude Opus 5.5)
related: [plan, handoff, specification]
---

# Journal

The provenance of the knowledge base of both repositories, newest first. Each entry records one coherent transition or one substantive session, with what changed, what was decided and what stayed open at the time, and where the result now stands. Current state lives in the documents listed in the [index](INDEX.md), open work in the [plan](plan.md).

The entries come in two forms, kept in one chronological order since the merge of 2026-10-28.

- Entries of the presentation layer, written in gams-www until 2026-10-28, follow the Promptotyping convention. Their heading carries the entry type, `integriert` for integrated knowledge, `verworfen` for a rejected point, `korrigiert` for a correction and `verdichtet` for a compaction of this journal, and their body names source, target and result. The Git history of gams-www keeps every earlier wording of these entries and of the presentation-layer knowledge up to the merge.
- Entries of the data repository are work-diary entries, one per substantive session, whose heading carries the date after a comma and whose body is labelled Changed, Decided, Checked, Found, Integrated and Open. The entries up to the organisation places of 2026-09-24 were written in German and translated on 2026-09-24, and Git keeps their wording.

## 2026-10-28 integriert knowledge bases of both repositories

- Source: the knowledge base of gams-www as copied on 2026-10-28, the knowledge base of the data repository, and a reading of the Cirilo datastreams on staging and production on 2026-10-28.
- Target: every document of this folder, listed in the [index](INDEX.md), and [deployment-architecture](deployment-architecture.md#ingest-stylesheets-in-cirilo).
- Result: everything GAMS does not serve moved from gams-www into the data repository, the harness to `local-test-build/`, the SPARQL templates from `query/` to `gams/query/`, and `szd-MODStoDC_MAPPING.xsl` and `szd-tei-hssf.xsl` to `gams/`, where `szd-TOMETS.xsl` is replaced by a byte copy of the inline production datastream. `szd-TORDF.xsl` stays in gams-www, because `cirilo:TEI.szd/TORDF` redirects to its served copy on each instance. The two knowledge bases are one, with lowercase kebab-case file names after the Promptotyping convention and `INDEX.md` as entry point. Merged are the two charters into [project](project.md), the two architecture documents into [architecture](architecture.md), with the data publication workflow and the Cirilo ingest dialog moved into [deployment-architecture](deployment-architecture.md#data-ingest), the two plans into [plan](plan.md) with a data side and a presentation side, the two journals into this journal, the two handoff inboxes and the two indexes with their glossaries. Renamed are `DATA.md` to [data-quality](data-quality.md), `COLLECTIONS.md` to [collections](collections.md), `DATA_MODEL.md` to [data-model](data-model.md), `MAPPING.md` to [konvolut-csv-mapping](konvolut-csv-mapping.md), `ONTOLOGY.md` to [ontology](ontology.md), `Lebenskalender-Lanes.md` to [lebenskalender-lanes](lebenskalender-lanes.md) and `archive/TASK-BRIEFING-v1.1.0.md` to [archive/task-briefing-v1.1.0](archive/task-briefing-v1.1.0.md). The data document of gams-www keeps the name [data](data.md). Links to files that stay in gams-www became file names in code formatting. The merge brought two conflicts to light. The former knowledge bases name different project leads, now an [operator question](plan.md#data-questions), and gams-www writes English commit messages since 2026-10-09 while the data repository sets its commit language in its `CLAUDE.md`.
- Checked: every relative link and every `#anchor` of the knowledge documents resolves, by a mechanical check with GitHub-style anchor slugs.

## 2026-10-21 integriert refactoring phase 1 in part and native data basket

- Source: operator commission of 2026-10-21 for phase 1 and phase 3 step 2 of the [plan](plan.md#refactoring).
- Target: `szd-TORDF.xsl`, `szd-Suche.xsl`, `szd-Bibliothek.xsl`, the data basket in `szd-context.xsl`, `js/databasket.js`, `css/szd.css`, `css/print.css`, the RDF golden and smoke tests, `test/search-results.smoke.mjs`, [rendering-architecture](rendering-architecture.md#project-scripts).
- Result: the library writes `szd:relationToWork` with one `#`, the English extent of the correspondence says "Piece" for one and "Pieces" for several, and that of library and autographs "leaf" for one leaf. Organisation hits get a block in the search results that links to the organisation index, and library entries without author render their titles italic like every library title. The RDF golden test pairs every intended corrected line with its baseline line. The data basket runs without DataTables, Buttons and pdfmake, with filter, sorting, CSV export and a print layout reached by the PDF button. Four phase 1 items remain open in the plan.
- Checked: per commit `npm run test:data` or `npm run test:frontend`. The RDF suites pass apart from the strict comparison, which differs from the previous commit only at the intended lines, confirmed by a line diff of the affected holdings. The frontend suites pass apart from the known duplicate `miscellaneous.2` of the English news fixture. Snapshot comparisons show only the intended pages. The basket was checked in Chrome at desktop and phone width in both languages and printed to PDF in A4 landscape.

## 2026-10-15 korrigiert test selection boundaries

- Source: operator request to refactor test separation and independent reviews of the runner and documentation.
- Target: [testing](testing.md#rule), [deployment-architecture](deployment-architecture.md#checking-an-instance), the scope selector and pre-push hook.
- Result: the shared language fixture selects both areas, invalid suite names fail before tests, and renamed files retain both source and destination scopes. Other ingest transforms conservatively select both areas but still lack dedicated checks. Release verification now follows the changed area. The Vault project architecture and harness explanation carry the same boundary.
- Checked: `npm run test:scope`, the runner with `--suite unit --no-build`, JavaScript syntax and `git diff --check` pass. The actual pre-push entry point was exercised in a temporary Git repository with a logging substitute for the rendering runner: a cross-scope rename selects both areas, unchanged refs skip rendering, and malformed input fails. No RDF or page build was repeated.

## 2026-10-15 korrigiert test scope

- Source: operator correction that cache and download changes do not affect RDF and must not trigger its builds.
- Target: [testing](testing.md#rule), the npm scripts, the optional pre-push hook and both agent instruction files.
- Result: frontend changes use `test:frontend` (unit, prototypes, pages); RDF generation uses `test:data` (RDF only). The complete `npm test` remains explicit for shared rendering or dependency changes. The hook classifies the paths in the pushed refs, with both areas for unknown code and a fast routing check for documentation or routing-only changes. Source-data curation remains a separate responsibility of the data repository.
- Checked: `npm run test:scope` verifies frontend, RDF, shared, mixed, documentation and unknown path selection plus the npm aliases. A hook invocation with unchanged refs requires no rendering. Script syntax and the diff check pass. No page or RDF rebuild was repeated for this routing-only change.

## 2026-10-15 korrigiert asset caching and image downloads

Found. Fresh HTML combined with the CSS from before the Bootstrap layer migration reproduces the reported broken menu and layout. Production HTML and project assets had no explicit Cache-Control response header when checked. The image ZIP failed independently: the manifest of `o:szd.260` points at raw GAMS datastreams without CORS permission, while the SZD alias serves the same paths directly.

Changed. The shared page shell versions project CSS and JavaScript with one release value; deferred download libraries and timeline JSON inherit it. Tokens also load through an explicit versioned link after the main stylesheet. The existing tokens import remains for cached old page heads. The download loader maps only known production GAMS SZD datastream paths to the current SZD alias, preserving external services and staging URLs. Regression checks cover release links, deferred requests and the download origin boundary. The register golden comparison excludes only independently checked asset release metadata.

Checked before integration with the newer remote state. The focused download and asset-version tests pass. The locally rendered home page displays a working dropdown menu, and the timeline loads its versioned lane data in the browser. A local browser run with the real manifest paths and original images of `o:szd.260` produced a ZIP whose two entries match the source images byte for byte. The local fixture replaces the manifest origin with its loopback proxy; production hostname selection is checked separately by the regression test.

Checked before integration. The complete `npm --prefix local-test-build test` run finished with 21 passed, no failures and no skipped tests, including the register golden and strict RDF comparisons. JavaScript syntax checks and `git diff --check` pass.

Integration. Once VPN access was restored, the remote revealed newer development and release commits. The fix was reapplied to current develop, retaining the disabled timeline and the upstream download and HTML fixes. Its documentation follows the current knowledge structure. Verification of the combined state: the complete harness finished with 20 passed, one failure and one skipped test. The failure is the existing duplicate miscellaneous.2 in the English news fixture, independently reproduced on unchanged 4c0554a; the timeline test is skipped because the view is disabled. The integrated browser checks covered German and English navigation by keyboard at desktop and narrow width, plus a fresh ZIP whose two images again match the original bytes. Edge was not connected and was not tested. Server response headers and deployment verification remain in the [plan](plan.md#cache-and-image-download-deployment), with the cache policy in the [deployment architecture](deployment-architecture.md#asset-releases-and-cache-headers).

## 2026-10-13 integriert audit of the live site and fixes of the presentation layer

- Source: read-only audit of production and staging on 2026-10-13 (references, pages in both languages, links, search, galleries, ingested data, RDF, HTML and accessibility, HTTP), the instance check and the operator's ingests of that day.
- Target: [testing](testing.md), [deployment-architecture](deployment-architecture.md#checking-an-instance), [search-architecture](search-architecture.md#renderer), [plan](plan.md).
- Result: production served the current stylesheets, but parts of the ingested data predated the data repository, five `TORDF` references pointed to the retired host glossa and four objects lacked RDF. The operator set the `TORDF` references and re-ingested indexes, holdings and theme pages; their RDF matched the local build triple by triple except where the ingest was still running. Theme page 8 failed in Cirilo because its title image was referenced with `file:///img/`; the data repository now references the existing datastream (`5a42fa9e`). The code fixes cover links that dropped the locale, jump and footnote anchors without target, language fallbacks of metadata rows and the English works page, the XHTML serialisation of every page instead of self-closed non-void elements, alt texts, the page title, skip link, heading level and language switch of the frame, host-relative figure links, the search renderer (one card per object, a neutral heading without hits, a truncation notice) and the robustness of the data basket and the IIIF download. Two checks were added, `test/page-hygiene.smoke.mjs` and `check-instance.py`.

## 2026-10-09 verdichtet knowledge base and journal

- Source: base `ee8ee90` on `develop`, the last commit before the refactoring, covering all documents under `knowledge/`, `README.md`, `AGENTS.md`, `CLAUDE.md` and the READMEs of `local-test-build/`, `local-test-build/proto/` and `query/`.
- Target: the documents listed in the [index](INDEX.md).
- Result: the documents are reorganised by function. `Architecture.md` became [architecture](architecture.md) and [deployment-architecture](deployment-architecture.md), `Data-Model.md` became [data](data.md) and [rdf-mapping](rdf-mapping.md), `Rendering-and-Search.md` became [rendering-architecture](rendering-architecture.md) and [search-architecture](search-architecture.md), `Facsimiles-Korrespondenzen.md` became [correspondence-gallery-architecture](correspondence-gallery-architecture.md), `Konvolut-Titles.md` became [konvolut-title-curation](konvolut-title-curation.md) and `Testing.md` became [testing](testing.md). The working principles and design decisions of `Frontend-Overhaul.md` and the dated operator decisions scattered over the documents moved into [specification](specification.md), the roles and rights of the README and the agent rules into [governance](governance.md), and the charter into [project](project.md). The finding inventory of 2026-09-11 (keys H, J, C, S, P, K) and the package list of the frontend overhaul, the dated findings log of the correspondence gallery and the session narratives of the former journal are kept only in Git at the base commit. Statements that the code no longer supports were removed, among them the live timeline, the namespaces `dcterms:partOf` and `owl:sameAs` and GeoNames as an anchor of the RDF, which the transformation declares but does not use. The agent instructions now require English commit messages, a dated decision of 2026-10-09 recorded in the [specification](specification.md#documentation), where the former `AGENTS.md` had asked for German ones.

## 2026-10-09 integriert production objects after the release

- Source: operator, readings of the production datastreams on 2026-10-09.
- Target: [plan](plan.md#production), [deployment-architecture](deployment-architecture.md#stylesheet-references).
- Result: `o:szd.organisation` and `o:szd.thema.8` were ingested in production, and the operator updated the five production `QUERY` datastreams from `query/`. The `RDF` datastream of `o:szd.organisation` still answered 404 at 19:20 UTC. Two Cirilo refreshes of `o:szd.thema.8` logged a UTF-8 error and left its `TEI_SOURCE` unchanged. The three index objects that reference include files kept serving the output from before the release, which suggests that GAMS does not notice changes in included stylesheets.

## 2026-10-09 integriert production go-live and release flow

- Source: operator, `6f47a8d`, `f5edb52`.
- Target: [deployment-architecture](deployment-architecture.md#release-flow), [governance](governance.md).
- Result: production went live with the full frontend overhaul. Development runs on `develop`, `main` carries the published state, the GAMS updater fast-forwards the production checkout to `main`, and the gamsdev mirror follows `develop`. A release merges `develop` into `main`, and `main` is never rewritten.

## 2026-10-09 integriert timeline switched off

- Source: `5baf289`, `0dbcef3`.
- Target: [specification](specification.md#lebenskalender), [rendering-architecture](rendering-architecture.md#lebenskalender).
- Result: the menu links the biography without the timeline, and the variable `timelineView` in `szd-static.xsl` makes every mode render the vertical view. The timeline smoke test counts as skipped while the switch is off.

## 2026-10-09 integriert findings of the live check

- Source: `ee8ee90`.
- Target: [rendering-architecture](rendering-architecture.md), [search-architecture](search-architecture.md#renderer).
- Result: news images load host-relatively, the jump bar links groups outside the alphabet such as work titles beginning with a digit, the work search names its type in the header, the English biography label of the search is set by locale, and the footer link to Salzburg is corrected. The plan item on digit groups without jump link is closed.

## 2026-09-30 integriert theme page 8

- Source: `2ea2145`, `329ad7c`.
- Target: [rdf-mapping](rdf-mapping.md#theme-pages), [search-architecture](search-architecture.md#query-objects), [plan](plan.md#production).
- Result: the menu links `o:szd.thema.8` first, and person and full-text search read its graph. The page header shows the `TITELBILD` datastream only where a theme page declares one, plus `o:szd.thema.1`, every other theme page shows its title in the page language. The RDF takes only the first header title as `szd:title`. Figures load host-relatively, and whitespace that Cirilo indents into titles at ingest is dropped.

## 2026-09-29 integriert test net (refactoring phase 0)

- Source: `cee7391` to `baa1046`, `aeeedec`, `9325258`.
- Target: [testing](testing.md), [local-test-build/README.md](../local-test-build/README.md).
- Result: the snapshot driver renders every page type of a commit or of the working tree and compares byte for byte, fixtures hold only GAMS inputs, the index golden test renders from `HEAD`, the stub imports the real library, the RDF build gained a strict mode, a triple diff and a read-only staging comparison, `npm test` runs every suite, and a pre-push hook can run it. `gams-objects.toml` records the expected Cirilo references for a read-only check. The checks of that day found the snapshot of `HEAD` reproducible and the staging RDF of library, correspondence and personal documents without the corporate bodies of the organisation fallback. SaxonJS 2.7 rejects the gallery's `xsl:for-each-group` with two sort keys calling `current-grouping-key()` (XTDE1071), which the Saxon of GAMS renders, so the harness joins the keys in its copy. The report of 2026-09-28 that the page tests passed held only against stale fixtures.

## 2026-09-29 integriert data repository clean-up (refactoring phase 4)

- Source: data repository commits `493ee5fa`, `a0512b1b`, `f78b8b2f`, `deb763d1`, `25857564`, `2198922e`, `f6ff1bb0`, `d716d5bd`, `e44e641f`.
- Target: [plan](plan.md#phase-4-data-repository), data repository.
- Result: the scripts use shared TEI, GND and Git helpers from `_szd_io.py`, `check_data.py` checks the data read-only before every staging package, script output is written as UTF-8, the name search of unlinked persons normalises to NFC, double-encoded umlauts in Konvolut text nodes are repaired, multi-valued `@ref` separate with blanks, empty `date/@when` attributes are removed, and the staging package is built from `HEAD` and collects staging errors. NFC normalisation of the sources and the century corrections stay operator questions.

## 2026-09-29, script repairs and a data check before staging

Changed. The script part of the refactoring plan of the presentation layer (phase 4) is done in `scripts/`, one commit per repair. `list_unlinked_persons.py` no longer stops when `--csv` points outside the repository, and `unlinked_persons.csv` is regenerated without the persons removed on 2026-09-24. `find_unlinked_persons.py` normalises names and text to NFC before it splits them into words, because the person index writes names such as that of `SZDPER.21` decomposed and the word index never found them. Twelve scripts wrote their console output in the ANSI code page and lost umlauts in a pipe, and `console_utf8()` in `_szd_io.py` now sets stdout and stderr to UTF-8. The staging package reads its files from `HEAD`, names uncommitted changes under `data/`, refuses an `--out` inside the repository and lists staging answers other than a redirect, 400 or 404 as errors with exit code 1, where it used to count them as new objects. `fix_titles.py`, `add_bundle_signatures.py` and `fix_classification.py` append every applied change to a CSV log beside them, and `fix_classification.py` checks well-formedness before it writes. The newer scripts take namespaces, `text_of`, `head_revision` and `gnd_ids` from `_szd_io.py`, while the finished checkup scripts keep their copies as provenance.

Changed. `scripts/check_data.py` checks every TEI file under `data/` read-only and returns an exit code. The open findings of the decided checks are frozen in the script as known exceptions, each group with the place in the [plan](plan.md) where its question stands, so that only a new finding fails. `build_staging_package.py` runs it over the `HEAD` files before it writes and stops on a file that is not well formed or on a new finding. Tests cover the century rule of `fix_titles.py` on `SZDKOR.freud-sigmund.5` and `SZDKOR.heidelbach-paul.B.1` at a fixed data commit, the group order and PID rule of the package, the reading of staging answers and the corpus state of the check.

Decided. NFC, correspondence dates after 1950 and whitespace in `@ref` only warn in `check_data.py`, because the operator has not decided them. `fix_titles.py --apply` was not run. The deterministic data corrections of the same day ran in a separate session under `scripts/datenkorrektur_2026_09_29/`.

Open. The check found a date that does not exist, two GND numbers on one index person, a name in `@ref`, an eleven-digit GND number and `@ref` values with leading whitespace, all in the [plan](plan.md). The NFC question, the tooling of the repository and the unexplained red `--verify` of `fix_konvolut_defects.py` are there too.

## 2026-09-29 integriert refactoring plan and letter edition

- Source: operator decisions, `6fbb1fb`, `05c97d9`.
- Target: [plan](plan.md#refactoring), [specification](specification.md#refactoring-settings-operator-decision-of-2026-09-29).
- Result: the refactoring plan in four phases with seven settings, and the letter edition stays a prototype.

## 2026-09-28 integriert index filing after DIN 5007-1

- Source: operator decision, `d6e5e1d`, `933b075`.
- Target: [specification](specification.md#indexes-and-sorting), [rendering-architecture](rendering-architecture.md#indexes).
- Result: `fn:filing-key` and `fn:filing-letter` carry the rule for indexes, jump bars, anchors, gallery title groups and the Aufsatzablage register. The index sort had depended on the processor before, a language collation in SaxonJS and, inferred from the processor defaults, codepoint order on GAMS. Full-page builds of the indexes before and after showed the same entries in filing order with every jump link resolving.

## 2026-09-24, staging ingest of the data package

Checked. The operator ingested the whole package on staging, and Cirilo created the Konvolute missing there. Indexes and Konvolute on staging match the repository in content, the person index without the removed persons and the organisation index with places and "Großbritannien". The RDF of the holdings still lacks the corporate bodies, because they went in before the organisation fallback of `szd-TORDF.xsl` reached the mirror, and many objects carry `TORDF` references that end in an illegal character. The package README now lists the references per object, treats the include stylesheets of the registers as valid and leaves the Cirilo log in the package folder alone when the package is rebuilt (`faeda672`). The renewed ingest is in the [plan](plan.md#staging-ingest).

## 2026-09-24, timeline lanes on the complete Konvolute

Changed. `build_lanes.py` ran on the complete Konvolute, and the corpus tests pin the new state with values read from the run. Correspondence events from the index carry three new fields, `konvolut` with the detail page of the named Konvolut where its file exists, `repository` for bundles held outside the Literaturarchiv Salzburg and `extent` with the pieces per direction ([lebenskalender-lanes](lebenskalender-lanes.md#event-schema)). `extent` is a list, because some bundles carry a measure for letters sent and one for letters received. Event ids are unique across all lanes, because several Konvolut files reuse the `xml:id` values of another Konvolut and the view uses ids as DOM ids and fragments. Such an id carries the file slug after a tilde in every occurrence, unique ids stay unchanged. The `href` of a Konvolut record takes its PID from the file name, so the defective Jugendverein and Rascher objects link to the objects GAMS holds. The lane files went to `docs/lebenskalender/lanes/` and to `ZIMLAB/szd/data/lebenskalender/`.

Open. The conflicting facsimile groups, the Konvolut files with shared ids, the two index entries whose Konvolut PID has no file and the Konvolut dates after 1950 are in the [plan](plan.md#timeline-lanes).

## 2026-09-24, complete Konvolute, person index clean-up, staging package

Changed.

- Every correspondence Konvolut of GAMS production is in `data/Correspondence/konvolute/` (`e1b156fa`), taken over byte for byte from `TEI_SOURCE` by `scripts/konvolute_import/fetch_konvolute.py`, and the three new Konvolute of the staging package of 2026-09-23 from that package. Before, the repository held only the Konvolute edited here. Three defective production objects are recorded in the import README.
- 41 corrections of the Konvolut files that the archive checkup reported and that the verification notes or the facsimile objects on GAMS prove (`2d085b98`, `scripts/checkup_2026_09_konvolute/`), among them wrong and missing facsimile PIDs, the `correspDesc/@type` of the Freud letters, title dates and a duplicate entry in the Hirschfeld Konvolut. Cases without an established value stay unchanged.
- Person index. `verify_orphan_persons.py` (`81a56e58`) takes the persons without text hit from `find_unlinked_persons.py` and checks identifier, GND and the person search on production and staging. `remove_orphan_persons.py` (`f2bb270c`) removed the 230 persons that pass every check. The removed entries stay unchanged in `scripts/checkup_2026_09_index/removed_persons.xml`, and their identifiers are never assigned again.
- Organisation index with country and place from the GND (`82da76ee`, entry below). Afterwards "England" became "Großbritannien" in the organisation and the location index (`c63379f6`), because the country switch of the index pages showed two groups for one country, and the script writes "Großbritannien" for `XA-GB` throughout.
- `scripts/staging_package/build_staging_package.py` (`0b1328e7`) writes the staging ingest package outside the repository, in the order indexes, holdings, Konvolute, with checksums and the `STYLESHEET` and `TORDF` references each object still needs, read live from staging. A Konvolut whose file does not name its own PID stays out.
- SZDO 2.0.0 with English identifiers (`8f54aeed`, entry below).
- Documentation refactored after the model of the frontend knowledge base. `knowledge/README.md` became the [index](INDEX.md) with a glossary, the [plan](plan.md) and the [handoff](handoff.md) inbox are new, the journal is English throughout, the open lists of DATA.md and of the journal moved into the plan, and CLAUDE.md became a compact rules file. `reconcile_org_places.py` and its test moved into `scripts/organisationen_index/`.

Found. The import brought back the sister Konvolute decided for deletion on 2026-09-22 and 2026-09-23, and several imported Konvolute carry dates after 1950. Four corpus tests of the timeline lanes pin the corpus before the import and fail since `e1b156fa`. All three are in the plan.

Presentation layer. `szd-TORDF.xsl` read the autograph classification with the absolute path `//t:textClass` and is being fixed in `ZIMLAB/szd` the same day. `o:szd.autographen` needs a renewed ingest afterwards.

## 2026-09-24, SZDO 2.0.0 with English identifiers

Changed. The ontology uses English identifiers only, as the operator decided on
2026-09-23 and 2026-09-24. `szdo:` moves to 2.0.0 and `nachlass:` to 0.2.0. Wherever the
GAMS vocabulary of `szd-TORDF.xsl` already has an English term with the same meaning,
that term is canonical, so live GAMS data conforms unchanged. Shapes, sample instances,
Klawiter links, the documentation site and both generating scripts use the new names.
`ontology/migration-v2.csv` maps every retired identifier to its successor.

Decided. The German v1.2.0 identifiers are dropped without deprecated aliases, because
aliases would keep German identifiers in the ontology and no live data uses v1.x. The
missing shelfmark on a record became a SHACL warning, since privately held books have
inventory numbers only.

Found and fixed. Sample instances and Klawiter links wrote entry IRIs as prefixed names
with `#`, which Turtle reads as a comment, so every entry collapsed onto its collection
node and the instance shapes never fired. Both scripts now write full IRIs, the instance
generator reads the untyped shelfmark of SZDBIB and the GND-referenced correspondents of
SZDKOR, and `validate.py` now validates the sample instances with SHACL and fails on any
retired identifier. `reconciliation.ttl` was regenerated from the stored results, which
also applies the script's `isSubjectOf` for secondary literature.

Open. `szd:glossar`, the hybrid `szd:objecttyp` and the glossary concepts of
`szdg:DatumEvidenz` keep German-derived identifiers, because they belong to the live GAMS
vocabulary and glossary. The namespace `https://w3id.org/nachlass#` keeps its name.

## 2026-09-24, country and place in the organisation index from the GND

Changed. `scripts/reconcile_org_places.py` adds `<country>` and `<settlement>` to `SZDORG.xml` from the GND record of each corporate body, `placeOfBusiness` for the place and `geographicAreaCode` for the country, never estimated and never combined across levels. 42 values were added, both fields for 16 of the 32 entries that had been incomplete since the migration from the person index, and the country alone for 10 more, because their GND record names no place. For the GND code `XA-GB` the script followed the split already present in the data, "England" where a city is known and "Großbritannien" otherwise (SZDORG.32/49 against SZDSTA.15), a setting the script derived from the data. Five entries give no geographic code in their GND record, three have no GND reference at all, and for Herbert Reichner Verlag (SZDORG.24) country and place stay open, because the record lists Wien, Zürich and Leipzig with equal rank. The log `scripts/organisationen_index/reconcile_places_log.csv` records only values actually written, and `scripts/test_reconcile_org_places.py` accompanies the script.

Checked. The known contradiction at SZDORG.15 (David H. Lowenherz, the GND points to London, the data carry USA/New York) is unchanged and was not overwritten. No further contradiction between data and GND turned up among the entries that already carried country and place. Well-formedness, an unchanged number of `<org>` entries, a purely additive diff and a second run without effect are checked, as are `pytest scripts/test_reconcile_org_places.py` and `ruff check`.

Open. The organisation index must be ingested again after the change. 16 entries stay without place, six of them without country or place, because their GND record gives nothing or stays ambiguous.

## 2026-09-24 korrigiert person relations of the autographs

- Source: `6a13df9`, the earlier statement in the RDF findings list.
- Target: [rdf-mapping](rdf-mapping.md#mapping-from-tei), [testing](testing.md).
- Result: `RDF_autograph` grouped person terms over the absolute path `//t:textClass` and related every autograph to the persons of all entries, and a leftover `xsl:value-of` wrote their names as text into the RDF. The fault dates from 2024 and became visible when the data normalisation of September put index references on the terms. The path is now relative to the entry, and the golden test allows exactly this removal against the baseline `faa784a`.

## 2026-09-24 integriert organisation index fallback

- Source: staging ingest of `o:szd.bibliothek`, `c537c05`.
- Target: [rdf-mapping](rdf-mapping.md#index-hosts), [testing](testing.md).
- Result: the organisation index is read from the first of derived host, production and staging that serves it, checked by `npm run test:rdf-fallback`.

## 2026-09-24 integriert timeline lanes from every Konvolut

- Source: `0465b95`, generator of the data repository.
- Target: [data](data.md#timeline-lane-files).
- Result: an entry of the correspondence index names sender and recipient as search links, the repository of holdings outside Salzburg and a link to its Konvolut.

## 2026-09-24 integriert decisions on staging data

- Source: operator decisions.
- Target: data repository.
- Result: the entries of "Aktuelles" are not ingested on staging, persons of the index without any reference were removed in the data repository after a deterministic check, and England and Großbritannien are unified to Großbritannien in both indexes. No datastream of `context:szd` on production or staging referenced a file removed in `ec8cc3d` or `bb663e1` (read on 2026-09-24).

## 2026-09-23 to 2026-09-24 integriert search, indexes and frontend clean-up

- Source: `07ba5d4`, `e668732`, `8e52646`, `e7acd7d`, `15b7f26`, `f70882d`, `ec8cc3d`, `bb663e1`, `f5c10f4`, `2f116c0`, operator decisions of 2026-09-23 and 2026-09-24.
- Target: [rdf-mapping](rdf-mapping.md), [search-architecture](search-architecture.md), [rendering-architecture](rendering-architecture.md), [specification](specification.md#decisions).
- Result: theme pages are found by person and full-text search and appear as a block "Themen". `szd-TORDF.xsl` and `szd-Suche.xsl` were refactored without change in output and their unfixed findings recorded. All five query templates are in the repository. Indexes, view switch and jump bar are unified, every token of a multi-valued `@ref` and every GND in `https` resolves, dead files and code are removed, tabs carry only `aria-selected`, and the Bootstrap bundle with Popper 1 replaces the vendored Popper 2, which had kept the glossary dropdowns closed. The documentation became English. The checks compared full pages and RDF byte for byte before and after the refactorings and computed styles at 390 and 1440 pixels after the CSS removals. Persons, repositories, organisations and theme pages were re-ingested on staging, and the person search found the theme pages there.

## 2026-09-23, review list of unlinked persons, staging package, knowledge documents

Changed. `scripts/checkup_2026_09_index/find_unlinked_persons.py` (`10728679`) lists the index persons the person search does not find because no object references them, and searches the element text of the holdings for places that name them without a reference, on request also in the Konvolute of the staging package not yet ingested. The output is an archive-internal review list under `Documents/PROJECTS/szd/checkup-2026-09/` outside the repository.

The staging package under `Documents/PROJECTS/szd/ingest_staging_2026-09-23/` stands at `aac08670`. Since the merges of the day it again contains the person index and in addition the Konvolute of the newly linked correspondence partners. The Masereel theme page is now on staging, and its `TEI_SOURCE` there carries the tagged person references.

Integrated. The knowledge documents are brought to this state and deduplicated, with `10728679` as predecessor. The organisation index is described in [collections.md](collections.md) instead of DATA.md, and delivery state and coverage of the Lebenskalender lanes stand only in [lebenskalender-lanes.md](lebenskalender-lanes.md). [data-quality.md](data-quality.md) carries the counting conventions, the findings of the day and the collected open points instead of the collection statistics. Examples in COLLECTIONS and DATA_MODEL now come from the data, and invented signatures and date forms are replaced. ARCHITECTURE describes the two-repository topography instead of general platform details. The licence statement in PROJECT follows the README (code MIT), and the Zenodo link points to the public record. Outside the journal no document names the first editions as a collection any more. At the operator's request the knowledge documents and script READMEs that had been German were translated into English, as CLAUDE.md provides, while the journal stayed German.

Presentation layer. The organisation page links every corporate body, repositories to the location search and the others to the person search, and shows place and country in the heading line (`ZIMLAB/szd` `e7acd7d`).

Open. The RDF transformation in `ZIMLAB/szd` is being adapted for several identifiers in one `@ref` and for GND references with `https`. Until then `GetPersonlist` reads only the first token, and a corporate-body reference resolves only if it matches the index character for character. ONTOLOGY.md and `ontology/README.md` are revised in a separate session with English identifiers, and there the organisation index is still missing from the mapping of the TEI files. The root document `mail.md`, a mail text on the SZ-AAL/B correspondence from July 2026, has no function in the repository.

## 2026-09-23, dead person references and unlinked correspondence partners

Changed. In `SZDAUT.xml` four author references carried, beside the valid identifier, a second one that `c1a9a34e` had removed from the index as a GND duplicate in 2022, namely Michelangelo twice (1579 beside 194), Joachim Murat (1623 beside 1009) and Gounod (1617 beside 1588). The dead identifiers are deleted. From the candidate list of unlinked persons only the unambiguous cases are linked, meaning a `persName` without reference whose surname and forename equal the index entry exactly while no other entry carries the same name. This applies to the correspondence partners Kahn, Mayer, Süssland, Birman, Monath, Sambat and Garcés, each in the collective line of `SZDKOR.xml` and in their own Konvolut, plus pieces in `altmann-eva` and `zweig-lotte`. The persons without reference thereby go down from 354 to 347. Birman and Sambat stand in index and holdings with an initial only, and their entries are the only ones of that surname.

Open. Neydisser (`SZDPER.1026`) has been only a name variant of Lernet-Holenia (`SZDPER.818`) since `a108c6f3` of April 2025, but the library names the pseudonym's own GND. `SZDPER.1304` never existed, and what is meant is the Selbsthilfevereinigung der jüdischen Blinden in Deutschland, a corporate body without an entry in the organisation index. Seven correspondence partners carry a GND in `SZDKOR.xml` that their index entry lacks. Also with the operator are divergent forenames (Altmann, Miller, Bischoff), mentions in titles and running text, and Kuro Masu and Králík, whose envelope already points to another entry. The check script does not recognise identifiers with a letter suffix such as `SZDPER.2080a` as references.

## 2026-09-23, colour coding of the person index list evaluated

Changed. The colour coding of the archive list for the person index is read from the Word original, because it was lost in the text export. What follows unambiguously from the data is carried out. Kesten and Pilnjak are each merged into the entry with the valid GND after a check with the DNB (`merge_person_duplicates.py`, log extended), because 1185617155 does not exist and 1089928157 redirects to 118594397. The non-existent Kesten GND in `SZDKOR.xml` is replaced by 118561715. The persons Frenkel, Kaufmann and Tomaselli, marked yellow by the archive as wrongly unlinked, now point to their index entry in the Konvolute `frenkel-lotte`, `kaufmann-charlotte` and `zweig-lotte` and in `SZDKOR.xml`. Kaufmann appears in the data as Charlotte and in the index as Lotte, and the identification follows the archive's marking.

"Britain in Pictures", marked green by the archive as a corporate body, is added by hand to the organisation index as `SZDORG.67` and removed from the person index by `migrate_org_references.py`. The numbering continues instead of restarting, because the identifiers are part of the RDF URIs. Because the script rewrote its migration log, the older rows are put back in front from the Git history.

The knowledge documents are updated. [data-quality.md](data-quality.md) carries the colour coding as a source, the results and the open points in the section on the archive checkup, and the statements on organisation and person index in COLLECTIONS, PROJECT, README and the README of the organisation script are brought up to date. The organisation section in DATA.md still described `GetOrglist` as never called, which frontend commit `ef9a4ce` had made obsolete.

Open. Neumann, writer or architect, remains a question for the archive. With the operator are the entries "Filed as …", "Unidentified signatures" and "Zweig Family", the names marked bold and the question whether the unlinked names the archive wants removed leave the person index. `SZDKOR.xml` carries further person references with the placeholder `gnd/placeholder`. `SZDSTA.xml` has had no `geo` data since the data update of June 2021 (`1ed133c2`), so the new RDF of the locations has no coordinates. `ontology/reconciliation.ttl` for Klawiter rests on title matching with percentage values.

Open and planned as the next step, at the operator's suggestion, is a reconciliation script of its own. It adds Wikidata identifiers through the GND, meaning Wikidata P227, and writes only unambiguous hits automatically. It checks the existing GNDs at DNB or lobid for existence and redirects and reports contradictions to Wikidata. Entries without GND receive only a suggestion list, written hits carry their provenance, and places follow later. As of that day 521 persons have a GND but no Wikidata identifier, 220 persons have no GND, and none of the 67 corporate bodies carries a Wikidata identifier. For corporate bodies `szd-TORDF.xsl` also still lacks the output of `szd:wikidata`.

## 2026-09-23, first editions removed, staging ingest prepared

Decided. The operator abandoned the first editions (SZDPUB). Both versions, `data/Publication/SZDPUB.xml` and `data/Index/Erstveröffentlichungen/SZDPUB.xml`, are removed and remain in the Git history. They carried the same PID `o:szd.publikation`, differed in content and named no source. The object never existed in production, and the RDF transformation had no branch for it. The references in COLLECTIONS, DATA, ONTOLOGY and PROJECT are deleted. The total row of the collection statistics in DATA.md and the description of DATA.md in the README still contained SZDPUB and were corrected the same day.

Changed. The element-level comparison between this repository and `TEI_SOURCE` on staging gave the objects for the next staging ingest, the six holdings, the organisation index, three Konvolute and three new Konvolute from the source folder outside the repository. The package with checksums lies outside the repository under `Documents/PROJECTS/szd/ingest_staging_2026-09-23/`. Persons, locations, work index, Lebenskalender and the other Konvolute match staging.

Open. On staging `o:szd.publikation` can be deleted, and so can the orphaned `o:szd.korrespondenzen.ferencak-mirko-m`, whose only piece the new Konvolut `ferencak-mirko` carries more completely. The tagged Masereel theme page is not yet ingested on staging.

## 2026-09-22, duplicate pairs of the checkup decided

Decided. On 22 September 2026 the main agent instance decided the four open duplicate pairs of the checkup after delegation by the operator, revisably. For SZ-SHB/W3 `o:szd.359` stays and the byte-identical `o:szd.375` is deleted. For SZ-AP2/W-H206 `o:szd.2939` stays as the object in the newer cataloguing standard, and `o:szd.263` becomes dispensable once its signature and date are taken over. For Berger and Oppeln-Bronikowski the Konvolut identifier with `-von`, to which the index points, stays in each case and takes up the curated content of the sister identifier.

Changed. In the work index SZDMSK.299 points to `o:szd.359` instead of "Amerigo" `o:szd.358`, and SZDMSK.201 to `o:szd.2939`. The merged Konvolute lie, as with Ferenčak, in the source folder outside the repository, with direction `fromZweig`, titles after the title convention and, for Berger, signature SZ-SEF/B1 and facsimile `o:szd.1384`. Index and gallery anchors already point to the remaining identifiers.

Open. On GAMS the ingest of both Konvolute and of the work index, the deletion of `o:szd.375`, `o:szd.263` and of both sister Konvolute, and signature and date in `o:szd.2939` are pending. The sheet of SZ-AP2/W-H206 also lies as the first two images in `o:szd.220`.

## 2026-09-18 to 2026-09-20 integriert shared index stylesheet and organisations

- Source: `ef9a4ce`.
- Target: [rendering-architecture](rendering-architecture.md#indexes), [rdf-mapping](rdf-mapping.md#organisations).
- Result: `szd-Index.xsl` renders the four indexes with the former files as includes, the RDF writes `szd:Organisation` and resolves corporate-body references, and four query templates read `o:szd.organisation`. The work of 2026-09-18 was committed as one unit on 2026-09-20.

## 2026-09-18, superseded person identifiers, checkup notes moved out

Changed. The sixteen back-references of the organisation index to former entries of the person index carry `subtype="superseded"`, so that they can be told apart from the live cross-references `idno type="SZDSTA"`. `build_org_index.py` writes this form, and the README of the script folder explains it. The RDF transformation of the presentation layer outputs `dcterms:replaces` from it, pointing to the old person resource.

Decided. The archive-internal verification notes of the checkup of September 2026 lie under `Documents/PROJECTS/szd/checkup-2026-09/` outside the repository, and the pattern `reports/checkup-*/` is ignored. The durable result stands in [data-quality.md](data-quality.md) in the section on the archive checkup.

Checked. Person, location, work and organisation index were ingested on GAMS staging the same day. No holding points to a superseded person identifier any more, and the migration log of the organisation index matches the targets that the RDF harness of the presentation layer resolves for the library.

Open. The organisation index must be ingested again after the change. Most corporate bodies lack country and place, because they come from the person index. Proposed and not begun are a GND-to-Wikidata reconciliation for persons with a GND and without a Wikidata identifier, and a place list with GeoNames identifiers as a first step towards a places index, with the autographs as the starting holding. `data/derived/lebenskalender/` is untracked although the lanes contract provides the files there, and the delivered copy under `docs/lebenskalender/lanes/` has the same content.

## 2026-09-17 integriert findings of the archive check-up

- Source: `8ec067b`.
- Target: [rendering-architecture](rendering-architecture.md), [rdf-mapping](rdf-mapping.md#mapping-from-tei).
- Result: `printAuthor` handles partners that are organisations, the Konvolut page sorts undated pieces last, the extent row prints both measures, `term[@type='person_affected']` maps to `szd:affectedPerson`, and the person query matches the deployed datastream again.

## 2026-09-11 integriert frontend overhaul and timeline

- Source: inventory of 2026-09-11, decisions of 2026-09-11, `b616496`, `06382eb`, `3cb6596`, `c23f0c5`.
- Target: [specification](specification.md#frontend-principles), [rendering-architecture](rendering-architecture.md).
- Result: six packages covering usability, loading, CSS consolidation, entry and header structure, visible details and maintainability, the integrated timeline, the asset path derived from the stylesheet location and switches in the sticky header. The metadata rendering of the fixtures was byte-identical before and after the template extraction in both languages. The release reached staging, and a staging link of the timeline went to the project partners as information without approval.

## 2026-09-10 korrigiert recovery of the local clone from ZimLab and Konvolut mode

- Source: recovery of the local clone from ZimLab (state of 2026-06-16), `67fd924`, `a260ff4`.
- Target: [correspondence-gallery-architecture](correspondence-gallery-architecture.md).
- Result: the clone was restored from ZimLab, and the Konvolut mode, its knowledge document, its smoke test and the prototypes were written back from the session. An unpushed commit of 2026-06-19 and some June edits of the documentation were lost for good. The Konvolut mode groups by B shelfmark, the gallery gained IIIF thumbnails, collapsing of large groups and the list view switch, and the Konvolut title sheet was regenerated from the gallery data.
