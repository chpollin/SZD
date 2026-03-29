---
doc: DATA
project: SZD
version: 1.0.0
updated: 2026-03-29
tags: [data, zweig, tei, statistics]
---

# TEI-XML Data Overview

## Collection Statistics (29 Mar 2026)

| Collection | File | Lines | Size | Entries | Dates | Machine-readable |
|------------|------|------:|-----:|--------:|------:|-----------------:|
| Korrespondenz | `data/Correspondence/SZDKOR.xml` | 37,472 | 1.2 MB | 723 | 721 | 702 (97%) |
| Autographen | `data/Autograph/SZDAUT.xml` | 58,718 | 3.1 MB | 997 | 1,250 | 1,248 (100%) |
| Bibliothek | `data/Library/SZDBIB.xml` | 103,319 | 4.2 MB | 1,303 | 1,304 | 1,281 (98%) |
| Aufsaetze | `data/Aufsatzablage/SZDESS.xml` | 56,284 | 2.9 MB | 624 | 1 | 1 (100%) |
| Werke/Manuskripte | `data/Work/SZDMSK.xml` | 33,015 | 2.1 MB | 352 | 1 | 1 (100%) |
| Lebensdokumente | `data/PersonalDocument/SZDLEB.xml` | 12,739 | 661 KB | 143 | 1 | 1 (100%) |
| Erstveroeffentlichungen | `data/Publication/SZDPUB.xml` | 8,609 | 506 KB | 159 | 159 | 159 (100%) |
| Biographie | `data/Biography/SZDBIO.xml` | 1,614 | 87 KB | 104 | 208 | 208 (100%) |
| Glossar | `data/Glossary/szd-Glossary.xml` | 442 | 58 KB | -- | 0 | -- |
| **Gesamt** | | **311,212** | **15.0 MB** | **4,405** | **3,645** | **3,601 (99%)** |

**Entries** = `<biblFull>` (Sammlungen), `<event>` (Biographie), oder `<person>` (Index).
**Machine-readable** = `<date>` mit `@when`, `@notBefore`, `@notAfter`, `@from`, oder `@to`.

### Index-Dateien (nicht in Tabelle)

| File | Lines | Purpose |
|------|------:|---------|
| `data/Index/Person/SZDPER.xml` | 21,937 | Personen-Normdaten (GND, Wikidata, VIAF) |
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
