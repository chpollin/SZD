# FAIR-Prinzipien Compliance - Stefan Zweig Digital Archive

**Datum:** 2025-10-22
**Version:** 1.0.0
**Projekt:** Stefan Zweig Digital Archive Backup

---

## Übersicht: FAIR-Prinzipien

**FAIR** = **F**indable, **A**ccessible, **I**nteroperable, **R**eusable

Diese Analyse prüft die Einhaltung aller 15 FAIR-Prinzipien für Forschungsdaten.

**Status:** ⚠️ **Teilweise erfüllt** - Verbesserungen notwendig

---

## F - FINDABLE (Auffindbar)

### ✅ F1: Globally unique and persistent identifier

**Status:** ✅ **ERFÜLLT** (nach Zenodo Upload)

**Aktuell:**
- Zenodo DOI wird vergeben (sowohl Concept DOI als auch Version DOI)
- DOI ist global eindeutig und persistent

**Beispiel:**
- Version DOI: `10.5281/zenodo.XXXXXX` (wird bei Upload erstellt)
- Concept DOI: `10.5281/zenodo.YYYYYY` (persistent für alle Versionen)

---

### ⚠️ F2: Data described with rich metadata

**Status:** ⚠️ **TEILWEISE ERFÜLLT** - Verbesserungen möglich

**Erfüllt:**
- ✅ Titel, Beschreibung, Creators, Keywords
- ✅ License (CC-BY-4.0)
- ✅ Publication Date, Version, Language
- ✅ Related Identifiers (GAMS, stefanzweig.digital)

**FEHLT oder unvollständig:**
- ❌ **Funding Information** (Förderer des Projekts)
- ❌ **Geographic Coverage** (Salzburg, Österreich)
- ❌ **Temporal Coverage** (Zweigs Lebenszeit: 1881-1942)
- ❌ **Subjects/Disciplines** (OECD oder andere Klassifikation)
- ⚠️ **Contributors** - nur GAMS erwähnt, Literaturarchiv Salzburg fehlt als Contributor

**EMPFEHLUNG:**
```json
"subjects": [
  {"term": "Literary studies", "scheme": "OECD"},
  {"term": "Cultural heritage", "scheme": "OECD"}
],
"dates": [
  {"type": "Collected", "start": "1881", "end": "1942"}
],
"locations": [
  {"place": "Salzburg, Austria"}
],
"grants": [
  {"id": "GRANT_ID", "funder": "FUNDER_NAME"} // Falls zutreffend
]
```

---

### ✅ F3: Metadata include identifier of data

**Status:** ✅ **ERFÜLLT**

**Aktuell:**
- Zenodo Metadata referenzieren den DOI
- CITATION.cff enthält DOI-Referenz
- README.md wird mit DOI aktualisiert

---

### ✅ F4: Registered in searchable resource

**Status:** ✅ **ERFÜLLT** (nach Zenodo Upload)

**Aktuell:**
- Zenodo ist bei DataCite registriert
- Durchsuchbar via:
  - Zenodo Search
  - DataCite Search
  - Google Dataset Search
  - OpenAIRE
  - Re3data

---

## A - ACCESSIBLE (Zugänglich)

### ✅ A1: Retrievable by identifier using standardized protocol

**Status:** ✅ **ERFÜLLT** (nach Zenodo Upload)

**Aktuell:**
- HTTPS-Protokoll
- DOI-Resolution über https://doi.org/
- REST API verfügbar

---

### ✅ A1.1: Protocol is open, free, and universally implementable

**Status:** ✅ **ERFÜLLT**

**Aktuell:**
- HTTPS ist offen und frei
- Keine proprietären Protokolle

---

### ✅ A1.2: Protocol allows authentication where necessary

**Status:** ✅ **ERFÜLLT**

**Aktuell:**
- Zenodo unterstützt Zugriffskontrolle (nicht genutzt, da Open Access)
- API-Token-basierte Authentifizierung verfügbar

---

### ✅ A2: Metadata accessible even when data unavailable

**Status:** ✅ **ERFÜLLT**

**Aktuell:**
- Zenodo garantiert Metadaten-Persistenz
- Selbst bei Datenverlust bleiben Metadaten erhalten

---

## I - INTEROPERABLE (Interoperabel)

### ⚠️ I1: Formal, accessible, shared language for knowledge representation

**Status:** ⚠️ **TEILWEISE ERFÜLLT** - Verbesserungen möglich

**Erfüllt:**
- ✅ METS/MODS (standardisiertes XML-Format)
- ✅ DFG-METS (deutsche Forschungsgemeinschaft Standard)
- ✅ JSON (maschinenlesbar)
- ✅ DataCite Metadata Schema (Zenodo)

**FEHLT:**
- ❌ **RDF/Linked Data** nicht implementiert
- ❌ **Schema.org Markup** fehlt
- ❌ **OAI-PMH** nicht direkt verfügbar (aber via Zenodo)

**EMPFEHLUNG:**
- Zenodo bietet automatisch OAI-PMH und Schema.org
- Optional: RDF-Export aus METS-Daten generieren

---

### ❌ I2: Vocabularies follow FAIR principles

**Status:** ❌ **NICHT ERFÜLLT**

**Problem:**
- Keywords sind Freitext, keine kontrollierten Vokabulare
- Keine URIs für Konzepte
- Keine Referenzen auf standardisierte Thesauri

**FEHLT:**
- ❌ **LCSH** (Library of Congress Subject Headings)
- ❌ **GND** (Gemeinsame Normdatei) für Personen
- ❌ **Wikidata/VIAF** IDs

**EMPFEHLUNG:**
```json
"creators": [
  {
    "name": "Zangerl, Lina Maria",
    "affiliation": "Literaturarchiv Salzburg",
    "orcid": "XXXX-XXXX-XXXX-XXXX"  // Falls vorhanden
  }
],
"subjects": [
  {
    "identifier": "http://id.loc.gov/authorities/subjects/sh85143931",
    "term": "Stefan Zweig",
    "scheme": "LCSH"
  },
  {
    "identifier": "https://www.wikidata.org/wiki/Q78491",
    "term": "Stefan Zweig",
    "scheme": "Wikidata"
  }
],
"related_identifiers": [
  {
    "identifier": "https://d-nb.info/gnd/118637479",
    "relation": "isAbout",
    "scheme": "GND",
    "resource_type": "other"
  }
]
```

---

### ⚠️ I3: Qualified references to other data

**Status:** ⚠️ **TEILWEISE ERFÜLLT**

**Erfüllt:**
- ✅ Related Identifiers (GAMS, stefanzweig.digital)
- ✅ Relation Types (`isSupplementTo`)

**FEHLT:**
- ❌ **Keine Referenzen zu verwandten Datensätzen**
- ❌ **Keine Links zu Publikationen über Stefan Zweig**
- ❌ **Keine Verknüpfung mit anderen Literaturarchiven**

**EMPFEHLUNG:**
```json
"related_identifiers": [
  {
    "identifier": "10.XXXX/related-zweig-publication",
    "relation": "isReferencedBy",
    "scheme": "doi"
  },
  {
    "identifier": "https://www.deutsche-digitale-bibliothek.de/...",
    "relation": "isRelatedTo",
    "scheme": "url"
  }
]
```

---

## R - REUSABLE (Wiederverwendbar)

### ⚠️ R1: Richly described with relevant attributes

**Status:** ⚠️ **TEILWEISE ERFÜLLT**

**Erfüllt:**
- ✅ Beschreibung, Creators, Keywords
- ✅ Technische Metadaten (Format, Größe)
- ✅ Known Issues dokumentiert

**FEHLT (wichtig für Forschungsdaten):**
- ❌ **Methodology** (Wie wurden Daten erstellt/gesammelt?)
- ❌ **Quality Assurance** (Validierung, aber nicht formal beschrieben)
- ❌ **Versioning Policy** (existiert, aber nicht in Metadaten)
- ❌ **Contact Information** (Wer ist verantwortlich?)

**EMPFEHLUNG:**
- Methodologie-Beschreibung hinzufügen
- Kontaktperson mit Email
- Verweis auf Validierungsbericht in Description

---

### ✅ R1.1: Clear and accessible usage license

**Status:** ✅ **ERFÜLLT**

**Aktuell:**
- ✅ CC-BY 4.0 (klar, standardisiert, maschinenlesbar)
- ✅ Link zur Lizenz inkludiert

---

### ⚠️ R1.2: Detailed provenance

**Status:** ⚠️ **TEILWEISE ERFÜLLT**

**Erfüllt:**
- ✅ Quelle dokumentiert (GAMS)
- ✅ Download-Datum (2025-10-22)
- ✅ Version (1.0.0)

**FEHLT:**
- ❌ **Digitization Workflow** (Wie wurden Originale digitalisiert?)
- ❌ **Processing Steps** (Download-Methode nur im Script)
- ❌ **Original Archive Location** (Literaturarchiv Salzburg physisch)
- ❌ **Digitization Date** (Wann wurden Originale gescannt?)

**EMPFEHLUNG:**
Provenance-Sektion in Description erweitern:
```
## Provenance

**Original Materials:** Literaturarchiv Salzburg (physical archive)
**Digitization:** [YEAR] by Literaturarchiv Salzburg
**Platform:** GAMS, University of Graz
**This Archive:** Downloaded 2025-10-22 via automated Python scripts
**Validation:** Cross-checked against METS metadata specifications
**Known Limitations:** 22 objects incomplete due to source metadata issues
```

---

### ✅ R1.3: Domain-relevant community standards

**Status:** ✅ **ERFÜLLT**

**Aktuell:**
- ✅ **METS/MODS** (library/archive standard)
- ✅ **DFG-METS** (German research community)
- ✅ **JPEG** (standard image format)
- ✅ **tar.gz** (standard archive format)
- ✅ **DataCite** Metadata Schema (via Zenodo)

**Domain:** Digital Humanities / Cultural Heritage

---

## FAIR-Compliance Übersicht

| Kategorie | Erfüllt | Teilweise | Nicht erfüllt | Score |
|-----------|---------|-----------|---------------|-------|
| **Findable (F1-F4)** | 3 | 1 | 0 | 87.5% |
| **Accessible (A1-A2)** | 4 | 0 | 0 | 100% |
| **Interoperable (I1-I3)** | 0 | 2 | 1 | 33% |
| **Reusable (R1-R1.3)** | 2 | 2 | 0 | 75% |
| **GESAMT** | 9 | 5 | 1 | **73%** |

---

## 🔴 KRITISCHE LÜCKEN (Priorität HOCH)

### 1. Kontrollierte Vokabulare (I2) - KRITISCH

**Problem:** Keywords sind Freitext, keine standardisierten IDs

**Lösung:**
- GND-ID für Stefan Zweig: `https://d-nb.info/gnd/118637479`
- LCSH Subject Headings verwenden
- Wikidata IDs für Konzepte

**Aufwand:** Mittel (Recherche + Update Metadaten)

---

### 2. Provenance Details (R1.2) - WICHTIG

**Problem:** Digitalisierungs-Workflow nicht dokumentiert

**Lösung:**
- Literaturarchiv Salzburg kontaktieren für Digitalisierungs-Info
- Workflow-Beschreibung in README erweitern
- In Zenodo Description aufnehmen

**Aufwand:** Niedrig (Text hinzufügen)

---

### 3. Rich Metadata (F2) - WICHTIG

**Problem:** Temporal/Geographic Coverage fehlt

**Lösung:**
```json
"dates": [{"type": "Collected", "start": "1881", "end": "1942"}],
"locations": [{"place": "Salzburg, Austria"}],
"subjects": [{"term": "Literary studies", "scheme": "OECD"}]
```

**Aufwand:** Niedrig (Metadaten erweitern)

---

## ✅ EMPFOHLENE ERGÄNZUNGEN

### Sofort (vor Upload):

1. **GND-ID für Stefan Zweig hinzufügen**
```json
"related_identifiers": [
  {
    "identifier": "https://d-nb.info/gnd/118637479",
    "relation": "isAbout",
    "scheme": "url"
  }
]
```

2. **Temporal Coverage hinzufügen**
```json
"notes": "... Temporal coverage: 1881-1942 (Stefan Zweig's lifetime). Geographic origin: Salzburg, Austria."
```

3. **Contact Person hinzufügen**
```json
"contributors": [
  {
    "name": "Literaturarchiv Salzburg",
    "type": "ContactPerson",
    "email": "info@literaturarchiv-salzburg.at"  // Falls verfügbar
  }
]
```

4. **ORCID IDs für Creators** (falls vorhanden)

---

### Optional (zukünftige Versionen):

1. **RDF/Linked Data Export** aus METS generieren
2. **Schema.org JSON-LD** im Archiv einbetten
3. **Detaillierte Provenance-Datei** (PROV-O Standard)
4. **Funding Information** recherchieren und hinzufügen

---

## 📊 FAIR Score Verbesserung

### Aktuell: **73%** FAIR-konform

### Nach Ergänzungen: **~90%** FAIR-konform

| Verbesserung | Auswirkung | Score-Gewinn |
|--------------|------------|--------------|
| GND-ID + LCSH | I2 → Teilweise | +17% |
| Temporal/Geographic | F2 → Vollständig | +4% |
| Provenance Details | R1.2 → Vollständig | +6% |
| Contact Person | R1 → Vollständig | +3% |

---

## 🎯 Umsetzungsplan

### Phase 1: Vor Zenodo Upload (TODAY)

```python
# In zenodo_upload_simple.py METADATA aktualisieren:

"related_identifiers": [
    {
        "identifier": "https://gams.uni-graz.at/context:szd",
        "relation": "isSupplementTo",
        "scheme": "url"
    },
    {
        "identifier": "https://stefanzweig.digital",
        "relation": "isSupplementTo",
        "scheme": "url"
    },
    # NEU: GND-ID
    {
        "identifier": "https://d-nb.info/gnd/118637479",
        "relation": "isAbout",
        "scheme": "url"
    }
],

"subjects": [
    {"term": "Stefan Zweig", "identifier": "https://d-nb.info/gnd/118637479"},
    {"term": "Literary studies", "scheme": "OECD FOS 2007", "identifier": "6.02"}
],

# Notes erweitern:
"notes": f"... Temporal coverage: 1881-1942 (Stefan Zweig's lifetime). Geographic location: Salzburg, Austria. Original materials held by Literaturarchiv Salzburg. Digitization by GAMS, University of Graz. This backup created 2025-10-22 for long-term preservation."
```

### Phase 2: Nach Upload (Optional)

1. README.md mit DOI-Badge aktualisieren
2. CITATION.cff mit DOI aktualisieren
3. Literaturarchiv Salzburg über Archiv informieren
4. Optional: Bei Re3data registrieren

---

## 📚 Referenzen

**FAIR Principles:**
- https://www.go-fair.org/fair-principles/
- https://www.nature.com/articles/sdata201618

**Standards:**
- GND (Gemeinsame Normdatei): https://www.dnb.de/gnd
- LCSH (Library of Congress): https://id.loc.gov/
- DataCite Metadata Schema: https://schema.datacite.org/
- METS/MODS: https://www.loc.gov/standards/mets/

**Tools:**
- FAIR Evaluation Tool: https://fairsharing.github.io/FAIR-Evaluator-FrontEnd/
- F-UJI Assessment: https://www.f-uji.net/

---

## ✅ Checkliste für Upload

- [ ] GND-ID für Stefan Zweig hinzugefügt
- [ ] Temporal Coverage (1881-1942) hinzugefügt
- [ ] Geographic Location (Salzburg) hinzugefügt
- [ ] OECD Subject Classification hinzugefügt
- [ ] Provenance-Details in Description erweitert
- [ ] Contact Person/Email hinzugefügt (falls verfügbar)
- [ ] ORCID IDs für Creators hinzugefügt (falls verfügbar)
- [ ] Funding Information recherchiert (falls zutreffend)

---

**FAIR-Compliance Version:** 1.0
**Letzte Aktualisierung:** 2025-10-22
**Nächste Review:** Nach Zenodo Upload
