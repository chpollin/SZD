---
title: Rendering architecture
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD  # the served files it describes are in https://zimlab.uni-graz.at/gams/projects/szd/gams-www
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: complete
language: en
created: 2026-06-15
updated: 2026-10-28
authors: [Christopher Pollin]
generated-with: Claude Code (Claude Opus 5.5)
related: [architecture, specification, search-architecture, correspondence-gallery-architecture, testing]
---

# Rendering architecture

Which stylesheet renders which page, how the central template library, the two languages, the frontend scripts and the styles work. Stylesheets, scripts, styles and assets named in code formatting without a link lie in gams-www (https://zimlab.uni-graz.at/gams/projects/szd/gams-www). The rendering pattern it builds on is described in [architecture](architecture.md#rendering-pattern), the search pages in [search-architecture](search-architecture.md) and the correspondence gallery in [correspondence-gallery-architecture](correspondence-gallery-architecture.md).

## Page types

| Stylesheet | Page type | Input |
|---|---|---|
| `szd-Werke.xsl` | grouped catalogue of works and personal documents, by category | TEI |
| `szd-Essays.xsl` | catalogue of the Aufsatzablage, a derived copy of `szd-Werke.xsl` | TEI |
| `szd-Autographen.xsl` | catalogue of the autographs, alphabetical by author | TEI |
| `szd-Bibliothek.xsl` | catalogue of Zweig's library, alphabetical | TEI |
| `szd-Korrespondenzen.xsl` | correspondence overview by partner | TEI |
| `szd-Konvolut.xsl` | page of one Personen-Konvolut | TEI |
| `szd-Briefedition.xsl` | full-text letter edition, prototype (`mode=view:editionobject`) | TEI |
| `szd-Facsimiles.xsl` | IIIF image gallery as card grid | SPARQL result from Mulgara |
| `szd-Thema.xsl` | curated theme page with footnotes | TEI |
| `szd-Lebenskalender.xsl` | biography as vertical view, with a switchable multi-holding timeline | TEI (`listEvent`) |
| `szd-Glossar.xsl` | SKOS glossary | SKOS/RDF |
| `szd-Index.xsl` | the indexes of persons, repositories, organisations and works | TEI (`listPerson`, `listOrg`, `listBibl`) |
| `szd-Personenliste.xsl`, `szd-Standortliste.xsl`, `szd-Werkliste.xsl`, `szd-Organisationen.xsl` | include `szd-Index.xsl` for references set earlier in Cirilo | TEI |
| `szd-context.xsl` | start and static pages by `mode` (home, `about`, `imprint`, `miscellaneous`, `databasket`, `memory`) | context datastreams |
| `szd-Suche.xsl` | search results | SPARQL result from Blazegraph |

The menu item of `mode=miscellaneous` reads "Aktuelles", in English "News". Its content comes from the datastream `MISCELLANEOUS` of `context:szd`, which `szd-static.xsl` renders through the template for `t:div[@type='miscellaneous']`. Images in this datastream and in theme pages load host-relatively, so staging shows the images of its own objects.

A gallery reads object metadata from Mulgara and can therefore show only what exists as an object metadatum, for instance the shelfmark at the end of the title, and never an `szd:` property of the RDF.

## The template library

`szd-Templates.xsl` consists of named templates and three functions, `fn:query-href`, `fn:filing-key` and `fn:filing-letter`.

### Page frame

- `getStickyNavbar` renders the sticky page header with title, TEI and RDF buttons, glossary icon, the controls passed in `$Controls` (for instance a view switch) and the PID-dependent jump navigation by letters, digits, categories, years or glossary categories with their subcategory dropdowns. The jump links carry the class `header-jump-link`, and the bar wraps onto further lines.
- `getNavbar` is a slimmer variant.
- `getFooter` renders the entry footer with reference, citation, permalink (`https://stefanzweig.digital/{PID}#{xml:id}`) and PDF.
- `printPERMALINK` renders the permalink button, `printPermalinkBox` the collapsible permalink box with its copy button. The Lebenskalender uses the same pair.
- `getListViewSwitch` renders the view switch, see [View switch](#view-switch).
- `createFootnote` and `printCameraIcon`.

### Metadata lists

The templates `FillbiblFull_SZDMSK` (works, personal documents), `FillbiblFull_SZDBIB` (library), `FillbiblFull_SZDAUT` (autographs, with provenance and acquisition), `FillbiblFull_SZDKOR` and `FillbiblFull_SZDKOR-Konvolut` (correspondence), with `getEntry_SZDBIB_SZDAUT` as shared entry head, produce definition lists `dl.szd-metadata`. Every row stands in a `div.row` with `dt` for the label and `dd` for the value, and the labels come from `<i18n:text>`. The Bootstrap columns `col-12 col-sm-3` and `col-12 col-sm-9` set label and value side by side on wide screens and stack them on narrow ones, and a container query in `css/szd.css` stacks them also in a metadata area up to 30 rem wide.

Ten shared `Metadata*` templates bundle identical rows (language, correspondents, corporate bodies, correspondence place, affected persons, writing material, writing instrument, secretarial hands, provenance and acquisition). The holding templates decide order and presence of the other fields and keep their own rules for title, extent, dating and repository.

### Entity resolution and search links

- `GetPersonList` and `GetStandortList` resolve against the global variables `$PersonList` and `$StandorteList`, loaded from the `TEI_SOURCE` of `o:szd.personen` and `o:szd.standorte`.
- `fn:query-href` builds every search URL, see [search-architecture](search-architecture.md#request-flow).
- `createPersonSearchHREF`, `LocationSearch` and `WorkSearch` render names, places and works as search links and accept an optional parameter `text` for the link text. `createPersonSearchHREF` accepts the parameter `Index` (default `o:szd.personen`), with which the organisation index links corporate bodies to the person search. `WorkSearch` queries `o:szd.werkindex#SZDWRK.n`. `PersonSearch` takes only the locale.
- `printAuthor` formats names uniformly, including a partner that is an `orgName` without `persName`.

### Language helpers and others

- `printEnDe`, `print_title_en_de` and `languageCode` (ISO 639-2 to a German or English name)
- `createViewerHref` for the Mirador viewer (`sdef:IIIF/getMirador`)
- `AddData-Databasket` and `getLabelDatabasket` for the data basket buttons
- `getfirstforABC` for invisible letter anchors

Global variables at the top hold icon paths, `$PersonList`, `$StandorteList`, `$Languages` and `$ABCarray`.

## Two languages

1. The parameter `$locale` is passed through and evaluated in `<xsl:choose>` or in XPath conditionals.
2. Static interface labels are Cocoon i18n keys, `<i18n:text>key</i18n:text>`, which GAMS resolves on the server after the XSLT. The catalogue is in neither repository. Where it lacks a key, as for the English label of the biography block in the search results, the stylesheet sets the label by locale.
3. TEI content is chosen by `@xml:lang` through `printEnDe` and `print_title_en_de`.
4. The language switch (`languageButton` in `szd-static.xsl`) renders links with the class `language-link`. `js/szd.js` rewrites such a link on activation so that it keeps the current query parameters, filters and fragment and sets only the new `locale`. Context galleries keep their `sdef:Context/get` path, so a language change on the correspondence gallery in `mode=konvolut` stays on the gallery.

Every navigation link appends `?locale={$locale}`.

## Indexes

`szd-Index.xsl` renders the four indexes from one file. The `content` template branches on the list element, `listPerson` for persons, `listOrg` for repositories and organisations, which differ by PID (`o:szd.standorte` against `o:szd.organisation`), and `listBibl` with `bibl` entries for works.

`indexPage` builds the sticky header with the title from the `titleStmt` in the page language, the letter jump bar and, for repositories and organisations, the switch between alphabet and country. The sort and group name of an entry is the `sortKey` of a work, the surname or name of a person and the untyped `orgName` in the page language or without language. Variants (`orgName[@type='variant']`) are ignored. Entries stand in letter groups under an `h2` whose `id` is the letter.

Letter groups and order follow German library filing (DIN 5007-1). `fn:filing-key` lower-cases the name, files umlauts and every other letter with a diacritic under the base letter (Ä as A, Č as C, Ø as O), ß as ss, Æ and Œ as AE and OE, and skips leading punctuation, so "…1914 und heute" files under 1. `fn:filing-letter` is the upper-cased first character of that key. The indexes group by the letter and sort by the key and then by the NFC name, both with the codepoint collation, because SaxonJS in the harness sorts with a language collation and the Saxon of GAMS by codepoint. The jump bar of `getStickyNavbar`, the anchors of `getfirstforABC`, the library anchors, the title groups of the facsimile gallery and the register keys of the Aufsatzablage use the same letter, so a jump link always finds its target. Groups outside the alphabet, such as work titles beginning with a digit, receive their own jump links after the letters. The catalogue lists keep their `lang="ger"` sort of the entries.

`indexEntry` is the shared entry container, a `list-group-item` with the `xml:id` as `id`, as the permalinks expect, and a heading line of title (`h3`) and a narrow column of authority links. `indexEntryContent` supplies both parts per index.

- A person name links to the person search through `createPersonSearchHREF`, followed by the life years. The link column holds GND, Wikidata and Wikipedia.
- A repository name links to the repository search through `LocationSearch`. Place and country follow in brackets (`span.szd-place`) unless a name form already contains them. The link column holds GND and the website from `@corresp`.
- An organisation with `idno[@type='SZDSTA']` is also a repository, and its name links to the repository search for that entry. Every other body links to the person search with `o:szd.organisation#SZDORG.n`. Place and country follow as for repositories. The link column holds, for a repository, the pin `a.szd-repository-pin` to its entry in the repository index, then GND and the website. `idno[@type='SZDPER']` is a migration trace and is not shown.
- A work title links to the work search through `WorkSearch`, the link column holds GND.

## View switch

The grouped catalogue lists, the indexes of repositories and organisations and the correspondence gallery show the same entries grouped by different keys without reloading the page. The Aufsatzablage sets the alphabetical register against the category, works and personal documents the category with uniform title against the year, autographs the alphabet against the acquisition year, the library the alphabet against the publication year, and the two `listOrg` indexes the alphabet against the country. The server renders the default structure and the switch in the sticky header, and the script regroups and rebuilds the jump navigation for the chosen arrangement.

The page stylesheet writes every entry once and gives it the group keys of all modes. `data-view-<mode>` holds the heading of the entry in this mode, the optional `data-view-<mode>-key` the sort key behind it, `data-view-sub` and `data-view-sub-key` the second grouping level and `data-view-sort` the order within the lowest group. Groups are sorted by the key of their first entry in document order. All visible labels stay in the stylesheet.

`getListViewSwitch` renders the switch as a tab bar (`role="tablist"` with `role="tab"` buttons, `aria-selected`, `aria-controls` and a roving `tabindex`). It receives the list of modes and the default mode. Labels and the flat or nested character of a mode are defined there once for all pages. The parameters `hook`, `handler`, `idPrefix` and `panel` default to `list-viewswitch`, `setListView`, `list-view-` and `content`. The correspondence gallery passes `facsimiles-modeswitch`, `setFacsimilesView`, `facsimiles-view-` and `facsimiles-gallery`.

`js/list-views.js` finds the list through the class `list-views` and the bar through `list-viewswitch`. For another mode it rebuilds headings, subgroups and jump navigation and takes over the classes of the server-rendered structure. It restores the default mode from the remembered initial HTML, so switching back reproduces the server structure exactly. Without the attributes it hides the bar, and without JavaScript the default structure stays in place. Arrow keys, Home and End move between the tabs. The mode `land` groups flat by `country`, with entries without a country as the last group. As pattern for subgroups the script takes the first `h3` outside an entry, because index entries carry their own title as `h3`, and a rebuilt jump link loses the `title` of the copied letter link.

The order of the categories follows the document order of the TEI and is changed through the variable `kategorienReihenfolge` in `szd-Essays.xsl` and `szd-Werke.xsl`. The register key of the Aufsatzablage comes from the uniform title. Register sheets are titled "Register A" to "Register Y-Z", and their key is what follows "Register". Every other title takes `fn:filing-letter` of the title as key.

A further list needs only the attributes on its entries and the call of `getListViewSwitch`. [list-views.smoke.mjs](../local-test-build/test/list-views.smoke.mjs) and [extended-list-views.smoke.mjs](../local-test-build/test/extended-list-views.smoke.mjs) check the behaviour against the rendered pages.

## Lebenskalender

`szd-Lebenskalender.xsl` renders the vertical biography through `contentDefault`, grouped by the machine-readable date in the leading head line. `szd-static.xsl` adds `css/lebenskalender.css` to the head of this page while the timeline is switched off.

The multi-holding timeline is implemented in the template `contentTimeline`, the module `js/lebenskalender-timeline.js` and `css/lebenskalender-timeline.css`, and it reads the lane files described in [data](data.md#timeline-lane-files). It is switched off by the variable `timelineView` in `szd-static.xsl`, so every mode renders the vertical view and neither module nor lane files are loaded. With the switch on, `mode=timeline` and its older alias `mode=fancy` render the timeline. It shows life events, letters, personal documents and acquisitions of autographs as switchable lanes on a shared year scale, with filters for place, person and period and a density switch. Its filters live in the URL fragment behind the year or entry target, for instance `#y1933?from=1930&to=1935&lanes=biography`, because GAMS rejects further query parameters. The scale ends in 1950, later dated entries are held back and logged, and undated entries follow the dated groups per lane. Every visible entry stays in the DOM, and CSS `content-visibility` limits the layout work.

### Timeline internals

- `contentTimeline` renders the controls inside the shared page shell as `section#zl-app` and passes the scale through `Controls` to `getStickyNavbar`. The section carries the base URL of the lane files in `data-lane-base`, built from `$server` and `$gamsdev`.
- The fragment carries the keys `lanes`, `place`, `person`, `from`, `to` and `density`, while year and entry stay addressable as targets. A selection without any active lane survives a reload.
- The density buttons form a `role="group"` whose buttons carry `aria-pressed`, styled like the view tabs and handled by event delegation. The module defines `setLebenskalenderDensity` for existing calls.
- Within a year, periods and inferred dates come first, then year-only entries, then month and day dates in date order.
- Stylesheet, module, CSS and the five JSON files form one deliverable state and are deployed together.
- [lebenskalender-timeline.smoke.mjs](../local-test-build/test/lebenskalender-timeline.smoke.mjs) checks the view against the rendered page and the JSON files and counts as skipped while the switch is off.

## Frontend

The frontend is procedural jQuery and plain JavaScript without a build step for the project scripts.

### Script loading

- On every page, in the `<head>` of `szd-static.xsl`, are jQuery and the Bootstrap bundle from `/lib`, which carries Popper 1, and the project scripts `databasket.js`, `buildquery.js`, `download_images_iiif_manifest.js`, `szd.js`, `facsimiles-konvolut.js` and `list-views.js`. All carry `defer` except jQuery and `databasket.js`, whose functions inline scripts call while the HTML is parsed.
- On the glossary and on pages with TEI figures (`$PID = 'o:szd.glossar' or //t:figure/t:graphic/@url`) the fancybox script and stylesheet come from `/lib/1.0/plugins/fancybox_v2.1.5/`. `initSzd` initialises an available fancybox with `type: 'image'`.
- The data basket at `mode=databasket` loads no library. Its template in `szd-context.xsl` renders the controls and the empty table, which `databasket.js` fills.
- For the IIIF image download, `download_images_iiif_manifest.js` loads the local `FileSaver.js` and `jszip.js` on demand.
- Only at `mode=memory` does `szd-context.xsl` load `memory.js` and `css/memory.css`, the memory game with Zweig's self-portraits from `img/memory/`.
- `cslink.js` (a webpack bundle of Vue 2 with Font Awesome) and `gamsTemplate.js` (a webpack bundle with hash jumps under a sticky navbar, language and HTTPS handling and a small-device warning) are included by no stylesheet. GAMS datastreams outside gams-www may use them, so they are verified before any change or deletion.
- The vendored `js/popper.min.js` is Popper 2, which Bootstrap 4.5 cannot use, and is not loaded.

### Project scripts

- `js/databasket.js` keeps the data basket, a bookmark list for catalogue and edition objects in `localStorage` under the key `project = "szd"`. `add_DB` reads the `data-*` attributes of an entry, `keepCheckboxes` restores the checked state across pages, deduplication follows the object URI. On the basket page `showData` renders the table with the columns collection key, title, author, location, signature and URI. A filter field matches every word of the query against all columns, ignoring case, diacritics and German umlaut spellings, and the column heads sort ascending and descending with `aria-sort`. The CSV button downloads the entries shown as UTF-8 with BOM, semicolon-separated, with CRLF line ends and every field quoted, named `szd-datenkorb-YYYY-MM-DD.csv` (English `szd-databasket-…`). A value that would start a spreadsheet formula (`=`, `+`, `@`, tab, carriage return) gets a leading apostrophe. The PDF button opens the print dialog, and `css/print.css` prints title, date, collection key and table in landscape, without navigation, controls and the remove column. Removing an entry or clearing the basket renders the table anew on this page and keeps filter, sort order and focus. The pure helpers `basketToCsv`, `basketCsvName`, `filterBasket` and `sortBasket` are global so that the unit test can call them.
- `js/download_images_iiif_manifest.js` runs the IIIF image download. It reads `/archive/objects/<PID>/methods/sdef:IIIF/getManifest`, checks HTTP status, JSON and the canvas structure of the first sequence and takes every image of every canvas. At most four image requests run at a time. Image responses must be successful, non-empty and of type `image/*`, and the ZIP file is created only after every image has arrived, named after the PID without its `o:` or `context:` prefix and with dots as underscores (`szd_377_images.zip`), with numbered image files inside. The libraries load from the asset base in `data-asset-base`. Concurrent downloads share one loading run of the libraries, existing library globals are reused, and a failed library load can be retried. On an image error the run waits for pending requests and creates no ZIP file, and the loading indicator is reset in a `finally` block. Status and errors appear in an ARIA live region in German or English. [iiif-download.smoke.mjs](../local-test-build/test/iiif-download.smoke.mjs) checks these runs with simulated network responses, libraries and downloads.
- In `js/szd.js`, `copy()` copies the permalink of the clicked box. The script keeps the collapse arrows in sync with their panels, rewrites the language links and offsets hash targets below the sticky header for jump links and `scrolldown()`.
- `js/list-views.js` runs the view switch of lists and indexes, `js/facsimiles-konvolut.js` that of the correspondence gallery.

### Global functions

These functions are called from inline attributes or inline scripts of the generated HTML, or through a handler name passed to `getListViewSwitch`. Their names and signatures stay unchanged.

| Signature | Defined in | Caller |
|---|---|---|
| `copy(element)` | `js/szd.js` | copy buttons of the permalink boxes and gallery cards, called with the clicked element |
| `add_DB(input_id)` | `js/databasket.js` | data basket checkbox of an entry |
| `delet_DB(id)` | `js/databasket.js` | remove buttons that `databasket.js` itself creates |
| `clearData()`, `showData()` | `js/databasket.js` | data basket page in `szd-context.xsl` |
| `scrolldown(src)` | `js/szd.js` | in-page reference links of entries, for instance to an enclosure |
| `download_images_iiif_manifest(PID)` | `js/download_images_iiif_manifest.js` | image download buttons of entries and gallery cards |
| `build_zip_download(canvases, PID)`, `downloadImage(imageSrc)` | `js/download_images_iiif_manifest.js` | kept global beside the download function |
| `setListView(mode)` | `js/list-views.js` | default handler of `getListViewSwitch` |
| `setFacsimilesView(mode, updateHistory)` | `js/facsimiles-konvolut.js` | handler passed by the correspondence gallery |
| `setLebenskalenderDensity(value)` | `js/lebenskalender-timeline.js` | density switch of the timeline, unused while the timeline is off |

## CSS

- `css/szd.css` is the main theme. It declares the cascade layers `reset, legacy, base, tokens, layout, components, utilities`, imports the Bootstrap CSS into `legacy` and `css/tokens.css` for colours, focus ring and target size. It carries typography, the edition elements (`span.page` for `<pb>`, footnote counters), the loading overlay, the image lightbox, entry and card layout and the `.szd-metadata` definition lists. The web fonts BauerBodoni and Source Sans Pro load locally as WOFF2 with an OpenType fallback and `font-display: swap`. The utility classes `.szd_color` (wine red) and `.szd_gold` (text gold) replace inline colours.
- The project colours are wine red and the brand gold `#c3a461`. The token `--szd-gold-text` is the brand gold itself, see [specification](specification.md#visible-design-2026-09-11-with-later-changes).
- `css/navbar.css` styles the top navigation, `css/lebenskalender.css` the vertical biography, `css/lebenskalender-timeline.css` the timeline, `css/cards-gallery.css` the card gallery and `css/memory.css` the memory game.
- `css/print.css` is the print stylesheet, included with `media="print"`.
- The data basket styles live in the components layer of `szd.css`, its print layout in `print.css`. The named page `databasket` (A4 landscape) is declared at the end of `szd.css`, because Chrome applied the `@page` size of the Bootstrap import to it while the rule stood in `print.css`. Browsers without named pages print the basket upright.
## Asset releases and download origins

The shared shell builds project CSS and JavaScript links with `fn:asset-url` and `$asset-version`. The lazy download dependencies and timeline JSON inherit this release value. The explicitly versioned tokens stylesheet follows `szd.css`; its older import remains for cached HTML compatibility. The deployment and response-header policy lives in [deployment architecture](deployment-architecture.md#asset-releases-and-cache-headers).

On the two production SZD aliases, the image downloader resolves raw `https://gams.uni-graz.at/o:szd.<id>/<datastream>` resources through the current origin. The public alias serves these paths directly, while the raw GAMS image responses lack CORS permission. External image services and staging addresses retain the manifest URL, including its query and fragment.
