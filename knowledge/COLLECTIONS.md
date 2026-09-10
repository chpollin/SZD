---
title: Collections - Stefan Zweig Digital
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD.git
method:
  name: Promptotyping
  url: https://dhcraft.org/promptotyping
status: complete
created: 2025-10-23
updated: 2026-09-10
---

# Collections - Stefan Zweig Digital

Detailed overview of all archival collections in the Stefan Zweig Digital project, their TEI encoding, and content organization.

---

## Collection Overview

The SZD project organizes Stefan Zweig's digitized materials into thematic collections, each encoded in TEI-XML:

| Collection | File | PID | Description |
|------------|------|-----|-------------|
| Correspondence | SZDKOR.xml | o:szd.korrespondenzen | Letters and correspondence |
| Works | SZDMSK.xml | o:szd.werke | Published writings and literary works |
| Autographs | SZDAUT.xml | o:szd.autographen | Handwritten manuscripts |
| Library | SZDBIB.xml | o:szd.bibliothek | Personal book collection |
| Biography | SZDBIO.xml | o:szd.lebenskalender | Life calendar timeline |
| Essays | SZDESS.xml | o:szd.essays | Articles and academic essays |
| Personal Documents | SZDLEB.xml | o:szd.lebensdokumente | Life documents |
| Publications | SZDPUB.xml | o:szd.publikationen | Publication records |
| Glossary | szd-Glossary.xml | o:szd.glossar | Subject terminology |

**Person Index:** SZDPER.xml (o:szd.personen) - Authority file linking to GND and Wikidata

---

## Correspondence (SZDKOR)

**File:** [data/Correspondence/SZDKOR.xml](../data/Correspondence/SZDKOR.xml)
**PID:** o:szd.korrespondenzen

### Structure

Uses `<listBibl>` containing `<biblFull>` elements for correspondence bundles:

```xml
<listBibl>
  <biblFull xml:id="SZDKOR.1">
    <fileDesc>
      <titleStmt>
        <title xml:lang="de">1 Korrespondenzstück AN Stefan Zweig</title>
        <title xml:lang="en">1 Piece of Correspondence TO Stefan Zweig</title>
      </titleStmt>
      <publicationStmt>
        <ab>Briefkonvolut</ab>
      </publicationStmt>
      <sourceDesc>
        <msDesc>
          <msIdentifier>
            <repository>Literaturarchiv Salzburg</repository>
            <idno type="signature">SZ-AAP/W20</idno>
          </msIdentifier>
        </msDesc>
      </sourceDesc>
    </fileDesc>
  </biblFull>
</listBibl>
```

### Two-level architecture: index + konvolut objects

Correspondence is modelled on **two levels**:

1. **Index** — `SZDKOR.xml` (`o:szd.korrespondenzen`): one aggregate `<biblFull>` per
   archival bundle, carrying the piece count (`measure[@type="correspondence"]`) and two
   pointers in `msIdentifier/altIdentifier`:
   - `idno[@type="konvolut"]` → the per-person konvolut object,
   - `idno[@type="context"]` → the facsimile gallery anchor.

   A correspondent may have **several** index entries (one per archival bundle/signature).

2. **Konvolut objects** — `o:szd.korrespondenzen.<person>`: one full TEI document per
   correspondence partner, with a `<biblFull>` per **individual letter**. Each letter entry
   carries the facsimile PID in `msIdentifier/altIdentifier/idno[@type="PID"]`, so
   `szd-Konvolut.xsl` renders a Mirador link straight to the digitised image, alongside a
   rich `physDesc`/`correspDesc` (sender/recipient with GND, date, place, material).

The `<person>` slug must equal the gallery anchor that `szd-Facsimiles.xsl` generates
(`translate(lower-case(normalize-space(name)), ' ,', '-')` plus diacritic folding) —
otherwise the index→konvolut and gallery→konvolut links do not resolve. `correspDesc/@type`
(`fromZweig` when Stefan is the sender, else `toZweig`) drives the sender display in both the
konvolut and the index renderer.

**SZ-AAL/B (June 2026):** the ~480 letters of the Stefan Zweig–Lotte Altmann correspondence
were catalogued across **42 person konvolute** (30 new objects, 12 extending existing ones),
generated from per-letter CSVs joined to live facsimile PIDs (via risearch). Konvolut object
files live in [data/Correspondence/konvolute/](../data/Correspondence/konvolute/).

### Entry title and date convention (konvolut objects)

The title of a single-letter entry is derived, not written: it is generated from
`correspDesc/correspAction` and the physical extent, in both languages.

```
de: <Dokumenttyp> von <Sender> an <Empfänger> [<Tag>. <Monat> <Jahr>]
en: <Document type> from <Sender> to <Recipient>, <ISO date>
```

The document type is the leading noun of `extent/span` in the respective language
(Brief/Letter, Brieffragment/Letter, Ansichtspostkarte/Picture postcard,
Postkarte/Postcard, Telegramm/Telegram, Kuvert/Envelope); anything else falls back to
Brief/Letter. Partner names are `Vorname Nachname`, taken from `persName`
(`forename` + `surname`); `orgName` stands in only where the action names no person.
Several senders or recipients are encoded as several `correspAction` elements of the same
`@type` and are joined with *und* / *and*.

`correspAction[@type="sent"]/date` is the sole carrier of the date. The German title
repeats it in long form inside square brackets, the English title as the ISO value of
`@when`; the brackets mark the title date as derived from that element, not the degree of
editorial certainty, which `@cert` and `@ana` carry. An entry without `@when` gets no date
in the German title. Neither title carries an ISO date of its own, and neither carries the
archival signature — that lives in `msIdentifier/idno[@type="signature"]`.

Two deviations from this convention are editorial and stay: entries addressed to Lotte
Altmann before the 1939 marriage keep the maiden name although `correspAction` records
`Zweig, Lotte`, and the aggregate titles of the index `SZDKOR.xml` describe bundles
(`N Korrespondenzstücke AN/VON Stefan Zweig`) rather than single pieces.

`scripts/korrespondenz_titel/` regenerates deviating titles from this rule and verifies
that the rule reproduces the existing corpus.

### Content

Letters to and from Stefan Zweig organized by correspondence partner. Each entry contains:

- Bilingual titles
- Repository information
- Signature identifiers
- Sender/recipient information
- Date ranges
- Physical descriptions
- Links to digitized images

### Related Documentation

- [DATA.md](DATA.md) - Correspondence corpus statistics and data gaps
- [MAPPING.md](MAPPING.md) - Complete TEI-CSV schema mapping

---

## Location Index (SZDSTA)

**File:** [data/Index/Location/SZDSTA.xml](../data/Index/Location/SZDSTA.xml)
**PID:** o:szd.standorte

### Structure

Repository directory using `<listOrg>`:

```xml
<listOrg>
  <org xml:id="SZDSTA.1">
    <orgName>Literaturarchiv Salzburg</orgName>
    <country>Oesterreich</country>
    <settlement>Salzburg</settlement>
  </org>
</listOrg>
```

### Content

40 repositories worldwide that hold Stefan Zweig materials (archives, libraries, museums). Each entry includes institution name, country, and city.

---

## Person Index (SZDPER)

**File:** [data/Index/Person/SZDPER.xml](../data/Index/Person/SZDPER.xml)
**PID:** o:szd.personen

### Structure

Authority file using `<listPerson>`:

```xml
<listPerson>
  <person corresp="https://de.wikipedia.org/wiki/Pierre_Abraham" xml:id="SZDPER.1">
    <persName ref="http://d-nb.info/gnd/12490310X">
      <surname>Abraham</surname>
      <forename>Pierre</forename>
    </persName>
  </person>
</listPerson>
```

### Content

Authority file for all persons mentioned in SZD collections with:

- GND identifiers (`@ref`)
- Wikipedia links (`@corresp`)
- Wikidata links
- Structured names (forename, surname)
- Internal cross-references (`xml:id`)

### Usage

All person references in other collections link to SZDPER using `ref="#SZDPER.{NUMBER}"` pattern.

---

## Biography (SZDBIO)

**File:** [data/Biography/SZDBIO.xml](../data/Biography/SZDBIO.xml)
**PID:** o:szd.lebenskalender

### Structure

Life calendar using `<listEvent>`:

```xml
<listEvent>
  <event xml:id="SZDBIO.1">
    <head>
      <span xml:lang="de">Wien <date when="1881-11-28">28. November 1881</date></span>
      <span xml:lang="en">Vienna, <date when="1881-11-28">28 November 1881</date></span>
    </head>
    <ab xml:lang="de">Stefan Zweig wird als zweiter Sohn von Ida und Moriz Zweig geboren.</ab>
    <ab xml:lang="en">Stefan Zweig is born the second son of Ida and Moriz Zweig.</ab>
  </event>
</listEvent>
```

### Content

Chronological biographical timeline from birth to death:

- Bilingual event descriptions
- ISO 8601 dates
- Place names
- Person references to SZDPER
- Life milestones and significant events

**Author:** Oliver Matuschek

---

## Works (SZDMSK)

**File:** [data/Work/SZDMSK.xml](../data/Work/SZDMSK.xml)
**PID:** o:szd.werke

### Structure

Published works using `<listBibl>` with bibliographic metadata.

### Content

Stefan Zweig's published literary works including:

- Novels, novellas, short stories
- Biographies and historical essays
- Dramas and libretti
- Publication details
- Editions and translations

---

## Autographs (SZDAUT)

**File:** [data/Autograph/SZDAUT.xml](../data/Autograph/SZDAUT.xml)
**PID:** o:szd.autographen

### Structure

Manuscript descriptions using `<msDesc>`:

```xml
<msDesc>
  <msIdentifier>
    <repository>Literaturarchiv Salzburg</repository>
    <idno type="signature">SZ-AUT/001</idno>
  </msIdentifier>
  <physDesc>
    <objectDesc>
      <supportDesc>
        <extent>
          <measure type="pages">12</measure>
        </extent>
      </supportDesc>
    </objectDesc>
  </physDesc>
</msDesc>
```

### Content

Handwritten manuscripts and autographs with:

- Physical descriptions
- Material details
- Extent and pagination
- Repository locations
- Facsimile links

---

## Library (SZDBIB)

**File:** [data/Library/SZDBIB.xml](../data/Library/SZDBIB.xml)
**PID:** o:szd.bibliothek

### Structure

Personal book collection using `<listBibl>` with annotations.

### Content

Books from Stefan Zweig's personal library including:

- Bibliographic descriptions
- Provenance information
- Annotations and marginalia
- Dedications
- Current repository locations

---

## Essays (SZDESS)

**File:** [data/Aufsatzablage/SZDESS.xml](../data/Aufsatzablage/SZDESS.xml)
**PID:** o:szd.essays

### Structure

Articles and essays using `<listBibl>`.

### Content

Academic and journalistic essays about Stefan Zweig:

- Publication details
- Authors
- Bibliographic metadata
- Abstracts

### Classification is mandatory in both languages

SZDESS is rendered by the same `szd-Werke.xsl` as the Works and the Lebensdokumente, so
the rendering contract below applies here too. Every entry must carry
`term[@type="classification"]` in German **and** English: the outer `for-each-group` keys
on the term of the current locale, so an entry classified in one language only vanishes
from the other language's output entirely, while still being present and ingested.
Spelling matters as much as presence, because a value that differs from the established
one only in capitalisation opens a second, near-identical navbar category holding a single
entry.

The vocabulary is closed. A new object type does not warrant a new category; the
classification places the item in the navigation, the object type
(`extent/span/term[@type="objecttyp"]`) describes the piece itself, and the two are kept
apart. Where an entry needs a category, it takes the pair that the entries with the same
object type already use. Two German categories, Druckfahnen and Korrekturfahnen, share the
English term Galley proofs, so the English navigation has one category where the German has
two; that is an editorial decision on record, not a defect.

`scripts/essay_klassifikation/` completes and normalises these keys and surveys the grouped
lists for entries that the renderer would drop.

---

## Personal Documents (SZDLEB)

**File:** [data/PersonalDocument/SZDLEB.xml](../data/PersonalDocument/SZDLEB.xml)
**PID:** o:szd.lebensdokumente
**Entries:** 156 `<biblFull>`

### Structure

Each life document is one `<biblFull>` (RNA-based description, emphasis on physical features). The manuscript description is nested under `fileDesc/sourceDesc/msDesc`:

```xml
<biblFull xml:id="SZDLEB.1">
  <fileDesc>
    <titleStmt>… title[@ana], author, editor[@role="contributor"] …</titleStmt>
    <sourceDesc><msDesc>
      <msIdentifier>… country, settlement, repository, idno[@type="signature"], altIdentifier/idno[@type="PID"] …</msIdentifier>
      <msContents>… summary, textLang, msItem/incipit, msItem/docEdition …</msContents>
      <physDesc>… support/material[@ana="szdg:…"], extent, foliation, handDesc, bindingDesc, accMat …</physDesc>
      <history>… origin/origDate, origin/origPlace, provenance, acquisition …</history>
    </msDesc></sourceDesc>
  </fileDesc>
  <profileDesc><textClass><keywords>… term[@type] …</keywords></textClass></profileDesc>
</biblFull>
```

### Content

Per the glossary's own definition: Zweig's diaries and contracts for his literary works, but also official documents, bank records, theatre posters, invitation cards, unused stationery — a heterogeneous group of life documents.

### Data fields vs. frontend display

The TEI holds **41 distinct data fields** (every `@type`/`@ana`-discriminated element path across all 156 records). The public frontend renders only **~22** of them as labelled fields; the rest exist in the TEI/backend only:

- **Not rendered as fields:** Einheitssachtitel & Gesamttitel (fold into the heading bar), `term[@type="work"]` (related work), `term[@type="classification"]` (genre), signature (folded into *Heutiger Standort / Current Location*), internal identifiers (`PID`, `extern`, `mediaid`, `subject`), `summary`.

The **bilingual labels and definitions** of the glossary-backed fields — Beteiligte/Parties Involved, Datierung/Date, Incipit, Aufschrift/Identifying Inscription, Umfang/Einband/Physical Description, Beschreibstoff/Writing Material, Schreibstoff/Writing Instrument, Beilage/Enclosures, Zusatzmaterial/Additional Material — come from the SZD glossary (`szdg:` SKOS concepts), **not** from free templating. The display label for `docEdition[@ana="szdg:IdentifyingInscription"]` is **Aufschrift** (not "Identifizierende Beschriftung").

The complete field catalogue (22 displayed fields, DE/EN label + DE/EN definition) is maintained as a spreadsheet: [docs/SZDLEB_Datenfelder.xlsx](../docs/SZDLEB_Datenfelder.xlsx).

> **Inspecting display labels:** the collection-level dissemination `https://stefanzweig.digital/{PID}/sdef:TEI/get?locale={de|en}` renders the full bilingual frontend view of an entire collection — the reliable way to enumerate display labels. The single-object variant (`o:szd.{n}/sdef:TEI/get`) currently returns HTTP 500.

### Rendering contract (why an ingested entry can stay invisible)

The Lebensdokumente edition and the Works list share one renderer, `szd-Werke.xsl` in the **gams-www** repo (`ZIMLAB/szd`). It builds the page with a two-level `xsl:for-each-group`: the **outer** group is `term[@type="classification"]` (the h2 navbar category), the **inner** group is `title[@type="Einheitssachtitel"]` (the h3 document-type heading). An entry missing **either** grouping key is silently dropped — present in the TEI, ingested, yet rendered nowhere. A classification present in one language only drops the entry from that other language's output while it still renders in the first.

Every `biblFull` in a grouped list must therefore carry, beyond its content fields:

- `profileDesc/textClass/keywords/term[@type="classification"]` (de+en) — navbar category;
- `titleStmt/title[@type="Einheitssachtitel"]` — document-type sub-heading. The inner
  `group-by` selects the title of the current locale **or** one without `@xml:lang`, so a
  language-less Einheitssachtitel groups correctly in both languages and only a completely
  absent one drops the entry. The classification has no such fallback: it is keyed on the
  locale alone and is therefore required in both languages;
- the PID as `msIdentifier/altIdentifier/idno[@type="PID"]` (not a bare `idno`), or the IIIF/Mirador facsimile link is not built.

**Controlled vocabulary:** navbar categories are a closed set — reuse an existing `classification`, add a new one only for something fundamental and permanent. Reuse existing `Einheitssachtitel` values **verbatim** (de and en) so the entry joins the existing heading group instead of spawning a near-duplicate. The renderer side is documented in gams-www `knowledge/Rendering-and-Search.md` (§1).

> **Observed 2026-06:** the 13 SZ-AAL/L documents were ingested with valid PIDs but appeared nowhere in the frontend until each received an `Einheitssachtitel` and its PID was wrapped in `altIdentifier`.

### Rendering contract: correspondence facsimile gallery (person grouping)

A second, independent grouping contract governs the correspondence facsimile gallery
`context:szd.facsimiles.korrespondenzen`, rendered by `szd-Facsimiles.xsl` (gams-www).
The default person view groups every letter by its correspondent:
`group-by="creator[not(. = 'Zweig, Stefan')] | contributor[@bound != 'false']"` — the key
is `dc:creator` unless it is exactly `Zweig, Stefan`, otherwise a bound `dc:contributor`.
A letter **authored by Stefan Zweig with no `dc:contributor`** has an empty key and falls
out of the grouping entirely; only a catch-all branch ("Without correspondent" / "Ohne
Korrespondenzpartner") can render it, and only if that XSL is deployed.

The correspondence objects are **`cm:dfgMETS` book objects**, not list TEI. In their GAMS
`<book>` viewer-format source, `<author>` → `dc:creator` and `<contributor>` →
`dc:contributor`. Every Stefan-authored letter must therefore carry a `<contributor>`
element = the recipient (`Lastname, Firstname`; several recipients → several
`<contributor>`), or it never appears in the gallery. The recipient sits in the title
("Brief von Stefan Zweig **an** <recipient> [date]"). The legacy `enrichXML-briefe.py`
only matched the older ' an '…' vom ' title pattern and silently skipped bracketed-date
titles, which is why the SZ-AAL letters stayed contributor-less.

> **Observed 2026-06:** ~204 SZ-AAL Stefan-authored letters (all of B2, ~94 of B1, part
> of B3) were ingested and were context members, yet absent from the gallery because their
> book-XML had no `<contributor>`. Fixed by deriving the recipient from the title.
> Renderer side: gams-www `knowledge/Facsimiles-Korrespondenzen.md` (Befundprotokoll,
> "Gruppierungs-Lücke").

> **IIIF manifest and structure labels (observed 2026-09-10):** the GAMS method
> `sdef:IIIF/getManifest` copies the `<div type="…">` labels of the `<book>` structure
> into the JSON `label` of each `sc:Range` without escaping. A straight double quote in
> such a label (`&quot;` in the XML) therefore yields invalid JSON, Mirador cannot parse
> the manifest and the viewer stays empty, although every image datastream and the
> Image API are intact. Affected: `o:szd.174` (SZ-AP2/L-S1.1, label „Deckblatt
> "VERLEGER vor dem Index"“), `o:szd.67` (SZ-AAP/L2, „Zeitungsausschnitt/Vom
> "österreichischen" Dichter“), `o:szd.314` (SZ-AP2/W-G104.1, three quoted incipits).
> Object titles with quotes are escaped correctly (`o:szd.259`, `o:szd.1481`). Rule for
> the ingest sources under `PROJECTS/szd/done/**/Result_*.xml`: no straight double
> quotes in `div/@type`; use typographic „…“ or drop them. Root cause fix would be the
> escaping in the GAMS manifest generator (ZIM); until then the three sources need
> corrected labels and a re-ingest.

> **Cache caveat:** the rendered `…/sdef:Context/get` page is cached; context membership
> (the `QUERY` datastream, queryable live via `risearch`) updates immediately, but the
> rendered gallery only reflects metadata/membership changes after GAMS rebuilds it.

---

## Publications (SZDPUB)

**File:** [data/Publication/SZDPUB.xml](../data/Publication/SZDPUB.xml)
**PID:** o:szd.publikationen

### Structure

Publication records using `<listBibl>`.

### Content

Comprehensive publication history including:

- First editions
- Translations
- Reprints
- Modern editions

---

## Glossary (SZDGLR)

**File:** [data/Glossary/szd-Glossary.xml](../data/Glossary/szd-Glossary.xml)
**PID:** o:szd.glossar

### Structure

Controlled vocabulary using custom namespace `szdg:`.

### Content

Subject terminology for classification and indexing:

- Bilingual terms
- Definitions
- Cross-references
- Hierarchical relationships

---

## Licensing

All collections are published under Creative Commons licenses:

- **Most collections:** CC-BY 4.0
- **All collections:** CC-BY 4.0

License information is specified in each TEI header `<availability>` element.

---

## Access

### Online Access
All collections are accessible via GAMS platform:
- Main portal: https://stefanzweig.digital/
- GAMS context: https://gams.uni-graz.at/context:szd
- Individual PIDs: https://gams.uni-graz.at/{PID}

### Archival Access
Long-term preservation copies on Zenodo:
- https://zenodo.org/uploads/17421555

---

## Related Documentation

- [DATA_MODEL.md](DATA_MODEL.md) - TEI-XML encoding patterns
- [ARCHITECTURE.md](ARCHITECTURE.md) - System integration
- [DATA.md](DATA.md) - Data quality and statistics
- [MAPPING.md](MAPPING.md) - TEI-CSV schema for correspondence

---

**Last Updated:** September 2026

**See also:** [ONTOLOGY.md](ONTOLOGY.md) for how each collection maps to SZDO ontology classes (Section 7), [PROJECT.md](PROJECT.md) for the full project context.
