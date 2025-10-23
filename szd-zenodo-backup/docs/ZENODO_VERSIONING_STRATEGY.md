# Zenodo Versionierungsstrategie - Stefan Zweig Digital Archive

**Erstellt am:** 2025-10-22
**Projekt:** Stefan Zweig Digital - Archival Backup
**Ziel:** Langzeitarchivierung mit sinnvoller Versionierung

---

## Übersicht

Diese Strategie definiert, wie das Stefan Zweig Digital Archive auf Zenodo versioniert wird, um sowohl initiale Uploads als auch zukünftige Updates systematisch zu verwalten.

---

## Versionierungs-Philosophie

### Semantische Versionierung: MAJOR.MINOR.PATCH

**Format:** `v{MAJOR}.{MINOR}.{PATCH}`

#### MAJOR (Breaking Changes)
Erhöht bei fundamentalen Änderungen:
- Komplette Neustrukturierung des Archives
- Wechsel des Metadaten-Formats (z.B. METS → anders)
- Entfernung großer Teile des Archives
- Inkompatible strukturelle Änderungen

**Beispiel:** v1.0.0 → v2.0.0

#### MINOR (Feature Updates)
Erhöht bei signifikanten Erweiterungen:
- Neue Container hinzugefügt (z.B. 5. Container)
- Wesentlich mehr Objekte verfügbar (z.B. +500 neue Objekte)
- Neue Metadaten-Felder in METS
- Verbesserte Bildqualität (Re-Digitalisierung)

**Beispiel:** v1.0.0 → v1.1.0

#### PATCH (Bug Fixes & Minor Updates)
Erhöht bei kleineren Korrekturen:
- Korrektur fehlender Bilder (z.B. o:szd.267 vervollständigt)
- Metadaten-Korrekturen
- Hinzufügen einzelner Objekte (< 50)
- Dokumentations-Updates
- Fehlerhafte Downloads neu geladen

**Beispiel:** v1.0.0 → v1.0.1

---

## Initiale Version

### Version: v1.0.0 (Erste Veröffentlichung)

**Datum:** 2025-10-22
**Status:** Geplant

#### Inhalt:
- **Objekte:** 2.107 (100% der verfügbaren Objekte)
- **Bilder:** 18.719 (96,3% der METS-Einträge)
- **Datenvolumen:** ~24,7 GB
- **Container:** 4 (facsimiles, aufsatz, lebensdokumente, korrespondenzen)

#### Bekannte Einschränkungen:
- 22 unvollständige Objekte (1,0%)
- 729 fehlende Bilder (3,7%) aufgrund server-seitiger METS-Probleme
- Siehe: `DATA_QUALITY_ISSUES.md`

#### Metadaten-Tags:
```
version: v1.0.0
snapshot-date: 2025-10-22
source: GAMS (gams.uni-graz.at)
collection: Stefan Zweig Digital
completeness: 99.0%
known-issues: yes (see documentation)
```

---

## Zukünftige Versionierungs-Szenarien

### Szenario 1: Fehlende Bilder werden verfügbar
**Auslöser:** Server fügt fehlende Bilder hinzu (z.B. o:szd.267/IMG.108-232)

**Aktion:** PATCH Version erhöhen
- Neuer Download nur der betroffenen Objekte
- Validierung der Änderungen
- Upload als v1.0.1

**Änderungslog:**
```
v1.0.1 (2025-XX-XX)
- Fixed: o:szd.267 - added 125 previously missing images
- Fixed: o:szd.268 - added 230 previously missing images
- Fixed: o:szd.939 - added 328 previously missing images
- Completeness increased from 96.3% to 99.8%
```

### Szenario 2: Neue Objekte im bestehenden Container
**Auslöser:** GAMS fügt neue Dokumente hinzu (z.B. 50 neue Briefe)

**Aktion:** MINOR Version erhöhen (wenn > 50 Objekte) oder PATCH (wenn < 50)
- Vollständiger Re-Download des betroffenen Containers
- Aktualisierung der Metadaten
- Upload als v1.1.0 oder v1.0.1

**Änderungslog:**
```
v1.1.0 (2025-XX-XX)
- Added: 87 new objects in 'korrespondenzen' container
- Total objects increased from 2,107 to 2,194
- Total images: 19,856 (+1,137)
```

### Szenario 3: Neuer Container hinzugefügt
**Auslöser:** GAMS erstellt neuen Bereich (z.B. "szd.bibliothek")

**Aktion:** MINOR Version erhöhen
- Download des neuen Containers
- Aktualisierung aller Metadaten
- Upload als v1.1.0 (oder v1.2.0 wenn bereits v1.1.0 existiert)

**Änderungslog:**
```
v1.1.0 (2025-XX-XX)
- Added: New container 'szd.bibliothek' with 342 objects
- Containers: 4 → 5
- Total objects: 2,107 → 2,449
```

### Szenario 4: Strukturelle Änderungen in METS
**Auslöser:** GAMS wechselt Metadaten-Standard oder -Struktur

**Aktion:** MAJOR Version erhöhen
- Kompletter Re-Download mit neuem Parser
- Neue Validierungs-Skripte
- Upload als v2.0.0

**Änderungslog:**
```
v2.0.0 (2025-XX-XX)
- BREAKING: METS format changed from DFG-METS to MODS-METS
- Complete re-download and restructuring
- Updated parser and validation scripts
```

---

## Zenodo Upload-Strategie

### Datei-Organisation

#### Option A: Ein großes Deposit (Empfohlen für v1.0.0)
```
stefan-zweig-digital-v1.0.0.tar.gz (24.7 GB)
├── facsimiles/
├── aufsatz/
├── lebensdokumente/
├── korrespondenzen/
├── metadata/
├── logs/
└── README.md
```

**Vorteile:**
- Einfache Verwaltung
- Ein DOI für gesamtes Archiv
- Klare Versionierung

**Nachteile:**
- Große Download-Größe
- Bei Updates: Kompletter Re-Download nötig

#### Option B: Separate Container-Deposits
```
stefan-zweig-digital-facsimiles-v1.0.0.tar.gz (16.2 GB)
stefan-zweig-digital-aufsatz-v1.0.0.tar.gz (3.8 GB)
stefan-zweig-digital-lebensdokumente-v1.0.0.tar.gz (2.1 GB)
stefan-zweig-digital-korrespondenzen-v1.0.0.tar.gz (2.6 GB)
stefan-zweig-digital-metadata-v1.0.0.tar.gz (0.1 GB)
```

**Vorteile:**
- Modulare Updates (nur betroffene Container)
- Kleinere Downloads für Nutzer
- Parallele Uploads möglich

**Nachteile:**
- 5 separate DOIs
- Komplexere Verwaltung
- Mehr Zenodo-Deposits

### Empfehlung: **Option A für v1.0.0**

**Begründung:**
1. Initiale Version = einmaliger Upload
2. Nutzer wollen wahrscheinlich komplettes Archiv
3. Einfachere Zitierung (ein DOI)
4. Bei zukünftigen Updates: kann zu Option B gewechselt werden

---

## Metadaten für Zenodo

### Deposit Metadata (v1.0.0)

```json
{
  "title": "Stefan Zweig Digital - Complete Archive Backup (v1.0.0)",
  "upload_type": "dataset",
  "description": "Complete backup of the Stefan Zweig Digital collection from GAMS (Geisteswissenschaftliches Asset Management System, University of Graz). Contains 2,107 digitized objects with 18,719 high-resolution images (24.7 GB) across four collections: facsimiles, essays, life documents, and correspondence. Downloaded on 2025-10-22. Note: 22 objects (1%) are incomplete due to server-side metadata issues (see DATA_QUALITY_ISSUES.md for details). This archive ensures long-term preservation of this important cultural heritage resource.",

  "creators": [
    {
      "name": "Literaturarchiv Salzburg",
      "affiliation": "University of Salzburg"
    },
    {
      "name": "Zentrum für Informationsmodellierung",
      "affiliation": "University of Graz"
    }
  ],

  "keywords": [
    "Stefan Zweig",
    "Digital Humanities",
    "Literary Archive",
    "METS",
    "GAMS",
    "Cultural Heritage",
    "Manuscripts",
    "Correspondence",
    "Facsimiles"
  ],

  "notes": "This is an independent backup created for preservation purposes. Source: https://gams.uni-graz.at. Version: v1.0.0. Snapshot date: 2025-10-22. Completeness: 99.0% (22/2107 objects incomplete due to source data issues). See included DATA_QUALITY_ISSUES.md for detailed information about missing images.",

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
    }
  ],

  "contributors": [
    {
      "name": "Your Name / Organization",
      "type": "DataCurator"
    }
  ],

  "license": "CC-BY-4.0",

  "access_right": "open",

  "version": "1.0.0",

  "language": "deu"
}
```

---

## Update-Prozess

### Workflow für neue Versionen:

1. **Änderungen erkennen**
   ```bash
   python fetch_metadata.py
   # Vergleich mit logs/download_progress.json
   ```

2. **Versionsnummer bestimmen**
   - Entscheidungsbaum (siehe Szenarien oben)
   - Changelog erstellen

3. **Download durchführen**
   ```bash
   python download_archive.py
   # Nutzt Resume-Funktion für neue/geänderte Objekte
   ```

4. **Validierung**
   ```bash
   python validate_downloads.py
   # Vergleich mit vorheriger Version
   ```

5. **Archive erstellen**
   ```bash
   # Mit Versionsnummer im Dateinamen
   tar -czf stefan-zweig-digital-v1.0.1.tar.gz data/ metadata/ logs/ *.md
   ```

6. **Zenodo Upload**
   - Neues Deposit in bestehender Version (Zenodo-Versionierung)
   - Metadaten aktualisieren
   - Changelog hinzufügen

7. **Dokumentation**
   - README.md aktualisieren
   - CHANGELOG.md erstellen/erweitern
   - Git Tag erstellen: `git tag v1.0.1`

---

## Monitoring & Automatisierung

### Empfohlene Aktualisierungs-Intervalle

**Manuell:**
- Initiale Version: v1.0.0 (sofort)
- Quartalsweise Prüfung auf Updates (z.B. jedes Quartal)
- Bei bekannten Änderungen (z.B. Newsletter vom GAMS-Team)

**Automatisiert (optional):**
```bash
# Cron-Job: Monatliche Prüfung
0 2 1 * * cd /path/to/szd-backup && python check_for_updates.py
```

**check_for_updates.py** (zu implementieren):
- Fetch aktuelle Metadaten
- Vergleich mit lokaler Version
- Email-Benachrichtigung bei Änderungen

---

## Zenodo Collection vs. Versioning

### Option 1: Zenodo Versioning Feature (Empfohlen)
- Nutzt Zenodo's eingebaute Versionierung
- Ein Deposit-Konzept mit mehreren Versionen
- Automatische Version-DOI + Concept-DOI
- Nutzer sehen alle Versionen auf einer Seite

**Struktur:**
```
Concept DOI: 10.5281/zenodo.XXXXX (permanent, zeigt immer auf neueste)
├── v1.0.0: DOI: 10.5281/zenodo.XXXXX1
├── v1.0.1: DOI: 10.5281/zenodo.XXXXX2
└── v1.1.0: DOI: 10.5281/zenodo.XXXXX3
```

### Option 2: Zenodo Community
- Eigene "Stefan Zweig Digital Archive" Community
- Alle Versionen als separate Einträge
- Bessere Sichtbarkeit
- Kann mit Option 1 kombiniert werden

---

## Empfohlene Dateien im Archive

### v1.0.0 Struktur:
```
stefan-zweig-digital-v1.0.0/
├── data/
│   ├── facsimiles/
│   ├── aufsatz/
│   ├── lebensdokumente/
│   └── korrespondenzen/
├── metadata/
│   ├── container_metadata/
│   └── object_ids_summary.txt
├── logs/
│   ├── download_progress.json
│   ├── validation_report.json
│   └── download.log
├── scripts/
│   ├── fetch_metadata.py
│   ├── download_archive.py
│   ├── validate_downloads.py
│   └── requirements.txt
├── README.md
├── DATA_QUALITY_ISSUES.md
├── CHANGELOG.md
├── LICENSE.md
└── CITATION.cff
```

---

## CHANGELOG.md Template

```markdown
# Changelog - Stefan Zweig Digital Archive

All notable changes to this archive will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-22

### Initial Release
- Complete backup of Stefan Zweig Digital collection from GAMS
- 2,107 objects across 4 containers
- 18,719 high-resolution images
- 24.7 GB total data volume
- METS/MODS metadata for all objects

### Known Issues
- 22 objects (1.0%) incomplete due to server-side metadata issues
- 729 images (3.7%) missing from METS-referenced resources
- See DATA_QUALITY_ISSUES.md for detailed list

### Statistics
- facsimiles: 169 objects (161 complete)
- aufsatz: 625 objects (619 complete)
- lebensdokumente: 127 objects (123 complete)
- korrespondenzen: 1,186 objects (1,182 complete)

---

## [Unreleased]

### Planned
- Monitor source for updates quarterly
- Re-download if missing images become available
```

---

## Zusammenfassung

### Für v1.0.0:
1. ✅ Ein großes Archiv (24.7 GB)
2. ✅ Zenodo Versioning nutzen
3. ✅ Umfassende Dokumentation einbetten
4. ✅ Concept-DOI für langfristige Zitierbarkeit

### Für Updates:
1. Semantische Versionierung (MAJOR.MINOR.PATCH)
2. Klare Changelog-Dokumentation
3. Neue Version über Zenodo Versioning hochladen
4. Git Tags für Nachvollziehbarkeit

### Nächste Schritte:
1. Archive erstellen (tar.gz)
2. Zenodo Sandbox-Test
3. Upload zu Zenodo Production
4. DOI dokumentieren & teilen

---

**Strategie-Version:** 1.0
**Autor:** Archive Maintainer
**Letzte Aktualisierung:** 2025-10-22
