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
- [../scripts/validation/README.md](../scripts/validation/README.md) - Validation tools

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

---

## Personal Documents (SZDLEB)

**File:** [data/PersonalDocument/SZDLEB.xml](../data/PersonalDocument/SZDLEB.xml)
**PID:** o:szd.lebensdokumente

### Structure

Life documents using `<msDesc>` for archival materials.

### Content

Personal documents from Stefan Zweig's life including:

- Official documents
- Certificates
- Legal papers
- Personal notes
- Ephemera

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
- **Some collections:** CC-BY-NC 4.0 or CC-BY-NC-SA 4.0

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

**Last Updated:** October 2025
