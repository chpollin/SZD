---
title: Correspondence gallery architecture
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD  # the served files it describes are in https://zimlab.uni-graz.at/gams/projects/szd/gams-www
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: complete
language: en
created: 2026-06-16
updated: 2026-10-28
authors: [Christopher Pollin]
generated-with: Claude Code (Claude Opus 5.5)
related: [rendering-architecture, data, deployment-architecture, konvolut-title-curation, plan]
---

# Correspondence gallery architecture

Stylesheets, scripts, styles and assets named in code formatting without a link lie in gams-www (https://zimlab.uni-graz.at/gams/projects/szd/gams-www). How the facsimile gallery of the correspondence groups its cards by correspondence partner and by Konvolut, where its data come from and how its grouping relates to the curated Personen-Konvolute. Page frame and view switch are described in [rendering-architecture](rendering-architecture.md), the open direction of the Konvolut grouping in the [plan](plan.md#operator-questions).

## The page

`context:szd.facsimiles.korrespondenzen` is a context object (`cm:Context`). `…/sdef:Context/get?locale=de` renders it through `szd-Facsimiles.xsl` in the branch `$cid = 'context:szd.facsimiles.korrespondenzen'` as a card gallery. The default view groups by correspondence partner, a second mode by Konvolut.

## Data flow

The gallery result is the SPARQL query in the `QUERY` datastream of the context object, run against the Mulgara resource index. The query, and not the stylesheet, fixes the result schema. The production query selects `container`, `cid`, `pid`, `model`, `title`, `identifier`, `creator` and optionally `contributor` and `date`, all from the Dublin Core of the member objects.

```sparql
select distinct * where {
  <fedora:context:szd.facsimiles.korrespondenzen> <dc:title> ?container .
  <fedora:context:szd.facsimiles.korrespondenzen> <dc:identifier> ?cid .
  ?pid <fedora-rels-ext:isMemberOf> <fedora:context:szd.facsimiles.korrespondenzen> .
  ?pid <fedora-model:hasModel> ?model .
  ?pid <dc:title> ?title .
  ?pid <dc:identifier> ?identifier .
  ?pid <dc:creator> ?creator .
  OPTIONAL{ ?pid <dc:contributor> ?contributor . }
  OPTIONAL{ ?pid <dc:date> ?date . }
  filter regex(str(?model), "^info:fedora/cm:")
}
```

The stylesheet groups by `creator` and `contributor`. A `QUERY` datastream without these fields, such as the generic GAMS context query with `ownerId`, `createdDate`, `lastModifiedDate` and `description`, leaves every grouping key empty, and the gallery renders nothing although the object metadata are correct. The fix is to bring the datastream to the production version in Cirilo, without a new ingest. The result of the query is readable as the datastream `METADATA` of the context object, and the harness renders the gallery from a versioned copy of it.

## Three Konvolut levels

The shelfmark of a card stands at the end of its title (`…, SZ-SAM/B7.3`). Three levels have to be kept apart. The first two derive syntactically from the shelfmark, the third is the curated Konvolut axis of the project.

- Bestand (holding), the prefix before `/`, for instance `SZ-SAM`. It records provenance only and bundles the correspondence of many partners.
- B shelfmark, `B<nr>` after `/`, for instance `SZ-SAM/B7`, the physical bundle within a holding.
- Personen-Konvolut, `o:szd.korrespondenzen.<person>`, rendered by `szd-Konvolut.xsl`. It is the curated edition of the correspondence with one person, with a readable title and a page of its own. Entries of the correspondence index that belong to a Personen-Konvolut carry its PID in `msIdentifier/altIdentifier/idno[@type='konvolut']`.

After the `/`, shelfmarks fall into three classes, and only `B` carries a Konvolut level.

| Class | Example | Konvolut level |
|---|---|---|
| `B<nr>.<piece>` | `SZ-AAP/B1.107` | `SZ-AAP/B1` |
| `AK.<nr>` | `SZ-SAM/AK.105` | none, picture postcards |
| `L<nr>` | `SZ-AAP/L10` | none, loose single pieces |

Compared with the curated `konvolut` references, the B shelfmark mostly maps one to one onto a Personen-Konvolut (`SZ-LAS/B1` is Masereel). `SZ-SAM/AK` merges the Personen-Konvolute of all postcard senders, which have long been curated by sender. A few B shelfmarks are coarser than the curation, `SZ-LAS/B7` splits into Anna and Sigmund Freud and `SZ-AAP/B10` into members of the Zweig family. Most B Konvolute have exactly one partner and coincide with the person view, so the B view adds something only for the collective ones. The Konvolut in the sense of the project is therefore the correspondence with one person.

## Person view

The default view groups by `creator` and `contributor` except Zweig. Pieces with Zweig as creator and no bound contributor fall into a catch-all group "Ohne Korrespondenzpartner" ("Without correspondent"), so that no piece is lost. A letter appears under sender and receiver with the same `pid`.

The stack icon of a person heading links to the Personen-Konvolut. `fn:bundle-pid` reads the correspondence index once and assigns the PID from the explicit `idno[@type='konvolut']` reference of the exactly normalised partner name. Only a unique, syntactically valid PID produces a link, and a missing or ambiguous assignment produces none. Links keep the current host and language. The former name-based slug (`fn:konvolut-slug`) remains for stable heading anchors. PIDs such as `o:szd.korrespondenzen.birman-c.` keep their final dot.

## Konvolut mode

The second mode groups the same cards by B shelfmark. It runs on the client in `js/facsimiles-konvolut.js`, because the rendered HTML already carries the necessary information.

- In the correspondence branch, `szd-Facsimiles.xsl` sets `data-pid`, `data-signatur` and `data-konvolut` on every card and gives the gallery container the `id` `facsimiles-gallery`. `data-konvolut` is the B level (`SZ-AAP/B1.107` becomes `SZ-AAP/B1`), while `AK` and `L` fall into one group per holding (`SZ-SAM/AK`, `SZ-AAP/L`). A card carries for instance `data-pid="o:szd.377" data-signatur="SZ-SAM/AK.1" data-konvolut="SZ-SAM/AK"`.
- The switch is the shared `getListViewSwitch` in the sticky header with the modes `person` and `konvolut` ("Person", "Konvolut", in English "Bundle"), see [rendering-architecture](rendering-architecture.md#view-switch).
- The script regroups the cards by `data-konvolut`, hides the person-based jump navigation in Konvolut mode and publishes the regrouping as `window.setFacsimilesView`. Without cards carrying `data-konvolut` it hides the switch, so stylesheets and script are deployed together.
- `mode=konvolut` in the URL opens the Konvolut view directly. A mode change updates the URL and keeps other parameters and the fragment, browser back and forward restore the view, and a language change keeps the gallery as target.
- Each view keeps its DOM nodes, including expanded groups, and a repeated click on the active mode changes nothing.
- Deduplication follows `data-pid`, because different objects can share a shelfmark (`SZ-AAP/B2.3` on two PIDs).
- `konvolutLabel()` supplies the group heading, the curated title from `KONVOLUT_TITLES` (key is the B shelfmark, values de and en) or a readable fallback such as `Konvolut SZ-LAS/B7`, `Ansichtskarten SZ-SAM` or `Einzelstücke SZ-AAP`. `KONVOLUT_TITLES` is empty until the archive staff supply titles, see [konvolut-title-curation](konvolut-title-curation.md).
- Groups with more cards than `COLLAPSE_AFTER` (eight) show only the first cards and hide the rest behind a "show all" button, in both views. Handled groups are marked, so a repeated call adds no second button.

## Cards

A card embeds an IIIF derivative from the image server of `gams.uni-graz.at`, `…/iiif/<pid>/IMG.1/full/400,/0/default.jpg` as `src` with a `srcset` of 400 and 800 pixels width, `sizes` matching the column grid, `loading="lazy"` and `decoding="async"`. The master datastream `IMG.1` is too large for a card and `THUMBNAIL` too small, and the IIIF path is not reachable under `stefanzweig.digital`, so the cards address the GAMS host directly. The card is the same in every facsimile gallery.

The card text consists of date and shelfmark. The date comes from the Dublin Core of the object, mostly in German day notation and in single records as a machine date. A shared template brings both forms into the notation of the page language, the dotted day form in German and the form of the Lebenskalender in English ("7 January 1933"), and passes everything else, such as an inferred date in square brackets, unchanged. The shelfmark is printed only when the title really ends with one.

## Metadata quirks

The facsimile metadata stay untouched by project decision, and the frontend compensates.

- The `dc:title` values of the Konvolut objects follow several patterns, mostly "Korrespondenz <name>: Stefan Zweig digital", some with surname first, some with the suffix "digitale", and some objects of the Altmann family carry "Untitled". A heading taken from the title cuts the suffix and falls back to the person name, and sorting uses the person name of the heading. Harmonising the titles belongs in the data repository.
- For large Konvolute the partner assignment from Dublin Core can differ from the archival definition. `SZ-AAP/B1` lists many partners but is "Reichner" according to the archive.
- The partner names in `creator` and `contributor` do not always match the index, through diacritics, dots after initials or typos (`Podbieliki` in the gallery, `podbielski` in the Konvolut PID).

## Coupled Konvolut view

A local prototype in [local-test-build/proto/](../local-test-build/proto/README.md#coupled-konvolut-view) groups the gallery by Personen-Konvolut without a GAMS change. It assigns a piece to a Konvolut through the person heading, because the index carries the `konvolut` reference at Konvolut level only, so a piece with two partners lands in both Konvolute and the coupling depends on matching names. A production version needs the Konvolut PID per piece in the gallery result, that is an extension of the context query. Whether that reference reaches the Dublin Core in Mulgara at all or exists only in the `szd:` RDF in Blazegraph is not yet clarified.

## Checks

[konvolut.smoke.mjs](../local-test-build/test/konvolut.smoke.mjs) checks the regrouping against the rendered HTML (B, AK and L grouping, curated title first, AK and L not labelled as Konvolut, deduplication by `pid`), the IIIF thumbnails, collapsing in both views, direct call, browser history, keyboard use and the preservation of expanded groups. [stack-link.smoke.mjs](../local-test-build/test/stack-link.smoke.mjs) checks the source-based stack links and `fn:bundle-pid` on constructed index files. Both are part of `npm run test:pages`, see [testing](testing.md).
