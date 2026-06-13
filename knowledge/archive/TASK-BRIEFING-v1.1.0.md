---
title: "Task Briefing: SZDO Datenmodellierung"
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD.git
method:
  name: Promptotyping
  url: https://dhcraft.org/promptotyping
status: archived
created: 2026-03-29
updated: 2026-03-29
---

# Task Briefing: SZDO Datenmodellierung

Archiviertes Aufgabenbriefing der vier Datenmodellierungs-Aufgaben, die mit SZDO v1.1.0 umgesetzt wurden.

## Status: ABGESCHLOSSEN (v1.1.0, März 2026)

Alle vier Aufgaben wurden in SZDO v1.1.0 umgesetzt:
- [x] Aufgabe 1: `szdo:datumEvidenz` als SKOS-Vokabular implementiert (4 Konzepte in szdg:DatumEvidenz)
- [x] Aufgabe 2: `szdo:hatBeteiligtenAkteur` als Superproperty mit 10 Rolleneigenschaften + RiC-Alignment
- [x] Aufgabe 3: Klawiter-Reconciliation geprüft, 8 Typ-Korrekturen (historical-study zu hatManifestation)
- [x] Aufgabe 4: Validierungspipeline erweitert (CQ16, CQ17, SHACL Shape 14)

## Kontext

Die Stefan Zweig Digital Nachlass-Ontologie (SZDO) v1.0.0 ist publiziert (72 Klassen, 130 Properties). Sie integriert RiC-O, IFLA LRM und CIDOC-CRM in einer geschichteten Architektur. Dokumentation: `knowledge/ONTOLOGY.md`. OWL-Datei: `ontology/szd-ontology.ttl`. Validierungspipeline: `ontology/validate.py`.

## Aufgaben

### 1. Evidenzquellen-Modell ergänzen

Aktuell hat die SZDO nur `szdo:sicherheitsgrad` (low/medium/high) für Datumsunsicherheit. Ergänze eine Property `szdo:datumEvidenz`, die die *Quelle* einer Datierung qualifiziert:

- `aus-dokument` — Datum steht im Dokument selbst
- `aus-kontext` — Aus Kontext erschlossen (z.B. benachbarte Briefe)
- `aus-externer-quelle` — Aus externer Quelle (Katalog, Sekundärliteratur)
- `unbekannt` — Evidenzquelle nicht dokumentiert

Das komplementiert den bestehenden Sicherheitsgrad. Implementiere als SKOS-Vokabular im SZD-Glossar (analog zu `szdg:ProvenanceFeature`). Aktualisiere die SHACL-Shapes.

Referenz: M³GIM-Projekt verwendet `m3gim:dateEvidence` für dasselbe Konzept. Siehe `knowledge/ONTOLOGY.md` Section "Known Limitations".

### 2. Personen-Rollendifferenzierung

Aktuell unterscheidet die SZDO nicht zwischen Personen, die *aktiv beteiligt* sind (Autor, Adressat, Schreiber) und solchen, die nur *erwähnt* werden. Ergänze:

- `szdo:hatBeteiligtenAkteur` (⊂ `rico:hasOrHadContributor`) — aktive Beteiligung
- Nutze `rico:hasOrHadSubject` für thematische Erwähnung (existiert bereits in RiC-O)

Prüfe die bestehenden Properties `szdo:hatAutor`, `szdo:hatSchreiberhand`, `szdo:hatAdressat` — diese sind implizit "aktive Beteiligung" und sollten als `rdfs:subPropertyOf szdo:hatBeteiligtenAkteur` deklariert werden.

Aktualisiere die Competency Questions: Ergänze eine CQ, die aktive Beteiligung von Erwähnung unterscheidet (relevant für Netzwerkanalysen der Korrespondenz).

### 3. Klawiter-Reconciliation Mapping prüfen

1.545 von 6.296 Klawiter-Einträgen sind mit dem Werkindex reconciliert. Prüfe die bestehenden Mappings in der Ontologie:

- `szdo:hatManifestation` verknüpft Werk → Klawiter-Eintrag
- Sind die 1.545 Verknüpfungen korrekt typisiert? (Erstausgaben → `szdo:Manifestation`, Übersetzungen → `szdo:WerkExpression`, Sekundärliteratur → `szdo:Sekundaerliteratur`)
- Gibt es Inkonsistenzen zwischen den Klawiter JSON-LD-Typen und den SZDO-Klassen?

Klawiter-Daten: Das Repo `../klawiter-rescue/data/output/klawiter.jsonld` enthält die vollständigen Daten. Vocabulary-Definition: `../klawiter-rescue/pipeline/lib/vocabulary.py`.

### 4. Validierungspipeline erweitern

Erweitere `ontology/validate.py` um:

- Tests für die neuen Properties (datumEvidenz, hatBeteiligtenAkteur)
- Eine neue Competency Question: "Welche Personen sind aktiv an einem Dokument beteiligt vs. nur erwähnt?"
- SHACL-Shapes für die Evidenzquellen

## Nicht in Scope

- Frontend-Arbeit (anderer Claude Code)
- Korrespondenz-Datenlücken: 270 von 289 date-Elementen ohne maschinenlesbare Attribute wurden in SZDKOR.xml nachgetragen (Maerz 2026). 19 `n. d.`-Eintraege bleiben ohne Datum.

## Relevante Dateien

| Datei | Zweck |
|-------|-------|
| `ontology/szd-ontology.ttl` | Hauptdatei — hier editieren |
| `ontology/szd-shapes.ttl` | SHACL-Shapes — erweitern |
| `ontology/validate.py` | Validierungspipeline — erweitern |
| `knowledge/ONTOLOGY.md` | Design-Dokument — aktualisieren |
| `knowledge/DATA_MODEL.md` | Datenmodell-Doku — bei Bedarf aktualisieren |
