---
title: Testing
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD  # the served files it describes are in https://zimlab.uni-graz.at/gams/projects/szd/gams-www
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: complete
language: en
created: 2026-09-20
updated: 2026-10-28
authors: [Christopher Pollin]
generated-with: Claude Code (Claude Opus 5.5)
related: [architecture, deployment-architecture, rdf-mapping, specification]
---

# Testing

The test contract of the presentation layer states why checks run locally, what the harness covers, what only staging can check and which rule applies before a push. Operating the harness, its commands per page type and the single tests are described in [local-test-build/README.md](../local-test-build/README.md).

## Why checks run locally

GAMS runs the transformations of gams-www on the server, the HTML of a page when it is called and the RDF of an object at ingest. An error in a page stylesheet therefore becomes visible only on staging, after push and synchronisation of the gamsdev mirror, and an error in `szd-TORDF.xsl` only after the next ingest, which only the operator triggers. Staging is moreover a shared instance. The harness brings the transformations onto the local machine and runs them against real data with SaxonJS, which executes XSLT 2.0 and 3.0.

## Building blocks

Four building blocks live under [local-test-build/](../local-test-build/README.md) of this repository.

- The full-page build (`build-full.mjs`) renders a page stylesheet with page shell and template library against a file of the data repository or a versioned GAMS input, with the index data of the data repository and the assets of gams-www. It is the preview closest to the staging rendering. Its materialisation (`harness.mjs`), shared by every page build, redirects each `document()` call against GAMS to a local file.
- The snapshot driver (`snapshot.mjs`) renders every page type listed in `snapshot.manifest.json` in both languages, from the stylesheets of a chosen commit or of the working tree, and compares two snapshots byte for byte.
- The RDF build (`build-rdf.mjs`) runs `szd-TORDF.xsl` against TEI files of the data repository, redirects every index URL to the local indexes and aborts when a network call remains. `--rev` takes the stylesheet from a commit of gams-www and so produces a baseline, and every commit named for a baseline in this document is a gams-www commit, `--unavailable` lets a host lack an index object, as a GAMS instance does before that object is ingested there.
- The smaller page build (`run.sh`) replaces only the entry point of the page shell through `stub-lib.xsl`, which imports the real shell and template library, for a quick look in the browser.

The tests under `local-test-build/test/` run with jsdom against the built HTML, or with text comparison and rdflib against the RDF.

| Script | Subject |
|---|---|
| `npm run test:frontend` | unit, prototype and page suites after building the page snapshot; no RDF build |
| `npm run test:data` | RDF suites and their builds; no page snapshot |
| `npm test` | explicit complete check of both areas, excluding live instance comparisons |
| `npm run test:scope` | fast check of test selection and npm aliases; no rendering |
| `npm run test:unit` | data basket |
| `npm run test:ui` | navigation, language switch, IIIF download with simulated responses |
| `npm run test:lists` | autographs, library, work index in both languages |
| `npm run test:register` | the four indexes on `szd-Index.xsl`, smoke and golden against a snapshot of `HEAD` |
| `npm run test:rdf` | RDF ingest, golden against the baseline and smoke per holding |
| `npm run test:rdf-strict` | RDF byte-identical to the stylesheet of `HEAD`, for refactorings |
| `npm run test:rdf-fallback` | RDF of correspondence and library unchanged while production lacks the organisation index |
| `npm run test:rdf-thema` | every person a theme page marks with `name/@ref` on `SZDPER` stands as `szd:connectedWithPerson` |
| `npm run test:rdf-staging` | triples of the local RDF against the `RDF` datastreams on staging, read-only and outside `npm test` |
| `npm run test:pages` | gallery, Konvolut mode, list switch, stack links, Konvolut dates, the timeline, whose test counts as skipped while the timeline is switched off, and the full-text result page with an organisation hit |
| `npm run test:hygiene` | every snapshot page: page links without locale, dead jump links, duplicate ids, self-closed non-void elements, placeholder alt texts, empty metadata values, retired hosts, entries missing in one language; part of `npm test` |
| `npm run check:production`, `npm run check:staging` | the Cirilo settings of an instance against `gams-objects.toml` and the `TEI_SOURCE` of every object against the data repository, read-only and outside `npm test` |
| `npm run test:proto` | the prototypes under `proto/` |

The optional pre-push hook selects frontend, RDF or both from the paths in the pushed refs, see the [harness README](../local-test-build/README.md#pre-push-hook).

## Fixtures

Fixtures are real data. Index files, holdings, glossary, theme pages and Konvolute come unchanged from the data repository. The few inputs that only GAMS holds, the `METADATA` results of the context objects, the language catalogue, the static datastreams of `context:szd`, the TEI of the letter edition and a search hit list, are versioned under `local-test-build/fixtures/` with their source URL in the manifest. Versioned test data are thus the data repository commit and these GAMS inputs, never rendered pages. A snapshot records the commit of the data repository and the hash of every input, and a comparison notes when two snapshots were built from different data.

The build places the input as `<page>.input.xml` next to the output, so a test reads its expectations from the file the page was built from. Expected values are derived from the source, for instance the number of entries from the `xml:id` values of the TEI or the targets of a reference resolution from the migration log of the organisation index, and never copied from the HTML. A file that is too large is cut down to real entries, and the test states the selection.

## Kinds of checks

Smoke tests check structure and operation of a built page, unique `id` values, existing jump targets, focusable switches and links, `dt`/`dd` pairs and both languages, and for pages with scripts the behaviour with the real JavaScript from `js/`, for instance switching and switching back with a preserved DOM.

Golden tests compare an output with the output of a named commit, rendered anew from the same data instead of stored. They demand byte identity where nothing should change and name the intended deviations where a change is meant to be visible. The index golden test renders the four indexes from `HEAD` and reports for a differing page the entries that disappeared, appeared or moved. For RDF, unaffected holdings stay byte-identical, and affected holdings may only gain lines of the expected form. The tolerant RDF golden test allows only added reference lines to a person or organisation against the baseline `faa784a`, plus the named corrections of refactoring phase 1, each of which pairs a removed baseline line with the line that replaces it, the strict mode demands byte identity with the stylesheet of `HEAD`, and the triple diff compares two outputs against a named list of expected added and removed triples.

Structural checks of the RDF make sure that every output is well-formed and parses as RDF/XML, that every `rdf:about` stays unique apart from known old cases, that no empty resource and no link to a superseded identifier arises and that the number of error comments of the stylesheet does not grow.

## Refactoring without change in behaviour

A structure-preserving refactoring counts as checked only when the output before and after matches byte for byte.

- For pages, the snapshot of the commit before the refactoring is compared with the snapshot of the working tree, `node snapshot.mjs --rev HEAD --compare worktree`.
- For the RDF transformation, the data files are built with `--rev` on the state before and with the working state and compared file by file, which `npm run test:rdf-strict` does for the golden set.
- For the search page no local query run exists, so real hit lists serve as fixtures. `sdef:Query/getXML` returns the unrendered SPARQL result of a search with the same parameters as the search link, the search page is rendered from it with both stylesheet states and compared, and one such hit list is a manifest entry of the snapshot.

A build directory whose path contains `--` breaks the build, because the path ends up in XML comments where `--` is not allowed. `SZD_TEST_BUILD_DIR` therefore points to a path without a double hyphen.

## What only staging checks

The Cocoon translation catalogue lies on the server, so the `i18n:text` keys stay visible in the local preview. The server-side modification date, the stylesheet references, the context membership of the facsimile objects, the `QUERY` datastreams and the `TORDF` references exist only in GAMS. The references, the queries, the presence of the `RDF` datastreams and the currency of the ingested TEI are read by `check-instance.py` from the datastream URLs listed in [deployment-architecture](deployment-architecture.md#checking-an-instance), the context membership still by hand. Which index host an ingest reaches is shown only by an ingest, see [rdf-mapping](rdf-mapping.md#index-hosts). An ingest uses the `szd-TORDF.xsl` that lies in the gamsdev mirror at that moment, so an object ingested before push and synchronisation carries the old RDF and must be ingested again.

## Rule

Every change to a page stylesheet, to JavaScript or to `szd-TORDF.xsl` runs through the harness before the push.

- A change to CSS, JavaScript or page XSLT runs `npm run test:frontend`. It does not rebuild RDF. A change meant to be invisible also needs a snapshot comparison with the commit before it.
- A change to the RDF transformation runs `npm run test:data`, which builds and checks the RDF without rendering the pages. Preserve a baseline with `--rev` before the change; intended RDF differences must be stated explicitly.
- Shared rendering infrastructure, the language fixture used by both builds, or dependency changes require both areas (`npm test`). Changes confined to test routing are checked with `npm run test:scope`; they do not require unchanged rendering pipelines to be rebuilt.
- Documentation-only changes need no rendering test. The data gate checks the RDF generation of gams-www, not every kind of TEI curation. Source-data validation stays with the scripts of the data repository, among them `scripts/check_data.py`.

Existing tests stay green, and the commit message records the test run. Staging is not reachable for development since 2026-10-13, and a push to `main` publishes. The last look before a release is therefore the local build in a browser, in both languages, with the keyboard and at narrow width. After a frontend release, check the changed pages, asset versions, menu and image download in the browser, including a returning browser with a populated cache. Read instance references when the change affects their configuration. After RDF or source-data changes and the corresponding ingest, `npm run check:production` checks references and ingested data; `SZD_STAGING_HOST=https://gams.uni-graz.at npm run test:rdf-staging` compares the affected objects with their local RDF builds. A frontend-only release does not require this data comparison.

## Transferability

The setup carries over to other GAMS projects, which share page stylesheets with the same two includes, an RDF transformation with `document()` calls against indexes and query objects whose templates lie in a repository. The stub, the redirection of includes and `document()` calls, the fixture storage and the split into smoke, golden and structural checks can be copied. Fixtures, expectations and the list of page types are project-specific.

## Asset and download regressions

`test/asset-version.smoke.mjs` checks the freshly rendered snapshot for release versions on project CSS and JavaScript, the explicit tokens stylesheet and, while the timeline is enabled, deferred timeline JSON. The register golden comparison ignores only the release query, release data attribute and explicit tokens link, which this test checks independently. All other register markup remains compared.

`test/iiif-download.smoke.mjs` includes the production resource address from the manifest of `o:szd.260`, simulates the missing CORS permission, checks the production alias mapping and preserves external and staging addresses. Its fetch and ZIP mocks do not replace a browser download and inspection of the actual archive.
