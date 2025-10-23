# Data Model - Stefan Zweig Digital

Technical documentation of TEI-XML structure, bilingual architecture, and encoding patterns used across all SZD collections.

---

## TEI-XML Structure

### Core Architecture

All SZD data uses TEI P5 (Text Encoding Initiative) XML with consistent header and body structure:

```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <!-- Metadata -->
  </teiHeader>
  <text>
    <body>
      <!-- Collection-specific content -->
    </body>
  </text>
</TEI>
```

### TEI Header Components

**titleStmt** - Bilingual titles
```xml
<titleStmt>
  <title xml:lang="de">Korrespondenzen Stefan Zweig digital</title>
  <title xml:lang="en">Correspondences Stefan Zweig digital</title>
</titleStmt>
```

**publicationStmt** - Publisher, authority, distributor
```xml
<publicationStmt>
  <publisher>
    <orgName ref="d-nb.info/gnd/1047605287">Literaturarchiv Salzburg</orgName>
  </publisher>
  <authority>
    <orgName ref="d-nb.info/gnd/1137284463">Zentrum für Informationsmodellierung</orgName>
  </authority>
  <distributor>
    <orgName ref="https://gams.uni-graz.at">GAMS</orgName>
  </distributor>
  <availability>
    <licence target="https://creativecommons.org/licenses/by/4.0">CC BY 4.0</licence>
  </availability>
  <idno type="PID">o:szd.korrespondenzen</idno>
  <date when="2021-02-25">25.02.2021</date>
</publicationStmt>
```

**seriesStmt** - Project metadata and responsibilities
```xml
<seriesStmt>
  <title ref="https://gams.uni-graz.at/szd">Stefan Zweig digital</title>
  <respStmt>
    <resp>Projektleitung</resp>
    <persName>
      <forename>Manfred</forename>
      <surname>Mittermayer</surname>
    </persName>
  </respStmt>
  <respStmt>
    <resp>Datenmodellierung</resp>
    <persName>
      <forename>Christopher</forename>
      <surname>Pollin</surname>
    </persName>
  </respStmt>
</seriesStmt>
```

**projectDesc** - Project description in German
```xml
<projectDesc>
  <p>Das Projekt verfolgt das Ziel, den weltweit verstreuten Nachlass von
  Stefan Zweig im digitalen Raum zusammenzuführen und ihn einem
  literaturwissenschaftlich bzw. wissenschaftlich interessierten Publikum
  zu erschließen...</p>
</projectDesc>
```

---

## Bilingual Architecture

All user-facing content is encoded in both German and English using `xml:lang` attributes.

### Implementation Patterns

**Titles**
```xml
<title xml:lang="de">Korrespondenzstück AN Stefan Zweig</title>
<title xml:lang="en">Piece of Correspondence TO Stefan Zweig</title>
```

**Biographical Events**
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

**Person Names**
```xml
<person xml:id="SZDPER.1">
  <persName ref="http://d-nb.info/gnd/12490310X">
    <surname>Abraham</surname>
    <forename>Pierre</forename>
  </persName>
</person>
```

### Display Logic

Frontend XSL stylesheets select content based on language parameter:
- German content: `xml:lang="de"`
- English content: `xml:lang="en"`

SPARQL queries include bilingual result sets using FILTER clauses on language tags.

---

## Authority File Integration

### Person References

All persons link to authority files using standard identifiers:

**GND (Gemeinsame Normdatei)**
```xml
<persName ref="http://d-nb.info/gnd/12490310X">
  <surname>Abraham</surname>
  <forename>Pierre</forename>
</persName>
```

**Wikidata/Wikipedia**
```xml
<person corresp="https://de.wikipedia.org/wiki/Pierre_Abraham" xml:id="SZDPER.1">
  <persName ref="http://d-nb.info/gnd/12490310X">
    <surname>Abraham</surname>
    <forename>Pierre</forename>
  </persName>
</person>
```

### Organization References

```xml
<orgName corresp="https://www.uni-salzburg.at/index.php?id=72"
         ref="d-nb.info/gnd/1047605287">
  Literaturarchiv Salzburg
</orgName>
```

### Reference Patterns

- `@ref` - Primary authority file identifier (GND)
- `@corresp` - Additional links (Wikipedia, Wikidata, institutional URLs)
- `@type` - Reference type (person, place, organization)

---

## Identifier System

### Collection Identifiers

Each collection has a persistent identifier (PID) pattern:

- `o:szd.korrespondenzen` - Correspondence collection
- `o:szd.personen` - Person index
- `o:szd.lebenskalender` - Biography timeline
- `o:szd.autographen` - Autographs
- `o:szd.bibliothek` - Library
- `o:szd.werke` - Works

### Item Identifiers

Individual items use collection-specific IDs:

**Correspondence**
```xml
<biblFull xml:id="SZDKOR.1">
```

**Persons**
```xml
<person xml:id="SZDPER.1">
```

**Biographical Events**
```xml
<event xml:id="SZDBIO.1">
```

**Pattern:** `{COLLECTION_CODE}.{NUMBER}`

---

## Collection-Specific Structures

### Correspondence (SZDKOR)

Uses `<biblFull>` for correspondence bundles with nested `<msDesc>` for individual letters:

```xml
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
```

See [MAPPING.md](MAPPING.md) for complete TEI-CSV schema mapping.

### Person Index (SZDPER)

Authority file using `<listPerson>` with external identifiers:

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

### Biography (SZDBIO)

Timeline using `<listEvent>` with bilingual descriptions:

```xml
<listEvent>
  <event xml:id="SZDBIO.1">
    <head>
      <span xml:lang="de">Wien <date when="1881-11-28">28. November 1881</date></span>
      <span xml:lang="en">Vienna, <date when="1881-11-28">28 November 1881</date></span>
    </head>
    <ab xml:lang="de">Stefan Zweig wird als zweiter Sohn geboren.</ab>
    <ab xml:lang="en">Stefan Zweig is born the second son.</ab>
  </event>
</listEvent>
```

### Works (SZDWRK)

Uses `<listBibl>` for published works with publication details and classifications.

### Library (SZDLIB)

Personal book collection using `<listBibl>` with annotations and provenance information.

### Autographs (SZDAUT)

Handwritten manuscripts using `<msDesc>` with physical descriptions and facsimile links.

---

## Date Encoding

### ISO 8601 Dates

All machine-readable dates use `@when` attribute:

```xml
<date when="1881-11-28">28. November 1881</date>
```

### Date Ranges

```xml
<date from="1900" to="1910">1900-1910</date>
```

### Uncertain Dates

```xml
<date when="1920" cert="medium">ca. 1920</date>
```

---

## Metadata Standards

### METS/MODS

Used for structural metadata in GAMS infrastructure (not visible in TEI files).

### DataCite Schema 4.0

Used for Zenodo deposits - metadata extracted from TEI and transformed to DataCite JSON.

### Dublin Core

Generated from TEI header for OAI-PMH harvesting.

---

## Character Encoding

All files use UTF-8 encoding:

```xml
<?xml version="1.0" encoding="UTF-8"?>
```

Special characters are encoded as UTF-8 rather than XML entities where possible.

---

## Validation

### TEI P5 Schema

All files validate against TEI P5 schema with SZD-specific customizations.

### Quality Assurance

See [../scripts/validation/README.md](../scripts/validation/README.md) for validation tools including:

- `validate_tei_csv.py` - TEI-XML structure validation
- `validate_tei_against_csv.py` - Cross-reference validation
- `fix_mojibake.py` - Character encoding cleanup

---

## Related Documentation

- [COLLECTIONS.md](COLLECTIONS.md) - Collection-specific encoding details
- [MAPPING.md](MAPPING.md) - Complete TEI-CSV schema for correspondence
- [DATA.md](DATA.md) - Data quality and coverage statistics
- [ARCHITECTURE.md](ARCHITECTURE.md) - System integration and data flow

---

**Standards:**
- TEI P5 Guidelines: https://tei-c.org/guidelines/
- ISO 8601: Date/time encoding
- GND: https://www.dnb.de/gnd
- Wikidata: https://www.wikidata.org/

**Last Updated:** October 2025
