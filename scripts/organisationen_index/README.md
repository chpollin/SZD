# Organisationenindex SZDORG

Zwei Skripte, die den Organisationenindex erzeugen und den Bestand darauf umstellen.

- `build_org_index.py` schreibt [`data/Index/Organisation/SZDORG.xml`](../../data/Index/Organisation/SZDORG.xml)
  und daneben die Entscheidungstabelle `organisation_decisions.csv`.
- `migrate_org_references.py` entfernt die als Körperschaft entschiedenen Einträge aus
  `SZDPER.xml`, stellt die Verweise der Bestandsdateien um und protokolliert jede
  Umstellung in `migration_log.csv`.

Die Reihenfolge ist fest, das zweite Skript verwendet die Kennungen, die das erste vergibt.

## Warum

Die Präsentationsschicht erwartet das Objekt `o:szd.organisation` bereits.
`szd-TORDF.xsl` im Repo `ZIMLAB/szd` lädt es in die Variable `$OrganisationList` und löst
darin `t:org[t:orgName[@ref = …]]` zu einer internen `SZDORG`-Kennung auf. In GAMS fehlt
das Objekt. Die `@ref`-Schreibung muss deshalb zeichengleich zu der im Bestand sein, also
`http://d-nb.info/gnd/<Nummer>`.

`o:szd.standorte` bleibt daneben bestehen und bleibt die kuratierte Sicht auf die
Aufbewahrungsorte. `o:szd.organisation` führt alle Körperschaften einschließlich dieser
Aufbewahrungsorte, verknüpft über die `idno`-Rückverweise. `<idno type="SZDSTA">` ist ein
lebender Querverweis auf den Standortindex. `<idno type="SZDPER" subtype="superseded">`
nennt die Kennung eines Personeneintrags, den die Migration entfernt hat. Sie existiert im
Personenindex nicht mehr, und `szd-TORDF.xsl` gibt sie als `dcterms:replaces` aus, damit
alte Verweise auf die Personenkennung zur Körperschaft zurückführen.

## Zwei Quellen

1. `data/Index/Person/SZDPER.xml`. Körperschaften, die der Personenindex als `person`
   führt. Sie sind nirgends als solche markiert, das Skript findet sie über zwei
   Heuristiken, eine `persName` ohne `surname`/`forename` und ein Namensmuster für
   Körperschaftsbezeichnungen. Was ein Treffer dann ist, steht als Einzelentscheidung in
   der Tabelle `DECISIONS` im Skript.
2. Jedes `orgName/@ref` unter `data/`. Körperschaften, auf die der Bestand schon über die
   Normdatennummer zeigt. Sie müssen alle im Index auflösen, auch ohne Eintrag in SZDPER.

Der Standortindex `SZDSTA.xml` wird mitgelesen, und zwar nicht als Zugabe. Der Bestand
zeigt auf die meisten Aufbewahrungsorte über dasselbe `orgName/@ref`, sie müssen hier also
ohnehin auflösen. Aus SZDSTA kommen sie unter ihrem kuratierten Namen mit Land, Ort und
Institutionslink herein statt in der Schreibung einer Signaturzeile, jeweils mit einem
Verweis auf ihre `SZDSTA`-Kennung.

Ein Kandidat, den die Tabelle nicht kennt, gilt als Person, wenn seine GND-Nummer im
Personenformat steht, sonst als ungeklärt. Eine neu in SZDPER eingetragene Körperschaft
taucht damit im Bericht auf, statt unbemerkt in den Index zu rutschen.

Normdatennummern werden nie geraten. Fehlt einem SZDPER-Eintrag die GND, übernimmt das
Skript sie nur dann aus dem Bestand, wenn dort genau ein `orgName` desselben Namens steht.

## Regeln der Redaktionsentscheidungen vom 11.09.2026

Beide Entscheidungen stehen als Konstante im Skript, nicht als Handkorrektur an der
erzeugten Datei.

`NON_CORPORATE_SZDSTA` hält die SZDSTA-Einträge aus dem Index heraus, die zwar Material
verwahren, aber keine Körperschaft benennen, also die sechs Einträge „Privatbesitz, Land“
und „Erben Stefan Zweigs“. Sie bleiben im Standortindex, und die Verweise des Bestands auf
sie zeigen weiter auf `o:szd.standorte`.

`MERGE_INTO` führt zwei SZDPER-Einträge zusammen, die dieselbe Körperschaft unter Namen
führen, die zu verschieden sind, als dass die Namensangleichung sie fassen könnte. Der Wert ist der
Eintrag, dessen Name und Normdatennummer den zusammengeführten Eintrag anführen, der
Schlüssel wird zur Namensvariante mit eigenem `idno`-Rückverweis. Zurzeit betrifft das
`SZDPER.1735` „Home Office, Whitehall“, das in `SZDPER.2326` „Großbritannien. Home Office“
mit GND 35565-3 aufgeht.

## Aufruf

```bash
# Index und Entscheidungstabelle schreiben
python scripts/organisationen_index/build_org_index.py

# nur berichten
python scripts/organisationen_index/build_org_index.py --dry-run

# SZDPER bereinigen und die Verweise des Bestands umstellen
python scripts/organisationen_index/migrate_org_references.py --dry-run
python scripts/organisationen_index/migrate_org_references.py
```

Beide Läufe sind deterministisch, zwei Läufe auf demselben Stand liefern dieselben
Dateien. Der Migrationslauf ist zusätzlich idempotent, ein zweiter Lauf findet nichts mehr
zu tun und lässt das Protokoll stehen.

Die `SZDORG`-Kennungen ergeben sich aus der Sortierung nach Hauptnamen und verschieben sich
daher, wenn Einträge hinzukommen. Nach dem Migrationslauf ist der Index nicht mehr aus den
Quellen erzeugbar, weil die Körperschaften den Personenindex verlassen haben.
`build_org_index.py` bricht dann mit einer Meldung ab, statt einen verkürzten Index zu
schreiben. Ab hier wird die Datei von Hand gepflegt.

## Form der umgestellten Verweise

Die Umstellung wählt die Form, die der Bestand für Körperschaften schon verwendet.

- Das Namenselement wird zu `<orgName ref="http://d-nb.info/gnd/<Nummer>">`, wo der
  Indexeintrag eine Normdatennummer trägt. So schreiben SZDLEB und SZDKOR durchgehend.
- Ohne Normdatennummer wird es zu
  `<orgName ref="https://gams.uni-graz.at/o:szd.organisation#SZDORG.<n>">`, gebaut wie das
  `https://gams.uni-graz.at/o:szd.standorte#SZDSTA.<n>`, mit dem SZDAUT und SZDBIB einen
  Aufbewahrungsort ohne GND referenzieren. `szd-TORDF.xsl` reicht einen solchen Wert
  unverändert durch.
- Das `@ref` des umgebenden `author`- oder `editor`-Elements wird ebenfalls auf die
  `SZDORG`-Form umgestellt und nicht gestrichen. `szd-Bibliothek.xsl` gruppiert und
  sortiert die Bibliotheksliste über dieses Attribut, ein leeres Attribut würde mehrere
  Titel unter einer Überschrift zusammenfallen lassen.

Wo aus einem `persName` ein `orgName` wird, bleiben die Attribute erhalten und das innere
`<name>` fällt weg, weil der Bestand den Körperschaftsnamen direkt im `orgName` führt.

## Spalten der Entscheidungstabelle

| Spalte | Inhalt |
|---|---|
| `szdper_id` | Kennung im Personenindex, leer bei Einträgen ohne SZDPER-Herkunft |
| `name` | Name in der Schreibung der Quelle |
| `gnd` | GND-Nummer ohne Präfix |
| `entscheidung` | `org`, `person`, `unclear` oder `keine-koerperschaft` |
| `grund` | Begründung der Entscheidung |
| `szdorg_id` | Kennung im neuen Index, leer außer bei `org` |
| `quelle` | `SZDPER`, `SZDSTA` oder `Bestand` |

Ungeklärte Fälle und die als Nicht-Körperschaft ausgeschlossenen Standorte stehen in der
Tabelle und nicht im Index.

## Spalten des Migrationsprotokolls

| Spalte | Inhalt |
|---|---|
| `datei` | Pfad relativ zur Repo-Wurzel |
| `kontext` | `xml:id` des umgebenden `biblFull`, bei SZDPER die entfernte Kennung |
| `zeile` | Zeile in der Datei vor der Umstellung |
| `alte_referenz` | Attribut und Wert vor der Umstellung |
| `neue_referenz` | Attribut und Wert danach |
| `aktion` | `Verweis umgestellt` oder `SZDPER-Eintrag entfernt` |

## Offene Befunde in den Quelldaten

Zwei Widersprüche bleiben nach Entscheidung vom 11.09.2026 unverändert stehen und sind hier
festgehalten, damit sie redaktionell entschieden werden können.

GND 38379-X trägt im Standortindex zwei verschiedene Körperschaften, `SZDSTA.37` „The
British Museum“ und `SZDSTA.38` „David H. Lowenherz“. Weil der Index über die
Normdatennummer zusammenführt, stehen beide Namen im Eintrag `SZDORG.15`, der Handelsname
als Hauptname und das Museum als Variante, und nur `SZDSTA.38` ist rückverwiesen. Korrekt
ist 38379-X für das British Museum, die Autographenhandlung braucht eine eigene Nummer oder
gar keine.

GND 117322695 steht im Bestand an einem `orgName` „Schweizerisches Vereinssortiment Olten“
in `SZDKOR`, ist im Personenindex aber die Nummer einer Person. Die Nummer kommt deshalb
nicht in den Index, und dieser eine Verweis im Bestand bleibt bewusst unaufgelöst. Der
Lauf meldet ihn als Warnung.

## Was die Skripte nicht anfassen

- Den Standortindex. SZDSTA bleibt wie er ist, auch wo SZDORG dieselbe Körperschaft
  führt.
- Die Präsentationsschicht. `szd-TORDF.xsl` und die übrigen Stylesheets liegen im Repo
  `ZIMLAB/szd` und werden dort gepflegt.
