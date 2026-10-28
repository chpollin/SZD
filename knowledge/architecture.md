---
title: Architecture
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD  # the served files it describes are in https://zimlab.uni-graz.at/gams/projects/szd/gams-www
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: complete
language: en
created: 2025-10-23
updated: 2026-10-28
authors: [Christopher Pollin]
generated-with: Claude Code (Claude Opus 5.5)
related: [project, data, rdf-mapping, rendering-architecture, search-architecture, deployment-architecture]
---

# Architecture

Stefan Zweig Digital is published on GAMS (Geisteswissenschaftliches Asset Management System), the Fedora-based asset management system of the University of Graz. Its sources and presentation are split across two Git repositories, with Zenodo for long-term preservation and GitHub Pages for the ontology and project documentation. The presentation layer is an XSLT application layer on GAMS. This document describes the two repositories, the platform concepts the layer depends on, its two layers and their data flow, the rendering pattern, the asset conventions, the derived timeline assets, preservation, GitHub Pages, the repository structures and the known debt. Deployment, the data ingest and the Cirilo settings are described in [deployment-architecture](deployment-architecture.md), the pages in [rendering-architecture](rendering-architecture.md), the search in [search-architecture](search-architecture.md) and the ingest output in [data](data.md) and [rdf-mapping](rdf-mapping.md). Stylesheets, scripts, styles and assets named in code formatting without a link lie in gams-www.

## Two repositories

| Repository | Role |
|------------|------|
| `chpollin/SZD` (this repository) | Curated TEI sources in `data/`, the Nachlass-Ontologie in `ontology/`, the scripts that turn partner deliveries into TEI and repair the catalogue data, the GitHub Pages site in `docs/`, the Zenodo pipeline in `szd-zenodo-backup/`. Since October 2026 also the knowledge base of both repositories in `knowledge/`, the harness in [local-test-build/](../local-test-build/README.md), the SPARQL query templates in [gams/query/](../gams/query/README.md) and the copies of the ingest stylesheets that GAMS does not read from gams-www in [gams/](../gams/) |
| gams-www, `https://zimlab.uni-graz.at/gams/projects/szd/gams-www` (local checkout `ZIMLAB/szd`) | Presentation layer, meaning the XSLT, JavaScript and CSS that GAMS applies, including the RDF transformation `szd-TORDF.xsl`, with fonts, icons, images and the lane copies of the timeline. Until October 2026 it also held the SPARQL query templates, the harness, three ingest stylesheets and the knowledge base of the presentation layer |

The repositories do not see each other automatically. Their cross-references stand in the agent instructions, for this repository in [CLAUDE.md](../CLAUDE.md). The operator pushes and ingests. Scripts that must read the presentation layer, such as `scripts/checkup_2026_09_index/verify_orphan_persons.py`, expect its checkout at `ZIMLAB/szd` beside this repository.

```
TEI in chpollin/SZD
  └─ Cirilo ingest ──► GAMS object (Fedora, PID o:szd.*)
                         ├─ TEI_SOURCE datastream
                         ├─ RDF via szd-TORDF.xsl ──► Blazegraph triple store
                         └─ rendering via gams-www XSLT ──► https://stefanzweig.digital
```

The publication workflow of the data and the Cirilo ingest dialog are described in [deployment-architecture](deployment-architecture.md#data-ingest), the release flow of gams-www in [deployment-architecture](deployment-architecture.md#release-flow).

## Repository and server

gams-www holds the transformation and presentation logic (XSLT, JavaScript, CSS), static assets and the generated JSON assets of the multi-holding timeline. The following live on the GAMS server.

- the ingested data objects, whose curated TEI sources are maintained in this data repository
- the Cocoon i18n catalogue, which resolves the `<i18n:text>` keys of the stylesheets
- the executed SPARQL queries of the query and context objects, of which [gams/query/](../gams/query/README.md) holds the templates for the search
- the runtime environment, a Fedora repository with a Cocoon pipeline and two triplestores

gams-www alone therefore does not run. The harness in [local-test-build/](../local-test-build/README.md) renders the page types and the RDF transformation locally against real data, see [testing](testing.md).

## GAMS concepts

- The PID is the persistent identifier of an object, `o:szd.*` for data objects, `context:szd.*` for context and static pages, `query:szd.*` for search objects. The PID is the central control value, and most templates branch on it.
- A disseminator is a service method `sdef:…/get` that transforms an object into an output format. SZD uses `sdef:TEI/get?locale=…` for the HTML view of a TEI object, `sdef:Context/get?…&mode=…` for context and static pages, `sdef:SKOS/get` for the glossary, `sdef:Query/get?params=…` for the searches, `sdef:IIIF/getMirador` and `sdef:IIIF/getManifest` for the facsimile viewer and the IIIF manifest, and `sdef:Ontology/get` and the raw datastreams for downloads.
- Every object has named datastreams at `…/archive/objects/<PID>/datastreams/<DSID>/content`, for instance `DC`, `RELS-EXT`, `METADATA`, `QUERY`, `TEI_SOURCE`, `STYLESHEET`, `TORDF` and `RDF`. The `SELECT` variables of the `QUERY` datastream of a context object fix the result schema the page stylesheet receives.
- GAMS runs two triplestores. Mulgara is the Fedora resource index with the administrative metadata of every object, Dublin Core, content model `cm:…` and collection and context membership. It feeds the metadata-driven lists such as the facsimile galleries. Blazegraph holds the project-specific `szd:` RDF that the ingest transformation produces, and it is the basis of the content search. A metadata-driven list therefore cannot use an `szd:` property, because that property lies in the other store.
- In Blazegraph the `szd:` RDF of every object lands in a graph whose URI is its PID, and a query addresses it with `FROM <o:szd.…>`.

## Layers and data flow

Everything starts from the curated TEI source of a holding.

```
curated TEI source (ingested into GAMS)
   │
   ├─ INGEST LAYER ─→ szd-TORDF.xsl        → RDF (szd: ontology) → Blazegraph   search basis
   │                  szd-TOMETS.xsl       → METS/MODS                           facsimile viewer
   │                  szd-MODStoDC_MAPPING → OAI Dublin Core                     harvesting
   │                  szd-tei-hssf.xsl     → Gnumeric spreadsheet                editorial checks
   │
   └─ PRESENTATION LAYER (sdef:TEI/get?locale=…)
          szd-static.xsl     page shell: head, navbar, footer
        + szd-Templates.xsl  central library: headers, metadata lists, resolvers
        + page stylesheet    main area through the named template content
        → XHTML with Bootstrap 4 classes
```

The ingest layer of the diagram names the four stylesheets as gams-www held them before October 2026. The reading of the Cirilo datastreams on 2026-10-28 shows that only `szd-TORDF.xsl` is read from gams-www, that METS comes from the inline datastream `cirilo:szd/TOMETS`, and that neither instance references `szd-MODStoDC_MAPPING.xsl` or `szd-tei-hssf.xsl`, see [deployment-architecture](deployment-architecture.md#ingest-stylesheets-in-cirilo). Copies of the latter three lie in [gams/](../gams/).

Independently of the `szd:` RDF, the object metadata of every object lie in the Mulgara resource index and feed the metadata-driven galleries.

## Rendering pattern

Every page stylesheet includes the same two building blocks and supplies only the main area.

```xml
<xsl:include href="szd-static.xsl"/>      <!-- page shell and the match="/" template -->
<xsl:include href="szd-Templates.xsl"/>   <!-- reusable templates and functions -->
<xsl:template name="content"> … </xsl:template>   <!-- the <main> area only -->
```

Among the presentation stylesheets, `szd-static.xsl` alone has a `match="/"` template. It renders the whole page shell and calls `<xsl:call-template name="content"/>` in the middle. Every page stylesheet, for instance `szd-Werke.xsl`, defines the `content` template and fills only `<main>`. A new page is therefore one stylesheet with the two includes and a `content` template, and a new PID needs its branch in the PID case distinctions of `szd-Templates.xsl`. The four index include files are the exception, they include `szd-Index.xsl` only.

## Global parameters

`szd-static.xsl` declares three parameters that are passed through all templates.

| Parameter | Purpose |
|---|---|
| `$locale` | language `de` or `en`, from which `$lang` is derived |
| `$mode` | sub-view switch, for instance `databasket`, `about`, `imprint`, `miscellaneous`, `memory` and `view:editionobject` |
| `$search` | search input |

Derived from them or from the input are `$PID` (from the SKOS `@rdf:about` or `t:idno[@type='PID']`), `$model` and `$cid` (from the SPARQL result). The variable `$timelineView` switches the multi-holding timeline of the Lebenskalender on or off, see [specification](specification.md#lebenskalender).

## Input formats

- TEI (`t:` namespace) for the catalogue and detail pages, the Lebenskalender, the theme pages, the letter edition and the indexes (`listPerson`, `listOrg`, `listBibl` in `szd-Index.xsl`).
- SPARQL result XML (`s:` namespace, `s:sparql/s:results/s:result`) for the galleries and the search results.
- SKOS/RDF (`skos:`, `rdf:`) for the glossary.
- Derived JSON files in `data/lebenskalender/` of gams-www for the multi-holding timeline, which is currently switched off, see [data](data.md#timeline-lane-files).

## Assets and paths

- `$gamsdev` in `szd-static.xsl` is the base path of the project's own assets (`…/css/`, `…/js/`, `…/icons/`, `…/img/`, `…/data/`). It is taken from the URL of the stylesheet itself with the host removed, so assets come from the gamsdev mirror on staging and from `/szd` in production. Without an http URL, as in a local run, it falls back to `/szd`.
- `$server` is empty, so all asset URLs are host-relative.
- GAMS serves the third-party libraries under `/lib/`, namely jQuery 3.5.1 and the Bootstrap 4.5.0 JavaScript bundle with Popper 1 (`/lib/2.0/`), the Bootstrap CSS, which `css/szd.css` imports into the cascade layer `legacy`, Font Awesome (`/lib/2.0/fa/`) and fancybox 2.1.5 (`/lib/1.0/plugins/`).
- `js/` holds the project scripts and vendored libraries, among them Popper 2 (no longer loaded), FileSaver, jszip, DataTables with Buttons and pdfmake with `vfs_fonts` (no longer loaded since the data basket rebuild of 2026-10-21, to be deleted), and two webpack bundles that no stylesheet includes, `cslink.js` and `gamsTemplate.js`. Their loading conditions are listed in [rendering-architecture](rendering-architecture.md#script-loading).
- Colour and size tokens live in `css/tokens.css`, imported by `szd.css`.

## Derived timeline assets

The timeline of the Lebenskalender adds a static JSON delivery path beside the GAMS ingest. `scripts/lebenskalender_lanes/build_lanes.py` derives the lane files from the TEI sources and writes identical copies to `data/derived/lebenskalender/` (ignored by Git, reproduced by the generator) and `docs/lebenskalender/lanes/`. The presentation repository carries a further copy under `data/lebenskalender/`, refreshed explicitly. Schema, dating rules and delivery state are in [lebenskalender-lanes](lebenskalender-lanes.md).

## Long-term preservation

The pipeline in [szd-zenodo-backup/](../szd-zenodo-backup/README.md) downloads the digitised objects from GAMS, packs them into TAR.GZ archives with DataCite metadata and uploads them to Zenodo with DOI versioning. The data itself is generated locally and never committed. The deposit is https://zenodo.org/records/17421555.

## GitHub Pages

The `docs/` folder is served from the `master` branch at https://chpollin.github.io/SZD/ without a build step. The only workflow, `.github/workflows/deploy-ontology-docs.yml`, regenerates the ontology documentation from `ontology/szd-ontology.ttl`. The site holds the ontology reference, the project page, downloads and the Lebenskalender prototype.

The design is aligned to the Stefan Zweig Digital GAMS site as one visual family with the Klawiter Bibliography.

- Palette from GAMS, burgundy `#631a34` for header, links and primary accent, gold `#C2A360` for metadata labels, cream `#FAF8F3` as page background. The ontology site is burgundy-forward with section headings in burgundy, the Klawiter site gold-forward.
- Typography Source Serif 4 for headings and body, Source Sans 3 for UI elements and navigation, JetBrains Mono for URIs and code.
- The landing page is an ontology dashboard with a stats row, three primary cards (reference, visualisation, downloads) and a row of secondary links. All pages are in English.
- A slim bar above the header connects Stefan Zweig Digital (GAMS), the Klawiter Bibliography and this site.
- `ontology/visualize.html` is a fullscreen force-directed D3.js graph with layer toggles and hover highlighting.
- `docs/css/szd-ontology.css` is the stylesheet for all pages except `visualize.html`, which carries inline styles for its fullscreen layout.

## Repository structure

gams-www after the split of October 2026:

```
gams-www/
├── szd-static.xsl            page shell (head, navbar, footer) with the match="/" template
├── szd-Templates.xsl         central template library
├── szd-<View>.xsl            one page stylesheet per view, see rendering-architecture
├── szd-Index.xsl             indexes of persons, repositories, organisations and works
├── szd-context.xsl           start and static pages, dispatched by mode
├── szd-Suche.xsl             renderer of the search results
├── szd-TORDF.xsl             ingest: TEI → RDF (szd: ontology)
├── js/                       project scripts and vendored libraries
├── css/                      szd.css, tokens.css and view-specific stylesheets
├── data/lebenskalender/      generated lane files of the timeline and index.json
├── icons/ img/ fonts/        static assets
├── LICENSE
└── README.md
```

Before the split gams-www also held `szd-TOMETS.xsl`, `szd-MODStoDC_MAPPING.xsl` and `szd-tei-hssf.xsl`, the SPARQL templates in `query/`, the harness in `local-test-build/`, the project knowledge in `knowledge/` and the agent files `AGENTS.md` and `CLAUDE.md`.

The data repository, with the folders this knowledge base refers to:

```
SZD/
├── data/                     curated TEI sources, one folder per collection, and derived/ (ignored by Git)
├── ontology/                 SZDO sources, shapes, sample instances and validation
├── scripts/                  import, repair, check and reconciliation scripts, each folder with a README
├── docs/                     GitHub Pages site, with the ontology reference and the Lebenskalender prototype
├── webpage/                  sources of the static pages of context:szd
├── szd-zenodo-backup/        Zenodo pipeline
├── gams/                     copies of three ingest stylesheets and the SPARQL templates in query/
├── local-test-build/         harness, tests, fixtures and prototypes of the presentation layer
├── knowledge/                project knowledge of both repositories
└── README.md, CLAUDE.md
```

## Known debt

Duplicates are always changed on both sides.

- `szd-Essays.xsl` is a derived copy of `szd-Werke.xsl` and follows its structure closely.
- The person and repository resolvers exist twice, `GetPersonList` and `GetStandortList` in `szd-Templates.xsl` for rendering, `GetPersonlist` and `GetStandortelist` in `szd-TORDF.xsl` for the ingest.
- The four index include files stay until the Cirilo references point to `szd-Index.xsl`, see [deployment-architecture](deployment-architecture.md#stylesheet-references).
- The `FillbiblFull_*` family keeps one template per holding type. Identical metadata rows are shared `Metadata*` templates, and the remaining differences are intended.

Further debt.

- The language marking of the SPARQL queries is a documented quick hack ([gams/query/README.md](../gams/query/README.md)), and `szd-MODStoDC_MAPPING.xsl` derives object types heuristically from shelfmark and title. Both are error-prone. Neither instance referenced the crosswalk when read on 2026-10-28, see [data](data.md#dublin-core-for-harvesting).
- `szd-Templates.xsl` is the largest file of gams-www and branches by PID, so a change there keeps every PID branch in view.
- The open findings in `szd-TORDF.xsl` and `szd-Suche.xsl` are listed in [rdf-mapping](rdf-mapping.md#open-findings) and [search-architecture](search-architecture.md#open-findings-in-the-renderer).
- The frontend depends on jQuery, Bootstrap, Popper, fancybox and Font Awesome. Their removal is planned in [plan](plan.md#phase-3-dependency-removal).
- The letter edition (`szd-Briefedition.xsl`) is a prototype.
- Compression and cache control for JavaScript are server configuration and were passed to the ZIM GAMS team as a request during the frontend overhaul of September 2026.

## Related

- [data-model](data-model.md), encoding patterns and authority references
- [collections](collections.md), collections and rendering contracts
- [ontology](ontology.md), the formal ontology and its documentation site
- [project](project.md), project context and standards
- [deployment-architecture](deployment-architecture.md), data ingest, release flow and Cirilo references
- [plan](plan.md), the pending staging and production ingest
