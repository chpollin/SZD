# local-test-build

Local test harness that runs the SZD page stylesheets and the RDF transformation of a gams-www checkout against the data of this repository without the GAMS runtime, so that the generated HTML and RDF can be inspected and tested. The test contract, meaning what is checked locally and what only on staging, is laid down in [knowledge/testing.md](../knowledge/testing.md).

## Requirements

- Node.js (tested with v24).
- SaxonJS as XSLT 3.0 and 2.0 processor and jsdom for the tests, installed once in this folder with `npm install`.
- Python for `serve-full.py`, the prototype generators and the RDF checks with rdflib (optional, a check without it reports "NOT CHECKED").
- A checkout of the ZimLab repository gams-www (https://zimlab.uni-graz.at/gams/projects/szd/gams-www) with the served files, by default at `../ZIMLAB/szd` beside this repository, otherwise at the path in `SZD_WWW`. Revisions such as `--rev HEAD` and the RDF baseline name commits of gams-www.
- The data come from this repository, or from the path in `SZD_DATA_ROOT`.

## Choosing the test scope

```powershell
npm run test:frontend   # CSS, JavaScript and page XSLT; no RDF build
npm run test:data       # RDF generation; no page build
npm test                # explicit full check or shared rendering changes
npm run test:scope      # routing changes only; no rendering
```

[test/run-all.mjs](test/run-all.mjs) builds what the tests need and then runs every suite, unit tests, prototypes, pages and RDF, and prints passed, failed and skipped. The build is the working-tree snapshot of all pages (see below) and the RDF of the golden set, of the theme pages and of the baseline `faa784a` (`SZD_RDF_BASELINE_REV`), which is rebuilt only when its inputs change. The autographs, the library, the correspondence index and the gallery take minutes each, which makes the full run the slow part of the check before a push. `--suite unit,proto,pages,rdf` selects suites, `--no-build` reuses the existing builds. Without the data repository the page and RDF suites count as skipped. The data basket unit test alone runs with `npm run test:unit`.

All tests find their builds through [test/paths.mjs](test/paths.mjs). `SZD_TEST_BUILD_DIR` is the folder with the full pages, by default `build-snap/worktree`, `SZD_RDF_BUILD_DIR` the folder with one RDF build per label, by default `build-rdf`. A build directory must not contain `--`, see [testing](../knowledge/testing.md#refactoring-without-change-in-behaviour).

### Pre-push hook

[hooks/pre-push](hooks/pre-push) reads the refs being pushed and selects suites with [test/scope.mjs](test/scope.mjs). Frontend paths run unit, prototype and page checks; RDF paths run RDF checks. Shared infrastructure, the shared language fixture, dependencies and unknown code paths run both. Renames include the source and destination paths. The hook tests the current working tree, so push the checked-out commit with a clean tracked tree. Documentation and routing-only changes run only the fast routing check. A new remote branch has no comparison baseline, so its entire tree is classified. Missing Git objects stop the hook; fetch the remote before retrying. A failed selected check blocks the push. The hook guards pushes of gams-www and passes that clone to the harness as `SZD_WWW`. It is not active until it is enabled once in the gams-www clone with the absolute path of this folder:

```powershell
git config core.hooksPath <data-repository>/local-test-build/hooks
```

`core.hooksPath` replaces the folder `.git/hooks` for every hook of the clone. Where other hooks live there, copying the file to `.git/hooks/pre-push` enables it instead. `git push --no-verify` skips the hook.

## Snapshots

[snapshot.mjs](snapshot.mjs) renders every page listed in [snapshot.manifest.json](snapshot.manifest.json), page stylesheet times input times language times mode, from the `szd-*.xsl` of a commit or of the working tree into `build-snap/<label>/`, and compares two snapshots byte for byte. Rendered pages are never versioned. A snapshot is reproducible from the commit, the commit of the data repository and the input hashes, which `meta.json` records next to the pages.

```powershell
node snapshot.mjs --rev HEAD                       # build-snap/<hash>/
node snapshot.mjs                                  # the working tree, build-snap/worktree/
node snapshot.mjs --rev HEAD --compare worktree    # build both and compare
node snapshot.mjs --diff build-snap/a build-snap/b # compare two existing snapshots
node snapshot.mjs --rev HEAD --only szd-Personenliste,szd-Werkliste
```

A comparison lists every differing page with the byte, line and column of the first difference and the text around it in both versions, and it notes when the two snapshots were built from different data. A commit snapshot is reused while manifest, inputs and fixtures are unchanged, `--force` rebuilds it and `--out` chooses the folder. A partial snapshot (`--only`) gets a folder of its own. `SZD_JOBS` sets the number of parallel renders.

The manifest covers the autographs, the library, the Aufsatzablage, `szd-Werke.xsl` on both works and personal documents, the correspondence index, one Konvolut, the Lebenskalender without mode and with `mode=timeline` (both render the vertical view while the timeline is switched off), the four indexes through their wrappers, the correspondence gallery, the glossary, the theme pages 1 to 8, `context:szd` in the modes home, about, imprint, miscellaneous, databasket and memory, the letter edition and a search result, each in both languages. Not covered are the search page without hits and with a glossary query, which need further GAMS inputs.

A structure-preserving change counts as checked when the snapshot of the commit before it and the snapshot of the working tree are byte-identical, `node snapshot.mjs --rev HEAD --compare worktree`.

### Inputs and fixtures

Holdings, indexes, glossary, theme pages and Konvolut come unchanged from the data repository. The few inputs that only GAMS holds lie versioned under [fixtures/](fixtures/), each fetched read-only from the URL named in the manifest. They are the `METADATA` of `context:szd` and of the correspondence gallery context, the language catalogue `LANGUAGES`, the static datastreams of `context:szd` (`STARTSEITE`, `ABOUT`, `IMPRINT`, `MISCELLANEOUS`, `SEARCH_HELP`), the TEI of the letter edition and a hit list of the person search from staging. A fixture is refreshed by fetching it again from its URL.

[harness.mjs](harness.mjs) materialises the stylesheets for every build. It redirects each `document()` call against GAMS to the data repository or to a fixture and replaces the server-side modification date by an empty metadata result. SaxonJS 2.7 fails on an `xsl:for-each-group` with two sort keys that call `current-grouping-key()` (XTDE1071), which the correspondence gallery has used since `d6e5e1d`, while the Saxon of GAMS renders it. The harness joins the two keys into one key with the same order, only in its copy.

## Full pages with the shared templates

`build-full.mjs` renders a single page with `szd-static.xsl`, `szd-Templates.xsl` and every further included stylesheet from the working tree, with the same materialisation as the snapshots. The output lies in `build-full/`, or under `SZD_TEST_BUILD_DIR`. `SZD_LANGUAGES_FILE` replaces the versioned language catalogue.

```powershell
node build-full.mjs szd-Autographen <data-repository>/data/Autograph/SZDAUT.xml de
node build-full.mjs szd-context fixtures/context-szd.METADATA.xml en about
python serve-full.py --port 8769
```

The preview is at `http://127.0.0.1:8769/local-test-build/build-full/`, and a snapshot folder can be served the same way. The server delivers the gams-www checkout as site root and under `/szd/`, this harness under `/local-test-build/`, and loads the required `/lib/` and `/templates/` assets from GAMS into an ignored local cache. It listens on the loopback address only. A port that is already taken has to be replaced by another. The source data are not changed.

The Cocoon catalogue of interface texts is not part of it, so its `i18n:text` keys stay visible in the local preview. The server-side modification date is replaced by an empty metadata result. This build therefore checks structure, entries, behaviour and local assets, while the translated page and the modification date are checked on staging.

## Tests on the full pages

The tests read the pages from `SZD_TEST_BUILD_DIR`, English pages are named `*.en.html`, and the input a page was built from lies next to it as `<name>.input.xml`.

- [test/extended-list-views.smoke.mjs](test/extended-list-views.smoke.mjs), `npm run test:lists`, checks autographs, library and work index in both languages against their inputs.
- [test/list-views.smoke.mjs](test/list-views.smoke.mjs) checks the list view switch of the Aufsatzablage and the personal documents (`szd-Lebensdokumente`). Switching changes groups and jump navigation, switching back restores the initial structure, and the number of entries and of categories comes from the input.
- [test/konvolut.smoke.mjs](test/konvolut.smoke.mjs) checks the person and Konvolut switch of the gallery, IIIF thumbnails with `srcset` and lazy loading, collapsing of large groups in both views, direct call with `mode=konvolut`, browser history, ARIA state, keyboard use, the preservation of expanded groups and the language links to the gallery context object. `FACSIMILES_HTML` points it at another page.
- [test/stack-link.smoke.mjs](test/stack-link.smoke.mjs) checks the normalisation rule of the stack link against the rendered links and then runs `fn:bundle-pid` of the built gallery stylesheet on constructed index files (ambiguity, duplicate references, organisations, invalid and missing input).
- [test/konvolut-datum.smoke.mjs](test/konvolut-datum.smoke.mjs) checks the date block of the Konvolut page against its TEI.
- [test/lebenskalender-timeline.smoke.mjs](test/lebenskalender-timeline.smoke.mjs) checks the view `mode=timeline` of the biography with its four lanes, place, person and period filters, URL state, density switch and output in both languages. It serves the JSON assets of `data/lebenskalender/` as test responses. `TIMELINE_HTML` takes a page saved from staging instead. While `timelineView` in `szd-static.xsl` is `false()`, the test exits with code 2 and counts as skipped.
- [test/full-pages.smoke.mjs](test/full-pages.smoke.mjs) checks label and value pairs of the metadata, button targets, language links and included assets of the pages named as arguments.
- `npm run test:ui` checks navigation and the complete ZIP download with simulated network responses, without a build.

### Page hygiene

[test/page-hygiene.smoke.mjs](test/page-hygiene.smoke.mjs), `npm run test:hygiene`, walks every page of the snapshot and counts the defect classes that the live audit of 2026-10-13 found across the site: page links (`/o:…`, `/context:…`, `/query:…`) without `locale`, jump links whose target id does not exist, duplicate ids, non-void elements the XML serialiser self-closed (an HTML parser reads `<div/>` as an open tag), placeholder or inverted alt texts, metadata rows with an empty value, links to retired or staging hosts, and entries that one language renders and the other drops (the entry ids `SZD….n` of the German and the English page must agree). It prints one line per page with counts and samples and fails on any finding. Raw datastreams, viewer and image addresses count as non-pages. It is part of the `pages` suite of `npm test`.

### Indexes

`szd-Index.xsl` renders the four indexes, and the snapshot builds them through their wrappers `szd-Personenliste`, `szd-Standortliste`, `szd-Organisationen` and `szd-Werkliste` from the four index files of the data repository, so the inclusion is checked as well. `npm run test:register` runs two checks.

[test/register-index.smoke.mjs](test/register-index.smoke.mjs) loads the eight pages into jsdom and checks that every source entry appears exactly once with its `xml:id`, that no `id` is duplicated, that every jump target exists and every jump link and switch is focusable, that the menu item for organisations stands between repositories and works in both languages, and per index the heading line and links (search link, life years, GND, Wikidata and Wikipedia for persons, search link and place for repositories, search link, place, repository pin, GND and website for organisations, search link and GND for works). For the two `listOrg` indexes it switches to the arrangement by country and back with the real `list-views.js`.

[test/register-index.golden.mjs](test/register-index.golden.mjs) renders the eight pages through the snapshot driver from the commit in `SZD_GOLDEN_REV`, by default `HEAD`, with the same data, and demands that the pages in `SZD_TEST_BUILD_DIR` are byte-identical. It reports every differing page and, per page, the entries that disappeared, appeared or moved. An intended change of the indexes is checked against the commit before it and the reported differences are compared with the intended ones.

### RDF ingest

`build-rdf.mjs` runs `szd-TORDF.xsl` against TEI files of the data repository, because GAMS produces the RDF only at ingest and an error there can be corrected only with the next ingest. The three index objects, the work index and the language catalogue, which the stylesheet loads from GAMS through `document()`, are redirected to the local files in the stylesheet copy under `build-rdf/<label>/`, whatever form the URL takes in the stylesheet, and a remaining network call aborts the build. `--unavailable <host>/<pid>` lets that host lack the index object, so `doc-available()` answers false for it and `document()` aborts the build. The output `build-rdf/<label>/<file>.rdf.xml` holds one element per line, `<file>.raw.xml` is the unchanged serialisation. `--rev <commit>` takes the stylesheet from that commit and so produces the baseline. `e7acd7d` is the state before the resolution of multi-valued references and of GND references in `https`, `faa784a` the state before the fix of the autograph relations of 2026-09-24, which is the current baseline. `SZD_RDF_BUILD_DIR` moves the output directory, `SZD_DATA_ROOT` the data repository.

```powershell
$D = "$env:SZD_DATA_ROOT/data"
$F = "$D/Index/Location/SZDSTA.xml", "$D/Index/Organisation/SZDORG.xml",
     "$D/Correspondence/SZDKOR.xml", "$D/Library/SZDBIB.xml", "$D/Autograph/SZDAUT.xml",
     "$D/PersonalDocument/SZDLEB.xml",
     "$D/Correspondence/konvolute/szd.korrespondenzen.meiler-friedrich.xml"
node build-rdf.mjs --rev faa784a --label baseline $F
node build-rdf.mjs $F
npm run test:rdf
```

`test:rdf` runs two checks. Both read their expectations from the TEI files of the data repository and from the migration log of the organisation index, not from invented values.

[test/tordf.golden.mjs](test/tordf.golden.mjs) compares baseline and current state per file. Only reference lines to a person or organisation may be added, `<szd:… rdf:resource="…/o:szd.personen#SZDPER.n"/>` or `…/o:szd.organisation#SZDORG.n`, and no line may disappear, except the autograph relations and stray text lines removed by the fix of 2026-09-24, which the test also checks entry by entry. A baseline from before `8ec067b` had no template for `SZDORG`, this case is checked separately. `SZD_RDF_BASELINE_DIR` and `SZD_RDF_CURRENT_DIR` choose the directories.

[test/tordf.smoke.mjs](test/tordf.smoke.mjs) checks the organisation index (exactly one `szd:Organisation` per `org` under its URI, no `szd:Location`, name, GND, website, place, country, repository link, `dcterms:replaces`, full text, collection), the resolution in holding cases (the correspondence entry SZDKOR.41 with the corporate body GND 5158511-X as sender beside the person, the four library entries of the migration log as GND resolution and SZDORG pass-through, corporate bodies as participants in the personal documents, the autographs without organisation URI while repositories still resolve), the person resolution of every entry in `SZDBIB`, `SZDKOR`, `SZDLEB` and, if built, `SZDESS` and `SZDMSK` (every person of a multi-valued `@ref` and every GND in `https` stands as a triple on `o:szd.personen`), the negative cases (a GND without index match produces nothing, no empty resource, no repository URI on an actor role and no organisation URI on `szd:location`, a superseded person identifier only in `dcterms:replaces`, no growth of the comments `Error: no GND or SZDPER found`, no new duplicate `rdf:about`) and finally that every output parses as RDF/XML with rdflib.

[test/tordf-org-fallback.smoke.mjs](test/tordf-org-fallback.smoke.mjs), `npm run test:rdf-fallback`, builds `SZDKOR` and `SZDBIB` again under the label `org-fallback` with `--unavailable https://gams.uni-graz.at/o:szd.organisation` and demands the same RDF as in `current`, which must come from the working tree. It stands for the GAMS ingest, which runs the stylesheet without an http base URI and so asks production first, where the organisation index is still missing. A stylesheet that loads the organisation index from production fails the check.

[test/tordf-thema.smoke.mjs](test/tordf-thema.smoke.mjs), `npm run test:rdf-thema`, checks the theme pages. Every person that a theme page marks with `name/@ref` on `SZDPER` must stand in the RDF as `szd:connectedWithPerson` on `o:szd.personen`, otherwise the person search does not find the page. The test reads `build-rdf/thema/`, `SZD_RDF_THEMA_DIR` moves it.

[test/tordf.strict.mjs](test/tordf.strict.mjs), `npm run test:rdf-strict`, is the strict mode for a refactoring of `szd-TORDF.xsl` that must not change the output. It builds the golden set without the autographs, or the TEI files given as arguments, with the stylesheet of `SZD_RDF_STRICT_REV` (default `HEAD`) and with the working tree, and demands byte identity of every serialisation, reporting the first difference.

[test/rdf-triples.mjs](test/rdf-triples.mjs) compares two RDF/XML files triple by triple with rdflib and checks the difference against a named expectation list. Each line of the list is `+ <triple>` for a triple only the second file may have or `- <triple>` for one only the first may have, in N-Triples, and `#` starts a comment. Every difference must be listed and every listed change must occur.

```powershell
node test/rdf-triples.mjs build-rdf/strict-<hash>/SZDKOR.raw.xml build-rdf/strict-worktree/SZDKOR.raw.xml expected-SZDKOR.txt
```

[test/rdf-staging.mjs](test/rdf-staging.mjs), `npm run test:rdf-staging`, fetches the `RDF` datastream of each object built in `build-rdf/current` read-only from `gams-staging.uni-graz.at` and reports the triples only on staging and only local, optionally against an expectation list with `--expect`. `SZD_STAGING_HOST` replaces the staging host. Staging changes with every ingest, so this comparison is not part of `npm test`.

## Instance check

[check-instance.py](check-instance.py) reads the Cirilo settings of every object in [gams-objects.toml](gams-objects.toml) from the public datastream URLs of staging or production and compares them with the expected values, without login and without writing. Per object it checks the redirect of `STYLESHEET` and `TORDF` (expected file, generic stylesheet, retired host, `http` instead of `https`, trailing illegal character, dead target), the `QUERY` datastream of the query objects against the template in [gams/query/](../gams/query/README.md), and the presence of the `RDF` datastream of every TEI object. With `--data` it also compares the `TEI_SOURCE` of every object that has a file in the data repository, and the static datastreams of `context:szd` listed under `[[datastreams]]`, with the files there, in canonical XML with collapsed whitespace, because Cirilo re-serialises what it ingests. The Konvolute are expanded from the files of the data repository, `--skip-konvolute` leaves them out and `--pids` restricts the run.

```powershell
python check-instance.py --instance production --data --checklist production-checklist.md
npm run check:production
npm run check:staging
```

The run ends with the operator checklist, grouped by what has to be done (reference to set, ingest to repeat, object to delete), and exits with 1 on any deviation other than an `http` base. It is the replacement for reading the datastream URLs by hand, see [deployment-architecture](../knowledge/deployment-architecture.md#checking-an-instance), and applies to instance configuration changes and ingest verification. Frontend-only releases use the page, asset and download checks in [testing](../knowledge/testing.md#rule).

## The smaller page build with run.sh

`run.sh` renders a single page with a simplified page shell, for a quick look at the page logic in the browser.

```
bash run.sh <page-stylesheet> <data-url-or-file> [locale] [mode]
```

- `<page-stylesheet>` is the name of the stylesheet in the gams-www root, with or without `.xsl`, for instance `szd-Facsimiles`.
- `<data-url-or-file>` is a GAMS datastream (URL) or a local XML file. Either is kept as `build/<stylesheet>.input.xml`.
- `[locale]` is `de` (default) or `en`.
- `[mode]` is the value of the `mode` parameter for a sub-view, for instance `about` for `szd-context`. Without it `$mode` stays unbound, with it the output is named `build/<stylesheet>.<mode>.html`.

The page stylesheet includes [stub-lib.xsl](stub-lib.xsl) instead of its two production includes, and the stub imports the real `szd-static.xsl` and `szd-Templates.xsl`, materialised into `build/` by `harness.mjs`. Every template, function and global variable of the library therefore runs as in production, and only the entry point differs. It loads styles and card images from the live site through `<base href="https://stefanzweig.digital/">` and the local `js/facsimiles-konvolut.js` and `js/list-views.js` of gams-www from the local web server on port 8080, which `serve.sh` starts as `serve-full.py`.

```
bash run.sh szd-Essays ../data/Aufsatzablage/SZDESS.xml
bash run.sh szd-Werke ../data/PersonalDocument/SZDLEB.xml
bash serve.sh
```

The preview is at `http://localhost:8080/local-test-build/build/szd-Essays.html`. Because of `<base>`, plain anchor links lead to the live site. The index wrappers include `szd-Index.xsl` and are built with `build-full.mjs` or the snapshot instead.

## JavaScript unit tests

Client-side logic without a GAMS dependency is tested directly. [test/databasket.test.mjs](test/databasket.test.mjs), `npm run test:unit`, loads the real `js/databasket.js` of gams-www through `<script>` into jsdom with a simulated DOM and `localStorage`. Checking stores an item, checking again creates no duplicate, unchecking removes it, two different URIs coexist (deduplication by `uri`, not by shelfmark), `keepCheckboxes` restores the checks after a page change, the counter is right, an empty basket does not throw, and `showData`, `delet_DB` and `clearData` work. For the basket page it checks the CSV (BOM, header, six separate columns, semicolons, CRLF, doubled quotes, a semicolon inside a field, the blank library location, the formula guard and the file name), filtering across columns with diacritics and umlaut spellings, numeric and stable sorting in both directions with empty values last, the table with status line and `aria-sort`, the remove button with its accessible name and the focus after removal, the download of the entries shown and the print call of the PDF button. The script must load without jQuery.

## Prototypes

`npm run test:proto` runs [proto/proto.smoke.mjs](proto/proto.smoke.mjs), [proto/lebenskalender.smoke.mjs](proto/lebenskalender.smoke.mjs) and [proto/zeitleiste-lanes.smoke.mjs](proto/zeitleiste-lanes.smoke.mjs), apart from the application code. The prototypes are described in [proto/README.md](proto/README.md).
