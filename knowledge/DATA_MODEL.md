---
title: Data Model
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

# Data Model

The TEI P5 encoding patterns that all SZD files share, covering the header, the bilingual encoding, authority references, identifiers and dates. The collection-specific structures, with entry examples taken from the data, are in [COLLECTIONS.md](COLLECTIONS.md), the formal ontology in [ONTOLOGY.md](ONTOLOGY.md).

## TEI Header

Every file is a TEI document in the namespace `http://www.tei-c.org/ns/1.0` with a `teiHeader` and a `text` whose `body` holds the collection list. The header of the correspondence index shows the common parts, with bilingual titles in `titleStmt`, publisher, authority and distributor in `publicationStmt`, the licence and the object PID.

```xml
<titleStmt>
  <title xml:lang="de">Korrespondenzen Stefan Zweig digital</title>
  <title xml:lang="en">Correspondences Stefan Zweig digital</title>
</titleStmt>
<publicationStmt>
  <publisher>
    <orgName corresp="https://www.uni-salzburg.at/index.php?id=72" ref="d-nb.info/gnd/1047605287">Literaturarchiv Salzburg</orgName>
  </publisher>
  <authority>
    <orgName corresp="https://informationsmodellierung.uni-graz.at" ref="d-nb.info/gnd/1137284463">Zentrum für Informationsmodellierung - Austrian Centre for Digital Humanities, Karl-Franzens-Universität Graz</orgName>
  </authority>
  <distributor>
    <orgName ref="https://gams.uni-graz.at">GAMS - Geisteswissenschaftliches Asset Management System</orgName>
  </distributor>
  <availability>
    <licence target="https://creativecommons.org/licenses/by/4.0">Creative Commons BY 4.0</licence>
  </availability>
  <idno type="PID">o:szd.korrespondenzen</idno>
  <date when="2021-02-25">25.02.2021</date>
</publicationStmt>
```

`seriesStmt` names the project and the responsibilities (`respStmt` with `resp` Datenerfassung and Datenmodellierung), and `encodingDesc/projectDesc` carries the German project description. The `idno[@type="PID"]` in `publicationStmt` is the object PID that scripts such as the timeline generator read.

## Bilingual Encoding

User-facing content is encoded in German and English with `xml:lang`, either as parallel elements (`title`, `span`, `ab`, `material`, `date`) or as parallel `span` elements inside one element. The frontend XSL selects the language by a locale parameter, and SPARQL queries filter by language tag. Where a language is missing, the renderers behave differently per field. The rendering contract in [COLLECTIONS.md](COLLECTIONS.md#rendering-contract-grouped-lists) names the keys that must exist in both languages.

## Authority References

- `@ref` carries the primary authority identifier, for persons and corporate bodies the GND (`http://d-nb.info/gnd/<id>`), for places a GeoNames URI where present.
- `@corresp` carries additional links, the Wikipedia article on `person` and institutional websites on `org` and `orgName`.
- `idno[@type="wikidata"]` in the person index carries the Wikidata entity (`http://www.wikidata.org/entity/<Q-id>`).

References from the holdings to the indices take the forms `ref="#SZDPER.<n>"`, the GND of the index entry, or for bodies without GND `https://gams.uni-graz.at/o:szd.organisation#SZDORG.<n>` and `https://gams.uni-graz.at/o:szd.standorte#SZDSTA.<n>`. How the RDF transformation resolves them is described per index in [COLLECTIONS.md](COLLECTIONS.md).

The spelling of the GND prefix is not uniform across the files. Headers carry `d-nb.info/gnd/…` without scheme, the holdings `http://d-nb.info/gnd/…`, and some values `https://`. A comparison of GND values therefore normalises scheme and trailing slash, or it matches character for character and inherits this variation.

## Identifiers

- Object PIDs follow `o:szd.<name>` for collections and indices (`o:szd.werke`, `o:szd.personen`), `o:szd.korrespondenzen.<person>` for konvolut objects and `o:szd.<number>` for facsimile objects. The full list is the overview table in [COLLECTIONS.md](COLLECTIONS.md#collection-overview).
- Entries carry `xml:id` values after the pattern `{COLLECTION_CODE}.{NUMBER}` (`SZDKOR.1`, `SZDPER.1`, `SZDBIO.1`), letters in konvolut objects `SZDKOR.<person>.<n>` (`SZDKOR.altmann-hannah.1`).
- Index identifiers are part of the RDF URIs and are never renumbered. A new entry receives the next free number, and the identifier of a removed or merged entry is never assigned again. Removed persons are kept in `scripts/checkup_2026_09_index/removed_persons.xml`, superseded persons that became corporate bodies stay visible as `idno[@type="SZDPER"][@subtype="superseded"]` in the organisation index.

## Date Encoding

Machine-readable dates use ISO 8601 values in the attributes of `date` or `origDate`, beside the display text of the source. The forms below are taken from the data.

```xml
<!-- exact date, SZDBIO -->
<date when="1881-11-28">28. November 1881</date>

<!-- range, SZDBIO -->
<date from="1906-04" to="1906-08">April bis August 1906</date>

<!-- inferred range, SZDBIB -->
<date notBefore="1899" notAfter="1900">1899-1900</date>

<!-- uncertain date, SZDKOR -->
<date xml:lang="en" cert="low" when="1939">1939 (?)</date>

<!-- supplied date in a konvolut object -->
<date when="1939-02" ana="supplied/verified" xml:lang="de">Februar 1939</date>
```

The coverage of machine-readable dates and the remaining gaps are in [DATA.md](DATA.md#dates), the reading rules of the timeline generator in [Lebenskalender-Lanes.md](Lebenskalender-Lanes.md#dating-rules).

## Metadata Standards

- METS/MODS carries the structural metadata of the facsimile objects in GAMS and does not appear in the TEI files.
- Dublin Core is generated from the TEI for OAI-PMH harvesting.
- DataCite Schema 4.0 describes the Zenodo deposits and is derived from the TEI.

## Character Encoding and Validation

All files are UTF-8, and special characters are written as characters rather than XML entities where possible. Some konvolut files carry double-encoded umlauts from earlier imports.

The repository holds no TEI schema or ODD. The processing scripts check well-formedness and the invariants of their own changes with `--verify`. The ontology is validated separately with `python ontology/validate.py`.

## Related

- [COLLECTIONS.md](COLLECTIONS.md), collection-specific encoding and rendering contracts
- [MAPPING.md](MAPPING.md), TEI-CSV schema for correspondence
- [DATA.md](DATA.md), data gaps
- [ARCHITECTURE.md](ARCHITECTURE.md), system integration and data flow
- [ONTOLOGY.md](ONTOLOGY.md), the formal ontology SZDO
