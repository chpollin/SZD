---
title: Collections
project:
  name: Stefan Zweig Digital, data repository
  repository: https://github.com/chpollin/SZD
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: complete
created: 2025-10-23
updated: 2026-09-24
---

# Collections

The collections and indices of Stefan Zweig Digital, their files and PIDs, their collection-specific TEI encoding and the rendering contracts the presentation layer imposes on them. Encoding patterns shared by all files are in [DATA_MODEL.md](DATA_MODEL.md), data gaps and checkup results in [DATA.md](DATA.md).

## Collection Overview

| Collection | File | PID | Content |
|------------|------|-----|---------|
| Works | `data/Work/SZDMSK.xml` | `o:szd.werke` | Manuscripts, typescripts, notebooks, bundles and proofs of Zweig's works |
| Correspondence | `data/Correspondence/SZDKOR.xml` and `data/Correspondence/konvolute/` | `o:szd.korrespondenzen`, `o:szd.korrespondenzen.<person>` | Letters to and from Zweig, grouped by correspondence partner |
| Autographs | `data/Autograph/SZDAUT.xml` | `o:szd.autographen` | Zweig's collection of autographs by other hands |
| Library | `data/Library/SZDBIB.xml` | `o:szd.bibliothek` | Reconstructed private library with provenance features |
| Essays (Aufsatzablage) | `data/Aufsatzablage/SZDESS.xml` | `o:szd.aufsatzablage` | The essay filing of the estate, with newspaper clippings, register sheets, typescripts, manuscripts and proofs |
| Personal Documents | `data/PersonalDocument/SZDLEB.xml` | `o:szd.lebensdokumente` | Diaries, contracts, official documents and ephemera |
| Biography | `data/Biography/SZDBIO.xml` | `o:szd.lebenskalender` | Biographical timeline 1881–1942 |
| Themes | `data/Issue/*/szd-thema*.xml` | `o:szd.thema.<n>` | Curated thematic pages |

| Index | File | PID | Content |
|-------|------|-----|---------|
| Person index | `data/Index/Person/SZDPER.xml` | `o:szd.personen` | Persons with GND, Wikidata and Wikipedia links |
| Organisation index | `data/Index/Organisation/SZDORG.xml` | `o:szd.organisation` | Corporate bodies, including the repositories |
| Location index | `data/Index/Location/SZDSTA.xml` | `o:szd.standorte` | Repositories holding Zweig material |
| Work index | `data/Index/Werke/SZDWRK.xml` | `o:szd.werkindex` | Abstract works (intellectual level) |
| Glossary | `data/Glossary/szd-Glossary.xml` | `o:szd.glossar` | SKOS vocabulary (`szdg:`) for provenance features and materials |

## Catalogue Entry Structure

Works, Correspondence, Autographs, Library, Essays and Personal Documents share one outline. Each file holds a single `listBibl`, each catalogue entry is a `biblFull` with its manuscript description under `fileDesc/sourceDesc/msDesc`. The outline of a Personal Documents entry shows the elements in use:

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

Works, Essays and Personal Documents are rendered as grouped lists and must follow the [rendering contract](#rendering-contract-grouped-lists).

## Correspondence (SZDKOR)

### Two-level architecture

Correspondence is modelled on two levels.

1. The index `SZDKOR.xml` (`o:szd.korrespondenzen`) holds one aggregate `biblFull` per archival bundle, with the piece count in `measure[@type="correspondence"]` and two pointers in `msIdentifier/altIdentifier`, `idno[@type="konvolut"]` to the per-person konvolut object and `idno[@type="context"]` to the facsimile gallery anchor. A correspondent may have several index entries, one per archival bundle, and the signature distinguishes them.
2. The konvolut objects `o:szd.korrespondenzen.<person>` in [data/Correspondence/konvolute/](../data/Correspondence/konvolute/) are one TEI document per correspondence partner with one `biblFull` per individual letter. Each letter carries its facsimile PID in `msIdentifier/altIdentifier/idno[@type="PID"]`, which `szd-Konvolut.xsl` turns into a Mirador link, and a `correspDesc` with sender, recipient, date and place. Since 24 September 2026 the folder holds every Konvolut that GAMS production publishes, imported with [scripts/konvolute_import/](../scripts/konvolute_import/README.md). The repository copy is the edited one and can be ahead of production.

An index entry as it stands in the data:

```xml
<biblFull xml:id="SZDKOR.1">
  <fileDesc>
    <titleStmt>
      <title xml:lang="de">1 Korrespondenzstück AN Stefan Zweig</title>
      <title xml:lang="en">1 Piece of Correspondence TO Stefan Zweig</title>
    </titleStmt>
    <publicationStmt><ab>Briefkonvolut</ab></publicationStmt>
    <sourceDesc><msDesc>
      <msIdentifier>
        <country>USA</country>
        <settlement>Fredonia</settlement>
        <repository ref="http://d-nb.info/gnd/2156743-8">Reed Library – Stefan Zweig Collection</repository>
        <idno type="signature">SZ-AP1/B-1.1</idno>
      </msIdentifier>
      <physDesc>… <measure type="correspondence" unit="piece" subtype="received">1</measure> …</physDesc>
    </msDesc></sourceDesc>
  </fileDesc>
  <profileDesc>
    <correspDesc type="toZweig">
      <correspAction type="sent"><persName ref="http://d-nb.info/gnd/116007605">…</persName><date xml:lang="en" when="1930">1930</date></correspAction>
      <correspAction type="received"><persName ref="http://d-nb.info/gnd/118637479">…</persName></correspAction>
    </correspDesc>
  </profileDesc>
</biblFull>
```

A letter in a konvolut object:

```xml
<biblFull xml:id="SZDKOR.altmann-hannah.1">
  <fileDesc>
    <titleStmt>
      <title xml:lang="de">Brief von Stefan Zweig an Hannah Altmann [Februar 1939]</title>
      <title xml:lang="en">Letter from Stefan Zweig to Hannah Altmann, 1939-02</title>
    </titleStmt>
    <publicationStmt><ab>Einzelbrief</ab></publicationStmt>
    <sourceDesc><msDesc>
      <msIdentifier>
        … <idno type="signature">SZ-AAL/B1.2</idno>
        <altIdentifier><idno type="PID">o:szd.3132</idno></altIdentifier>
      </msIdentifier>
      <!-- physDesc with material and extent in de and en, msContents/textLang, history -->
    </msDesc></sourceDesc>
  </fileDesc>
  <profileDesc>
    <correspDesc type="fromZweig">
      <correspAction type="sent">… <date when="1939-02" ana="supplied/verified" xml:lang="de">Februar 1939</date> <placeName xml:lang="de">Salt Lake City, Utah</placeName></correspAction>
      <correspAction type="received"><persName ref="http://d-nb.info/gnd/1170430066">…</persName></correspAction>
    </correspDesc>
  </profileDesc>
</biblFull>
```

`correspDesc/@type` is `fromZweig` when Zweig is the sender and `toZweig` otherwise. It drives the sender display in the konvolut and the index renderer. The gallery links of the presentation layer use the curated `idno[@type="konvolut"]` values of the index. A partner heading receives a link only when its normalised person or organisation name identifies one unambiguous PID, and name-derived slugs remain local gallery anchors.

The SZ-AAL/B correspondence was catalogued in June 2026 as person konvolute generated from per-letter CSVs joined to the live facsimile PIDs. The derived timeline keeps both catalogue levels, see [Lebenskalender-Lanes.md](Lebenskalender-Lanes.md#duplicates-and-coverage-of-the-correspondence).

### Entry title and date convention (konvolut objects)

The title of a single-letter entry is derived from `correspDesc/correspAction` and the physical extent, in both languages.

```
de: <Dokumenttyp> von <Sender> an <Empfänger> [<Tag>. <Monat> <Jahr>]
en: <Document type> from <Sender> to <Recipient>, <ISO date>
```

The document type is the leading noun of the German `extent/span`, mapped to a German and English pair (Brief/Letter, Brieffragment/Letter, Ansichtspostkarte/Picture postcard, Postkarte/Postcard, Telegramm/Telegram, Kuvert/Envelope). Anything else falls back to Brief/Letter. Partner names are `Vorname Nachname`, taken from `persName` (`forename` and `surname`), and `orgName` stands in only where the action names no person. Several senders or recipients are encoded as several `correspAction` elements of the same `@type` and are joined with *und* or *and*.

`correspAction[@type="sent"]/date` is the sole carrier of the date. The German title repeats it in long form inside square brackets, the English title as the ISO value of `@when`. The brackets mark the title date as derived from that element. The degree of editorial certainty is carried by `@cert` and `@ana`. An entry without `@when` gets no date in the German title. The archival signature stays in `msIdentifier/idno[@type="signature"]` and never enters a title.

Two deviations are editorial and stay. Entries addressed to Lotte Altmann before the 1939 marriage keep the maiden name although `correspAction` records `Zweig, Lotte`, and the aggregate titles of the index describe bundles (`N Korrespondenzstücke AN/VON Stefan Zweig`).

[scripts/korrespondenz_titel/](../scripts/korrespondenz_titel/README.md) regenerates deviating titles from this rule and verifies that the rule reproduces the existing corpus.

## Person Index (SZDPER)

`listPerson` with one `person` per entry. An entry as it stands in the data:

```xml
<person corresp="https://de.wikipedia.org/wiki/Pierre_Abraham" xml:id="SZDPER.1">
  <persName ref="http://d-nb.info/gnd/12490310X">
    <surname>Abraham</surname>
    <forename>Pierre</forename>
  </persName>
  <note type="variants">Bloch, Pierre Abraham</note>
  <birth when="1892"/>
  <death when="1974"/>
  <idno type="wikidata">http://www.wikidata.org/entity/Q3383636</idno>
</person>
```

The GND sits in `persName/@ref`, the Wikipedia article in `person/@corresp`, the Wikidata entity in `idno[@type="wikidata"]`. Corporate bodies are held in the organisation index.

On 24 September 2026 the persons that no holding, index, theme page or stylesheet references and that no text of the holdings names were removed from the index after a deterministic check, described in [DATA.md](DATA.md#dead-references-and-unlinked-correspondence-partners). The removed entries are kept unchanged in `scripts/checkup_2026_09_index/removed_persons.xml`, and their identifiers are never assigned again.

Holdings reference a person either by `ref="#SZDPER.<n>"` or by the GND of the index entry. `GetPersonlist` in `szd-TORDF.xsl` resolves both forms against the index, and only a reference it resolves makes the object findable in the person search. The reading rules that follow from the mapping are documented with [scripts/personen_ohne_verweis/](../scripts/personen_ohne_verweis/README.md), the normalisation of the reference form with [scripts/checkup_2026_09_index/](../scripts/checkup_2026_09_index/README.md).

## Organisation Index (SZDORG)

`listOrg` with one `org` per corporate body, built like the location index. The index holds publishers, banks, authorities, newspapers, associations and the repositories. It was generated in September 2026 from the corporate bodies that the person index carried as persons and from the `orgName/@ref` values of the holdings.

```xml
<org corresp="http://ahl.sbg.ac.at/" xml:id="SZDORG.1">
  <orgName ref="http://d-nb.info/gnd/1047604132">Adolf Haslinger Literaturstiftung im Literaturarchiv Salzburg</orgName>
  <country>Österreich</country>
  <settlement>Salzburg</settlement>
  <idno type="SZDSTA">SZDSTA.17</idno>
</org>
```

- `idno type="SZDSTA"` is a live cross-reference to the location index where the body is also a repository.
- `idno type="SZDPER" subtype="superseded"` names a person index entry the migration removed. The identifier no longer exists in the person index, and `szd-TORDF.xsl` emits it as `dcterms:replaces`, so old references to the person resource lead to the body.
- Where two person entries named the same body, both back-references stand in one entry and the second name as `orgName type="variant"`.

Country and settlement of a repository come from the location index. For the other bodies `scripts/organisationen_index/reconcile_org_places.py` takes them from the GND record (`geographicAreaCode`, `placeOfBusiness`) and writes a value only where the record gives exactly one. Organisation and location index both name Great Britain „Großbritannien“.

`o:szd.standorte` remains the curated view of the repositories. The location entries that hold material without naming a corporate body, the private-ownership entries and the heirs, stay out of the organisation index, and references to them keep pointing to `o:szd.standorte`.

Holdings reference a body by `orgName/@ref` with its GND, and without a GND by `https://gams.uni-graz.at/o:szd.organisation#SZDORG.<n>`, built like the location reference `https://gams.uni-graz.at/o:szd.standorte#SZDSTA.<n>`. The `@ref` of an enclosing `author` or `editor` carries the same value, because `szd-Bibliothek.xsl` groups and sorts the library list by that attribute.

`szd-TORDF.xsl` loads the object into `$OrganisationList` and resolves `t:org[t:orgName[@ref = …]]` to the internal `SZDORG` identifier, so the `@ref` spelling of index and holdings must match character for character. The `document()` call sits in a global variable, and a missing object on an instance therefore breaks the whole transformation. The holdings call the template `GetOrglist` since frontend commit `ef9a4ce`. The index carries no Wikidata identifiers yet. At ingest, `o:szd.personen` and `o:szd.organisation` precede the holdings, because the RDF transformation resolves the references against them at ingest time.

Since the migration the index is maintained by hand. A new body receives the next free `SZDORG` number, because the identifiers are part of the RDF URIs. The procedure, the decision table and the open source findings are in [scripts/organisationen_index/](../scripts/organisationen_index/README.md).

## Location Index (SZDSTA)

`listOrg` with one `org` per repository, holding name, country and city.

```xml
<org corresp="https://www.uni-salzburg.at/index.php?id=72" xml:id="SZDSTA.1">
  <orgName ref="http://d-nb.info/gnd/1047605287">Literaturarchiv Salzburg</orgName>
  <country>Österreich</country>
  <settlement>Salzburg</settlement>
</org>
```

The entries carry no `geo` elements, see [DATA.md](DATA.md#archive-checkup-september-2026).

## Biography (SZDBIO)

`listEvent` with one bilingual `event` per biographical entry from birth to death, carrying ISO dates, place names and person references to SZDPER. The biography was written by the project's biographer.

```xml
<event xml:id="SZDBIO.1">
  <head>
    <span xml:lang="de">Wien <date when="1881-11-28">28. November 1881</date></span>
    <span xml:lang="en">Vienna, <date when="1881-11-28">28 November 1881</date></span>
  </head>
  <ab xml:lang="de">Stefan Zweig wird als zweiter Sohn von Ida und Moriz Zweig geboren.</ab>
  <ab xml:lang="en">Stefan Zweig is born the second son of Ida and Moriz Zweig.</ab>
</event>
```

## Essays (SZDESS)

SZDESS is rendered by the same `szd-Werke.xsl` as the Works and the Personal Documents, so the [rendering contract](#rendering-contract-grouped-lists) applies. Every entry carries `term[@type="classification"]` in German and in English. The outer `for-each-group` keys on the term of the current locale, so an entry classified in one language only vanishes from the other language's output while it is still ingested. Spelling matters as much as presence, because a value that differs from the established one only in capitalisation opens a second, near-identical navbar category holding a single entry.

The vocabulary is closed. The classification places the item in the navigation, and the object type (`extent/span/term[@type="objecttyp"]`) describes the piece itself. Where an entry needs a category, it takes the pair that the entries with the same object type already use. The German categories Druckfahnen and Korrekturfahnen share the English term Galley proofs, so the English navigation has one category where the German has two. This is an editorial decision on record.

[scripts/essay_klassifikation/](../scripts/essay_klassifikation/README.md) completes and normalises these keys and surveys the grouped lists for entries that the renderer would drop.

## Personal Documents (SZDLEB)

Per the glossary's own definition the collection holds Zweig's diaries and contracts for his literary works, as well as official documents, bank records, theatre posters, invitation cards and unused stationery. Each entry is one `biblFull` described after RNA (Regeln zur Erschließung von Nachlässen und Autographen) with emphasis on physical features.

The public frontend renders only part of the TEI data fields as labelled fields. Einheitssachtitel and Gesamttitel fold into the heading bar, the signature folds into Heutiger Standort (Current Location), and `term[@type="work"]`, `term[@type="classification"]`, the internal identifiers (`PID`, `extern`, `mediaid`, `subject`) and `summary` are not rendered as fields.

The bilingual labels and definitions of the glossary-backed fields (Beteiligte, Datierung, Incipit, Aufschrift, Umfang und Einband, Beschreibstoff, Schreibstoff, Beilage, Zusatzmaterial) come from the SZD glossary (`szdg:` SKOS concepts). The display label for `docEdition[@ana="szdg:IdentifyingInscription"]` is Aufschrift. The field catalogue with German and English labels and definitions is maintained as a spreadsheet, [docs/SZDLEB_Datenfelder.xlsx](../docs/SZDLEB_Datenfelder.xlsx).

The collection-level dissemination `https://stefanzweig.digital/{PID}/sdef:TEI/get?locale={de|en}` renders the full bilingual view of a collection and is the reliable way to enumerate display labels. The single-object variant `o:szd.{n}/sdef:TEI/get` returned HTTP 500 on 23 September 2026 (checked with `o:szd.174`).

## Rendering contract (grouped lists)

The Personal Documents, the Works list and the Essays share one renderer, `szd-Werke.xsl` in the gams-www repository (`ZIMLAB/szd`). It builds the page with a two-level `xsl:for-each-group`. The outer group is `term[@type="classification"]` (the h2 navbar category), the inner group is `title[@type="Einheitssachtitel"]` (the h3 document-type heading). An entry missing either grouping key is dropped silently, present in the TEI and ingested, yet rendered nowhere.

Every `biblFull` in a grouped list therefore carries, beyond its content fields:

- `profileDesc/textClass/keywords/term[@type="classification"]` in German and English, the navbar category. It is keyed on the locale alone and has no language fallback.
- `titleStmt/title[@type="Einheitssachtitel"]`, the document-type sub-heading. The inner `group-by` selects the title of the current locale or one without `@xml:lang`, so a language-less Einheitssachtitel groups correctly in both languages and only a completely absent one drops the entry.
- the PID as `msIdentifier/altIdentifier/idno[@type="PID"]`, because a bare `idno` produces no IIIF or Mirador facsimile link.

Navbar categories are a closed set. A new classification is added only for something fundamental and permanent. Existing `Einheitssachtitel` values are reused verbatim in both languages, so the entry joins the existing heading group. The renderer side is documented in gams-www `knowledge/Rendering-and-Search.md`.

In June 2026 the thirteen SZ-AAL/L documents were ingested with valid PIDs and appeared nowhere in the frontend until each received an `Einheitssachtitel` and its PID was wrapped in `altIdentifier`.

## Rendering contract (correspondence facsimile gallery)

A second, independent grouping contract governs the correspondence facsimile gallery `context:szd.facsimiles.korrespondenzen`, rendered by `szd-Facsimiles.xsl` (gams-www). The person view groups every letter by its correspondent with `group-by="creator[not(. = 'Zweig, Stefan')] | contributor[@bound != 'false']"`. The key is `dc:creator` unless it is exactly `Zweig, Stefan`, otherwise a bound `dc:contributor`. A letter authored by Zweig with no `dc:contributor` has an empty key and falls out of the grouping. Only a catch-all branch (Ohne Korrespondenzpartner, Without correspondent) can render it, and only where that XSL is deployed.

The correspondence facsimiles are `cm:dfgMETS` book objects. In their GAMS `<book>` source format, `<author>` becomes `dc:creator` and `<contributor>` becomes `dc:contributor`. Every letter authored by Zweig therefore carries a `<contributor>` element with the recipient (`Lastname, Firstname`, several recipients as several elements), or it never appears in the gallery. The legacy `enrichXML-briefe.py` matched only the older title pattern with ' an ' and ' vom ' and skipped titles with bracketed dates, which is why the SZ-AAL letters authored by Zweig stayed without contributor after their ingest in June 2026 and were absent from the gallery until the recipient was derived from the title. The renderer side is documented in gams-www `knowledge/Facsimiles-Korrespondenzen.md`.

The rendered `…/sdef:Context/get` page is cached. Context membership (the `QUERY` datastream, queryable live via `risearch`) updates immediately, while the rendered gallery reflects metadata and membership changes only after GAMS rebuilds it.

## IIIF structure labels in book sources

The GAMS method `sdef:IIIF/getManifest` copies the `<div type="…">` labels of the `<book>` structure into the JSON `label` of each `sc:Range` without escaping. A straight double quote in such a label (`&quot;` in the XML) yields invalid JSON, Mirador cannot parse the manifest, and the viewer stays empty although every image datastream and the Image API are intact. Object titles with quotes are escaped correctly. Ingest sources under `PROJECTS/szd/done/**/Result_*.xml` therefore carry no straight double quotes in `div/@type`, and typographic quotes („…“) take their place. The root fix would be the escaping in the GAMS manifest generator. The affected objects, the prepared repaired sources and the ingest procedure are in [scripts/iiif_structure_labels/](../scripts/iiif_structure_labels/README.md).

## Licensing and Access

Each TEI header states CC BY 4.0 in its `availability` element, while the [README](../README.md#licence) reserves the rights of the archival research data to the archive. Which statement applies is an open question in the [plan](plan.md#operator-questions). They are accessible at https://stefanzweig.digital/, through the GAMS context https://gams.uni-graz.at/context:szd and per object at `https://gams.uni-graz.at/{PID}`. Long-term preservation copies are on Zenodo, https://zenodo.org/records/17421555.

## Related

- [DATA_MODEL.md](DATA_MODEL.md), encoding patterns shared by all files
- [DATA.md](DATA.md), data gaps and checkup results
- [MAPPING.md](MAPPING.md), TEI-CSV schema for correspondence
- [ONTOLOGY.md](ONTOLOGY.md), mapping of the collections to SZDO classes
- [ARCHITECTURE.md](ARCHITECTURE.md), system integration and ingest
