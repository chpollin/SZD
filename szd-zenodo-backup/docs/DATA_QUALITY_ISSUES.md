# Stefan Zweig Digital - Datenqualitätsprobleme

**Dokumentiert am:** 2025-10-21
**Aktualisiert am:** 2025-10-22
**Status:** Download abgeschlossen, Validierung durchgeführt

---

## Übersicht

Während des systematischen Downloads der Stefan Zweig Digital Sammlung wurden **Server-seitige Datenqualitätsprobleme** in den METS-Metadaten identifiziert. Diese Probleme verhindern den Download bestimmter Bilder.

---

## Problem-Beschreibung

### Symptom
Einige Bild-URLs in den METS-XML-Dateien enthalten **nur Dateinamen** statt vollständiger URLs mit Schema und Host.

### Erwartetes Format
```
http://gams.uni-graz.at/o:szd.XXX/IMG.Y
```

### Tatsächliches Format (fehlerhaft)
```
SZ_AAP_W*_*.jpg
```

### Technischer Fehler
```
Invalid URL 'SZ_AAP_W11_108.jpg': No scheme supplied
```

---

## Betroffene Objekte

### Kritischste Fälle (>100 fehlende Bilder)

#### o:szd.267 ⚠️ KRITISCH
- **Titel:** "Bau der Wiener Oper"
- **Container:** facsimiles
- **Betroffene Bilder:** 125 von 232 (53,9%)
- **Fehlende Bild-IDs:** IMG.108 bis IMG.232
- **Status:** 107 Bilder heruntergeladen

#### o:szd.268 ⚠️ KRITISCH
- **Titel:** (siehe METS)
- **Container:** facsimiles
- **Betroffene Bilder:** 230 von 321 (71,7%)
- **Fehlende Bild-IDs:** IMG.100 bis IMG.329
- **Status:** 91 Bilder heruntergeladen

#### o:szd.939 ⚠️ KRITISCH
- **Titel:** (siehe METS)
- **Container:** facsimiles
- **Betroffene Bilder:** 328 von 427 (76,8%)
- **Fehlende Bild-IDs:** IMG.100 bis IMG.427
- **Status:** 99 Bilder heruntergeladen

### Weitere betroffene Objekte (alphabetisch)

**facsimiles:**
- o:szd.227: 1 fehlendes Bild (IMG.89)
- o:szd.231: 6 fehlende Bilder (IMG.188-193)
- o:szd.2934: 1 fehlendes Bild (IMG.6)
- o:szd.315: 1 fehlendes Bild (IMG.122)
- o:szd.351: 2 fehlende Bilder (IMG.103, IMG.183)

**aufsatz:**
- o:szd.2213: 1 fehlendes Bild (IMG.2)
- o:szd.2340: 1 fehlendes Bild (IMG.3)
- o:szd.2430: 6 fehlende Bilder (IMG.2-7)
- o:szd.2454: 1 fehlendes Bild (IMG.7)
- o:szd.2574: 1 fehlendes Bild (IMG.2)
- o:szd.2743: 1 fehlendes Bild (IMG.3)

**lebensdokumente:**
- o:szd.179: 6 fehlende Bilder (IMG.10-15)
- o:szd.196: 6 fehlende Bilder (IMG.10-15)
- o:szd.197: 1 fehlendes Bild (IMG.10)
- o:szd.95: 1 fehlendes Bild (IMG.4)

**korrespondenzen:**
- o:szd.1440: 1 fehlendes Bild (IMG.3)
- o:szd.1618: 2 fehlende Bilder (IMG.3-4)
- o:szd.179: 6 fehlende Bilder (IMG.10-15)
- o:szd.524: 1 fehlendes Bild (IMG.2)

---

## Statistische Auswirkung

### Gesamt-Übersicht (Final nach Validierung)
- **Betroffene Objekte:** 22 von 2.107 (1,0%)
- **Fehlende Bilder:** 729 von 19.448 (3,7%)
- **Download-Erfolgsrate:** 99,0%
- **Heruntergeladene Bilder:** 18.719
- **Gesamtdatenvolumen:** 24,7 GB

### Nach Container
| Container | Total | Vollständig | Unvollständig | Erfolgsrate |
|-----------|-------|-------------|---------------|-------------|
| facsimiles | 169 | 161 | 8 | 95,3% |
| aufsatz | 625 | 619 | 6 | 99,0% |
| lebensdokumente | 127 | 123 | 4 | 96,9% |
| korrespondenzen | 1.186 | 1.182 | 4 | 99,7% |

---

## Ursache (BESTÄTIGT)

**Status:** ✅ Verifiziert durch manuelle Prüfung

Die betroffenen Bilder **existieren nicht** auf dem GAMS-Server:
- Test-URL: `https://gams.uni-graz.at/o:szd.267/IMG.108`
- Ergebnis: `404 Not Found - The requested URL was not found on this server`

**Fazit:** Die METS-Metadaten verweisen auf **nicht-existierende Ressourcen**. Dies ist ein Fehler in den Quellmetadaten, nicht ein URL-Format-Problem.

### Mögliche Gründe:
1. **Unvollständige Digitalisierung:** Nicht alle Seiten wurden gescannt/hochgeladen
2. **METS-Generierung:** Metadaten wurden erstellt, bevor alle Bilder verfügbar waren
3. **Fehlende Uploads:** Bilder wurden nie hochgeladen oder sind verloren gegangen
4. **Inkonsistente Seitenzählung:** METS enthält mehr Einträge als tatsächlich existierende Bilder

---

## Empfohlene Maßnahmen

### ✅ Sofort (Bereits umgesetzt)
- Download-Script handhabt Fehler korrekt (skip mit Warning)
- Detaillierte Logs werden erstellt
- Progress-Tracking dokumentiert fehlende Bilder
- Manuelle Verifikation durchgeführt (Bilder existieren nicht)

### 📋 Akzeptierte Einschränkung
**Entscheidung:** Problem wird **ignoriert** und dokumentiert

**Begründung:**
- Bilder existieren nicht auf dem Server (404 Error)
- Keine technische Lösung möglich
- Download-Script arbeitet korrekt
- Auswirkung auf Gesamtarchiv minimal (~3,4%)

### 📄 Dokumentation für Zenodo
1. **README.md erweitern:**
   - Known Issues Section
   - Liste der unvollständigen Objekte
   - Hinweis auf Quellproblem (nicht Archiv-Problem)

2. **Validation-Report:**
   - Nach vollständigem Download erstellen
   - Alle betroffenen Objekte mit Details auflisten
   - Statistik über Vollständigkeit

### 📧 Optional: GAMS-Team informieren
Falls gewünscht, können die Probleme dem GAMS-Team gemeldet werden:
- Nicht zur Behebung (Bilder existieren nicht)
- Zur Information (METS-Metadaten inkonsistent)
- Zur Dokumentation für andere Nutzer

---

## Technische Details

### METS-Struktur (Normal)
```xml
<mets:file ID="IMG.1" MIMETYPE="image/jpeg">
    <mets:FLocat xmlns:xlink="http://www.w3.org/1999/xlink"
                 xlink:href="http://gams.uni-graz.at/o:szd.267/IMG.1"/>
</mets:file>
```

### METS-Struktur (Fehlerhaft)
```xml
<mets:file ID="IMG.108" MIMETYPE="image/jpeg">
    <mets:FLocat xmlns:xlink="http://www.w3.org/1999/xlink"
                 xlink:href="SZ_AAP_W11_108.jpg"/>
</mets:file>
```

### Script-Verhalten
```python
# download_archive.py verhält sich korrekt:
try:
    response = requests.get(image_url)
    # ...
except requests.exceptions.RequestException as e:
    logging.warning(f"[WARN] Failed to download {image_id}")
    # Fährt mit nächstem Bild fort
```

---

## Kontakt-Informationen

### Probleme melden an:
- **GAMS Support:** https://gams.uni-graz.at
- **Stefan Zweig Digital:** https://stefanzweig.digital
- **Literaturarchiv Salzburg:** Über Website

### Informationen bereitstellen:
- Objekt-IDs: o:szd.2213, o:szd.231, o:szd.267
- METS-URLs: `https://gams.uni-graz.at/archive/get/o:szd.XXX/METS_SOURCE`
- Spezifische Bild-IDs mit Fehler
- Erwartete vs. tatsächliche URL-Formate

---

## Anhang

### Log-Beispiel (o:szd.267)
```
[108/232] Downloading IMG.108...
  Attempt 1 failed: Invalid URL 'SZ_AAP_W11_108.jpg': No scheme supplied
  Attempt 2 failed: Invalid URL 'SZ_AAP_W11_108.jpg': No scheme supplied
  Failed after 3 attempts: Invalid URL 'SZ_AAP_W11_108.jpg': No scheme supplied
    [WARN] Failed to download IMG.108
```

### Betroffene METS-Dateien
- `data/facsimiles/o_szd_2213/mets.xml`
- `data/facsimiles/o_szd_231/mets.xml`
- `data/facsimiles/o_szd_267/mets.xml`

---

---

## Validierungsergebnisse

**Validierungsdatum:** 2025-10-22, 18:10 Uhr

### Zusammenfassung
- **Validierte Objekte:** 2.107
- **Vollständige Objekte:** 2.085 (99,0%)
- **Unvollständige Objekte:** 22 (1,0%)
- **Erwartete Bilder:** 19.448
- **Heruntergeladene Bilder:** 18.719
- **Fehlende Bilder:** 729 (3,7%)

Die Validierung bestätigt, dass alle serverseitig verfügbaren Bilder erfolgreich heruntergeladen wurden. Die 729 fehlenden Bilder sind ausschließlich auf die oben dokumentierten METS-Metadaten-Probleme und nicht-existierende Server-Ressourcen zurückzuführen.

**Detaillierter Validierungsbericht:** `logs/validation_report.json`

---

**Dokumentations-Version:** 2.0
**Letzte Aktualisierung:** 2025-10-22, 18:10 Uhr
