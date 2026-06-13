---
title: Stefan Zweig Digital — Projektbeschreibung
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD.git
method:
  name: Promptotyping
  url: https://dhcraft.org/promptotyping
status: complete
created: 2026-03-29
updated: 2026-03-31
---

# Stefan Zweig Digital — Projektbeschreibung

Forschungsprojekt zur digitalen Nachlassrekonstruktion Stefan Zweigs aus der Perspektive der Digital Humanities und des Forschungsdatenmanagements.

---

## 1. Projektkontext

### Der Nachlass Stefan Zweigs

Stefan Zweig (1881–1942) zählt zu den meistgelesenen und meistübersetzten deutschsprachigen Autoren des 20. Jahrhunderts. Sein Nachlass ist durch Exil, Flucht und posthume Zerstreuung auf mehrere öffentliche und private Sammlungen weltweit verteilt — eine für die Forschung komplexe und hindernisreiche Situation.

Seit 2014 beherbergt das **Literaturarchiv Salzburg** eine der größten Sammlungen aus Zweigs literarischem Nachlass: über 50 Manuskripte und Typoskripte, mehr als ein Dutzend Notizbücher und alle bekannten Tagebücher. Ergänzt wird dies durch Bestände der **Daniel A. Reed Library** (SUNY Fredonia, USA) und der **National Library of Israel** (Jerusalem).

### Projektziel

**Stefan Zweig Digital** verfolgt das Ziel, den weltweit verstreuten Nachlass im digitalen Raum zusammenzuführen und einem wissenschaftlich interessierten Publikum zu erschließen. Es entsteht ein strukturierter Bestand digitaler Objekte, der im Sinne der digitalen Langzeitarchivierung repräsentiert wird und orts- und zeitunabhängig zugänglich ist.

Das Projekt ist so konzipiert, dass die spätere Erschließung und Anreicherung des Quellenmaterials (z.B. durch digitale Editionen) jederzeit möglich wird.

---

## 2. Inhalte und Sammlungen

### Nachlasssammlungen

| Sammlung | Kennung | Beschreibung |
|----------|---------|-------------|
| **Werke** | SZDMSK | Manuskripte, Typoskripte, Notizbücher, Konvolute, Korrekturfahnen |
| **Korrespondenz** | SZDKOR | Briefkonvolute mit Korrespondenzpartnern |
| **Autographen** | SZDAUT | Zweigs Sammlung handschriftlicher Dokumente Dritter |
| **Bibliothek** | SZDBIB | Rekonstruierte Privatbibliothek mit Provenienzmerkmalen |
| **Lebensdokumente** | SZDLEB | Verträge, Urkunden, Tagebücher, Ephemera |
| **Essays** | SZDESS | Journalistische und akademische Beiträge |
| **Publikationen** | SZDPUB | Erstveröffentlichungen und Editionsgeschichte |

### Indizes und Vokabulare

| Ressource | Kennung | Beschreibung |
|-----------|---------|-------------|
| **Personenindex** | SZDPER | Normdatenverknüpfung (GND, Wikidata, Wikipedia) |
| **Standortindex** | SZDSTA | Archive und Bibliotheken weltweit |
| **Werkindex** | SZDWRK | Abstrakte Werke (intellektuelle Ebene) |
| **Glossar** | szdg: | Kontrolliertes Vokabular (Provenienzmerkmale, Materialien) |
| **Lebenskalender** | SZDBIO | Biographische Zeitleiste (1881–1942) |

### Digitale Faksimiles

- Hochauflösende Digitalisate aller Sammlungsobjekte (JPEG)
- Online durchblätterbar über IIIF/Mirador-Viewer
- Langzeitarchivierung auf Zenodo

---

## 3. Methodischer Rahmen

### Digital Humanities Ansatz

Das Projekt verbindet vier methodische Säulen:

1. **Archivwissenschaftliche Erschließung**: Katalogisierung nach RNA (Regeln zur Erschließung von Nachlässen und Autographen) und internationalen Archivstandards
2. **Semantische Modellierung**: Formale Ontologie (SZDO v1.2.0) basierend auf Records in Context (RiC-O), IFLA LRM und CIDOC-CRM
3. **Linked Open Data**: Verknüpfung mit Normdateien (GND, Wikidata, VIAF, Geonames) und kontrollierten Vokabularen (SKOS)
4. **Digitale Langzeitarchivierung**: OAIS-konforme Speicherung in GAMS, Zenodo-Backup mit DOI-Versionierung

### Datenmodellierung

Das Datenmodell folgt dem TEI P5-Standard mit projektspezifischen Erweiterungen:

- **Bilingual**: Alle Metadaten in Deutsch und Englisch (`xml:lang="de"` / `xml:lang="en"`)
- **Normdatenverknüpft**: Personen, Orte und Werke über GND und Wikidata identifiziert
- **Dreischichtiges Werkmodell**: Werkindex (intellektuell) → Manuskriptzeugen (physisch) → Digitale Faksimiles (digital)
- **Provenienzerfassung**: Besitzwechsel, Provenienzmerkmale (Stempel, Exlibris, Marginalien) für die Bibliotheksrekonstruktion

### Nachlass-Ontologie (SZDO)

Die Stefan Zweig Digital Nachlass-Ontologie (SZDO v1.2.0) formalisiert das Datenmodell:

- **72 Klassen** (58 Kernklassen + 14 GAMS-Kompatibilitätsklassen)
- **130 Properties** (79 Kern + 51 GAMS-Kompatibilität)
- **Alignments**: Records in Context (Archiv), IFLA LRM (Werkschicht), CIDOC-CRM (Ereignisse/Provenienz)
- **Dokumentation**: https://chpollin.github.io/SZD/ontology/
- **Validierung**: 6-Stufen-Pipeline mit 22 Kompetenzfragen

Siehe [ONTOLOGY.md](ONTOLOGY.md) für das vollständige Design-Dokument.

---

## 4. Technische Infrastruktur

### Systemarchitektur

```
┌─────────────────────────────────────────────┐
│           Stefan Zweig Digital              │
│         https://stefanzweig.digital         │
└─────────────────┬───────────────────────────┘
                  │
     ┌────────────┼────────────┐
     │            │            │
┌────▼────┐ ┌────▼────┐ ┌─────▼─────┐
│  GAMS   │ │ GitHub  │ │  Zenodo   │
│Platform │ │  Pages  │ │  Archive  │
│(Produkt)│ │ (Doku)  │ │ (Backup)  │
└─────────┘ └─────────┘ └───────────┘
```

| Komponente | Technologie | Zweck |
|------------|-------------|-------|
| Datenformat | TEI P5 XML | Primärkodierung aller Sammlungen |
| Repository | GAMS (Fedora Commons) | Objektspeicher, PIDs, METS/MODS |
| Triple Store | Blazegraph | SPARQL 1.1, Volltextsuche |
| Transformation | XSLT 2.0/3.0 | TEI → HTML, TEI → RDF |
| Ontologie | OWL 2 (Turtle) | Formale Domänenontologie |
| Vokabular | SKOS | Kontrollierte Begriffe (Glossar) |
| Frontend | XSL + CSS + JS | Responsive Weboberfläche |
| Langzeitarchivierung | Zenodo | DOI-versioniertes Backup |
| Dokumentation | GitHub Pages | Ontologie-Referenz, Projektseite |

### Standards und Normen

- **TEI P5** — Text Encoding Initiative
- **METS/MODS** — Strukturelle und deskriptive Metadaten (DFG-METS)
- **DataCite 4.0** — Zenodo-Deposit-Metadaten
- **Dublin Core** — OAI-PMH-Harvesting
- **IIIF Presentation API** — Bildauslieferung und Viewer
- **RNA** — Regeln zur Erschließung von Nachlässen und Autographen
- **Records in Context (RiC-O)** — Archivische Ontologie
- **IFLA LRM** — Bibliographische Werkmodellierung
- **CIDOC-CRM** — Kulturerbe-Ereignismodellierung

---

## 5. Forschungsdatenmanagement

### FAIR-Compliance

| Prinzip | Maßnahmen |
|---------|-----------|
| **Findable** | DOI (Zenodo), ORCID, GND, Wikidata, PIDs in GAMS |
| **Accessible** | Open Access über GAMS und Zenodo, OAI-PMH |
| **Interoperable** | TEI P5, METS/MODS, RDF/SPARQL, kontrollierte Vokabulare |
| **Reusable** | CC-BY 4.0, detaillierte Provenienz, Community-Standards |

### Datenlebenszyklus

```
Physisches Objekt (Archiv)
    → Digitalisierung (Scan, 4912×7360 px)
    → Katalogisierung (TEI-XML, bilingual, normdatenverknüpft)
    → Transformation (XSLT → HTML, XSLT → RDF)
    → Publikation (GAMS, PIDs, SPARQL)
    → Langzeitarchivierung (Zenodo, DOI, METS)
    → Nachnutzung (Ontologie, Linked Data, Downloads)
```

### Lizenzierung

| Daten | Lizenz |
|-------|--------|
| TEI-XML Quelldaten | CC-BY 4.0 |
| Ontologie (SZDO) | CC-BY 4.0 |
| Zenodo-Archiv | CC-BY 4.0 |
| Quellcode | CC-BY 4.0 |
| Faksimiles | CC-BY 4.0 (Literaturarchiv Salzburg) |

### Zitierweise

```
Zweig, Stefan: [Werktitel], [Dokumenttyp]. Literaturarchiv Salzburg,
[Signatur]. In: Stefan Zweig digital, Hrsg. Literaturarchiv Salzburg,
URL: https://stefanzweig.digital/o:szd.werke#[ID]
```

---

## 6. Vernetzung und Anschlussprojekte

### Klawiter-Bibliographie

Die **Klawiter Bibliography** (6.296 Einträge) ergänzt Stefan Zweig Digital um die Rezeptions- und Publikationsgeschichte:

- Erstausgaben, Übersetzungen in 40+ Sprachen, Sekundärliteratur, Verfilmungen
- Verknüpfung über die SZDO-Werkschicht (szdo:Werk → szdo:Manifestation)
- GitHub: klawiter-rescue | Dokumentation: https://klawiter-rescue.github.io/

### Integrationsstrategie

Die SZDO-Ontologie dient als Brücke zwischen:
- **Archivperspektive** (SZD): Physische Objekte, Standorte, Provenienz
- **Bibliographische Perspektive** (Klawiter): Publikationen, Übersetzungen, Rezeption
- **Biographische Perspektive** (Lebenskalender): Lebensereignisse, Begegnungen, Orte

GND-Identifikatoren und Wikidata-Entitäten fungieren als gemeinsame Identifikatoren.

---

## 7. Projektchronologie

| Datum | Meilenstein |
|-------|-------------|
| 2014 | Literaturarchiv Salzburg erwirbt Stefan-Zweig-Bestände |
| 2017–2025 | Laufende Digitalisierung und Katalogisierung |
| Juni 2018 | Launch Version 1 (stefanzweig.digital) |
| Dezember 2019 | Version 2 — Englische Version hinzugefügt |
| Juli 2020 | Version 3 — Autographensammlung, erweiterte Daten |
| Oktober 2025 | Zenodo-Archivierung (2.107 Objekte, 22,3 GB) |
| März 2026 | SZDO v1.0.0 — Formale Nachlass-Ontologie, GitHub Pages |
| März 2026 | SZDO v1.1.0 — Datum-Evidenz, Personen-Rollenhierarchie, RiC-Alignments, Klawiter-Korrekturen |
| März 2026 | SZDO v1.2.0 — Generische Nachlass-Ontologie (`nachlass:`), Zwei-Schichten-Architektur, TEI-Datumsnormalisierung (SZDBIB/SZDPUB/SZDAUT/SZDKOR), Dokumentationsbereinigung |
| März 2026 | GAMS-Frontend (`gamsdev/`) aus Repository entfernt — Frontend wird direkt auf GAMS-Plattform verwaltet |

---

## 8. Beteiligte

### Personen

| Name | Rolle | Institution | ORCID |
|------|-------|-------------|-------|
| Oliver Matuschek | Projektleitung | Literaturarchiv Salzburg | — |
| Lina Maria Zangerl | Datenerfassung | Literaturarchiv Salzburg | 0000-0001-9709-3669 |
| Julia Rebecca Glunk | Datenerfassung | Literaturarchiv Salzburg | 0000-0001-6647-9729 |
| Verena Maria Höller | Datenerfassung | Literaturarchiv Salzburg | — |
| Christopher Pollin | Datenmodellierung | Digital Humanities Craft OG | 0000-0002-4879-129X |

### Institutionen

| Institution | Rolle |
|-------------|-------|
| Literaturarchiv Salzburg (Paris Lodron Universität Salzburg) | Quellenmaterial, Digitalisierung, Katalogisierung |
| Zentrum für Informationsmodellierung (Karl-Franzens-Universität Graz) | Digitale Infrastruktur, GAMS-Plattform |
| Digital Humanities Craft OG | Datenmodellierung, Ontologie, technische Umsetzung |
| Daniel A. Reed Library (SUNY Fredonia) | Kooperationspartner, Bestände |
| National Library of Israel (Jerusalem) | Kooperationspartner, Bestände |

---

## Referenzen

- **Website:** https://stefanzweig.digital
- **GAMS-Kontext:** https://gams.uni-graz.at/context:szd
- **Ontologie:** https://chpollin.github.io/SZD/ontology/
- **Zenodo-Archiv:** https://zenodo.org/uploads/17421555
- **GitHub:** https://github.com/chpollin/SZD
- **Klawiter-Bibliographie:** https://github.com/chpollin/klawiter-rescue
