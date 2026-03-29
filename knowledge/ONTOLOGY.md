# Stefan Zweig Digital Nachlass-Ontologie (SZDO)

Entwurf einer formalen Ontologie für den digitalen Nachlass von Stefan Zweig. Die Ontologie modelliert archivalische, bibliographische und biographische Entitäten und deren Beziehungen — abgeleitet aus der Archivwissenschaft (Records in Context), ergänzt durch bibliothekarische Standards (IFLA LRM) und kulturerbe-orientierte Modelle (CIDOC-CRM).

**Namespace:** `https://gams.uni-graz.at/o:szd.ontology#` (Prefix: `szdo:`)

---

## 1. Designprinzipien

1. **Archiv-first**: Records in Context (RiC-O) als Fundament für die Beschreibung von Nachlass-Materialien
2. **FRBR/LRM-kompatibel**: Werk-Ebene nach IFLA Library Reference Model für die intellektuelle Werkschicht
3. **CIDOC-CRM-anschlussfähig**: Ereignisbasierte Provenienz und biographische Modellierung
4. **Linked Data**: Maximale Verknüpfung mit GND, Wikidata, Geonames, VIAF
5. **Bilingual**: Alle Labels und Definitionen in Deutsch und Englisch
6. **Erweiterbar**: Klawiter-Bibliographie und zukünftige Projekte integrierbar

---

## 2. Externe Vokabulare und Alignments

| Prefix | Namespace | Rolle |
|--------|-----------|-------|
| `rico:` | `https://www.ica.org/standards/RiC/ontology#` | Archivische Kernmodellierung |
| `lrm:` | `http://iflastandards.info/ns/lrm/lrmer/` | Werk-Expression-Manifestation-Item |
| `crm:` | `http://www.cidoc-crm.org/cidoc-crm/` | Ereignisse, Provenienz, Akteure |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | Kontrollierte Vokabulare (Glossar) |
| `dc:` / `dcterms:` | `http://purl.org/dc/terms/` | Dublin Core Metadaten |
| `foaf:` | `http://xmlns.com/foaf/0.1/` | Personen-Grunddaten |
| `schema:` | `https://schema.org/` | Schema.org-Brücke (bes. für Klawiter) |
| `gams:` | `https://gams.uni-graz.at/o:gams-ontology#` | GAMS-Plattform-Ontologie |
| `szdg:` | `https://gams.uni-graz.at/o:szd.glossar#` | SZD Glossar (SKOS) |
| `klawiter:` | `https://klawiter-rescue.github.io/vocab/` | Klawiter-Bibliographie |
| `gnd:` | `http://d-nb.info/standards/elementset/gnd#` | GND-Normdaten |
| `wdt:` | `http://www.wikidata.org/prop/direct/` | Wikidata-Properties |
| `iiif:` | `http://iiif.io/api/presentation/3#` | IIIF Presentation API |

---

## 3. Klassenhierarchie

### 3.1 Archivschicht (Nachlass-Struktur)

Fundament: **Records in Context (RiC-O)** — beschreibt den Nachlass als archivisches Ganzes.

```
szdo:Nachlass                          ≡ rico:RecordSet (Fonds-Ebene)
│
├── szdo:Sammlung                      ⊂ rico:RecordSet (Teilbestand/Series)
│   ├── szdo:Werksammlung              # Manuskripte, Typoskripte, Entwürfe
│   ├── szdo:Korrespondenzsammlung     # Korrespondenz-Konvolute
│   ├── szdo:Autographensammlung       # Gesammelte Autographen Dritter
│   ├── szdo:Bibliothekssammlung       # Rekonstruierte Privatbibliothek
│   ├── szdo:Lebensdokumentesammlung   # Persönliche Dokumente
│   └── szdo:Aufsatzsammlung           # Essays und Aufsätze
│
├── szdo:NachlassObjekt                ⊂ rico:Record (Einzelstück)
│   ├── szdo:Manuskript                # Handschriftliches Werkmanuskript
│   ├── szdo:Typoskript                # Maschinschriftliches Dokument
│   ├── szdo:Typoskriptdurchschlag     # Durchschlag/Kohlepapier-Kopie
│   ├── szdo:Notizbuch                 # Notizbuch mit Entwürfen
│   ├── szdo:Konvolut                  # Zusammengestelltes Ensemble
│   ├── szdo:Korrekturfahne            # Druckfahne mit Korrekturen
│   ├── szdo:KorrespondenzKonvolut     ⊂ rico:Record # Briefbündel
│   ├── szdo:Autograph                 # Einzelner Autograph (Sammlung)
│   ├── szdo:Buch                      # Buch aus Privatbibliothek
│   └── szdo:Lebensdokument            # Persönliches Dokument
│
└── szdo:DigitalesObjekt               ⊂ rico:Instantiation
    ├── szdo:METSObjekt                # METS-Container (strukturelle Metadaten)
    ├── szdo:IIIFManifest              # IIIF Presentation Manifest
    └── szdo:Faksimile                 # Einzelnes digitales Bild
```

**RiC-Alignments:**

| SZDO-Klasse | RiC-O Alignment | Erklärung |
|-------------|-----------------|-----------|
| `szdo:Nachlass` | `rico:RecordSet` (mit `rico:hasRecordSetType` = Fonds) | Gesamtnachlass als Fonds |
| `szdo:Sammlung` | `rico:RecordSet` (mit `rico:hasRecordSetType` = Series) | Teilbestand/Kollektion |
| `szdo:NachlassObjekt` | `rico:Record` | Einzelnes archivisches Objekt |
| `szdo:DigitalesObjekt` | `rico:Instantiation` | Digitale Repräsentation |

### 3.2 Werkschicht (Intellektuelle Ebene)

Fundament: **IFLA LRM** — modelliert Werke unabhängig von physischen Trägern.

```
szdo:Werk                              ≈ lrm:Work
│  # Abstraktes intellektuelles Werk (z.B. "Schachnovelle")
│  # Entspricht SZDWRK-Einträgen im Werkindex
│
├── szdo:WerkExpression                ≈ lrm:Expression
│   # Sprachliche/textliche Realisierung (z.B. dt. Originaltext, engl. Übersetzung)
│
├── szdo:Manifestation                 ≈ lrm:Manifestation
│   # Publizierte Ausgabe (Erstausgabe, Neuauflage, Übersetzungsausgabe)
│   # → Brücke zu Klawiter-Einträgen
│
└── szdo:Exemplar                      ≈ lrm:Item
    # Konkretes physisches Exemplar
    # → Brücke zu szdo:NachlassObjekt (Manuskript, Buch, etc.)
```

**Werktypen (nach Inhalt):**

```
szdo:Werk
├── szdo:BelletristischesWerk          # Novellen, Romane, Erzählungen
├── szdo:EssayistischesWerk            # Essays, Feuilletons
├── szdo:BiographischesWerk            # Biographien (Fouché, Marie Antoinette, etc.)
├── szdo:HistorischesWerk              # Sternstunden der Menschheit etc.
├── szdo:DramatischesWerk              # Theaterstücke, Libretti
├── szdo:LyrischesWerk                 # Gedichte, Gedichtsammlungen
├── szdo:SammelWerk                    # Gesammelte Werke, Kompilationen
│   └── szdo:hatTeil → szdo:Werk       # Enthaltene Einzelwerke
├── szdo:Übersetzungswerk              # Zweigs Übersetzungen anderer Autoren
└── szdo:VorwortNachwort               # Vorworte, Nachworte, Einleitungen
```

### 3.3 Akteur- und Indexschicht

```
szdo:Akteur                            ≈ rico:Agent, crm:E39_Actor
├── szdo:Person                        ≈ rico:Person, crm:E21_Person
│   # Personen mit Normdatenverknüpfung
│   # Entspricht SZDPER-Einträgen
│
└── szdo:Organisation                  ≈ rico:CorporateBody, crm:E74_Group
    # Institutionen, Verlage, Archive
    # Entspricht SZDSTA-Einträgen (Standorte)
```

**Personenrollen (als Properties):**

| Property | Domain | Range | Beschreibung |
|----------|--------|-------|--------------|
| `szdo:hatAutor` | Werk, NachlassObjekt | Person | Verfasser |
| `szdo:hatHerausgeber` | Werk, Manifestation | Person | Herausgeber |
| `szdo:hatÜbersetzer` | WerkExpression | Person | Übersetzer |
| `szdo:hatKomponist` | Werk | Person | Komponist (Vertonungen) |
| `szdo:hatIllustrator` | Manifestation | Person | Illustrator |
| `szdo:hatVorwortAutor` | Manifestation | Person | Vorwort-Verfasser |
| `szdo:hatAbsender` | KorrespondenzKonvolut | Person | Briefabsender |
| `szdo:hatEmpfänger` | KorrespondenzKonvolut | Person | Briefempfänger |
| `szdo:hatSchreiberhand` | NachlassObjekt | Person | Schreiber/Sekretär |
| `szdo:hatBetroffenePerson` | Lebensdokument | Person | Betroffene Person |
| `szdo:hatBeteiligten` | NachlassObjekt | Person | Allgemein Beteiligte |

### 3.4 Biographie- und Ereignisschicht

Fundament: **CIDOC-CRM E5_Event** — Lebensereignisse als zeitgebundene Entitäten.

```
szdo:BiographischesEreignis            ≈ crm:E5_Event
│  # Entspricht SZDBIO-Einträgen im Lebenskalender
│
├── szdo:Geburt                        ⊂ crm:E67_Birth
├── szdo:Tod                           ⊂ crm:E69_Death
├── szdo:Reise                         # Reisen, Aufenthalte
├── szdo:Publikationsereignis          # Veröffentlichung eines Werks
├── szdo:Begegnung                     # Treffen mit Personen
├── szdo:InstitutionellesEreignis      # Verleihungen, Ehrungen
└── szdo:Exilereignis                  # Emigration, Flucht
```

### 3.5 Orts- und Raum-Schicht

```
szdo:Ort                               ≈ crm:E53_Place, rico:Place
├── szdo:GeographischerOrt             # Stadt, Land (Geonames-verknüpft)
├── szdo:Aufbewahrungsort              # Archiv, Bibliothek als Standort
│   # Entspricht SZDSTA-Einträgen
└── szdo:Entstehungsort                # Wo ein Objekt geschaffen wurde
```

### 3.6 Provenienz- und Materialschicht

```
szdo:Provenienz                        ≈ crm:E8_Acquisition
│  # Erwerbungskette eines Objekts
│
├── szdo:Provenienzeignis              # Einzelnes Erwerbungs-/Besitzwechsel-Ereignis
│   ├── szdo:hatVorbesitzer → Person/Organisation
│   ├── szdo:hatNachbesitzer → Person/Organisation
│   ├── szdo:hatDatum → xsd:date
│   └── szdo:hatQuelle → Literal       # z.B. "Christie's London 2014"
│
└── szdo:ProvenienzmerkmalInstanz      # Konkretes Merkmal an einem Objekt
    # Verknüpft mit szdg:ProvenanceFeature (SKOS)
    # z.B. Stempel, Exlibris, Marginalien, Bindung
```

**Physische Beschreibungseigenschaften:**

| Property | Domain | Range | SKOS-Konzept |
|----------|--------|-------|--------------|
| `szdo:hatBeschreibstoff` | NachlassObjekt | Literal | `szdg:WritingMaterial` |
| `szdo:hatSchreibstoff` | NachlassObjekt | Literal | `szdg:WritingInstrument` |
| `szdo:hatUmfang` | NachlassObjekt | szdo:Umfang | — |
| `szdo:hatFormat` | NachlassObjekt | Literal | `szdg:PhysicalDescription` |
| `szdo:hatBindung` | Buch | Literal | — |
| `szdo:hatAufschrift` | NachlassObjekt | Literal | `szdg:IdentifyingInscription` |
| `szdo:hatIncipit` | NachlassObjekt | Literal | `szdg:Incipit` |
| `szdo:hatBeilage` | NachlassObjekt | szdo:Beilage | `szdg:Enclosures` |
| `szdo:hatZusatzmaterial` | NachlassObjekt | Literal | `szdg:AdditionalMaterial` |
| `szdo:hatSprache` | NachlassObjekt, Werk | Literal (ISO 639-3) | — |

### 3.7 Kontrolliertes Vokabular (Glossar)

Der bestehende **SKOS-Glossar** (`szdg:`) bleibt erhalten und wird in die Ontologie eingebunden:

```
szdg:ConceptScheme                     = skos:ConceptScheme
│
├── szdg:Works                         # Werkbezogene Begriffe
│   ├── szdg:Title
│   ├── szdg:Incipit
│   ├── szdg:WritingMaterial           # Beschreibstoff (Papier, Notizbuch, etc.)
│   ├── szdg:WritingInstrument         # Schreibstoff (violette Tinte, Bleistift, etc.)
│   ├── szdg:PartiesInvolved
│   ├── szdg:Date
│   ├── szdg:IdentifyingInscription
│   ├── szdg:PhysicalDescription
│   ├── szdg:AdditionalMaterial
│   └── szdg:Enclosures
│
├── szdg:ProvenanceFeature             # Provenienzmerkmale (Bibliotheksrekonstruktion)
│   ├── szdg:Autograph
│   ├── szdg:Binding
│   ├── szdg:Insertion
│   ├── szdg:Bookplate (Exlibris)
│   ├── szdg:Marginalia
│   ├── szdg:Marker
│   ├── szdg:Note
│   ├── szdg:Stamp
│   ├── szdg:Overpasting
│   ├── szdg:RemovedPage
│   └── szdg:PresentationInscription
│
├── szdg:Library
├── szdg:PersonalDocuments
├── szdg:Biography
├── szdg:FirstEditions
├── szdg:Person
├── szdg:Standorte
├── szdg:LaterOwner
├── szdg:OriginalShelfmark
└── szdg:CurrentLocation
```

---

## 4. Identifikationssystem

### 4.1 URI-Muster

| Entität | URI-Pattern | Beispiel |
|---------|-------------|---------|
| Nachlass (Fonds) | `gams:{context-pid}` | `gams:context:szd` |
| Sammlung | `gams:{collection-pid}` | `gams:o:szd.werke` |
| Nachlassobjekt | `gams:{object-pid}` | `gams:o:szd.270` |
| Nachlassobjekt (intern) | `gams:{collection-pid}#{item-id}` | `gams:o:szd.werke#SZDMSK.6` |
| Werk (Werkindex) | `gams:o:szd.werkindex#{id}` | `gams:o:szd.werkindex#SZDWRK.4` |
| Person | `gams:o:szd.personen#{id}` | `gams:o:szd.personen#SZDPER.1560` |
| Standort | `gams:o:szd.standorte#{id}` | `gams:o:szd.standorte#SZDSTA.1` |
| Glossar-Konzept | `gams:o:szd.glossar#{id}` | `gams:o:szd.glossar#WritingMaterial` |
| Klawiter-Eintrag | `klawiter:entry/{id}` | `klawiter:entry/52` |

### 4.2 Externe Identifikatoren

| System | Property | URI-Pattern |
|--------|----------|-------------|
| GND | `szdo:gndIdentifier` | `http://d-nb.info/gnd/{id}` |
| Wikidata | `szdo:wikidataIdentifier` | `http://www.wikidata.org/entity/{id}` |
| VIAF | `szdo:viafIdentifier` | `http://viaf.org/viaf/{id}` |
| Geonames | `szdo:geonamesIdentifier` | `http://www.geonames.org/{id}` |
| Signatur | `szdo:signatur` | Literal (z.B. `SZ-AAP/W4.1`) |
| GAMS-PID | `dcterms:identifier` | `o:szd.{number}` |

---

## 5. Kernbeziehungen (Object Properties)

### 5.1 Strukturelle Beziehungen (Nachlass-Hierarchie)

```turtle
szdo:istTeilVon          rdfs:domain szdo:NachlassObjekt ;
                         rdfs:range  szdo:Sammlung ;
                         owl:equivalentProperty rico:isOrWasIncludedIn .

szdo:enthält             owl:inverseOf szdo:istTeilVon ;
                         owl:equivalentProperty rico:includesOrIncluded .

szdo:hatDigitalesObjekt  rdfs:domain szdo:NachlassObjekt ;
                         rdfs:range  szdo:DigitalesObjekt ;
                         owl:equivalentProperty rico:hasInstantiation .
```

### 5.2 Werk-Objekt-Beziehungen (LRM-Brücke)

```turtle
szdo:istManifestationVon  rdfs:domain szdo:NachlassObjekt ;
                          rdfs:range  szdo:Werk ;
                          rdfs:comment "Verbindet physisches Objekt (SZDMSK) mit abstraktem Werk (SZDWRK)" .

szdo:hatManuskriptzeuge   owl:inverseOf szdo:istManifestationVon ;
                          rdfs:comment "Vom Werk zu seinen physischen Textzeugen" .
```

**Drei-Ebenen-Modell (zentral für die Ontologie):**

```
szdo:Werk (SZDWRK.4 "Montaigne")
    │
    ├── szdo:hatManuskriptzeuge → szdo:Notizbuch (SZDMSK.6, SZ-AAP/W4.1)
    │   └── szdo:hatDigitalesObjekt → szdo:METSObjekt (o:szd.271)
    │       └── szdo:hatFaksimile → szdo:Faksimile (IMG.1, IMG.2, ...)
    │
    ├── szdo:hatManuskriptzeuge → szdo:Manuskript (SZDMSK.7, SZ-AAP/W4.2)
    │
    └── szdo:hatManuskriptzeuge → szdo:Konvolut (SZDMSK.8, SZ-AAP/W4.3)
        ├── szdo:hatSchreiberhand → "Stefan Zweig"
        ├── szdo:hatSchreiberhand → "Lotte Zweig"
        └── szdo:hatSchreiberhand → "Richard Friedenthal"
```

### 5.3 Korrespondenz-Beziehungen

```turtle
szdo:hatAbsender         rdfs:domain szdo:KorrespondenzKonvolut ;
                         rdfs:range  szdo:Person .

szdo:hatEmpfänger        rdfs:domain szdo:KorrespondenzKonvolut ;
                         rdfs:range  szdo:Person .

szdo:hatKorrespondenzDatum  rdfs:domain szdo:KorrespondenzKonvolut ;
                            rdfs:range  xsd:date .

szdo:hatPoststempel      rdfs:domain szdo:KorrespondenzKonvolut ;
                         rdfs:range  szdo:Ort .
```

### 5.4 Provenienz-Beziehungen

```turtle
szdo:hatProvenienz       rdfs:domain szdo:NachlassObjekt ;
                         rdfs:range  szdo:Provenienzeignis .

szdo:hatProvenienzmerkmal rdfs:domain szdo:NachlassObjekt ;
                          rdfs:range  szdo:ProvenienzmerkmalInstanz .

szdo:ProvenienzmerkmalInstanz
    szdo:hatMerkmaltyp   → szdg:ProvenanceFeature (SKOS-Konzept) ;
    szdo:hatBeschreibung → Literal@de, Literal@en .
```

**Typische Provenienzkette:**

```
szdo:Buch (SZDBIB.42)
    szdo:hatProvenienz →
        szdo:Provenienzeignis [
            szdo:hatVorbesitzer → "Stefan Zweig" ;
            szdo:hatNachbesitzer → "Späterer Besitzer X" ;
        ] ;
    szdo:hatProvenienzmerkmal →
        szdo:ProvenienzmerkmalInstanz [
            szdo:hatMerkmaltyp → szdg:Stamp ;
            szdo:hatBeschreibung → "Bibliotheksstempel Zweig"@de ;
        ] ;
        szdo:ProvenienzmerkmalInstanz [
            szdo:hatMerkmaltyp → szdg:Marginalia ;
            szdo:hatBeschreibung → "Bleistiftanmerkungen von Zweig"@de ;
        ] .
```

### 5.5 Biographische Beziehungen

```turtle
szdo:BiographischesEreignis
    szdo:hatDatum        → xsd:date ;
    szdo:hatOrt          → szdo:Ort ;
    szdo:betrifftPerson  → szdo:Person ;
    szdo:hatBeschreibung → Literal@de, Literal@en .
```

### 5.6 Aufbewahrungs-Beziehungen

```turtle
szdo:wirdAufbewahrtIn    rdfs:domain szdo:NachlassObjekt ;
                         rdfs:range  szdo:Aufbewahrungsort ;
                         owl:equivalentProperty rico:hasOrHadHolder .

szdo:hatSignatur         rdfs:domain szdo:NachlassObjekt ;
                         rdfs:range  xsd:string .
```

---

## 6. Klawiter-Integrationsschicht

Die **Klawiter-Bibliographie** (6.296 Einträge) ergänzt den Nachlass um die **Rezeptions- und Publikationsgeschichte**. Die Integration erfolgt über die Werk-Ebene.

### 6.1 Mapping Klawiter → SZDO

```
klawiter:FictionEntry        → szdo:Manifestation (von szdo:BelletristischesWerk)
klawiter:EssayEntry          → szdo:Manifestation (von szdo:EssayistischesWerk)
klawiter:PoetryEntry         → szdo:Manifestation (von szdo:LyrischesWerk)
klawiter:DramaEntry          → szdo:Manifestation (von szdo:DramatischesWerk)
klawiter:CorrespondenceEntry → szdo:Manifestation (Briefeditionen)
klawiter:FilmEntry           → szdo:WerkExpression (Adaption/Verfilmung)
klawiter:TranslationEntry    → szdo:WerkExpression (Übersetzung)
klawiter:SecondaryLiterature  → szdo:Sekundärliteratur (eigenständige Klasse)
klawiter:HistoricalStudy     → szdo:Sekundärliteratur
klawiter:SymposiumEntry      → szdo:WissenschaftlichesEreignis
klawiter:CollectedWorksEntry → szdo:Manifestation (von szdo:SammelWerk)
```

### 6.2 Verknüpfungsmechanismus

Die zentrale Brücke ist `szdo:Werk`:

```
szdo:Werk (SZDWRK.4 "Montaigne", GND: 1140124943)
    │
    ├── szdo:hatManuskriptzeuge → NachlassObjekte (SZDMSK.6, .7, .8)
    │   [Archiv-Perspektive: physische Überlieferung]
    │
    ├── szdo:hatManifestation → klawiter:entry/1234 (Erstausgabe 1982)
    │   [Bibliographische Perspektive: publizierte Ausgabe]
    │
    ├── szdo:hatManifestation → klawiter:entry/5678 (engl. Übersetzung)
    │   [Rezeptionsgeschichte: internationale Verbreitung]
    │
    └── szdo:wirdBehandeltIn → klawiter:entry/9012 (Sekundärliteratur)
        [Forschungsgeschichte: wissenschaftliche Rezeption]
```

### 6.3 Klawiter-spezifische Properties

| Property | Domain | Range | Mapping |
|----------|--------|-------|---------|
| `szdo:hatZeitperiode` | Manifestation | Literal | `klawiter:timePeriod` |
| `szdo:hatVerlag` | Manifestation | Organisation | `klawiter:publisher` → `schema:publisher` |
| `szdo:hatPublikationsort` | Manifestation | Ort | `klawiter:location` → `schema:locationCreated` |
| `szdo:hatSeitenanzahl` | Manifestation | xsd:integer | `klawiter:pageCount` → `schema:numberOfPages` |
| `szdo:istNachdruckVon` | Manifestation | Manifestation | `klawiter:reprints` |
| `szdo:istÜbersetzungVon` | WerkExpression | WerkExpression | `klawiter:translations` → `schema:workTranslation` |
| `szdo:hatInhaltsverzeichnis` | Manifestation | rdf:List | `klawiter:contentItems` → `schema:hasPart` |
| `szdo:sieheAuch` | Manifestation | Manifestation | `klawiter:seeAlso` → `schema:isRelatedTo` |

---

## 7. Datenquellen-Mapping

### 7.1 SZD TEI-XML → SZDO Klassen

| TEI-Datei | PID | SZDO-Klasse(n) |
|-----------|-----|----------------|
| `SZDMSK.xml` | `o:szd.werke` | `szdo:Manuskript`, `szdo:Typoskript`, `szdo:Notizbuch`, `szdo:Konvolut`, `szdo:Korrekturfahne` |
| `SZDKOR.xml` | `o:szd.korrespondenzen` | `szdo:KorrespondenzKonvolut` |
| `SZDAUT.xml` | `o:szd.autographen` | `szdo:Autograph` |
| `SZDBIB.xml` | `o:szd.bibliothek` | `szdo:Buch` |
| `SZDLEB.xml` | `o:szd.lebensdokumente` | `szdo:Lebensdokument` |
| `SZDESS.xml` | `o:szd.essays` | `szdo:NachlassObjekt` (Essay-Material) |
| `SZDPUB.xml` | `o:szd.publikationen` | `szdo:Manifestation` (Erstveröffentlichungen) |
| `SZDBIO.xml` | `o:szd.lebenskalender` | `szdo:BiographischesEreignis` |
| `SZDPER.xml` | `o:szd.personen` | `szdo:Person` |
| `SZDSTA.xml` | `o:szd.standorte` | `szdo:Aufbewahrungsort`, `szdo:Organisation` |
| `SZDWRK.xml` | `o:szd.werkindex` | `szdo:Werk` |
| `szd-Glossary.xml` | `o:szd.glossar` | `skos:ConceptScheme` (szdg:) |
| Themen-Dateien | `o:szd.thema.*` | `szdo:ThematischeSammlung` (kuratierte Sammlungen) |
| METS-Dateien | `o:szd.{N}` | `szdo:METSObjekt` |

### 7.2 Klawiter JSON-LD → SZDO Klassen

| Klawiter entryType | Anzahl | SZDO-Klasse |
|-------------------|--------|-------------|
| `fiction` | 1.118 | `szdo:Manifestation` → `szdo:BelletristischesWerk` |
| `essay` | 905 | `szdo:Manifestation` → `szdo:EssayistischesWerk` |
| `secondary-literature` | 1.406 | `szdo:Sekundärliteratur` |
| `historical-study` | 535 | `szdo:Sekundärliteratur` |
| `poetry` | 275 | `szdo:Manifestation` → `szdo:LyrischesWerk` |
| `collected-works` | 114 | `szdo:Manifestation` → `szdo:SammelWerk` |
| `correspondence` | 109 | `szdo:Manifestation` (Briefeditionen) |
| `film` | 92 | `szdo:WerkExpression` (Adaption) |
| `translation` | 56 | `szdo:WerkExpression` (Übersetzung Zweigs) |
| `drama` | 43 | `szdo:Manifestation` → `szdo:DramatischesWerk` |
| `symposium` | 39 | `szdo:WissenschaftlichesEreignis` |
| `foreword` | 36 | `szdo:VorwortNachwort` |
| `dramatic-reading` | 18 | `szdo:WerkExpression` (Aufführung) |

---

## 8. Schematische Gesamtübersicht

```
                        ┌─────────────────────────────────────┐
                        │       szdo:Nachlass (Fonds)         │
                        │   "Stefan Zweig Nachlass Salzburg"  │
                        └────────────────┬────────────────────┘
                                         │ szdo:enthält
              ┌──────────────┬───────────┼───────────┬──────────────┐
              │              │           │           │              │
     ┌────────▼───────┐ ┌───▼────┐ ┌────▼─────┐ ┌──▼────┐ ┌──────▼──────┐
     │  Werksammlung  │ │ Korresp│ │Autograph.│ │Biblioth│ │Lebensdok.   │
     │  (SZDMSK)      │ │(SZDKOR)│ │(SZDAUT)  │ │(SZDBIB)│ │(SZDLEB)     │
     └───────┬────────┘ └───┬────┘ └────┬─────┘ └──┬────┘ └──────┬──────┘
             │              │           │           │              │
     ┌───────▼────────┐     │     ┌─────▼────┐  ┌──▼────┐        │
     │ NachlassObjekt │     │     │ Autograph │  │ Buch  │        │
     │ (Manuskript,   │     │     │ (Sammlung │  │(Privat│        │
     │  Typoskript,..)│     │     │  Dritter) │  │ bibl.)│        │
     └───────┬────────┘     │     └──────────┘  └───┬───┘        │
             │              │                       │             │
             │ szdo:istManifestationVon        szdo:hatProvenienzmerkmal
             │                                      │
     ┌───────▼────────┐                    ┌────────▼────────┐
     │   szdo:Werk    │                    │  szdg:Glossar   │
     │  (SZDWRK)      │◄─── GND ────►     │  (SKOS)         │
     │ "Schachnovelle" │                   │ ProvenanceFeature│
     └───────┬────────┘                    │ WritingMaterial  │
             │                             │ WritingInstrument│
             │ szdo:hatManifestation       └─────────────────┘
             │
     ┌───────▼──────────────────┐
     │  Klawiter-Bibliographie  │
     │  (6.296 Einträge)        │
     │  Erstausgaben,           │
     │  Übersetzungen,          │
     │  Sekundärliteratur       │
     └──────────────────────────┘
             │
             │ szdo:hatÜbersetzer, szdo:hatVerlag, ...
             │
     ┌───────▼────────┐     ┌─────────────────┐    ┌──────────────┐
     │  szdo:Person   │     │   szdo:Ort       │    │szdo:Biograph.│
     │  (SZDPER)      │     │   (SZDSTA +      │    │Ereignis      │
     │  GND, Wikidata │     │    Geonames)     │    │(SZDBIO)      │
     └────────────────┘     └─────────────────┘    └──────────────┘
```

---

## 9. Kompetenzfragen (Competency Questions)

Die Ontologie soll folgende Fragen beantworten können:

### Archiv-Perspektive
1. Welche Sammlungen umfasst der Nachlass Stefan Zweigs?
2. Welche Manuskriptzeugen existieren zu einem bestimmten Werk?
3. Wie ist die Provenienzkette eines Bibliotheksbuchs?
4. Welche Schreiberhände finden sich auf einem Manuskript?
5. Wo wird ein bestimmtes Objekt aufbewahrt und unter welcher Signatur?

### Werk-Perspektive
6. Welche publizierten Ausgaben existieren zu einem Werk? (→ Klawiter)
7. In welche Sprachen wurde ein Werk übersetzt? (→ Klawiter)
8. Wie ist die Textgenese eines Werks (Notizbuch → Manuskript → Typoskript → Druck)?
9. Welche Sekundärliteratur gibt es zu einem Werk? (→ Klawiter)

### Biographische Perspektive
10. Welche Lebensereignisse sind mit einem bestimmten Ort verbunden?
11. Welche Korrespondenzpartner hatte Zweig in einem bestimmten Zeitraum?
12. Welche Werke entstanden während einer bestimmten Lebensphase?

### Verknüpfungsfragen (Cross-Projekt)
13. Kann ein Klawiter-Bibliographieeintrag einem SZD-Werkindex-Eintrag zugeordnet werden?
14. Welche GND-Entität verbindet einen Klawiter-Autor mit einem SZD-Personenindex-Eintrag?
15. Gibt es Manuskriptzeugen (SZD) zu den bei Klawiter verzeichneten Erstausgaben?

---

## 10. Migrations-Strategie (bestehende szd:-Ontologie → szdo:)

Die bestehende implizite `szd:`-Ontologie (definiert in `szd-TORDF.xsl`) wird schrittweise überführt:

### Phase 1: Formalisierung
- OWL-Datei erstellen (`szd-ontology.ttl` oder `.owl`)
- Bestehende 15 Klassen + 71 Properties formal definieren
- `rdfs:label`, `rdfs:comment` bilingual hinzufügen
- Bekannte Tippfehler korrigieren (`szd:realtionToWork` → `szdo:hatWerkbezug`)

### Phase 2: RiC-Alignment
- `szdo:Nachlass` als Fonds-Klasse
- Sammlungen als Series
- NachlassObjekte als Records
- Digitale Objekte als Instantiations

### Phase 3: LRM-Werkschicht
- `szdo:Werk` von SZDWRK ableiten
- Textgenese-Beziehungen modellieren (Notizbuch → Manuskript → Typoskript → Korrekturfahne)
- Expression-Ebene für Übersetzungen und Adaptionen

### Phase 4: Klawiter-Integration
- Manifestations-Brücke zu Klawiter-Einträgen
- Sekundärliteratur-Klasse
- Reconciliation über GND-IDs und Werktitel

### Phase 5: CIDOC-CRM-Events
- Biographie-Ereignisse als crm:E5_Event
- Provenienz-Ketten als crm:E8_Acquisition-Sequenzen

---

## 10a. Versionierung und GAMS-Kompatibilität

### Versionsstrategie

Die SZDO nutzt Standard-OWL-Versionierung:

| Version | Ort | Status | Beschreibung |
|---------|-----|--------|-------------|
| **v0.x** | GAMS (`stefanzweig.digital`) | Produktiv | Implizit in `szd-TORDF.xsl` definiert. Englische camelCase-Bezeichner. 14 Klassen, 67 Properties. Über Jahre gewachsen. |
| **v1.0.0** | GitHub Pages (`chpollin.github.io/SZD/ontology/`) | Neu | Formale OWL-Ontologie. Deutsche Bezeichner. 58 Klassen, 77 Properties. RiC-O/LRM/CRM-Alignments. GAMS-Kompatibilitätsschicht. |

**OWL-Metadaten:**
```turtle
owl:versionInfo "1.0.0" ;
owl:versionIRI <https://gams.uni-graz.at/o:szd.ontology/1.0.0> ;
owl:priorVersion <https://gams.uni-graz.at/o:szd.ontology/0.x> ;
owl:backwardCompatibleWith <https://gams.uni-graz.at/o:szd.ontology/0.x> ;
```

### GAMS-Kompatibilitätsschicht (PART 10 in szd-ontology.ttl)

Die bestehenden GAMS-Daten verwenden englische Bezeichner im selben Namespace. Die Kompatibilitätsschicht definiert alle 14 alten Klassen und 53 alten Properties als `owl:deprecated` mit `owl:equivalentClass`/`owl:equivalentProperty`-Verknüpfungen zu den neuen v1.0.0-Bezeichnern.

**Klassen-Mapping (Auszug):**

| GAMS v0.x (engl.) | SZDO v1.0.0 (dt.) | Mapping |
|--------------------|--------------------|---------|
| `szd:Work` | `szdo:NachlassObjekt` | `owl:equivalentClass` |
| `szd:Book` | `szdo:Buch` | `owl:equivalentClass` |
| `szd:BundleOfCorrespondence` | `szdo:KorrespondenzKonvolut` | `owl:equivalentClass` |
| `szd:PersonalDocument` | `szdo:Lebensdokument` | `owl:equivalentClass` |
| `szd:BiographicalEvent` | `szdo:BiographischesEreignis` | `owl:equivalentClass` |
| `szd:Agent` | `szdo:Akteur` | `owl:equivalentClass` |
| `szd:Location` | `szdo:Aufbewahrungsort` | `owl:equivalentClass` |
| `szd:WorkIndexEntry` | `szdo:Werk` | `owl:equivalentClass` |
| `szd:Extent` | `szdo:Umfang` | `owl:equivalentClass` |
| `szd:Enclosur` (Typo) | `szdo:Beilage` | `owl:equivalentClass` |

**Property-Mapping (Auszug):**

| GAMS v0.x | SZDO v1.0.0 | Anmerkung |
|-----------|-------------|-----------|
| `szd:title` | `szdo:titel` | Direkt äquivalent |
| `szd:author` | `szdo:hatAutor` | Namenskonvention: "hat"-Präfix |
| `szd:sender` | `szdo:hatAbsender` | |
| `szd:receiver` | `szdo:hatEmpfaenger` | |
| `szd:writingMaterial` | `szdo:beschreibstoff` | Englisch → Deutsch |
| `szd:signature` | `szdo:signatur` | |
| `szd:gnd` | `szdo:gndIdentifier` | |
| `szd:wikidata` | `szdo:wikidataIdentifier` | |
| `szd:provenance` | — | In v1.0.0 als `Provenienzereignis` modelliert |
| `szd:acquired` | — | In v1.0.0 als `Provenienzereignis` modelliert |
| `szd:text` | — | Generischer Container, kein 1:1-Equivalent |
| `szd:Enclosur` | `szdo:Beilage` | Typo in v0.x dokumentiert |

### Bekannte Abweichungen zwischen GAMS v0.x und SZDO v1.0.0

1. **Namenskonvention**: v0.x nutzt englisches camelCase, v1.0.0 nutzt deutsche Bezeichner
2. **Flach vs. geschichtet**: v0.x kennt nur `szd:Work` für alle Manuskripte; v1.0.0 differenziert (Manuskript, Typoskript, Notizbuch, etc.)
3. **Provenienz**: v0.x nutzt flache Literale (`szd:provenance`, `szd:acquired`); v1.0.0 modelliert als Event-Klasse
4. **SKOS-Namespace**: v0.x nutzt `https://gams.uni-graz.at/skos/scheme/o:oth/#`; v1.0.0 nutzt Standard W3C SKOS
5. **Schreiberhand**: v0.x `szd:secretarialHand` ist DatatypeProperty (Literal); v1.0.0 `szdo:hatSchreiberhand` ist ObjectProperty (→ Person)

---

## 11. Bekannte Lücken und offene Fragen

| Lücke | Beschreibung | Möglicher Ansatz |
|-------|-------------|-----------------|
| Datenunsicherheit | TEI `@cert` nicht in RDF abgebildet | `szdo:hatSicherheitsgrad` (low/medium/high) |
| Datumsintervalle | `@notBefore`/`@notAfter` nicht modelliert | `szdo:frühestensDatum`, `szdo:spätestensDatum` |
| Adressstruktur | Keine strukturierte Adressmodellierung | `szdo:hatAdresse` → schema:PostalAddress |
| Verantwortlichkeiten | Katalogisierer, Digitalisierer nicht modelliert | `rico:hasOrHadAgent` mit Rollenqualifizierung |
| Namensvarianten | Pseudonyme, Schreibvarianten | `szdo:hatNamensform` (skos:altLabel) |
| Klawiter-Reconciliation | 4.751 Einträge noch nicht mit SZDWRK verknüpft | GND-Matching + Titel-Fuzzy-Match |
| Werkrelationen | Kompilationen/Sammelwerke nicht formal | `szdo:hatTeil` / `szdo:istTeilVon` auf Werkebene |

---

## 12. Dateiformat und Serialisierung

Die Ontologie wird in folgenden Formaten bereitgestellt:

- **Turtle (`.ttl`)**: Primärformat, menschenlesbar
- **RDF/XML (`.rdf`)**: Für GAMS-Kompatibilität
- **JSON-LD (`.jsonld`)**: Für Klawiter-Integration und Web-APIs
- **SKOS (bestehend)**: Glossar bleibt in `szd-Glossary.xml`

---

## 13. Validierungspipeline

Die Ontologie wird durch eine 6-Stufen-Pipeline validiert (`ontology/validate.py`):

| Stufe | Methode | Prüft |
|-------|---------|-------|
| 1. Syntax | rdflib Turtle-Parser | Gültige Turtle-Syntax |
| 2. Metriken | Klassen-/Property-Zählung | Strukturelle Vollständigkeit |
| 3. SHACL | pySHACL + `szd-shapes.ttl` | Kardinalitäten, Pflicht-Annotationen, Namenskonventionen, Orphan-Klassen |
| 4. OWL Checks | rdflib-basiert | Orphans, Multi-Domain, Circular SubClassOf, InverseOf-Konsistenz, Disjointness |
| 5. OntoClean | Rigidity-Analyse | Taxonomische Korrektheit (rigide vs. anti-rigide Klassen) |
| 6. Kompetenzfragen | 17 SPARQL ASK-Queries | Ontologie beantwortet alle definierten Fragen (inkl. RiC/WEMI-Alignment) |

**Ausführung:** `python ontology/validate.py`

**SHACL Shapes** (`ontology/szd-shapes.ttl`): 13 Constraints für bilinguale Labels, Comments, Property-Domains, Instanzdaten-Validierung und Namenskonventionen.

---

## 14. GitHub Pages Dokumentation

Die Ontologie wird als interaktive HTML-Dokumentation auf GitHub Pages publiziert:

- **URL:** https://chpollin.github.io/SZD/ontology/
- **Generator:** `ontology/generate_docs.py` (rdflib-basiert, kein pyLODE)
- **Features:**
  - Bilingualer DE/EN-Umschalter
  - Sidebar-Navigation nach Ontologie-Schichten
  - Fragment-Anker für jede Klasse/Property (`#Manuskript`, `#hatSchreiberhand`, etc.)
  - Download-Links (Turtle, JSON-LD)
  - Schema.org JSON-LD Metadata
  - Externe Vokabular-Badges (RiC-O, LRM, CRM, SKOS, FOAF, Schema.org)
- **CI/CD:** `.github/workflows/deploy-ontology-docs.yml` — automatische Regenerierung bei Ontologie-Änderungen
- **Namespace-Strategie:** Kanonischer Namespace bleibt `https://gams.uni-graz.at/o:szd.ontology#`, Dokumentation unter GitHub Pages via `rdfs:isDefinedBy`

---

## Referenzen

- **Records in Context (RiC-O)**: https://www.ica.org/standards/RiC/ontology
- **IFLA LRM**: https://www.ifla.org/publications/ifla-library-reference-model
- **CIDOC-CRM**: https://www.cidoc-crm.org/
- **SKOS**: https://www.w3.org/TR/skos-reference/
- **TEI P5**: https://tei-c.org/guidelines/
- **GAMS Ontology**: https://gams.uni-graz.at/o:gams-ontology
- **RNA (Nachlasserschließung)**: http://kalliope-verbund.info (Regeln zur Erschließung von Nachlässen und Autographen)
