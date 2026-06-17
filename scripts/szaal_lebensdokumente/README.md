# SZ-AAL Lebensdokumente → SZDLEB.xml

Workflow, um Lebensdokumente aus einem Google-Sheets-Export (CSV) in die TEI-Sammlung
[`data/PersonalDocument/SZDLEB.xml`](../../data/PersonalDocument/SZDLEB.xml) zu überführen.
Wiederverwendbar für jeden Nachzug weiterer Objekte mit demselben Spaltenlayout.

## Geltungsbereich

Nur **Lebensdokumente** (SZDLEB, `<biblFull>`). Die Briefserie `SZ-AAL/B2.N` gehört in die
Korrespondenz (SZDKOR) mit anderem Schema — dafür ist dieses Skript **nicht** gebaut.

## CSV-Format

38 Spalten, feste Reihenfolge (siehe `C_*`-Konstanten in `csv_to_szdleb.py`). Erste Zeile ist
die Kopfzeile. Wichtige Konventionen, die das Skript erwartet:

- Mehrere Personen je Zelle mit **Semikolon** trennen (`Zweig, Stefan; Hollander, Barnett`).
  Komma trennt nur `Nachname, Vorname` innerhalb *einer* Person.
- GND als URL, Reihenfolge parallel zur Namensspalte; leere Slots als leeres Semikolon-Segment.
- Personennamen möglichst als `Nachname, Vorname` (wird zu `surname`/`forename` zerlegt).
- Datierung: Original-, erschlossene und normalisierte Spalte. Das Skript zeigt den
  Original-Wortlaut an, erschlossene Daten in `[…]`, und setzt `@when` aus der ISO-Spalte
  (`YYYY`, `YYYY-MM`, `YYYY-MM-DD`).

## Ablauf

```bash
# 1) Trockenlauf: erzeugt den XML-Block + Report, schreibt nichts
python scripts/szaal_lebensdokumente/csv_to_szdleb.py --csv <export.csv> \
    --gesamttitel "Stefan Zweig - <Bestandsname>"

# 2) Report prüfen (siehe unten), dann anwenden
python scripts/szaal_lebensdokumente/csv_to_szdleb.py --csv <export.csv> \
    --gesamttitel "Stefan Zweig - <Bestandsname>" --apply
```

Parameter: `--csv` (Pflicht), `--szdleb`/`--szdper` (Default: Repo-Pfade), `--gesamttitel`
(Default-Platzhalter — **Klartextnamen setzen**), `--start-id` (0 = automatisch fortlaufend
aus der Datei), `--apply` (ohne diese Flag nur Trockenlauf).

Eingebaute Sicherungen: Abbruch, wenn die erste Signatur schon in SZDLEB steht (kein
Doppelimport); Wohlgeformtheitsprüfung des Blocks und der Gesamtdatei nach dem Schreiben;
GND→SZDPER-Auflösung live aus der Personenliste (keine hartkodierten Personen-IDs).

## Manuelle Nachbearbeitung (der Report sagt, was)

Das Skript kann nicht alles automatisch korrekt machen. Sein Report listet genau die Stellen:

- **„Personen OHNE SZDPER-Verknüpfung"** — diese Personen fehlen in
  [`SZDPER.xml`](../../data/Index/Person/SZDPER.xml). Anlegen (mit GND, falls vorhanden; sonst
  nur `surname`/`forename` — **keine GND raten**), dann im SZDLEB-Eintrag `ref="#SZDPER.N"`
  am `editor`/`author` ergänzen.
- **„Personen ohne 'Nachname, Vorname'-Form"** — als `persName`-Volltext übernommen, prüfen.
- **„Als Körperschaft (orgName) modelliert"** — Institutionen werden per Schlüsselwort-Heuristik
  (`ORG_KEYWORDS`) als `<editor><orgName>` erfasst (im SZDLEB-Bestand ein neueres Muster).
  Liste gegenlesen, ob nichts fälschlich als Körperschaft eingestuft wurde.
- **Gesamttitel** verifizieren: muss der ausgeschriebene Bestandsname sein, einheitlich über
  alle Einträge (analog `Stefan Zweig - Alberman Papers 2`).
- **Trennfehler im CSV**: ein Komma statt Semikolon klebt zwei Personen zusammen — der Report
  zeigt das als unstrukturierten Namen. Im CSV korrigieren oder im XML nachziehen.

PIDs (`o:szd.*`) werden **nicht** lokal vergeben, sondern beim GAMS-Ingest.

## Erstanwendung

SZ-AAL/L1–L13 → SZDLEB.144–156 (13 Einträge). Dabei in SZDPER nachgepflegt:
SZDPER.2314 Hollander (GND), 2315 Altmann (GND), 2316 Geiringer, 2317 Meiler, 2318 Ullmann
(letzte drei ohne GND). Korrigiert: SZDLEB.51 (Titel/Datierung Geburtsschein-Fotokopie),
SZDLEB.137 (`ana`→`xml:id`).
