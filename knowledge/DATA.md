---
title: TEI-XML Data Overview
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD.git
method:
  name: Promptotyping
  url: https://dhcraft.org/promptotyping
status: complete
created: 2025-10-23
updated: 2026-06-15
version: 1.0.0
tags: [data, zweig, tei, statistics]
---

# TEI-XML Data Overview

Bestandsuebersicht der TEI-XML-Sammlungen mit Umfangs- und Datumsstatistiken sowie dokumentierten Datenluecken.

## Collection Statistics (24 Jun 2026)

| Collection | File | Lines | Size | Entries | Dates | Machine-readable |
|------------|------|------:|-----:|--------:|------:|-----------------:|
| Korrespondenz (Index) | `data/Correspondence/SZDKOR.xml` | 39,649 | 1.28 MB | 765 | 760 | 741 (98%) |
| Korrespondenz-Konvolute | `data/Correspondence/konvolute/` (42 Dateien) | 69,461 | 3.0 MB | 904 | 1,720 | 1,629 (95%) |
| Autographen | `data/Autograph/SZDAUT.xml` | 58,718 | 3.1 MB | 997 | 1,250 | 1,248 (100%) |
| Bibliothek | `data/Library/SZDBIB.xml` | 103,319 | 4.2 MB | 1,303 | 1,304 | 1,281 (98%) |
| Aufsaetze | `data/Aufsatzablage/SZDESS.xml` | 56,284 | 2.9 MB | 624 | 1 | 1 (100%) |
| Werke/Manuskripte | `data/Work/SZDMSK.xml` | 33,015 | 2.1 MB | 352 | 1 | 1 (100%) |
| Lebensdokumente | `data/PersonalDocument/SZDLEB.xml` | 13,728 | 711 KB | 156 | 1 | 1 (100%) |
| Erstveroeffentlichungen | `data/Publication/SZDPUB.xml` | 8,609 | 506 KB | 159 | 159 | 159 (100%) |
| Biographie | `data/Biography/SZDBIO.xml` | 1,614 | 87 KB | 104 | 208 | 208 (100%) |
| Glossar | `data/Glossary/szd-Glossary.xml` | 442 | 58 KB | -- | 0 | -- |
| **Gesamt** | | **383,839** | **18.1 MB** | **5,364** | **5,404** | **5,269 (98%)** |

**Entries** = `<biblFull>` (Sammlungen), `<event>` (Biographie), oder `<person>` (Index).

**Korrespondenz-Konvolute** = die per-Person-Objekte `o:szd.korrespondenzen.<person>` (zweite Ebene, ein `biblFull` pro Einzelbrief mit Faksimile-PID); der Index SZDKOR aggregiert pro Bündel. Im Juni 2026 um die SZ-AAL/B-Korrespondenz erweitert (42 Konvolute, ~480 Briefe; 30 neu, 12 erweitert). Siehe [COLLECTIONS.md](COLLECTIONS.md) und [DATA_MODEL.md](DATA_MODEL.md).
**Machine-readable** = `<date>` mit `@when`, `@notBefore`, `@notAfter`, `@from`, oder `@to`.

### Index-Dateien (nicht in Tabelle)

| File | Lines | Purpose |
|------|------:|---------|
| `data/Index/Person/SZDPER.xml` | 21,967 | Personen-Normdaten (GND, Wikidata, VIAF) |
| `data/Index/SZDWRK.xml` | 5,422 | Werkindex (WEMI-Ebene) |
| `data/Index/Location/SZDSTA.xml` | 303 | Standorte/Aufbewahrungsorte |
| `data/Issue/szd-thema*.xml` (7 Dateien) | ~4,593 | Thematische Sammlungen |

---

## Date Normalization History

Maschinenlesbare Datumsattribute wurden am 29. Maerz 2026 systematisch nachgetragen:

| Datei | Vorher | Nachher | Methode |
|-------|-------:|--------:|---------|
| SZDKOR.xml | 60% | 97% | `@notBefore`/`@notAfter` fuer Jahresbereiche; `cert="low"` fuer unsichere Daten |
| SZDBIB.xml | 2% | 98% | `@when` fuer Jahresangaben; `s.d.` uebersprungen |
| SZDPUB.xml | 0% | 100% | `@when` fuer Jahre; Mojibake-Dashes repariert |
| SZDAUT.xml | 58% | 100% | `@when` fuer Jahre; `@notBefore`/`@notAfter` fuer Bereiche; Mojibake-Dashes repariert |

**Verbleibende Luecken:**
- 19 `n. d.`-Eintraege in SZDKOR (kein Datum verfuegbar)
- 19 `s.d.`-Eintraege in SZDBIB (sine dato)
- 1 unvollstaendiges Datum in SZDAUT (`24. April` ohne Jahr)

---

## Glossar -- Datenqualitaet

### DE/EN-Definitionen vertauscht (Beilagen vs. Zusatzmaterial)

Im Glossar (`data/Glossary/szd-Glossary.xml`) widersprechen sich bei zwei benachbarten SKOS-Konzepten die deutsche und die englische `skos:definition` -- die Definitionstexte sind ueberkreuz vergeben:

| Konzept (`prefLabel`) | DE-Definition beschreibt | EN-Definition beschreibt |
|-----------------------|--------------------------|--------------------------|
| `Enclosures` (Beilagen) | von Zweig selbst / zu Lebzeiten beigelegt | von Dritten / nach seinem Tod hinzugefuegt |
| `AdditionalMaterial` (Zusatzmaterial) | von Dritten / nach seinem Tod hinzugefuegt | von Zweig selbst / zu Lebzeiten |

Die `prefLabel` (DE/EN) sind in beiden Faellen korrekt; nur die Definitionstexte stehen ueber Kreuz. Innerhalb jedes Konzepts widersprechen sich DE und EN, ueber beide Konzepte hinweg passen sie kreuzweise zusammen. Die semantisch plausible Lesart ist die deutsche (Beilage = von Zweig/zu Lebzeiten, Zusatzmaterial = von Dritten/posthum); welche Sprachfassung kanonisch ist, muss aber redaktionell entschieden werden. **Fix:** die beiden englischen `skos:definition` gegeneinander tauschen.

_Gefunden 11. Juni 2026 beim Abgleich der SZDLEB-Anzeigefelder gegen das Glossar._

---

## Korrespondenz-Details

### Struktur

```
<TEI>
 +-- text
     +-- listBibl
         +-- biblFull*
             +-- idno type="signature"  ->  SZ-...
```

Ein Korrespondenzpartner kann **mehrere Signaturen** haben (z.B. ein Konvolut plus Einzelbriefe).

### Offene Datenluecken

| Issue | Count | Remedy |
|-------|------:|--------|
| `n. d.` Daten (kein Datum vorhanden) | 19 | Nur durch Archivrecherche loesbar |
| TEI-Signaturen ohne Katalog-Zuordnung | ~130 | Neue Katalogeintraege oder Markierung als unkatalogisiert |

---

_Last refresh: 29 Mar 2026._
