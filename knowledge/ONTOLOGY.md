---
title: Stefan Zweig Digital Estate Ontology (SZDO)
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD.git
method:
  name: Promptotyping
  url: https://dhcraft.org/promptotyping
status: complete
created: 2026-03-29
updated: 2026-09-24
---

# Stefan Zweig Digital Estate Ontology (SZDO)

The SZDO is the formal OWL ontology for the digital estate (Nachlass) of Stefan Zweig. It models archival, bibliographic and biographical entities and their relations. Its archival backbone follows Records in Contexts (RiC-O), the work layer follows the IFLA Library Reference Model (LRM), and events and provenance follow the CIDOC Conceptual Reference Model (CRM). The Turtle sources are in [../ontology/](../ontology/), the generated reference is at https://chpollin.github.io/SZD/ontology/.

## 1. Two-layer architecture

Since v1.2.0 the SZDO builds on a generic estate ontology that other estate projects can reuse.

| Layer | Namespace and prefix | File | Purpose |
|-------|----------------------|------|---------|
| Generic | `https://w3id.org/nachlass#` (`nachlass:`) | `nachlass-ontology.ttl` | Reusable core for any estate project |
| SZD | `https://gams.uni-graz.at/o:szd.ontology#` (`szdo:`) | `szd-ontology.ttl` | GAMS PIDs, Klawiter integration, work types, legacy GAMS terms |

The SZDO imports `nachlass:` via `owl:imports` and specialises its core classes.

```
nachlass:Estate            <--- szdo:Estate
nachlass:Collection        <--- szdo:Collection
nachlass:Record            <--- szdo:Record (+ SZD record types)
nachlass:DigitalObject     <--- szdo:DigitalObject
nachlass:Work              <--- szdo:WorkIndexEntry (+ work types, Klawiter)
nachlass:Agent             <--- szdo:Agent (+ SZDPER, SZDORG)
nachlass:BiographicalEvent <--- szdo:BiographicalEvent (+ SZDBIO)
nachlass:Place             <--- szdo:Place (+ SZDSTA)
```

## 2. Design principles

1. Archive first. RiC-O is the foundation for describing the estate material.
2. LRM-compatible work layer for the intellectual works.
3. CIDOC-CRM-compatible events for provenance and biography.
4. Linked data through GND, Wikidata, GeoNames and VIAF.
5. Bilingual labels and definitions in German and English.
6. Extensible for the Klawiter bibliography and later projects.
7. English identifiers that coincide with the production GAMS vocabulary wherever the meaning is the same (section 3).

## 3. Naming convention

- Identifiers are English and ASCII. Classes are UpperCamelCase, properties lowerCamelCase. The SHACL shapes 11 and 12 in `szd-shapes.ttl` enforce this for every `szdo:` term.
- The production vocabulary of GAMS (v0.x) lives in the same namespace and is produced by `szd-TORDF.xsl` in the presentation-layer repository (`ZIMLAB/szd`), which binds the namespace to the prefix `szd:`. Where a GAMS term has the same meaning as an SZDO concept, the GAMS term is the canonical SZDO identifier. Live GAMS data therefore conforms to v2.0.0 without a mapping layer. This is why agent-role properties are bare role nouns (`author`, `sender`, `previousOwner`) and why some canonical names keep GAMS wording (`signature` for the shelfmark, `when` for the date, `page` for the page count, `writerForeword`).
- Where GAMS uses a term with a different meaning, datatype or spelling, the SZDO concept has its own English name and the GAMS term stays as an `owl:deprecated` legacy term (section 11.3).
- Concepts without a GAMS term take their name from the English label or, where the ontology aligns with RiC-O or LRM, from that standard (`Record`, `Expression`, `Item`). Other object properties use `has`/`is` verbs (`hasPart`, `isPartOf`).
- Labels (`rdfs:label`) and definitions (`rdfs:comment`) stay bilingual. Only identifiers are English.
- Documentation uses the prefix `szdo:` throughout. `szd:` appears only when quoting the GAMS XSLT, and denotes the same namespace.
- The glossary concepts in `szdg:` are defined in `data/Glossary/szd-Glossary.xml` and keep their identifiers (for example `szdg:DatumEvidenz`).

## 4. External vocabularies

| Prefix | Namespace | Role |
|--------|-----------|------|
| `rico:` | `https://www.ica.org/standards/RiC/ontology#` | Archival core model |
| `lrm:` | `http://iflastandards.info/ns/lrm/lrmer/` | Work, expression, manifestation, item |
| `crm:` | `http://www.cidoc-crm.org/cidoc-crm/` | Events, provenance, actors |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | Controlled vocabularies (glossary) |
| `dc:` / `dcterms:` | `http://purl.org/dc/terms/` | Dublin Core metadata |
| `foaf:` | `http://xmlns.com/foaf/0.1/` | Basic person data |
| `schema:` | `https://schema.org/` | Schema.org bridge, mainly for Klawiter |
| `gams:` | `https://gams.uni-graz.at/o:gams-ontology#` | GAMS platform ontology |
| `szdg:` | `https://gams.uni-graz.at/o:szd.glossar#` | SZD glossary (SKOS) |
| `klawiter:` | `https://klawiter-rescue.github.io/vocab/` | Klawiter bibliography |
| `gnd:` | `http://d-nb.info/standards/elementset/gnd#` | GND authority data |
| `wdt:` | `http://www.wikidata.org/prop/direct/` | Wikidata properties |
| `iiif:` | `http://iiif.io/api/presentation/3#` | IIIF Presentation API |

## 5. Class hierarchy

### 5.1 Archival layer

```
szdo:Estate                          ⊂ rico:RecordSet (fonds)
│
├── szdo:Collection                  ⊂ rico:RecordSet (series)
│   ├── szdo:WorksCollection         # manuscripts, typescripts, drafts
│   ├── szdo:CorrespondenceCollection
│   ├── szdo:AutographCollection     # autographs by third parties
│   ├── szdo:LibraryCollection       # reconstructed personal library
│   ├── szdo:PersonalDocumentsCollection
│   ├── szdo:EssayCollection
│   └── szdo:ThematicCollection      # curated theme pages
│
├── szdo:Record                      ⊂ rico:Record
│   ├── szdo:Manuscript
│   ├── szdo:Typescript
│   ├── szdo:CarbonCopyTypescript
│   ├── szdo:Notebook
│   ├── szdo:Ensemble                # Konvolut
│   ├── szdo:GalleyProof
│   ├── szdo:BundleOfCorrespondence
│   ├── szdo:Autograph
│   ├── szdo:Book
│   └── szdo:PersonalDocument
│
└── szdo:DigitalObject               ⊂ rico:Instantiation
    ├── szdo:METSObject
    ├── szdo:IIIFManifest
    └── szdo:Facsimile
```

`szdo:Extent` and `szdo:Enclosure` are modelled as subclasses of `szdo:Record`, as in v1.2.0.

### 5.2 Work layer

```
szdo:WorkIndexEntry                  ⊂ lrm:Work, nachlass:Work
│  # abstract work, one entry of the work index SZDWRK
├── szdo:Expression                  ⊂ lrm:Expression (original text, translation, adaptation)
├── szdo:Manifestation               ⊂ lrm:Manifestation (published edition, Klawiter)
└── szdo:Item                        ⊂ lrm:Item (physical copy)
```

The work types by content are `FictionalWork`, `EssayisticWork`, `BiographicalWork`, `HistoricalWork`, `DramaticWork`, `PoeticWork`, `CollectedWork` (with `szdo:hasPart`), `TranslationWork` (Zweig's translations of other authors) and `ForewordAfterword`. They are subclasses of `szdo:WorkIndexEntry` and pairwise disjoint. `szdo:SecondaryLiterature` (⊂ `schema:ScholarlyArticle`) covers research about Zweig that is not part of the estate.

The abstract work is named `WorkIndexEntry` because GAMS types the SZDWRK entries with that class. The GAMS class `szd:Work` denotes the physical items of the works collection and therefore stays a legacy term under `szdo:Record` (section 11.3).

### 5.3 Agent layer

```
szdo:Agent                           ≡ rico:Agent, ⊂ crm:E39_Actor
├── szdo:Person                      ≡ rico:Person, ⊂ crm:E21_Person (SZDPER)
└── szdo:Organisation                ≡ rico:CorporateBody, ⊂ crm:E74_Group (SZDORG)
```

GAMS types the SZDPER entries as `szd:Agent` and the SZDORG entries as `szd:Organisation`.

Agent roles are properties.

| Property | Domain | Range | Meaning |
|----------|--------|-------|---------|
| `szdo:author` | WorkIndexEntry | Person | Author |
| `szdo:editor` | Manifestation | Person | Editor |
| `szdo:translator` | Expression | Person | Translator |
| `szdo:composer` | Expression | Person | Composer of a setting |
| `szdo:illustrator` | Manifestation | Person | Illustrator |
| `szdo:writerForeword` | Manifestation | Person | Author of a foreword |
| `szdo:writerAfterword` | Manifestation | Person | Author of an afterword |
| `szdo:sender` | BundleOfCorrespondence | Person | Sender |
| `szdo:receiver` | BundleOfCorrespondence | Person | Receiver |
| `szdo:scribalHand` | Record | Person | Person whose hand is identified on the document |
| `szdo:partyInvolved` | Record | Agent | Superproperty of all active roles |
| `szdo:affectedPerson` | Record | Person | Person the object is about, not an active participant |

`szdo:partyInvolved` is a subproperty of `rico:hasOrHadContributor`, and the ten active roles above it are its subproperties. `szdo:affectedPerson` is a subproperty of `rico:hasOrHadSubject` and not of `szdo:partyInvolved`.

### 5.4 Biographical and event layer

```
szdo:BiographicalEvent               ⊂ crm:E5_Event (SZDBIO)
├── szdo:Birth                       ⊂ crm:E67_Birth
├── szdo:Death                       ⊂ crm:E69_Death
├── szdo:Journey
├── szdo:PublicationEvent
├── szdo:Encounter
├── szdo:InstitutionalEvent
├── szdo:ExileEvent
└── szdo:ScholarlyEvent              # symposia, conferences, exhibitions
```

### 5.5 Place layer

```
szdo:Place                           ≡ rico:Place, ⊂ crm:E53_Place
├── szdo:GeographicalPlace           # GeoNames-linked
├── szdo:Location                    # repository, one entry of SZDSTA
└── szdo:PlaceOfOrigin
```

`szdo:Location` keeps the GAMS class name for the repositories of SZDSTA. Its English label is "Repository", and the generic layer calls the class `nachlass:Repository`.

### 5.6 Provenance layer

```
szdo:ProvenanceEvent                 ⊂ crm:E8_Acquisition
    szdo:previousOwner → Agent
    szdo:subsequentOwner → Agent
szdo:ProvenanceFeatureInstance       ⊂ crm:E13_Attribute_Assignment
    szdo:hasFeatureType → szdg:ProvenanceFeature (SKOS)
```

### 5.7 Physical description

| Property | Domain | Range | Glossary concept |
|----------|--------|-------|------------------|
| `szdo:writingMaterial` | Record | langString | `szdg:WritingMaterial` |
| `szdo:writingInstrument` | Record | langString | `szdg:WritingInstrument` |
| `szdo:extent` | Record | Extent | |
| `szdo:format` | Record | string | `szdg:PhysicalDescription` |
| `szdo:binding` | Book | langString | |
| `szdo:identifyingInscription` | Record | langString | `szdg:IdentifyingInscription` |
| `szdo:incipit` | | string | `szdg:Incipit` |
| `szdo:enclosures` | Record | Enclosure | `szdg:Enclosures` |
| `szdo:language` | | string (ISO 639-3) | |

`szdo:Extent` carries `szdo:leafCount`, `szdo:page` and `szdo:piecesOfCorrespondence`.

### 5.8 Glossary

The SKOS glossary (`szdg:`, `data/Glossary/szd-Glossary.xml`) stays the controlled vocabulary. Its main groups are the work terms (`szdg:Title`, `szdg:Incipit`, `szdg:WritingMaterial`, `szdg:WritingInstrument`, `szdg:PartiesInvolved`, `szdg:Date`, `szdg:IdentifyingInscription`, `szdg:PhysicalDescription`, `szdg:AdditionalMaterial`, `szdg:Enclosures`), the provenance features of the library (`szdg:ProvenanceFeature` with `Autograph`, `Binding`, `Insertion`, `Bookplate`, `Marginalia`, `Marker`, `Note`, `Stamp`, `Overpasting`, `RemovedPage`, `PresentationInscription`) and the date evidence scheme `szdg:DatumEvidenz`.

## 6. Identification

### 6.1 URI patterns

| Entity | URI pattern | Example |
|--------|-------------|---------|
| Estate (fonds) | `gams:{context-pid}` | `gams:context:szd` |
| Collection | `gams:{collection-pid}` | `gams:o:szd.werke` |
| Record | `gams:{object-pid}` | `gams:o:szd.270` |
| Record (catalogue entry) | `gams:{collection-pid}#{item-id}` | `gams:o:szd.werke#SZDMSK.6` |
| Work index entry | `gams:o:szd.werkindex#{id}` | `gams:o:szd.werkindex#SZDWRK.4` |
| Person | `gams:o:szd.personen#{id}` | `gams:o:szd.personen#SZDPER.1560` |
| Organisation | `gams:o:szd.organisation#{id}` | `gams:o:szd.organisation#SZDORG.1` |
| Location (repository) | `gams:o:szd.standorte#{id}` | `gams:o:szd.standorte#SZDSTA.1` |
| Glossary concept | `gams:o:szd.glossar#{id}` | `gams:o:szd.glossar#WritingMaterial` |
| Klawiter entry | `klawiter:entry/{id}` | `klawiter:entry/52` |

The patterns use the prefix `gams:` for `https://gams.uni-graz.at/` as shorthand. Turtle files write patterns with a fragment as full IRIs (`<https://gams.uni-graz.at/o:szd.werke#SZDMSK.6>`), because Turtle reads `#` in a prefixed name as the start of a comment.

### 6.2 External identifiers

| System | Property | URI pattern |
|--------|----------|-------------|
| GND | `szdo:gndIdentifier` | `http://d-nb.info/gnd/{id}` |
| Wikidata | `szdo:wikidataIdentifier` | `http://www.wikidata.org/entity/{id}` |
| VIAF | `szdo:viafIdentifier` | `http://viaf.org/viaf/{id}` |
| GeoNames | `szdo:geonamesIdentifier` | `http://www.geonames.org/{id}` |
| Shelfmark | `szdo:signature` | literal, for example `SZ-AAP/W4.1` |
| GAMS PID | `szdo:gamsIdentifier` | `o:szd.{number}` |

## 7. Core relations

### 7.1 Estate hierarchy

```turtle
szdo:contains          rdfs:domain szdo:Estate ;  rdfs:range szdo:Collection ;
                       owl:equivalentProperty rico:includesOrIncluded .
szdo:isPartOf          rdfs:domain szdo:Record ;  rdfs:range szdo:Collection ;
                       owl:inverseOf szdo:containsRecord ;
                       owl:equivalentProperty rico:isOrWasIncludedIn .
szdo:hasDigitalObject  rdfs:domain szdo:Record ;  rdfs:range szdo:DigitalObject ;
                       owl:equivalentProperty rico:hasInstantiation .
```

### 7.2 Records and works

`szdo:relationToWork` links a physical record (SZDMSK and other catalogues) to the abstract work it witnesses (SZDWRK). Its inverse is `szdo:hasManuscriptWitness`. GAMS already emits `szd:relationToWork` from the TEI keywords of type `work`.

```
szdo:WorkIndexEntry (SZDWRK.4 "Montaigne")
    ├── szdo:hasManuscriptWitness → szdo:Notebook (SZDMSK.6, SZ-AAP/W4.1)
    │   └── szdo:hasDigitalObject → szdo:METSObject (o:szd.271)
    │       └── szdo:hasFacsimile → szdo:Facsimile
    ├── szdo:hasManuscriptWitness → szdo:Manuscript (SZDMSK.7, SZ-AAP/W4.2)
    └── szdo:hasManuscriptWitness → szdo:Ensemble (SZDMSK.8, SZ-AAP/W4.3)
        └── szdo:scribalHand → Stefan Zweig, Lotte Zweig, Richard Friedenthal
```

### 7.3 Provenance

```
szdo:Book (SZDBIB.42)
    szdo:hasProvenance → szdo:ProvenanceEvent [
        szdo:previousOwner → Stefan Zweig ;
        szdo:subsequentOwner → later owner ] ;
    szdo:hasProvenanceFeature → szdo:ProvenanceFeatureInstance [
        szdo:hasFeatureType → szdg:Stamp ;
        szdo:description → "Bibliotheksstempel Zweig"@de ] .
```

### 7.4 Biographical events

A `szdo:BiographicalEvent` carries `szdo:when`, `szdo:hasPlace`, `szdo:concernsPerson` and `szdo:description`.

### 7.5 Date evidence

`szdo:certainty` records how certain a date is (TEI `@cert`). `szdo:dateEvidence` records where the date comes from and points to a concept of `szdg:DatumEvidenz`, which distinguishes a date from the document itself (`szdg:AusDokument`), inferred from context (`szdg:AusKontext`), from an external source (`szdg:AusExternerQuelle`) or unknown (`szdg:Unbekannt`). `szdo:notBefore` and `szdo:notAfter` take TEI `@notBefore` and `@notAfter`. The pattern follows the metadata model of the M³GIM project.

### 7.6 Holdings

`szdo:location` links a record to its `szdo:Location` and is equivalent to `rico:hasOrHadHolder`. `szdo:signature` holds the shelfmark.

## 8. Klawiter integration

The Klawiter bibliography adds the reception and publication history and connects through the work layer.

| Klawiter entry type | SZDO |
|---------------------|------|
| `fiction` | `szdo:Manifestation` of a `szdo:FictionalWork` |
| `essay` | `szdo:Manifestation` of a `szdo:EssayisticWork` |
| `poetry` | `szdo:Manifestation` of a `szdo:PoeticWork` |
| `drama` | `szdo:Manifestation` of a `szdo:DramaticWork` |
| `collected-works` | `szdo:Manifestation` of a `szdo:CollectedWork` |
| `correspondence` | `szdo:Manifestation` (letter editions) |
| `film`, `dramatic-reading` | `szdo:Expression` (adaptation, performance) |
| `translation` | `szdo:Expression` (Zweig's translations) |
| `foreword` | `szdo:ForewordAfterword` |
| `secondary-literature`, `historical-study` | `szdo:SecondaryLiterature` |
| `symposium` | `szdo:ScholarlyEvent` |

| Klawiter property | SZDO | Schema.org |
|-------------------|------|------------|
| `klawiter:title` | `szdo:title` | `schema:name` |
| `klawiter:year` | `szdo:dateOfPublication` | `schema:datePublished` |
| `klawiter:publisher` | `szdo:hasPublisher` | `schema:publisher` |
| `klawiter:location` | `szdo:hasPublicationPlace` | `schema:locationCreated` |
| `klawiter:pageCount` | `szdo:page` | `schema:numberOfPages` |
| `klawiter:translator` | `szdo:translator` | `schema:translator` |
| `klawiter:timePeriod` | `szdo:timePeriod` | |
| `klawiter:seeAlso` | `szdo:seeAlso` | `schema:isRelatedTo` |
| `klawiter:reprints` | `szdo:isReprintOf` | |
| `klawiter:translations` | `szdo:isTranslationOf` | `schema:workTranslation` |
| `klawiter:contentItems` | `szdo:hasPart` | `schema:hasPart` |
| `klawiter:categories` | `szdo:category` | |

`scripts/reconcile_klawiter.py` matches Klawiter entries to SZDWRK through GND identifiers and title matching and writes the links to `ontology/reconciliation.ttl` (`szdo:hasManifestation` for primary works, `szdo:isSubjectOf` for secondary literature). The match report is `scripts/reconciliation_report.md`.

## 9. Data sources

| TEI file | PID | SZDO class | GAMS class (v0.x) |
|----------|-----|------------|-------------------|
| `Work/SZDMSK.xml` | `o:szd.werke` | `szdo:Manuscript`, `szdo:Typescript`, `szdo:Notebook`, `szdo:Ensemble`, `szdo:GalleyProof` | `szd:Work` |
| `Correspondence/SZDKOR.xml` | `o:szd.korrespondenzen` | `szdo:BundleOfCorrespondence` | `szd:BundleOfCorrespondence` |
| `Autograph/SZDAUT.xml` | `o:szd.autographen` | `szdo:Autograph` | `szd:Autograph` |
| `Library/SZDBIB.xml` | `o:szd.bibliothek` | `szdo:Book` | `szd:Book` |
| `PersonalDocument/SZDLEB.xml` | `o:szd.lebensdokumente` | `szdo:PersonalDocument` | `szd:PersonalDocument` |
| `Aufsatzablage/SZDESS.xml` | `o:szd.aufsatzablage` | `szdo:Record` (essay material) | `szd:Essay` |
| `Biography/SZDBIO.xml` | `o:szd.lebenskalender` | `szdo:BiographicalEvent` | `szd:BiographicalEvent` |
| `Index/Person/SZDPER.xml` | `o:szd.personen` | `szdo:Person` | `szd:Agent` |
| `Index/Organisation/SZDORG.xml` | `o:szd.organisation` | `szdo:Organisation` | `szd:Organisation` |
| `Index/Location/SZDSTA.xml` | `o:szd.standorte` | `szdo:Location` | `szd:Location` |
| `Index/Werke/SZDWRK.xml` | `o:szd.werkindex` | `szdo:WorkIndexEntry` | `szd:WorkIndexEntry` |
| `Glossary/szd-Glossary.xml` | `o:szd.glossar` | `skos:ConceptScheme` (`szdg:`) | |
| theme files | `o:szd.thema.*` | `szdo:ThematicCollection` | `szd:Collection` |
| METS files | `o:szd.{N}` | `szdo:METSObject` | |

The organisation index SZDORG is its own GAMS object. The template `Organisationen` in `szd-TORDF.xsl` selects it by PID and types its entries as `szd:Organisation`, because the repository list SZDSTA is also a `listOrg`. Collection details are in [COLLECTIONS.md](COLLECTIONS.md). GAMS classes without an SZDO counterpart (`szd:Essay`, `szd:Correspondence`, `szd:PhysicalDescription`, `szd:Binding`) are not yet modelled.

## 10. Competency questions

The validation runs one SPARQL ASK query per question against the schema.

Archive
1. Which collections does the estate comprise?
2. Which manuscript witnesses exist for a work?
3. What is the provenance chain of a library book?
4. Which scribal hands appear on a manuscript?
5. Where is an object held and under which shelfmark?

Work
6. Which published editions exist for a work? (Klawiter)
7. Into which languages was a work translated? (Klawiter)
8. How did a text develop from notebook to print?
9. Which secondary literature exists on a work? (Klawiter)

Biography
10. Which life events are linked to a place?
11. Which correspondence partners did Zweig have in a period?
12. Which works were written in a phase of his life?

Linking
13. Can a Klawiter entry be assigned to an SZD work index entry?
14. Which GND entity connects a Klawiter author with an SZD person?
15. Are there SZD manuscript witnesses for first editions recorded by Klawiter?
16. Can active participants be told apart from persons an object is about? (`szdo:partyInvolved` against `szdo:affectedPerson`)
17. Can the evidence of a date be qualified? (`szdo:dateEvidence`, `szdo:when`, `szdo:certainty`)

Further checks cover the complete WEMI stack, the RiC-O alignment and the import and alignment of `nachlass:` (CQ-WEMI, CQ-RiC, CQ-G1 to CQ-G3 in `validate.py`).

## 11. Versions and GAMS alignment

### 11.1 Versions

| Version | Location | Change |
|---------|----------|--------|
| v0.x | GAMS (stefanzweig.digital) | Implicit in `szd-TORDF.xsl`, English camelCase terms, in production |
| v1.0.0 | GitHub Pages | Formal OWL ontology with German identifiers, RiC-O, LRM and CRM alignments, GAMS compatibility layer |
| v1.1.0 | GitHub Pages | Date evidence (SKOS), agent role hierarchy, RiC-O alignments, SHACL shape for date evidence, Klawiter corrections |
| v1.2.0 | GitHub Pages | Two layers, generic `nachlass:` ontology extracted and imported, generalisation competency questions |
| v2.0.0 | GitHub Pages | English identifiers only, GAMS terms canonical where the meaning is the same, compatibility layer reduced to legacy GAMS terms, `nachlass:` 0.2.0 with English identifiers |

```turtle
owl:versionInfo "2.0.0" ;
owl:versionIRI <https://gams.uni-graz.at/o:szd.ontology/2.0.0> ;
owl:priorVersion <https://gams.uni-graz.at/o:szd.ontology/1.2.0> ;
owl:incompatibleWith <https://gams.uni-graz.at/o:szd.ontology/1.2.0> ;
owl:backwardCompatibleWith <https://gams.uni-graz.at/o:szd.ontology/0.x> ;
owl:imports <https://w3id.org/nachlass> ;
```

### 11.2 Decisions of v2.0.0

- The German identifiers of v1.2.0 are dropped without `owl:deprecated` aliases. The operator decided on 2026-09-23 and 2026-09-24 that the formal ontology carries no German identifiers, and deprecated aliases would keep them in it. v1.x was published only as files and documentation of this repository, no live data, script or validation step uses its identifiers, and `migration-v2.csv` (section 11.4) translates old IRIs for anyone who holds them.
- The migration changes neither `szd-TORDF.xsl` in `ZIMLAB/szd` nor the live RDF of GAMS. Live data stays conformant because the canonical v2.0.0 names are the GAMS terms wherever the meaning is the same.
- The v1.x compatibility layer declared equivalences from the GAMS terms to the German terms. For every pair with the same meaning the GAMS term is now itself the canonical term, so live data needs no equivalence axiom.
- `szd:Work` (physical items of the works collection) was declared equivalent to the record class. v2.0.0 makes it a subclass of `szdo:Record`, because books, letters and autographs are records but not `szd:Work`.
- `szd:ProvenanceCharacteristic` aggregates all features of one book as literals, while `szdo:ProvenanceFeatureInstance` describes one feature. The former equivalence is replaced by `rdfs:seeAlso`, and the same holds for `szd:provenanceCharacteristic` and `szdo:hasProvenanceFeature`.
- `szd:secretarialHand` and `szd:pubPlace` are literal-valued, their SZDO successors `szdo:scribalHand` and `szdo:hasPublicationPlace` are object properties. An `owl:equivalentProperty` between a datatype and an object property is not valid OWL 2 DL, so both link with `rdfs:seeAlso`.
- `szd:relationToPerson` (any person keyword) is broader than `szdo:affectedPerson` (keywords of type `person_affected`). It keeps `rico:hasOrHadSubject` as superproperty instead of the former equivalence.
- Where GAMS has two terms for one concept, one becomes canonical and the other stays equivalent (`szdo:dateOfPublication` with `szd:pubDate`). For the general description neither `szd:content` (life calendar) nor `szd:desc` (content relations) covers the concept, so `szdo:description` is new and both stay equivalent.
- GAMS spellings that are not English words stay legacy terms (`szd:Enclosur` for `szdo:Enclosure`, `szd:objecttyp` for `szdo:objectType`).
- `szdo:Organisation` corresponds to the organisation index (`o:szd.organisation`) and `szdo:Location` to the repository list (`o:szd.standorte`), as GAMS produces them.

### 11.3 Legacy GAMS terms (PART 10 of `szd-ontology.ttl`)

These GAMS terms stay in live data and are `owl:deprecated` for new modelling.

| GAMS term | Relation to v2.0.0 |
|-----------|--------------------|
| `szd:Work` | `rdfs:subClassOf szdo:Record` |
| `szd:Enclosur` | `owl:equivalentClass szdo:Enclosure` |
| `szd:PublicationStmt` | `rdfs:subClassOf szdo:Manifestation` |
| `szd:ProvenanceCharacteristic` | `rdfs:seeAlso szdo:ProvenanceFeatureInstance` |
| `szd:OriginalShelfmark` | `rdfs:subClassOf szdo:Record` |
| `szd:objecttyp` | `owl:equivalentProperty szdo:objectType` |
| `szd:content`, `szd:desc` | `owl:equivalentProperty szdo:description` |
| `szd:pubDate` | `owl:equivalentProperty szdo:dateOfPublication` |
| `szd:gnd`, `szd:wikidata` | `owl:equivalentProperty szdo:gndIdentifier`, `szdo:wikidataIdentifier` |
| `szd:relationToPerson` | `rdfs:subPropertyOf rico:hasOrHadSubject`, `rdfs:seeAlso szdo:affectedPerson` |
| `szd:secretarialHand` | `rdfs:seeAlso szdo:scribalHand` |
| `szd:pubPlace` | `rdfs:seeAlso szdo:hasPublicationPlace` |
| `szd:publisher` | `rdfs:seeAlso szdo:hasPublisher` |
| `szd:provenanceCharacteristic` | `rdfs:seeAlso szdo:hasProvenanceFeature` |
| `szd:facsimile` | `rdfs:seeAlso szdo:hasDigitalObject` |
| `szd:hasContentRelation` | `rdfs:seeAlso szdo:seeAlso` |
| `szd:acquired`, `szd:provenance`, `szd:stamp` | `rdfs:seeAlso` to the provenance properties |
| `szd:relationTo`, `szd:glossar`, `szd:name`, `szd:settlement`, `szd:text`, `szd:head`, `szd:additionalMaterial`, `szd:edition`, `szd:series`, `szd:piecesOfEnclosures` | no direct counterpart, documented in the comment |

`szd:glossar` and the hybrid spelling `szd:objecttyp` are the only German-derived identifiers left in the ontology. Both are live GAMS terms, declared here only as deprecated legacy terms, and can only disappear together with a change of `szd-TORDF.xsl`. The concepts of the date evidence scheme (`szdg:DatumEvidenz` and its members) also keep German identifiers, because they belong to the SKOS glossary of GAMS (section 5.8), not to the ontology.

### 11.4 Mapping of the v1.2.0 identifiers

[../ontology/migration-v2.csv](../ontology/migration-v2.csv) maps every retired identifier of `szdo:` v1.2.0 and `nachlass:` 0.1.0 to its successor, with full IRIs, the kind of term and the source of the new name. The source is the GAMS term where one with the same meaning exists, the RiC-O or LRM term where the ontology aligns with that standard, and otherwise the English label. `validate.py` reads the file and fails if a retired identifier reappears in the ontology or in the generated RDF.

One retired name needs care. v1.2.0 `szdo:Werk` (the abstract work) becomes `szdo:WorkIndexEntry`, while `szdo:Work` is the deprecated GAMS class for the physical items of the works collection.

The generic layer uses the same names except where the SZD name follows a GAMS peculiarity. There `nachlass:` 0.2.0 uses plain English names, which are `Work` (SZD `WorkIndexEntry`), `Repository` (`Location`), `isManifestationOf` (`relationToWork`), `isHeldAt` (`location`), `hasEnclosure` (`enclosures`), `hasExtent` (`extent`), `shelfmark` (`signature`), `originalTitle` (`originaltitle`), `pageCount` (`page`), `pieceCount` (`piecesOfCorrespondence`), `date` (`when`), `dateOfBirth` (`birth`), `dateOfDeath` (`death`). Unchanged identifiers are `Autograph`, `IIIFManifest`, `Manifestation`, `Organisation`, `Person`, `format`, `incipit`, the external identifier properties and `gamsIdentifier`.

## 12. Known gaps

| Gap | Possible approach |
|-----|-------------------|
| Address structure is not modelled | `schema:PostalAddress` |
| Name variants and pseudonyms beyond `szdo:nameVariant` | `skos:altLabel` |
| Work relations of compilations are only schema-level (`szdo:hasPart`, `szdo:isPartOfWork`) | instance data from SZDWRK |
| Klawiter reconciliation covers part of SZDWRK | GND matching and fuzzy title matching, state in `scripts/reconciliation_report.md` |
| GAMS classes `szd:Essay`, `szd:Correspondence`, `szd:PhysicalDescription`, `szd:Binding` have no SZDO counterpart | model them or map them to `szdo:Record` subclasses |
| `szdo:Extent` and `szdo:Enclosure` are subclasses of `szdo:Record`, although an extent statement is not a record | revisit in a modelling release |
| `szd:gnd` and `szd:wikidata` are emitted with `rdf:resource`, while `szdo:gndIdentifier` and `szdo:wikidataIdentifier` are datatype properties | align datatype or emission |

## 13. Serialisation

- Turtle (`.ttl`) is the primary format.
- JSON-LD (`docs/ontology/szd-ontology.jsonld`) is generated for web use.
- The glossary stays in `szd-Glossary.xml`.

## 14. Validation

`python ontology/validate.py` runs six stages.

| Stage | Method | Checks |
|-------|--------|--------|
| 1. Syntax | rdflib Turtle parser | valid Turtle for both layers |
| 2. Metrics | class and property counts | structural overview |
| 3. SHACL | pySHACL with `szd-shapes.ttl` on the ontology together with `sample-instances.ttl` | bilingual labels, comments, property domains, instance constraints, ASCII naming convention, date evidence targets |
| 4. OWL checks | rdflib | orphans, multiple domains, circular subclassing, inverse consistency, disjointness, no retired v1.2.0 identifier in the ontology, `sample-instances.ttl` or `reconciliation.ttl` |
| 5. OntoClean | rigidity analysis | taxonomic correctness |
| 6. Competency questions | SPARQL ASK | section 10 |

Deprecated legacy terms are excluded from the label, domain and hierarchy checks, but not from the naming convention. A missing shelfmark on a record is a SHACL warning, not a violation, because books in private ownership carry inventory numbers but no shelfmark. `reconciliation.ttl` is a link set without entity descriptions and is not SHACL-validated.

## 15. Documentation site

`ontology/generate_docs.py` builds https://chpollin.github.io/SZD/ontology/ with rdflib, including a German and English toggle, anchors per class and property (`#Manuscript`, `#scribalHand`), Turtle and JSON-LD downloads and the interactive graph `visualize.html`. The workflow `.github/workflows/deploy-ontology-docs.yml` validates and regenerates the site when the ontology changes. The canonical namespace stays `https://gams.uni-graz.at/o:szd.ontology#`, and the site is linked through `rdfs:isDefinedBy`.

## References

- Records in Contexts (RiC-O), https://www.ica.org/standards/RiC/ontology
- IFLA LRM, https://www.ifla.org/publications/ifla-library-reference-model
- CIDOC-CRM, https://www.cidoc-crm.org/
- SKOS, https://www.w3.org/TR/skos-reference/
- TEI P5, https://tei-c.org/guidelines/
- GAMS ontology, https://gams.uni-graz.at/o:gams-ontology
- Regeln zur Erschließung von Nachlässen und Autographen (RNA), http://kalliope-verbund.info
