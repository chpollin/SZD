---
title: RDF mapping
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD  # the served files it describes are in https://zimlab.uni-graz.at/gams/projects/szd/gams-www
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: complete
language: en
created: 2026-06-15
updated: 2026-10-30
authors: [Christopher Pollin]
generated-with: Claude Code (Claude Opus 5.5)
related: [data, search-architecture, testing, deployment-architecture]
---

# RDF mapping

How `szd-TORDF.xsl` in gams-www turns the TEI of an SZD object into the `szd:` RDF that GAMS loads into Blazegraph at ingest and on which the content search runs. A fix here changes the search and takes effect only with a renewed ingest of the affected objects, so every change is checked as [testing](testing.md#rule) requires.

## Structure of the stylesheet

The stylesheet branches at the top on the PID of the TEI header (`//t:fileDesc/t:publicationStmt/t:idno[@type='PID']`) in one central `<xsl:choose>` and calls one named template per PID, each modelling one entity type. A PID without a branch falls into the `otherwise` branch, which writes an error text. The letter edition `o:szd.SZDBRI.1` has no branch since `07ba5d4`.

## Namespaces

| Prefix | Namespace | Use |
|---|---|---|
| `szd:` | `…/o:szd.ontology#` | project ontology, classes and most properties |
| `szdg:` | `…/o:szd.glossar#` | controlled vocabulary of work and material types |
| `gams:` | `…/o:gams-ontology#` | `gams:isMemberOfCollection`, `gams:textualContent` |
| `dcterms:` | Dublin Core terms | `dcterms:replaces` |
| `foaf:` | FOAF | `foaf:page` (Wikipedia page of a person) |
| `owl:`, `rdfs:` | OWL, RDFS | `owl:seeAlso`, `rdfs:seeAlso` |
| `gnd:` | GND | `gnd:gndIdentifier` |
| `wgs84_pos:` | WGS84 | `wgs84_pos:lat` and `wgs84_pos:long` (repository coordinates) |

`skos:` and the GeoNames prefix `gn:` are declared but not used by the transformation. SKOS lives in the separate glossary object.

## Classes

Every main resource has the URI `https://gams.uni-graz.at/` + PID + `#` + `@xml:id`, for instance `https://gams.uni-graz.at/o:szd.werke#SZDMSK.42`.

| Class | PID | Iteration root |
|---|---|---|
| `szd:Book` | `o:szd.bibliothek` | `listBibl/biblFull` |
| `szd:Autograph` | `o:szd.autographen` | `listBibl/biblFull` |
| `szd:Work` | `o:szd.werke` | `listBibl/biblFull` |
| `szd:PersonalDocument` | `o:szd.lebensdokumente` | `listBibl/biblFull` |
| `szd:Essay` | `o:szd.aufsatzablage` | `listBibl/biblFull` |
| `szd:BundleOfCorrespondence` | `o:szd.korrespondenzen` (Konvolut entries) | `listBibl/biblFull` |
| `szd:Correspondence` with `szd:PhysicalDescription` | `o:szd.korrespondenzen.*` (pieces) | `listBibl/biblFull` |
| `szd:BiographicalEvent` | `o:szd.lebenskalender` | `listEvent/event` |
| `szd:Agent` (person) | `o:szd.personen` | `listPerson/person` |
| `szd:Location` | `o:szd.standorte` | `listOrg/org` |
| `szd:Organisation` | `o:szd.organisation` | `listOrg/org` |
| `szd:Collection` | `o:szd.thema.<n>` | theme object |
| `szd:WorkIndexEntry` | `o:szd.werkindex` | `listBibl/bibl` |
| `szd:Manifestation` | `o:szd.klawiter` | `text/body/listBibl/biblStruct` |

Value objects with their own URI (base URI plus a suffix) are `szd:Extent` (`EX`), `szd:PublicationStmt` (`PU`), `szd:ProvenanceCharacteristic` (`PC`), `szd:OriginalShelfmark` (`OS`), `szd:Binding` (a shared resource through `for-each-group`), the enclosure (`EN`, written as `szd:Enclosur`), `szd:pubDateStmt` and `szd:creationStmt`.

## Mapping from TEI

- `titleStmt/title[@xml:lang]` to `szd:title` (de, en), `title[@type='original'|'Einheitssachtitel']` to `szd:originaltitle`
- `titleStmt/author|editor[@role]` to role-specific person properties (`szd:author`, `szd:editor`, `szd:composer`, `szd:illustrator`, `szd:translator`, `szd:writerForeword`, `szd:writerAfterword`, `szd:partyInvolved`)
- `sourceDesc/msDesc/msIdentifier/idno` to `szd:signature`, `…/repository` to `szd:location`
- `physDesc/objectDesc/supportDesc/extent` to an `szd:Extent` resource
- `physDesc/…/material[@ana='szdg:WritingMaterial'|'WritingInstrument']` to `szd:writingMaterial` and `szd:writingInstrument`
- `physDesc/additions`, `altIdentifier` and stamps to `szd:ProvenanceCharacteristic` and `szd:OriginalShelfmark`, with property names built from `substring-after(@target,':')`
- `history/origin/origDate/@when` to `szd:dateOfPublication`, `history/provenance` to `szd:provenance`, `history/acquisition` to `szd:acquired`
- `profileDesc/textClass/keywords/term[@type='person'|'work'|'classification']` to `szd:relationToPerson`, `szd:relationToWork` and `szd:category`, for the autographs relative to each entry
- `term[@type='person_affected']/@ref` to `szd:affectedPerson` (autographs and personal documents, read by the person search)
- `correspDesc/correspAction[@type='sent'|'received']` to `szd:sender` and `szd:receiver`, with `szd:sentDate` and `szd:sentLocation`
- persons (`listPerson/person`), `persName/@ref` to `szd:gnd`, `idno[@type='wikidata']` to `szd:wikidata`, `birth/death/@when` to `szd:birth` and `szd:death`, `@corresp` to `foaf:page`
- events (`listEvent/event`), `head/span/date/@from|@when` to `szd:when`, `ab[@xml:lang]` to `szd:content`, `ab/name/@ref` to a `szd:relationTo` resource chosen by the identifier prefix (SZDPER, SZDMSK, SZDLEB, SZDBIB, SZDAUT)
- repositories (`listOrg/org`), `orgName` to `szd:name`, `settlement` to `szd:settlement`, `orgName/@ref` to `gnd:gndIdentifier`, `location/geo` to `wgs84_pos:lat` and `wgs84_pos:long`
- language to `szd:language` with the Library of Congress vocabulary `http://id.loc.gov/vocabulary/iso639-2/…`

## Reference resolution

`GetPersonlist`, `GetStandortelist` and `GetOrglist` load the index objects with `document()` and normalise every person, repository or organisation reference, GND or SZD identifier, to a stable internal URI (`#SZDPER.n`, `#SZDSTA.n`, `#SZDORG.n`). Every token of a multi-valued `@ref`, separated by blanks, semicolons or commas, gets its own triple, and a GND is compared without scheme and trailing slash, so `http` and `https` forms resolve alike. Persons keep a substring comparison on the GND, because an exact comparison would drop an index entry whose GND carries an extra digit. Organisations are looked up through the key `OrgByGND` on the bare GND identifier. A GND without an index match produces nothing.

`GetOrglist` is called for `correspAction[@type='sent'|'received']/orgName` as `szd:sender` and `szd:receiver` (Konvolute and pieces), for `titleStmt/author|editor[not(@role)]/orgName` as `szd:author` and `szd:editor` (library, autographs) and for `titleStmt/editor[@role='contributor']/orgName` as `szd:partyInvolved` (works, personal documents). Holding places stay `szd:location` on `o:szd.standorte`. An actor role never points to `o:szd.standorte`, and `szd:location` never to `o:szd.organisation`. `term[@type='organization']` in the correspondence is not mapped.

Further helpers are `createTriple` (datatype or object property), `FulltextSearchData` (fills `gams:textualContent`), `printEnDe` and `getEnDe` (German and English through `@xml:lang`), `getDate` and the category mapping, which maps German GND subject groups ("Romane", "Tagebücher" and others) to glossary URIs (`szdg:#Novel`, `#Diary` and others).

### Index hosts

The resource URIs always use `https://gams.uni-graz.at/`. The index objects are read from a host that depends on where the stylesheet runs. Persons and repositories come from `$INDEX_HOST`, the host of `static-base-uri()` when that is an http URL and production otherwise. The organisation index comes from the first of `$INDEX_HOST`, production and staging that serves `o:szd.organisation`, tested with `doc-available()`.

The fallback rests on an inference from the staging ingest of `o:szd.bibliothek` on 2026-09-24. With a clean `TORDF` reference, its RDF resolved every person by GND but none of the corporate editors, although `o:szd.organisation` existed on staging and production answered 404 for it. The ingest therefore runs the stylesheet without an http base URI, `$INDEX_HOST` is production, and `document()` on the missing object yielded nothing without failing the ingest. Two consequences follow. A staging ingest resolves persons and repositories against the production indexes, which can differ from the staging copies. A production ingest while `o:szd.organisation` was missing in production resolved corporate bodies against the staging index, with URIs that still point to production. Production has had the object since 2026-10-09, and its `RDF` datastream still answered 404 at 19:20 UTC that day. Whether an ingest reaches the staging host at all is shown only by the next staging ingest of a holding with corporate bodies.

## Organisations

The organisation index `o:szd.organisation` (in the data repository `data/Index/Organisation/SZDORG.xml`, built by the scripts in `scripts/organisationen_index/`) is recognised by its PID, because `o:szd.standorte` is a `listOrg` as well. Every `org` becomes one `szd:Organisation` with the URI `https://gams.uni-graz.at/o:szd.organisation#SZDORG.n`.

| Property | Source | Remark |
|---|---|---|
| `szd:name` | `orgName[not(@type='variant')]` | de and en through `printEnDe` when `@xml:lang` is set, otherwise one literal without language. Variants reach only the full text |
| `szd:gnd` | `orgName/@ref` | object property on the GND URI as for `szd:Agent` |
| `rdfs:seeAlso` | `@corresp` | website of the institution |
| `szd:settlement`, `szd:country` | `settlement`, `country` | |
| `rdfs:seeAlso` | `idno[@type='SZDSTA']` | link to the repository entry of the same body, `…/o:szd.standorte#SZDSTA.n` |
| `dcterms:replaces` | `idno[@type='SZDPER'][@subtype='superseded']` | `…/o:szd.personen#SZDPER.n`, the person entry the migration removed |
| `gams:textualContent` | `FulltextSearchData` | all text nodes including variants and identifiers |
| `gams:isMemberOfCollection` | fixed | `https://gams.uni-graz.at/o:szd.organisation` |

## Theme pages

The template `Collection` maps every object `o:szd.thema.<n>` to one `szd:Collection` whose URI is the object URI without fragment, `https://gams.uni-graz.at/o:szd.thema.<n>`.

| Property | Source | Remark |
|---|---|---|
| `szd:title` | first `teiHeader//titleStmt/title` | one literal without language tag |
| `szd:connectedWithDocument` | `div/head/title/@ref`, split at blanks | taken over unchanged, which produces relative URIs such as `#SZDLEB.2` |
| `szd:connectedWithPerson` | every `text//name/@ref` with an `SZDPER` reference, with or without `@type="person"` | `https://gams.uni-graz.at/o:szd.personen#SZDPER.n`, once per person |
| `gams:textualContent` | title and all text nodes of `text` | basis of the full-text search |
| `gams:isMemberOfCollection` | fixed | `https://gams.uni-graz.at/context:szd` |

`szd:connectedWithPerson` is the bridge to the person search, which queries `?re ?hasrole <…/o:szd.personen#SZDPER.n>`. A new theme page is found only after its graph has been added as a `FROM` line to the person and full-text queries, see [search-architecture](search-architecture.md#query-objects).

## Klawiter bibliography

The template `Klawiter` maps every `biblStruct` of `o:szd.klawiter` to one `szd:Manifestation` with the URI `https://gams.uni-graz.at/o:szd.klawiter#SZDKLA.<page>.<n>`. The bibliography describes publications, not items SZD holds, so the class follows the ontology, which names Manifestation as the bridge to the Klawiter entries, and the holding vocabulary (`szd:location`, `szd:signature`, provenance, `szd:PublicationStmt`) stays out. The TEI profile is described in the repository of the bibliography (https://github.com/chpollin/klawiter-rescue, `knowledge/tei-profile.md`).

| Property | Source | Remark |
|---|---|---|
| `szd:title` | `monogr/title` | one literal without language tag, because the titles are transliterated; an empty title gives no triple |
| `szd:translator`, `szd:editor`, `szd:illustrator`, `szd:partyInvolved` | `monogr/respStmt/persName[@role]`, `contributor` to `szd:partyInvolved` | a blank node with `szd:name`, the name as the source gives it |
| `szd:dateOfPublication` | `imprint/date/@when` | `xsd:gYear` when castable, a date without `@when` gives no triple |
| `szd:pubPlace`, `szd:publisher` | `imprint/pubPlace`, `imprint/publisher` | literals |
| `szd:language` | `monogr/textLang/@mainLang` | ISO 639-1 mapped to the Library of Congress ISO 639-2 URI through the language catalogue of `context:szd`; a code without ISO 639-2 form (`sh`) keeps the language name of `textLang` as a literal |
| `gams:textualContent` | `FulltextSearchData` | all text of the `biblStruct` and its identifier |
| `gams:isMemberOfCollection` | fixed | `https://gams.uni-graz.at/o:szd.klawiter` |

No triple asserts an identity. No authority link of the bibliography is confirmed, so places and publishers stay literals instead of the object properties `szd:hasPublicationPlace` and `szd:hasPublisher` of the ontology, and a contributor is a blank node instead of a person URI, which also avoids a new identifier scheme. The person search therefore never finds a Klawiter entry, while the full-text query shows an editor through `szd:name`. Producer (`@resp`), passage (`@source`) and statement state (`@ana`) of every value stay in the TEI, because the RDF has no property for them and `szd:certainty` stands for TEI `@cert`, which the bibliography does not use. Every value reaches the RDF whatever its state, as the page shows it, after the operator decision of 2026-10-30 that the page in SZD shows no provenance. The identifiers `SZDKLA.<page>.<n>` are provisional until the identifier scheme of the bibliography is decided, so the object goes to staging with them and to production only after that decision.

## Search basis

At ingest, the `szd:` RDF of every object is loaded into Blazegraph as a named graph whose URI is the PID.

- Full text uses `gams:textualContent` as its index. The transformation enriches it with the name variants of the author from the person index, the SZD identifier and the written-out language names, which is why the enrichment happens at ingest.
- The person search works because every person reference, including every token of a multi-valued `@ref`, is normalised to a `#SZDPER.n` URI, and organisation references to `#SZDORG.n`.
- The repository search matches `szd:location` with a `#SZDSTA.n` URI.
- The category search matches glossary URIs, the work search `szd:relationToWork`.

The queries themselves are described in [search-architecture](search-architecture.md).

## Character of the model

The SZD ontology is a standalone, application-specific ontology. It is anchored externally through GND, Wikidata, WGS84 coordinates, the Library of Congress language codes and the SKOS glossary `szdg:`. Persons, repositories, organisations and works are separate index objects, and their relations hold only in Blazegraph through the shared SZD identifiers.

## Open findings

The structure-preserving refactoring of 2026-09-23 recorded these findings without fixing them, because every fix changes the RDF and therefore the search. A fix needs its own golden comparison and a renewed ingest of the affected objects. The RDF model questions among them wait for one operator pass, see [plan](plan.md#operator-questions).

- `szd:ProvenanceCharacteristic` separates with different characters in the English and the German version.
- `idno[@type='wikidata']` lacks the `t:` prefix, so `owl:seeAlso` never arises for persons.
- A German `orgName` is written with `xml:lang="en"`.
- The element of the enclosure is named `szd:Enclosur`.
- The test on `author[@ref='SZDPER.1560']` never matches.
- The languages of `szd:secretarialHand` are swapped.
- `szd:provenance` is written empty.
- `getDate` is meant to type a value castable as `xs:date` as `xsd:date`, but never does, because its callers already pass the attribute `@when`.
- The `SZDBIB` branch through the parameter `SZD_ID` is dead.
- The genre "Erzählung" is mapped to `#Movie`, "Vorträge" to `#Narration`.
- `getLocation` writes text into the resource when it fails.
- Correspondence pieces receive the fixed repository `SZDSTA.1`.
- `szd:connectedWithDocument` produces relative URIs such as `#SZDLEB.2`.
- The templates `GetPlace` and `languageCode` are never called.
