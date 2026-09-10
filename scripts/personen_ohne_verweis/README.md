# Personen ohne Verweis aus dem Bestand

Erhebt aus [`data/Index/Person/SZDPER.xml`](../../data/Index/Person/SZDPER.xml), welche
Personeneinträge von keiner anderen TEI-Datei unter `data/` referenziert werden, und legt
das Ergebnis als `unlinked_persons.csv` neben dem Skript ab.

Das Ergebnis ist eine Kandidatenliste. Ob ein Eintrag entfernt, für eine kommende
Lieferung behalten oder irgendwo verlinkt wird, entscheidet das Projekt. Das Skript ändert
keine TEI-Datei.

## Verweismuster

Alle Verweise auf die Personenliste laufen über `@ref`, in vier Schreibungen, die alle
aufgelöst werden:

```
ref="#SZDPER.42"
ref="SZDPER.42"
ref="https://gams.uni-graz.at/o:szd.personen#SZDPER.42"
ref="#SZDPER.42 SZDPER.43"
```

Verweise innerhalb von `SZDPER.xml` zählen nicht als Verwendung durch den Bestand, stehen
aber als eigene Spalte in der CSV.

## Spalten

| Spalte | Inhalt |
|---|---|
| `id` | Kennung `SZDPER.N` |
| `name` | Name in der Schreibung der Datei, `Nachname, Vorname` |
| `normdaten` | `persName/@ref` (GND), Wikidata- und Wikipedia-Kennungen, leerzeichengetrennt |
| `gnd_sonst_verwendet` | ob die GND dieser Person anderswo unter `data/` vorkommt, obwohl die SZDPER-Kennung nicht verwendet wird |
| `verweis_innerhalb_szdper` | ob die Personenliste selbst auf den Eintrag verweist |

`gnd_sonst_verwendet: ja` heißt, dass die Person im Bestand vorkommt und nur nicht über
die Personenliste verknüpft ist. Solche Einträge sind Verknüpfungslücken, keine
Streichkandidaten.

## Aufruf

```bash
# Trockenlauf: Zahlen, tote Verweise und die ersten Zeilen, keine CSV
python scripts/personen_ohne_verweis/list_unlinked_persons.py --dry-run

# CSV schreiben
python scripts/personen_ohne_verweis/list_unlinked_persons.py
```

Der Lauf meldet zusätzlich Verweise auf Kennungen, die es in der Personenliste nicht gibt.
Das ist ein eigener Befund, kein Löschkandidat.

## Was das Skript bewusst nicht anfasst

- **Die Personenliste selbst.** Nichts wird gelöscht, ergänzt oder umsortiert.
- **Verknüpfungen über Namen.** Erkannt werden nur Kennungs- und GND-Verweise. Eine
  Person, die anderswo bloß als Fließtextname steht, gilt hier als unverknüpft.
- **Andere Verweisziele.** Werk-, Orts- und Sacheinträge bleiben außer Betracht.
