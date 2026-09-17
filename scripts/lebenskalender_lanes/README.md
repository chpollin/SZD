# Zeitleisten-Lanes des Lebenskalenders erzeugen

Leitet aus den TEI-Quellen je Lane der integrierten Zeitleisten-Ansicht eine JSON-Datei mit
einem gemeinsamen Ereignisschema ab. Die Präsentationsschicht im Repo `ZIMLAB/szd` schaltet
die Lanes ein und aus und braucht dafür Ereignisse in einer Form, die über alle Bestände
gleich ist.

Die Frontendkopien der fünf Ausgabedateien sind in Commit `b616496` nach `ZIMLAB/szd`
gepusht und auf Staging mit identischen JSON-Inhalten bestätigt. Den laufenden
Auslieferungsstand führt die unten verlinkte Wissensdokumentation.

Schema, Datierungsregeln und Auslieferungsweg beschreibt
[`knowledge/Lebenskalender-Lanes.md`](../../knowledge/Lebenskalender-Lanes.md). Diese Datei
beschreibt den Lauf.

## Aufruf

```
python scripts/lebenskalender_lanes/build_lanes.py
```

Nur Standardbibliothek, kein Manifest, keine Installation. Der Lauf liest ausschließlich und
schreibt allein in die beiden Zielordner.

| Option | Wirkung |
|--------|---------|
| `--out-dir` | Zielordner der Lane-Dateien, Vorgabe `data/derived/lebenskalender` |
| `--docs-dir` | Kopierziel unterhalb von `docs/`, Vorgabe `docs/lebenskalender/lanes` |
| `--no-docs` | überspringt die Kopie unterhalb von `docs/` |

## Quellen

| Lane | Quelle |
|------|--------|
| `biography` | `docs/lebenskalender/SZDBIO.xml` |
| `correspondence` | `data/Correspondence/SZDKOR.xml` und die Konvolut-Objekte in `data/Correspondence/konvolute/` |
| `personal-documents` | `data/PersonalDocument/SZDLEB.xml` |
| `autographs` | `data/Autograph/SZDAUT.xml` |

Dazu `data/Index/Person/SZDPER.xml` für die Auflösung der Personenkennungen. Der Index wird
bei jedem Lauf frisch gelesen, GND-Verweise über die Nummer, direkte Verweise über die
SZDPER-Kennung. Änderungen am Personenindex wirken damit ohne Eingriff ins Skript.

Die Objekt-PID jeder Quelle stammt aus deren `teiHeader/publicationStmt/idno[@type="PID"]`
und steht nicht im Skript.

## Ausgabe

`<lane>.json` je Lane als Liste von Ereignissen, dazu `index.json` mit der Lane-Liste, den
Ereigniszahlen je Lane und je `datePrecision`, der Zahl der zusammengeführten Faksimilegruppen und
dem Erzeugungszeitpunkt im Feld `generated`.

Die Korrespondenz erhält alle Indexeinträge, weil gemeinsam verwendete Signaturen keine
vollständige Abdeckung durch Einzelbriefe belegen. Zusammengeführte Records bleiben mit
ihren ursprünglichen Metadaten im Feld `sources` erhalten. `mergedDuplicates` zählt die
Faksimilegruppen, `mergedRecords` die zusätzlich vereinigten Records.
`suppressedIndexEntries` bleibt für bestehende Leser als numerischer Wert `0` erhalten.

Die Lane-Dateien sind über zwei Läufe byteidentisch. Der einzige veränderliche Wert liegt in
`generated`; ein Vergleich klammert dieses Feld aus. Sortiert wird nach ISO-Datum und
Kennung, undatierte Ereignisse stehen am Ende. Geschrieben wird über eine Temporärdatei mit
anschließendem Umbenennen, UTF-8 mit LF.

## Was das Skript an den Quellen sichtbar macht

Der Lauf meldet auf `stderr` die Datumstexte, die er nicht auflösen konnte, und die
Auffälligkeiten, auf die er in den Kopfzeilen der Biographie trifft. Beides ist eine
Arbeitsliste für die Redaktion und löst keine Änderung an den Quellen aus.

## Prüfung

Der Generator parst alle Quellen und meldet unauflösbare Datierungen. Die Korpustests
prüfen zusätzlich, dass sämtliche Korrespondenzrecords einschließlich ihrer Metadaten
und Permalinks erhalten bleiben. Sie decken unvollständige Konvolute, gemeinsam verwendete
Signaturen, widersprüchliche Faksimilemetadaten und die drei Datierungen nach 1950 ab.
Geprüft werden außerdem der deterministische Export und die identische Kopie unter `docs/`.

```
python -m pytest scripts/lebenskalender_lanes/test_build_lanes.py -q
```

```
python -m ruff check --select E,F,W,I,UP,B,C4,SIM,PTH,RUF --ignore E501 scripts/lebenskalender_lanes/build_lanes.py
```
