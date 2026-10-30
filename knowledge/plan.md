---
title: Plan
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: active
language: en
created: 2026-09-24
updated: 2026-10-30
authors: [Christopher Pollin]
generated-with: Claude Code (Claude Opus 5.5)
related: [specification, journal, governance, deployment-architecture]
---

# Plan

The accepted open technical work on the data repository and on the presentation layer in gams-www, and the questions that need a decision by the operator or the archive. A finished item leaves this list, and its outcome goes into the [journal](journal.md). Standing decisions live in the [specification](specification.md). The work is grouped into a data side, a presentation side and the operator questions of both. The presentation side also lists the Cirilo reference readings of staging.

## Data side

### Staging ingest

The ingest runs from a package that `scripts/staging_package/build_staging_package.py --out <folder>` writes outside the repository from the current `HEAD`, in the order indexes, holdings, Konvolute, because `szd-TORDF.xsl` resolves persons, repositories and corporate bodies against the index objects at ingest time. The operator ingests each folder with Cirilo ([deployment-architecture](deployment-architecture.md#ingesting-tei-with-cirilo)).

The package of the data state of 2026-09-24 went in completely that afternoon, and Cirilo created the Konvolute missing on staging. Indexes and Konvolute on staging match the repository. Still open:

- Set the references the package README lists per object, read live from staging. Most existing Konvolute and several holdings carry a `TORDF` reference that ends in an illegal character, so their RDF is not regenerated, and the Konvolute created by the ingest carry the generic `tei.xsl` as `STYLESHEET` instead of `szd-Konvolut.xsl`. The presentation side records the same staging reading in [Staging, reading of 2026-09-24](#staging-reading-of-2026-09-24).
- Then ingest the folders `2-bestaende` and `3-konvolute` again. The holdings went in before the organisation fallback of `szd-TORDF.xsl` was on the mirror, so the RDF of library, correspondence and personal documents still lacks the corporate bodies resolved by GND. Their `RDF` datastreams show afterwards whether the ingest reaches the staging organisation index.

On staging after the ingest:

- Delete `o:szd.375`, `o:szd.263`, the two sister Konvolute, `o:szd.publikation` and `o:szd.korrespondenzen.ferencak-mirko-m.`, and carry signature and date into `o:szd.2939` (decisions of 2026-09-22 and 2026-09-23).
- Re-ingest the prepared book sources of `scripts/iiif_structure_labels/prepared/` into `o:szd.174`, `o:szd.67`, `o:szd.939`, `o:szd.2935`, `o:szd.2409` and `o:szd.2291`, then check that each manifest is valid JSON.
- The fix of the autograph RDF in `szd-TORDF.xsl` is on the mirror. `o:szd.autographen` still points its `TORDF` to the dead path `trunk/www` and gets its corrected RDF with the renewed ingest of `2-bestaende` once the reference is set.

For the Klawiter bibliography `o:szd.klawiter` (`data/Klawiter/SZDKLA.xml`), after push and synchronisation of the gamsdev mirror with `szd-klawiter.xsl`, the `Klawiter` branch of `szd-TORDF.xsl` and the row in `szd-Suche.xsl`:

- Ingest the TEI file alone into a new object under `cirilo:TEI.szd`. The staging package builder does not list it yet.
- Set `STYLESHEET` to `https://gams-staging.uni-graz.at/gamsdev/pollin/szd/gams-www/szd-klawiter.xsl` and check that `TORDF`, inherited from the content model, names the `szd-TORDF.xsl` of the mirror, both ending directly with `.xsl`. If a reference had to be corrected, ingest again, and check that the `RDF` datastream holds `szd:Manifestation` resources instead of the text "No data source define!".
- Copy `gams/query/fulltext_search.sparql` with the line `FROM <o:szd.klawiter>` into the datastream `QUERY` of `query:szd.fulltext`.
- Production follows only after the identifier scheme of the bibliography is decided ([rdf-mapping](rdf-mapping.md#klawiter-bibliography)), with the production base `https://gams.uni-graz.at/szd/` for both references.

Staging is not reachable for development since 2026-10-13, as the presentation side records.

### Production ingest

The corrections reach production only after the archive has approved them on staging, in the same order as on staging. Until then `o:szd.personen` in production keeps the persons removed from the repository on 2026-09-24, and the production Konvolute keep the defects corrected here. Partner review and publication of the timeline are pending as well, see [lebenskalender-lanes](lebenskalender-lanes.md#delivery-state). The production readings of October 2026 are in [Production](#production) on the presentation side.

### Konvolute

- Three production objects are defective and stay out of the staging package, because their files do not name their own PID. `o:szd.korrespondenzen.judischer-jugendverein` and `o:szd.korrespondenzen.judischer-jugendverein-dusseldorf` are two objects for one body, and both name the obsolete PID `o:szd.korrespondenzen.judischer-jugendverein-(dusseldorf)`. `o:szd.korrespondenzen.rascher-und-cie` carries the content of `alberts-margot` and no PID of its own. Operator question, which of the two Jugendverein objects stays, and where the correct content of the Rascher Konvolut can be recovered from.
- Left untouched by `scripts/checkup_2026_09_konvolute/fix_konvolut_defects.py` because the correct value is not established. Specht Richard `SZ-SEF/B9.1` (recipient Richard Specht or Lotte Altmann, archive at the original). `SZ-SAM/B18.1–3` (which date belongs to which piece, archive). `SZ-LAS/B3.33–35`, carried by both `fleischer-max` and `fleischer-victor` with diverging content (which object is canonical, operator). The remaining `needs-archive` and `needs-operator` items of the archive-internal operator report.
- Thalhuber `SZ-SAM/B17`. The defect lies in the correspondence index `SZDKOR.xml`, which the Konvolut script does not write. Technical, a correction with evidence in the index scripts.
- Dates after 1950. The imported Konvolute `bahr-hermann`, `feld-leo`, `freud-sigmund`, `heidelbach-paul`, `jeanrenaud`, `kaemmerer-ami`, `kaemmerer-maria`, `kubin-alfred`, `mees-friedrich-siegbert`, `unidentified` and `winternitz-friderike-von` carry `@when` values after 1950 (read on 2026-09-24). Most look like the century error of two-digit years described in [data-quality](data-quality.md#century-error-in-two-digit-years), while family letters may genuinely be later. Where title or display text proves the year, `scripts/korrespondenz_titel/fix_titles.py` corrects it, the rest needs an editorial decision. Its dry run is ready and logs every change, the run with `--apply` waits on the operator.
- `SZDKOR.reitter-eugenie.65` is dated 29 February 1934, a day that does not exist. Only the original can give the date.
- The `dc:title` values of the Konvolut objects follow several patterns ([correspondence-gallery-architecture](correspondence-gallery-architecture.md#metadata-quirks)). The header titles of the Konvolut files are their source.

### Timeline lanes

The lanes are generated from the complete Konvolute, and the corpus tests pin that state. The run messages leave editorial work in the Konvolut data.

- Facsimile groups whose records conflict and therefore stay separate, listed in `CONFLICTING_FACSIMILES` of the test. About half concern places that the Konvolut `zweig-friderike` gives as Salzburg against the sender's place in `fleischer-victor` and `fleischer-max`. Others involve the pairs `glucksmann-heinrich` and `gluecksmann-heinrich` or `meulenhoff` and `meulenhoff-johannes-marius`, which look like duplicate objects, and coarser dates in `reichner-herbert` and `meingast-anna` against day dates of the partner's record. In the two Jugendverein files one copy of `SZDKOR.judischer-jugendverein.1` carries a date as its place. `o:szd.3204` and `o:szd.3317` stand at records with different signatures and dates, and at `o:szd.909` one record dates 2019 for 1919 and one sits in the file `masereel-frans` with a `reichner-herbert` identifier.
- Konvolut dates after 1950 whose display text gives a two-digit year that `@when` places in the twenty-first century.
- `SZDKOR.696` names `o:szd.korrespondenzen.unbekannt` and `SZDKOR.857` names `o:szd.korrespondenzen.podbielski-gert-rene`, while the repository holds the probable counterparts `unidentified` and `podbieliki-gert-rene`. Which spelling is the correct PID is an operator question, and until then the two index entries carry no `konvolut` link. The audit of 2026-10-13 found the same pair, see [Audit findings of 2026-10-13](#audit-findings-of-2026-10-13).
- Konvolut files that reuse the `xml:id` values of another Konvolut, which the run lists and the lanes resolve with a file suffix. The largest group is `friedenthal-richard`, `masereel-frans` and `reichner-herbert`, the others involve `czech-suzanne`, `suzanne-czech`, `international-copyright-bureau-ltd.-the`, `heilbron-george`, `fleischer-max`, `fleischer-victor` and `max-und-victor-fleischer`, and the pairs `judischer-jugendverein` and `judischer-jugendverein-dusseldorf`, `meulenhoff` and `meulenhoff-johannes-marius`, `muller` and `muller-einigen-hans`, `weisflog` and `weisflog-heinrich`. Correcting the ids in the Konvolut files is editorial work.

### Person index

- `scripts/checkup_2026_09_index/find_unlinked_persons.py` classified 45 persons as "Kandidat gefunden" and 68 as "nur Nachname" in the run of 2026-09-24. The review list is archive-internal and stays outside the repository. A person is linked only where the text hit identifies the index entry unambiguously.
- Operator decisions on the colour-coded archive list. The entries "Filed as …", "Unidentified signatures" and "Zweig Family", the names marked bold, and whether unlinked names the archive wants removed leave the index beyond the certainly unreferenced persons removed on 2026-09-24. Also with the operator are the divergent forenames between holdings and index (Altmann, Miller, Bischoff), persons named only in titles and running text, and Kuro Masu and Králík, whose envelope already points to another entry.
- Archive question, whether the entry for Neumann means the writer or the architect of that name.
- `SZDPER.1026` (Neydisser) has been a name variant of `SZDPER.818` (Lernet-Holenia) since `a108c6f3`, while the library still names the pseudonym's own GND. `SZDPER.1304` never existed, and the body it means, the Selbsthilfevereinigung der jüdischen Blinden in Deutschland, has no entry in the organisation index.
- Correspondence partners whose GND in `SZDKOR.xml` is missing from their index entry, and person references in `SZDKOR.xml` that carry `gnd/placeholder`.
- `SZDPER.1680` carries two GND numbers on one `persName`, separated by " / ", and `SZDKOR.zweig-friderike.89` has the name "Zweig, Friderike" in `@ref` instead of a reference. `SZDKOR.371` and `SZDPER.1858` carry the eleven-digit number 11055719711, which fits no GND form.
- Several `@ref` values in `SZDKOR.xml`, `SZDPER.xml`, `SZDMSK.xml`, `SZDAUT.xml` and the Konvolut `kaemmerer-ami` begin or end with whitespace. Because `GetPersonlist` takes the part before the first space, a leading space probably leaves the mapping an empty value and loses the person. Trimming is deterministic, but the operator has not yet decided it.
- The check scripts do not read identifiers with a letter suffix such as `SZDPER.2080a` as references.

### Organisation and location index

- Entries still without country or place after the GND reconciliation, because their GND record gives no geographic code, names several places (Herbert Reichner Verlag, `SZDORG.24`) or is missing.
- `SZDORG.15` joins the British Museum and the dealer David H. Lowenherz under GND 38379-X, which belongs to the museum. The dealer needs a number of its own or none. GND 117322695 at "Schweizerisches Vereinssortiment Olten" in `SZDKOR.xml` is a person's number. Both are recorded in [scripts/organisationen_index/](../scripts/organisationen_index/README.md#open-findings-in-the-source-data) for an editorial ruling.
- `SZDSTA.xml` has had no `geo` elements since the data update of June 2021 (`1ed133c2`), so the location RDF carries no coordinates.

### Reconciliation

- A reconciliation script adds Wikidata identifiers through the GND (Wikidata property P227) and writes only unambiguous hits, each with its provenance. It checks the existing GND numbers against the German National Library (DNB) or lobid for existence and redirects and reports contradictions to Wikidata. Persons without GND receive only a suggestion list. Corporate bodies carry no Wikidata identifier yet, and `szd-TORDF.xsl` has no `szd:wikidata` output for them (presentation layer).
- A place list with GeoNames identifiers as the first step of a places index, starting with the autographs (proposed 2026-09-18, not begun).
- The Klawiter links in `ontology/reconciliation.ttl` rest on title matching with a percentage score. A reconciliation of the works by authority numbers is open.

### Audit findings of 2026-10-13

These corrections belong in the data repository, found by the audit of the live site of 2026-10-13.

- The correspondence index names `o:szd.korrespondenzen.podbielski-gert-rene`, while the Konvolut is `podbieliki-gert-rene`, and `o:szd.korrespondenzen.unbekannt`, which has no file.
- `szd.korrespondenzen.freud-sigmund`, `szd.korrespondenzen.unidentified` and `szd.korrespondenzen.rascher-und-cie` still contain double-encoded UTF-8.
- Facsimile targets that do not exist: `o:szd.8360` (theme page 1, English), `o:szd.8250` (news item 4), `o:szd.8231`, `o:szd.8232` and `o:szd.8249` (theme page 2).
- The Aufsatzablage holds an entry with the empty identifier `xml:id="SZDESS."`, two person entries have empty GND and Wikidata links (`SZDPER.2143`, `SZDPER.2299`), and the English part of `webpage/MISCELLANEOUS.xml` numbers two news items `n="2"`, and `SZDAUT.218` carries an empty `provenance` element beside its filled one.
- Several Konvolut files are linked from no index entry, several of them apparent duplicates such as `moeller-rudolf` and `moller-rudolf`.

### Scripts and documentation

- `reconcile_klawiter.py` and `generate_instances.py` with `reconciliation_report.md` and `reconciliation_results.json` stay at the top level of `scripts/`. They belong with the ontology, and a move changes the generator comments of `ontology/reconciliation.ttl` and `ontology/sample-instances.ttl`, `ontology/README.md` and [ontology](ontology.md), so it goes together with the next ontology regeneration.
- `scripts/check_data.py` runs before every staging package. Its checks for NFC, for correspondence dates after 1950 and for whitespace in `@ref` only warn until the operator decides NFC normalisation, the century corrections and the trimming. A decided check then moves into the enforced set with its remaining findings as known exceptions. The known exceptions of the enforced checks are the open findings listed in this plan.
- `scripts/checkup_2026_09_konvolute/fix_konvolut_defects.py --verify` finds, for several of its entries, neither the old nor the new value any more. Which later change replaced them is not yet traced.
- The Python tooling of the repository (`pyproject.toml`, `uv`, `ruff` configuration, pre-commit) is an operator decision. Until then the scripts touched in September 2026 are checked with the `ruff` rule set of the house style from the command line, and the formatter has not been run over the holdings.
- `scripts/SZ-AAL-Pipeline/` holds a second, diverging `szd_pipeline.py` beside `scripts/Processing Pipeline/` and has no README. Which one stays?

## Presentation side

### Cache and image download deployment

The asset-version and download fixes must reach production as one release after local verification. The GAMS operators still need to apply and verify the response policy in [deployment architecture](deployment-architecture.md#asset-releases-and-cache-headers). Check the download on the SZD domain after release, because other hosts do not expose its cross-origin failure.

### GAMS objects and references

These items need the operator, because they are Cirilo settings or ingests, see [governance](governance.md#who-does-what). The target values are listed in [deployment-architecture](deployment-architecture.md#cirilo-references).

#### Production

`local-test-build/check-instance.py --instance production --data` reads every reference, query and `RDF` datastream and compares every `TEI_SOURCE` with the data repository. Its checklist is the current list of open operator steps. The state of 2026-10-13, during the operator's re-ingest:

- The operator set the `TORDF` references of `o:szd.werke`, `o:szd.lebensdokumente`, `o:szd.standorte`, `o:szd.bibliothek` and `o:szd.lebenskalender` from the retired host glossa to `https://gams.uni-graz.at/szd/szd-TORDF.xsl` and re-ingested indexes, holdings and theme pages. The RDF of works, personal documents, organisation, locations, work index, biography, Aufsatzablage and all theme pages matches the local build. The library RDF and the indexes were refreshed afterwards. The Konvolute whose `TEI_SOURCE` still predates the data repository stay as they are for now, by operator decision of 2026-10-13. By the same decision the datastreams `STARTSEITE`, `ABOUT` and `MISCELLANEOUS` of `context:szd` and the `ONTOLOGY` of `o:szd.glossar` are not replaced from the data repository, so `check-instance.py` keeps listing them. The data repository version of `STARTSEITE` would also add a `figure` with `STARTBILD` to the rendered text, and that of `MISCELLANEOUS` holds the corrected news numbering and the repointed Dostojewski facsimile, so the live news page keeps the duplicate id `miscellaneous.2`. The production versions of `STARTSEITE`, `ABOUT` and `MISCELLANEOUS` still declared CC BY-NC-SA 4.0 on 2026-10-09 ([project](project.md#7-licences)).
- `o:szd.werkindex`, `o:szd.personen` and `o:szd.standorte` reference their include files `szd-Werkliste.xsl`, `szd-Personenliste.xsl` and `szd-Standortliste.xsl`. They serve the current output since the operator's update after 2026-10-09, but GAMS apparently caches a transformation by its top-level file, see [deployment-architecture](deployment-architecture.md#stylesheet-references). The operator sets the three `STYLESHEET` references to `https://gams.uni-graz.at/szd/szd-Index.xsl`, and afterwards the four include files can be deleted.
- Several `STYLESHEET` references use `http://gams.uni-graz.at/szd/` and work through a redirect. The target is `https`.
- `o:szd.korrespondenzen.berger-gisela`, `o:szd.korrespondenzen.ferencak-mirko-m.`, `o:szd.korrespondenzen.oppeln-bronikowski-friedrich` and `o:szd.collection.1` exist only in production and are superseded. The operator deletes them. `o:szd.korrespondenzen.warren-p.-munsell` has no entry and no RDF.
- `o:szd.nli` exists only on staging and has no source in the data repository, although [data](data.md) and the object manifest list it.
- A refresh of a TEI file whose graphic is referenced with `file:///img/…` uploads the image as a datastream and rewrites the reference. For theme page 8 on 2026-10-09 this step failed with "Invalid byte 2 of 3-byte UTF-8 sequence" while it succeeded for theme pages 2 to 7 on 2026-10-13, so the cause is not the encoding of the file. Referencing the existing datastream (`info:fedora/<PID>`) avoided it.

#### Staging, reading of 2026-09-24

Staging is not reachable for development since 2026-10-13. This reading is kept as the last known state.

- The data repository builds the ingest package with `scripts/staging_package/build_staging_package.py`. Its README gives the order (indexes, holdings, Konvolute) and lists per object the references still missing, read live from staging. The package is regenerated after every data change and never while an ingest from it runs.
- Many references end in a trailing illegal character (HTTP 400, "Illegal character in path"). References typed by hand, such as the `TORDF` of `o:szd.bibliothek` and of the index objects, were clean, which points to the way the other references were entered. The pages render, but an object with an unusable `TORDF` keeps RDF that differs from the local build.
- The `TORDF` reference of `o:szd.werkindex`, `o:szd.nli` and `o:szd.autographen` points to the dead path `trunk/www`.
- Konvolute created by the ingest reference the generic `tei.xsl` inherited from `cirilo:TEI.szd` instead of `szd-Konvolut.xsl`.
- `o:szd.publikation` and `o:szd.korrespondenzen.ferencak-mirko-m` exist only on staging and are to be deleted.
- The `QUERY` datastreams of `query:szd.standort_search` and `query:szd.category_search` lack `FROM <o:szd.organisation>`, that of `query:szd.work_search` lacks `FROM <o:szd.aufsatzablage>` (read on 2026-09-23). The production queries equal the templates in [gams/query/](../gams/query/README.md).

### Browser review of the release of 2026-09-24

The release of 2026-09-24 reached production with the go-live of 2026-10-09. These details have no recorded review in a browser yet, in both languages:

- the permalink button and box of the Lebenskalender
- the glossary with jump bar, subcategory dropdowns and category search links
- the gold arrow of the introduction on theme page 1 (`o:szd.thema.1`)

### Refactoring

Derived on 2026-09-29 from six read-only analyses (JavaScript, CSS, XSLT architecture, RDF and search, test harness, data repository). Phase 0, the test net, is done. The settings decided for it are in the [specification](specification.md#refactoring-settings-operator-decision-of-2026-09-29). Every step uses the scope-specific gate in [testing](testing.md#rule) and, where nothing visible may change, a snapshot comparison against the commit before it.

#### Phase 1, defects with visible effect

Done on 2026-10-21, see the [journal](journal.md#2026-10-21-integriert-refactoring-phase-1-in-part-and-native-data-basket): `relationToWork` of the library, organisation hits in `szd-Suche.xsl`, the English plural, English "Blatt" and the missing `PID` in the library entries.

Open, each with its expected difference and the objects that need a renewed ingest:

- Swapped languages of `secretarialHand`. A fix that writes every `handDesc/ab` in its own language, and an `ab` without `@xml:lang` as one untagged literal, passes the source-derived smoke test, but the line-based RDF golden test cannot pair values that span several lines, so it was not committed. The golden test needs a correction that compares per resource instead of per line.
- The missing provenance of the autographs. `RDF_autograph` passes a path from the entry while the context is already the `provenance` element, so `getEnDe` receives nothing and no `szd:provenance` arises. The parameter should be `t:span`.
- The language tag of German location names. The `Standorte` template writes a German `orgName` with `xml:lang="en"` and, where both languages exist, only the English one. One `szd:name` per `orgName[@xml:lang]` corrects it.
- Name variants never reaching the full text. `FulltextSearchData` looks for `persName[@type='Variantname']`, while the person index keeps the variants in `note[@type='variants']`. The author is to be resolved by `#SZDPER.n` or GND as in `GetPersonlist`. The changed `gams:textualContent` lines need an insertion rule in the golden test.

#### Phase 2, dead code and module split, without visible change

Dead variables (including the load from the retired host glossa), dead branches in `szd-TORDF.xsl` and `szd-Templates.xsl`, the commented block that breaks builds on paths with `--`. The jump anchor lookup `getfirstforABC` evaluates `fn:filing-letter` over every name once per letter group, and gallery, autographs, library and correspondence index take minutes each in SaxonJS. That this lookup causes the slowness is an unmeasured inference, and a faster form has to stay byte-identical in the snapshot. Then `szd-Templates.xsl` splits into five `szd-lib-*.xsl` modules (text, search, header, entry, metadata) behind the unchanged hub, each extraction byte-identical. Duplicates are merged afterwards with named differences.

#### Phase 3, dependency removal

The order is fixed. Every step keeps the [global functions](rendering-architecture.md#global-functions) and passes the harness as [testing](testing.md#rule) requires.

1. JavaScript. Own disclosure and dropdown handling, a `dialog` lightbox, the search form and the data basket without jQuery, with unchanged class names. `js/popper.min.js` is deleted.
2. Done on 2026-10-21 apart from deleting the six unreferenced library files (`js/pdfmake.min.js`, `js/vfs_fonts.js`, `js/datatable.js`, `js/dataTables.buttons.min.js`, `js/buttons.html5.min.js`, `css/dataTables.css`). A search found no reference in gams-www or the data repository. The data basket, rebuilt natively to a high standard (operator decision of 2026-10-21). It keeps filtering and sorting of the basket table and offers two exports. CSV is UTF-8 with BOM, semicolon-separated, with separate columns for collection key, title, author, location, signature and URI and a speaking file name, so it opens cleanly in German Excel and LibreOffice. PDF comes from a dedicated print layout in landscape with title, date and the complete collection key including C, without navigation, buttons and the delete column, reached through a "PDF" button that opens the browser's print dialog for saving as PDF. DataTables, Buttons and pdfmake leave, jszip stays for the IIIF download.
3. The Bootstrap CSS. Dead rules and duplicates go, literals move to tokens, and an own reset, layout, utilities and components layer replaces the import, verified by computed styles at several widths. The computed-style comparison used in September, the script `css-equivalence.cjs` kept untracked under `local-test-build/build/` of a working copy, becomes a test under `local-test-build/test/` with Playwright as development dependency. Breakpoints are unified as a deliberate visible change.
4. The icons, an SVG sprite with an `icon` template.

#### Phase 4, data repository

The script defects, the shared helpers in `_szd_io.py`, the read-only check `check_data.py` before every staging package and the deterministic corrections were done in the data repository on 2026-09-29, see the [journal](journal.md#2026-09-29-integriert-data-repository-clean-up-refactoring-phase-4). NFC normalisation of the sources and the century corrections of dates remain as [operator questions](#data-questions).

### Known findings without a planned fix

- The open findings in [rdf-mapping](rdf-mapping.md#open-findings) need a golden comparison and a renewed ingest each.
- The findings in the [search renderer](search-architecture.md#open-findings-in-the-renderer) and the [assessment of the queries](search-architecture.md#assessment-of-the-queries) wait on the operator question on the search queries.

## Operator questions

### Data questions

- Ontology identifiers. The namespace `https://w3id.org/nachlass#` keeps its German name, and `szd:glossar`, the hybrid `szd:objecttyp` and glossary concepts such as `szdg:DatumEvidenz` keep German-derived identifiers, because they belong to the live GAMS vocabulary and the glossary. Rename them together with the glossary and the presentation layer, or keep them?
- Einheitssachtitel. The former repository rules required `title[@type="Einheitssachtitel"]` in German and English, while the renderer groups a language-neutral one correctly in both languages ([collections](collections.md#rendering-contract-grouped-lists)). Is the bilingual form an editorial obligation?
- Rights. Every TEI header states CC BY 4.0 in `availability`, while the [README](../README.md#licence) says the rights of the archival research data remain with the archive. Which statement applies, and does the other change? The operator decision of 2026-10-09 publishes all content of the portal, data and texts, under CC BY 4.0 ([specification](specification.md#licences)).
- Glossary. The German and English definitions of `Enclosures` and `AdditionalMaterial` are crossed ([data-quality](data-quality.md#glossary)). Which language version is canonical?
- Editorial rulings from the archive checkup. Whether an index entry counts an archival bundle or a correspondence relationship, what bracketed title dates mean, one notation for unidentified senders, and the classification vocabulary of the Aufsatzablage.
- Archive questions on missing scans and on dates only the originals can supply.
- NFC. The person index writes a large part of its names decomposed, and a few further files carry single decomposed characters. Should the data repository normalise all its TEI sources to precomposed Unicode (NFC), or leave the form as delivered? The presentation side asks the same question, because the index sort compensates through `fn:filing-key` while other string comparisons do not ([data](data.md#known-data-issues)).
- Century corrections. Should the Konvolut dates after 1950 that read two-digit years as twenty-first century be corrected in the TEI sources? The open cases are listed under [Konvolute](#konvolute).
- The root file `mail.md`, a mail text of July 2026 on the SZ-AAL/B correspondence, has no function in the repository. Remove it?
- Project lead. The former data-repository knowledge named the Literaturarchiv Salzburg as project lead, the former presentation-layer knowledge, following the About and Imprint datastreams, DHCraft since 2022 ([project](project.md#10-participants)). Which statement holds? This question arose from the merge of the two knowledge bases on 2026-10-28.

### Presentation questions

- Konvolut direction of the correspondence gallery. Three ways are open, each analysed in [correspondence-gallery-architecture](correspondence-gallery-architecture.md#three-konvolut-levels).
  1. Couple to the curation. Extend the gallery query by the Konvolut PID per piece and group by Personen-Konvolut with titles and links from the objects. Exact and solves the postcards, but needs a GAMS change and yields roughly the person view.
  2. Keep the B view and split the postcards by sender. Local to gams-www, but coarser than the curation for the collective B shelfmarks.
  3. Drop the switch, since the person view with its stack links already leads to the Konvolute.
- Collapse threshold and person jump navigation. How should the collapsing of gallery groups beyond eight cards interact with the person-based jump navigation in the header, whose targets may lie in a collapsed part?
- Timeline. The integrated timeline is switched off since 2026-10-09, and its prototype `local-test-build/proto/zeitleiste-lanes.*` still runs in `npm run test:proto`. Should the prototype stay, and under which condition is the timeline published?
- Autographs without author. `szd-Autographen.xsl` renders a section `#withoutAuthor`, but the jump bar omits the link "o.V." for `o:szd.autographen`. Should the autographs receive the link?
- Groups SCH and ST in the register of the Aufsatzablage. Should they stay groups of their own?
- English title of the work index. Menu "Index" and menu "Estate" both show "Works" for two different pages. Should the work index become "Index of Works" in menu, heading and page title?
- Search queries. Does "the queries stay unchanged" of 2026-09-23 mean the datastreams running on staging or the templates in [gams/query/](../gams/query/README.md), formerly `query/` of gams-www? The templates differ from the running queries beyond the `FROM` gaps listed above.
- RDF model questions, collected for one pass: `szd:Enclosur`, the category mapping against the actual values, every correspondence piece fixed to `SZDSTA.1`, the base of `connectedWithDocument`, date typing of birth and death, the Wikidata block, `partyInvolved` on autographs. The full list of open findings is in [rdf-mapping](rdf-mapping.md#open-findings).
