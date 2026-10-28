# proto

Local prototypes for decisions on the correspondence gallery and the biography. Nothing here is deployed, and the production code in `js/` and in the stylesheets stays untouched. The Konvolut prototypes belong to way 1 of the open decision in the [plan](../../knowledge/plan.md#operator-questions), described in [knowledge/correspondence-gallery-architecture.md](../../knowledge/correspondence-gallery-architecture.md#coupled-konvolut-view), grouping the correspondence gallery by the curated Personen-Konvolute `o:szd.korrespondenzen.<person>`.

## Coupled Konvolut view

- `facsimiles-konvolut-proto.js` hooks into the built preview page, adds a third button "Nach Konvolut (Erschließung)", rewrites the card images to IIIF derivatives and collapses groups with more than eight cards.
- `konvolut-map.json` is the assignment table, generated from the index `o:szd.korrespondenzen` and the DC titles of the Konvolut objects.
- `build-konvolut-map.py` regenerates the table and loads index and DC titles into `build/` when they are missing.
- `proto.smoke.mjs` checks the view in jsdom against the real `build/szd-Facsimiles.html`.

### Rebuilding

All steps run from `local-test-build/`.

1. `bash run.sh szd-Facsimiles build/szd-Facsimiles.input.xml de` builds the preview page.
2. `python proto/build-konvolut-map.py` loads index and DC titles into `build/` if needed and writes the table.
3. Hook the prototype script in behind the production script in `build/szd-Facsimiles.html` with
   `sed -i 's#js/facsimiles-konvolut.js"> </script>#&<script src="http://localhost:8080/local-test-build/proto/facsimiles-konvolut-proto.js"> </script>#' build/szd-Facsimiles.html`.
4. `node proto/proto.smoke.mjs` checks, `bash serve.sh` serves.

Then open `http://localhost:8080/local-test-build/build/szd-Facsimiles.html`.

### Limits

The assignment of piece to Konvolut runs through the person heading, because the index carries the reference only at Konvolut level. A piece with two partners appears in both Konvolute. A production version needs the Konvolut PID per piece in the gallery result.

Thumbnails and collapsing have since moved into the application code. The prototype respects the marker of already handled groups and adds no second expand button there. `proto.smoke.mjs` checks the interplay with the current gallery script, `test/konvolut.smoke.mjs` the regular views.

## Lebenskalender

`lebenskalender-proto.html` is a second, independent prototype, an alternative presentation of `o:szd.lebenskalender` that reads the TEI datastream directly (`build/lebenskalender.xml`, obtained with `run.sh szd-Lebenskalender <TEI_SOURCE URL>`, which stores the datastream as `build/szd-Lebenskalender.input.xml`, copied from there under this name). Compared with the production page it adds a fixed year scale with event density and jump, a place filter from the head of the entries, a compact and full-text switch and a language change without reload. `lebenskalender.smoke.mjs` checks parsing, filters and language change in jsdom. It is opened at `http://localhost:8080/local-test-build/proto/lebenskalender-proto.html`.

`lebenskalender-szd-template.html` and `build-lebenskalender-szd.py` produce the same view inside the real page shell of stefanzweig.digital (navbar and footer of the live page, stylesheets through `<base>`) for the documentation site of the data repository (`docs/lebenskalender/index.html`). The generator prints the target path before writing, check it before it runs.

## Timeline with lanes

`zeitleiste-lanes.html` with `zeitleiste-lanes.css` and `zeitleiste-lanes.js` is the prototype of the timeline view decided in the frontend overhaul of September 2026, the biography with the holdings as lanes that can be switched on and off. Since 2026-09-11 the integrated view at `mode=timeline` supersedes it, which is switched off since 2026-10-09. That view is described in [rendering-architecture](../../knowledge/rendering-architecture.md#lebenskalender), and whether the prototype stays is an open question in the [plan](../../knowledge/plan.md#operator-questions).

The page carries navbar and footer of the live page, loads their stylesheets through `<base>` and brings only the control row, the scale and the list. It was built to judge whether the four lanes are understandable, the scale as main element and the arrangement of the controls, not the fine tuning of spacing.

A single row holds the controls, on the left the four lane chips with symbol, colour dot and count, on the right the place as dropdown with a search field, the person filter as narrow field with suggestions from the persons of the active lanes and the text tabs full text and compact. Set filters appear as removable chips in a second row that is otherwise absent. Below the tablet breakpoint the control row collapses behind a button "Filter", while the scale stays visible. Compact shortens letters, personal documents and autographs to one line and leaves the biography unchanged.

The scale shows for each active lane a row of bars with the number of dated events per year, without base line and grid lines, and below it a year axis with fine ticks and decade labels. A cursor follows the scrolling, a click on a year jumps, dragging across the bars selects a period, and year and count per lane appear only on hover or focus as a tooltip. Lanes, place, person, period, language and density stand as query parameters in the URL, the targeted year in the fragment, so the view can be shared. The integrated view keeps its filters in the fragment instead, because GAMS rejects further query parameters.

The data are the lane files of the data repository, described in `knowledge/lebenskalender-lanes.md` of the data repository `chpollin/SZD` and produced by `scripts/lebenskalender_lanes/build_lanes.py`. They lie under `data/` as fixtures, copied from `data/derived/lebenskalender/`, and the data repository stays untouched. A new copy means copying the five files into `proto/data/`.

It is opened from `local-test-build/` with `bash serve.sh`, then `http://localhost:8080/local-test-build/proto/zeitleiste-lanes.html`. The page shell comes live from stefanzweig.digital, so the call needs an internet connection. `node proto/zeitleiste-lanes.smoke.mjs`, part of `npm run test:proto`, checks in jsdom the loading of all lanes against the counts in `index.json` minus the held-back pieces, the year limit 1950, the structure of a row with lane symbol, switching a lane off and on in scale and list, the place selection in the dropdown with search, the filter chip of the second row, person and period filters, the tooltip on the axis, the plural of the entry count, the language change, the position of the undated pieces and the collapsing of the control row.

### Limits of the prototype

Only the year groups in or near the viewport are rendered, the others keep their height as placeholders. Browser search therefore finds only what is rendered at the moment, and the estimated placeholder height differs from the real one, so the scrollbar jumps when groups are rendered later. The integrated view keeps every visible entry in the DOM and limits the layout work with `content-visibility`.

Scale and list end in 1950. Three correspondence pieces of the unidentified Konvolut carry dates in the years 2012, 2018 and 2030, visibly misread years of the source. They stay out of the view, and the script counts them and writes them with identifier and date to the console. The correction belongs in the TEI source of the correspondence index, not in the display. The letters up to 1947 stay, since correspondence of the estate after Zweig's death is plausible.

The year cells of the axis are narrower than 24 pixels across a span of about seventy years. A click on the taller bar area above triggers the same jump, and all other controls keep the target size. The language switch of the navbar remains a `span` of the live page shell and only receives a role, keyboard use and the change without reload here.
