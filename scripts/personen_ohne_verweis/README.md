# Personen ohne Verweis aus dem Bestand

Erhebt aus [`data/Index/Person/SZDPER.xml`](../../data/Index/Person/SZDPER.xml), welche
Personeneinträge von keiner anderen TEI-Datei unter `data/` referenziert werden, und legt
das Ergebnis als `unlinked_persons.csv` neben dem Skript ab.

Das Ergebnis ist eine Kandidatenliste. Ob ein Eintrag entfernt, für eine kommende
Lieferung behalten oder irgendwo verlinkt wird, entscheidet das Projekt. Das Skript ändert
keine TEI-Datei.

## Verweismuster

Ein Verweis zählt, wenn das RDF-Mapping ihn liest, nicht wenn er wie ein Verweis aussieht.
`GetPersonlist` in `szd-TORDF.xsl` erzeugt ein Tripel für genau zwei Schreibungen:

```
ref="#SZDPER.42"
ref="https://gams.uni-graz.at/o:szd.personen#SZDPER.42"
ref="http://d-nb.info/gnd/118637479"   (nur am persName, über den Index aufgelöst)
```

Daraus folgen drei Leseregeln, die das Skript seit dem Checkup 2026-09 befolgt.

`ref="SZDPER.42"` ohne Fragmentmarke zählt nicht. Das Mapping verwirft den Wert, die
Personenansicht bleibt leer, und der Eintrag gehört auf die Liste, solange die Schreibung
nicht vereinheitlicht ist. Das erledigt
[`scripts/checkup_2026_09_index/normalize_person_refs.py`](../checkup_2026_09_index/).

Eine Normdatennummer an einem `persName` zählt, wo immer sie unter `data/` steht, denn das
Mapping löst sie über den Index auf. Dieselbe Nummer an einem `repository` oder `orgName`
benennt eine Institution und zählt nicht.

In `data/Aufsatzablage/SZDESS.xml` bleibt `author/@ref` unberücksichtigt, wo der innere
`persName` einen eigenen Verweis trägt, weil die Aufsatzvorlage zuerst den `persName` liest
und nur ohne dessen Verweis auf das Attribut am `author` zurückfällt.

Bei mehreren Kennungen in einem Attribut, `ref="#SZDPER.42 #SZDPER.43"`, liest
`GetPersonlist` nur das erste Token. Kennungen, die ausschließlich dahinter stehen, meldet
der Lauf gesondert, weil sie in der Personenansicht unsichtbar bleiben.

Verweise innerhalb von `SZDPER.xml` zählen nicht als Verwendung durch den Bestand, stehen
aber als eigene Spalte in der CSV.

## Spalten

| Spalte | Inhalt |
|---|---|
| `id` | Kennung `SZDPER.N` |
| `name` | Name in der Schreibung der Datei, `Nachname, Vorname` |
| `normdaten` | `persName/@ref` (GND), Wikidata- und Wikipedia-Kennungen, leerzeichengetrennt |
| `verweis_innerhalb_szdper` | ob die Personenliste selbst auf den Eintrag verweist |

Die frühere Spalte `gnd_sonst_verwendet` ist entfallen. Eine anderswo an einem `persName`
verwendete Normdatennummer ist ein Verweis, solche Einträge stehen deshalb gar nicht mehr
auf der Liste, und die Spalte trüge in jeder Zeile denselben Wert.

## Aufruf

```bash
# Trockenlauf: Zahlen, tote Verweise und die ersten Zeilen, keine CSV
python scripts/personen_ohne_verweis/list_unlinked_persons.py --dry-run

# CSV schreiben
python scripts/personen_ohne_verweis/list_unlinked_persons.py
```

Der Lauf meldet zusätzlich Verweise auf Kennungen, die es in der Personenliste nicht gibt,
und Kennungen, die nur hinter dem ersten Token eines Mehrfachverweises stehen. Beides ist
ein eigener Befund, kein Löschkandidat.

## Was das Skript bewusst nicht anfasst

- **Die Personenliste selbst.** Nichts wird gelöscht, ergänzt oder umsortiert.
- **Verknüpfungen über Namen.** Erkannt werden nur Kennungs- und GND-Verweise. Eine
  Person, die anderswo bloß als Fließtextname steht, gilt hier als unverknüpft.
- **Andere Verweisziele.** Werk-, Orts- und Sacheinträge bleiben außer Betracht.
