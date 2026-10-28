---
title: Specification
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
related: [project, architecture, rendering-architecture, governance, plan, journal]
---

# Specification

What the presentation layer of Stefan Zweig Digital has to do, under which constraints, and which standing decisions govern it. Stylesheets, scripts, styles and assets named in code formatting without a link lie in gams-www (https://zimlab.uni-graz.at/gams/projects/szd/gams-www). A decision keeps its date where the date is the ground of the rule. Its provenance is recorded in the [journal](journal.md), open decisions stand in the [plan](plan.md#operator-questions).

## Functional scope

The site offers, in German and English:

- a catalogue view per holding, works and personal documents grouped by category, the Aufsatzablage, autographs and Zweig's library, each with a view switch between arrangements, a sticky header with jump navigation, and per entry a permalink, a citation, a PDF and a data basket button
- the correspondence index and one page per Personen-Konvolut
- the indexes of persons, repositories, organisations and works, whose entries link to the matching search
- the content search over full text, persons and organisations, repositories, glossary categories and works
- facsimile galleries with IIIF thumbnails, the Mirador viewer and a ZIP download of the images of an object
- the Lebenskalender as vertical biography
- curated theme pages and the SKOS glossary
- the data basket, a bookmark list kept in the browser with export
- start page, About, Imprint and the news page "Aktuelles" from the datastreams of `context:szd`

Where each of these is rendered is listed in [rendering-architecture](rendering-architecture.md#page-types).

## Constraints

- The layer runs inside GAMS. Page stylesheets are XSLT 2.0 run by the Saxon of the GAMS Cocoon pipeline, and the project scripts are served without a build step.
- GAMS accepts only the query parameters `locale` and `mode` on a TEI or context page and answers further parameters with HTTP 404. Client-side state such as filters lives in the URL fragment.
- Every page exists in German and English. `$locale` is passed through every template, every link carries `locale`, and TEI content is chosen by `@xml:lang`.
- Asset and navigation URLs are host-relative, so that staging pages load staging assets and link to staging objects. Permalinks point to the public domain, `https://stefanzweig.digital/{PID}#{xml:id}`.
- Global JavaScript functions that the generated HTML calls keep their names and signatures. The list is in [rendering-architecture](rendering-architecture.md#global-functions).
- No new third-party library and no CSS framework enter the code. The existing ones are removed in the order of the [plan](plan.md#phase-3-dependency-removal).
- Search links are built only through `fn:query-href` and the search helpers of `szd-Templates.xsl`.
- The facsimile metadata in GAMS stay untouched. The frontend compensates for their inconsistencies (session with the archive, 2026-09-10).
- A refactoring meant to change nothing visible is accepted only with byte-identical output before and after, as [testing](testing.md#refactoring-without-change-in-behaviour) describes.

## Frontend principles

These principles of the frontend overhaul of September 2026 apply to every change of HTML, CSS and JavaScript.

- A change does exactly what its finding or requirement describes. A default view that is not meant to change stays byte-identical in the harness, otherwise the commit names the deviation.
- CSS uses cascade layers, with the old rules in `@layer legacy`, tokens as custom properties in `css/tokens.css`, logical properties wherever a rule is touched and `@supports` for features outside the browser baseline. Existing colour values are taken over and not redefined.
- The generated HTML may call global functions through event delegation instead of inline attributes.
- Every change extends the harness tests by the check that would have failed before it, for instance focusability, duplicate ids, heading order or loaded assets.
- Keyboard use, visible focus, landmark and heading structure and the tab semantics of switches are checked with every change.

## Decisions

### Grouping and Konvolute

- The holding prefix before `/` of a shelfmark records provenance only and is no ordering category for users. The Konvolut mode of the correspondence gallery groups by B shelfmark (feedback of the archive staff, June 2026).
- Groups of the correspondence gallery with more than eight cards collapse behind a "show all" button (session with the archive, 2026-09-10).
- The stack link of a person heading in the gallery comes from the explicit `konvolut` reference of the correspondence index, and an ambiguous or missing assignment produces no link (2026-09-11).
- The direction of the Konvolut grouping is open, see [plan](plan.md#operator-questions).

### Visible design (2026-09-11, with later changes)

- The focus ring is two pixels of wine red at a small offset, shown only on `:focus-visible`.
- One form of view switch serves gallery, lists, indexes and density switches, text tabs with a gold underline under the title. The jump navigation below the tabs wraps onto further lines.
- On phones the entry buttons show an icon without visible text, with `aria-label` and a target area of 44 pixels.
- Large lists keep every entry in the DOM. The catalogue lists render completely, because skipping their group layout moved the first letter jump under the fixed header in the tested browser.
- The placeholder buttons of the letter edition are removed.
- Works keep the switch between category and year, library and autographs have their own year views, and the work index stays alphabetical because its data carry no reliable year or category.
- The English card date of the galleries uses month names.
- The menu item of `mode=miscellaneous` reads "Aktuelles", in English "News". The mode identifier stays `miscellaneous`.
- Text uses the brand gold `#c3a461` itself, although it stays below the WCAG AA contrast of 4.5:1 on white (operator decision of 2026-09-23, recorded in `css/tokens.css`).

### Indexes and sorting

- Index letter groups and order follow German library filing (DIN 5007-1). Letters with diacritics file under their base letter, ß as ss, Æ and Œ as AE and OE (operator decision of 2026-09-28).

### Theme pages and search

- A person on a theme page counts for the person search with or without `@type="person"` on its `name` (operator decision of 2026-09-23).
- The SPARQL queries of the search stay unchanged, because no SPARQL endpoint exists against which a change could be tested (operator decision of 2026-09-23). Which version this decision covers is an open question in the [plan](plan.md#operator-questions).

### Lebenskalender

- The multi-holding timeline (Zeitleiste) at `mode=timeline` is not published. Since 2026-10-09 the variable `timelineView` in `szd-static.xsl` is `false()`, every mode of the Lebenskalender renders the vertical view, and the menu links the biography without a timeline entry. Setting the variable to `$mode = ('timeline', 'fancy')` enables the view again.

### Letter edition

- `szd-Briefedition.xsl` with the object `o:szd.SZDBRI.1` stays as the prototype of a full-text letter edition. The missing branch in the RDF transformation is no reason to remove it (operator decision of 2026-09-29).

### Refactoring settings (operator decision of 2026-09-29)

- The test stub imports the real `szd-Templates.xsl`, and full-page builds replace the stub world over time.
- Versioned test data are the data repository commit and the few GAMS inputs, never rendered pages.
- Playwright becomes a development dependency for the computed-style comparison of the CSS stage.
- The start page carousel loses its autoplay (WCAG 2.2.2) and becomes a strip with visible previous and next controls.
- The letter edition keeps a conditional jQuery and Bootstrap include, every other page loses both.
- Icons become an SVG sprite with the paths of the current Font Awesome glyphs, credited under CC BY 4.0.
- The invisible Glyphicon remnants in the glossary and at one mail link are removed.

### Licences

- All content of the portal, data and texts, is published under CC BY 4.0, and the code of gams-www under MIT (operator decision of 2026-10-09).

### Documentation

- All documentation of gams-www is English, as is this knowledge base, with German project terms defined in the [glossary](INDEX.md#glossary) (2026-09-24).
- Development of gams-www runs on `develop`, and `main` carries the published state (2026-10-09), see [deployment-architecture](deployment-architecture.md#release-flow).
- Commit messages of gams-www are English (2026-10-09), following the global rule of the repository owner. Earlier commits are German.
