---
title: Data
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
related: [project, rdf-mapping, architecture, search-architecture]
---

# Data

The GAMS objects of Stefan Zweig Digital, their TEI sources and the datastreams that the ingest derives from them. The mapping from TEI to the `szd:` RDF of the search is described in [rdf-mapping](rdf-mapping.md), files, PIDs and encoding of each collection in [collections](collections.md) and data gaps and checkup results in [data-quality](data-quality.md). Stylesheets, scripts, styles and assets named in code formatting without a link lie in gams-www (https://zimlab.uni-graz.at/gams/projects/szd/gams-www).

## Sources

The curated TEI sources are maintained in this data repository [chpollin/SZD](https://github.com/chpollin/SZD) under `data/` and ingested into GAMS with Cirilo. gams-www holds no TEI source. The harness in [local-test-build/](../local-test-build/README.md) reads the data of this repository (or of `SZD_DATA_ROOT`) and renders a gams-www checkout found at `../ZIMLAB/szd` or in `SZD_WWW`, see [testing](testing.md#fixtures). Corrections of the data belong in the data repository.

## Objects

Primary data are TEI `listBibl` files, one object per holding.

| Object | Content |
|---|---|
| `o:szd.werke` | works (manuscripts and typescripts) |
| `o:szd.lebensdokumente` | personal documents, structured like the works |
| `o:szd.autographen` | autographs |
| `o:szd.aufsatzablage` | Aufsatzablage, Zweig's essay files |
| `o:szd.bibliothek` | Zweig's library |
| `o:szd.nli` | holdings of the National Library of Israel, rendered like the works |
| `o:szd.korrespondenzen` | correspondence index |
| `o:szd.korrespondenzen.<person>` | one Personen-Konvolut per correspondence partner |
| `o:szd.<number>` | METS object of one digital facsimile |

Secondary data are the indexes and the curated context.

| Object | Content |
|---|---|
| `o:szd.personen` | person index, `listPerson` |
| `o:szd.standorte` | repository index, `listOrg` |
| `o:szd.organisation` | organisation index, `listOrg` |
| `o:szd.werkindex` | work index, `listBibl` with `bibl` entries |
| `o:szd.lebenskalender` | Lebenskalender, `listEvent` |
| `o:szd.glossar` | glossary as SKOS, the controlled vocabulary `szdg:` |
| `o:szd.thema.<n>` | theme pages, TEI |
| `o:szd.ontology` | the `szd:` ontology |
| `o:szd.SZDBRI.1` | prototype of the full-text letter edition |
| `context:szd` | start page, About, Imprint, search help and the news entries as datastreams |
| `context:szd.facsimiles.*` | the facsimile galleries |
| `query:szd.*` | the five search objects, see [search-architecture](search-architecture.md) |

Every catalogue entry carries an `xml:id` with a holding prefix, `SZDMSK` (works), `SZDLEB` (personal documents), `SZDAUT` (autographs), `SZDESS` (Aufsatzablage), `SZDBIB` (library) and `SZDKOR` (correspondence), and index entries carry `SZDPER`, `SZDSTA`, `SZDORG` and `SZDWRK`. The shelfmark of a correspondence piece consists of the holding prefix before `/`, the B shelfmark `B<nr>` and the piece number, for instance `SZ-SAM/B7.3`. [correspondence-gallery-architecture](correspondence-gallery-architecture.md#three-konvolut-levels) explains the levels.

## Derived datastreams

Until 2026-10-28 this knowledge base described four ingest stylesheets of gams-www that run on the TEI or METS of an object. The reading of the Cirilo datastreams on staging and production on 2026-10-28 shows that only `szd-TORDF.xsl` is read from gams-www, where it stays. The other three are kept in [gams/](../gams/) of this repository, and [deployment-architecture](deployment-architecture.md#ingest-stylesheets-in-cirilo) records what each instance runs instead.

| Stylesheet | Input | Output | Purpose |
|---|---|---|---|
| `szd-TORDF.xsl` (gams-www) | TEI | RDF/XML (`szd:`) | search basis in Blazegraph, see [rdf-mapping](rdf-mapping.md) |
| [szd-TOMETS.xsl](../gams/szd-TOMETS.xsl) | GAMS viewer XML | METS with embedded MODS | facsimile and page viewer |
| [szd-MODStoDC_MAPPING.xsl](../gams/szd-MODStoDC_MAPPING.xsl) | MODS from the METS stream | OAI Dublin Core | OAI-PMH harvesting |
| [szd-tei-hssf.xsl](../gams/szd-tei-hssf.xsl) | TEI | Gnumeric spreadsheet | editorial and quality export |

The object metadata (Dublin Core, content model, memberships) come from the Fedora ingest itself and lie in the Mulgara resource index, independently of these stylesheets, see [architecture](architecture.md#gams-concepts).

### METS for the facsimiles

`szd-TOMETS.xsl` produces from the GAMS viewer structure (`vi:book`) a METS document compatible with the DFG Viewer. The value that runs is the inline datastream `cirilo:szd/TOMETS`. Its production value equals the former gams-www file plus one `xsl:value-of select="vi:category"`, and [gams/szd-TOMETS.xsl](../gams/szd-TOMETS.xsl) is a byte copy of that production datastream as served on 2026-10-28. The staging value differs from both. The list below describes the former gams-www file.

- `mets:dmdSec` with embedded MODS (title, names with roles, language, `originInfo`, subject and genre, the shelfmark as `mods:note[@type='signature']`)
- `mets:amdSec` with the DFG Viewer rights (`dv:rights`, `dv:links`)
- `mets:fileSec` with one `mets:file` (image/jpeg) per `vi:page` and its `FLocat`
- `mets:structMap` of `TYPE="PHYSICAL"` (page sequence) and `TYPE="LOGICAL"` (structure)
- `mets:structLink`, which links logical units to physical pages

A catalogue entry reaches its facsimile through `szd:facsimile` in the RDF or through `altIdentifier/idno[@type='PID']` in the TEI.

### Dublin Core for harvesting

`szd-MODStoDC_MAPPING.xsl` is an XSLT 1.0 crosswalk. Neither instance references it (read on 2026-10-28). `cirilo:szd/DC_MAPPING` is a short generic mm:metadata-mapping, identical on staging and production, and [gams/szd-MODStoDC_MAPPING.xsl](../gams/szd-MODStoDC_MAPPING.xsl) is kept as a documented copy. The description below is that of the copy. It loads the METS stream of the object at runtime and maps MODS to Dublin Core. Fixed values are `dc:publisher` Literaturarchiv Salzburg and University of Salzburg, `dc:rights` CC BY 4.0 and `dc:relation` "STEFAN ZWEIG DIGITAL". Object types and subject groups are derived heuristically from shelfmark and title (`/W` a work, `/L` a personal document, `/AK` a picture postcard, `/B` a letter, "tagebuch" the diaries), an error-prone layer independent of the search.

### Spreadsheet export

`szd-tei-hssf.xsl` writes a Gnumeric workbook (`gmr:Workbook`) for editorial and quality checks and branches by PID. Neither instance references it. `HSSF_STYLESHEET` and `TEItoHSSF` of `cirilo:szd` are generic inline Gnumeric templates on staging, and `HSSF_STYLESHEET` answers 404 on production (read on 2026-10-28). [gams/szd-tei-hssf.xsl](../gams/szd-tei-hssf.xsl) is kept as an editorial export tool. Works and personal documents give collection, SZD ID, author, SZDPER, title, object type, repository, language and date, library and autographs give SZD ID, author, title, description, extent and binding, acquisition and repository. Missing values are marked "nope" or "xxx".

## Timeline lane files

`data/lebenskalender/` in gams-www holds the derived data of the multi-holding timeline, four lane files (`biography.json`, `correspondence.json`, `personal-documents.json`, `autographs.json`) and `index.json` with the generator state. The generator [scripts/lebenskalender_lanes/build_lanes.py](../scripts/lebenskalender_lanes/README.md) of this repository derives them from the Lebenskalender, the correspondence including every Konvolut, the personal documents and the acquisition data of the autographs, and [lebenskalender-lanes](lebenskalender-lanes.md) describes schema and selection rules. An update copies the matching generator state as a whole, so the timeline shows later TEI changes only after the files have been generated and copied again. The files carry relative links such as `/o:szd.korrespondenzen/sdef:TEI/get#SZDKOR.n`, so that staging links stay on staging.

The generator merges facsimile duplicates only when they share a non-empty shelfmark and carry no contradicting concrete date or place. An event of the correspondence index carries `konvolut` (the relative URL of the Konvolut object that lists its pieces), `repository` (only for holdings outside the Literaturarchiv Salzburg) and `extent`.

The timeline view is switched off since 2026-10-09, see [specification](specification.md#lebenskalender), and no page loads these files while the switch is off.

## Known data issues

- The person index, the library, the works, the Lebenskalender and the glossary write part of their names in decomposed Unicode (NFD) beside precomposed forms. The index sort compensates through `fn:filing-key`, other string comparisons do not. Normalising the sources to NFC is a decision for the data repository.
- Some Konvolut letters carry dates after 1950, mostly two-digit years that `@when` places in the twenty-first century. The timeline holds them back, and the correction belongs in the TEI sources.
- The data gaps and checkup results recorded on the data side are in [data-quality](data-quality.md), the open corrections in the [plan](plan.md#data-side).
- The `dc:title` values of the Konvolut objects follow several patterns, see [correspondence-gallery-architecture](correspondence-gallery-architecture.md#metadata-quirks).
- The Lebenskalender entry `SZDBIO.5` lacks its German `<date>` element and is therefore missing from the vertical view, which groups by the machine-readable date of the leading head line, while the lane derivation includes it.
