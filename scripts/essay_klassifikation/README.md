# Klassifikation der Aufsatzablage prüfen und ergänzen

Repariert den äußeren Gruppierungsschlüssel `term[@type="classification"]` in
[`data/Aufsatzablage/SZDESS.xml`](../../data/Aufsatzablage/SZDESS.xml) und erhebt für die
gruppierten Listen, welche Einträge dem Renderer Schlüssel schuldig bleiben.

## Warum das zählt

`szd-Werke.xsl` im gams-www-Repo gruppiert die Navigationsebene mit
`for-each-group group-by="term[@type='classification'][@xml:lang=$locale]"`. Fehlt der Term
in einer Sprache, fällt der Eintrag aus der Ausgabe dieser Sprache heraus, obwohl er
ingestiert ist. Weicht ein Term nur in der Schreibung ab, entsteht daneben eine zweite,
fast gleichnamige Kategorie mit einem einzigen Eintrag.

Die innere Gruppierung nach `title[@type="Einheitssachtitel"]` akzeptiert im Stylesheet
ausdrücklich auch Titel ohne `@xml:lang`; sprachlose Einheitssachtitel sind daher kein
Mangel, anders als die Formulierung „(de+en)" im Render-Vertrag nahelegt.

## Regeln

- **missing-language.** Ein Eintrag trägt die Klassifikation nur in einer Sprache. Das
  Paar wird von den Einträgen übernommen, die denselben Objekttyp führen
  (`extent/span/term[@type="objecttyp"]`, deutsch und englisch) und eine vollständige
  Klassifikation haben, aber nur, wenn alle diese Einträge auf genau ein Paar zeigen.
  Sonst bleibt der Eintrag unverändert und steht in der Restliste.
- **case-variant.** Ein Wert unterscheidet sich von der im Bestand überwiegenden
  Schreibung derselben Sprache nur durch Groß- und Kleinschreibung und wird auf sie
  gezogen.

Neue Kategorien legt das Skript nicht an. Das Vokabular bleibt geschlossen, es werden nur
Paare verwendet, die im Bestand vollständig belegt sind.

## Aufruf

```bash
# 1) Trockenlauf: geplante Änderungen, Restliste und Erhebung über die gruppierten Listen
python scripts/essay_klassifikation/fix_classification.py

# 2) Anwenden
python scripts/essay_klassifikation/fix_classification.py --apply

# 3) Prüflauf
python scripts/essay_klassifikation/fix_classification.py --verify
```

Der Prüflauf meldet einen Fehler, wenn die Eintragszahl sich gegenüber `HEAD` geändert
hat, die Reihenfolge verschoben ist, ein anderes Element als ein
`term[@type="classification"]` seinen Text geändert hat, noch ein Eintrag ohne
vollständige Klassifikation existiert oder noch Schreibvarianten derselben Kategorie
nebeneinander stehen. Ein zweiter Trockenlauf plant null Änderungen.

## Was das Skript bewusst nicht anfasst

- **`SZDMSK.xml` und `SZDLEB.xml`** werden nur gelesen. Die Erhebung zeigt dort fehlende
  Faksimile-PIDs, die kein Gruppierungsproblem sind, sondern nur den Mirador-Link
  verhindern.
- **Der Objekttyp** selbst. Er beschreibt das Stück, die Klassifikation ordnet es der
  Navigationsebene zu; beide bleiben getrennt.
- **Doppelte englische Entsprechungen.** `Druckfahnen` und `Korrekturfahnen` bilden beide
  auf `Galley proofs` ab, sind also in der englischen Ausgabe eine Kategorie und in der
  deutschen zwei. Das ist eine redaktionelle Frage, kein Datenfehler.
- **Vorhandene Mojibake** und die CRLF-Zeilenenden der Datei. Geschrieben werden nur die
  betroffenen `term`-Elemente.
