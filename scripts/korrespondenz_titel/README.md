# Eintragstitel der Korrespondenz-Konvolute normalisieren

Vereinheitlicht die Titel der Einzelbriefeinträge in
[`data/Correspondence/konvolute/`](../../data/Correspondence/konvolute/) auf das Muster,
das die Mehrheit der Einträge derselben Dateien bereits trägt. Repariert werden zwei
Importrückstände, keine redaktionellen Titel.

## Zielform

Beide Titel entstehen aus `profileDesc/correspDesc/correspAction` und dem physischen
Umfang, also aus derselben Quelle, aus der die bereits korrekten englischen Titel erzeugt
wurden.

```
de: <Dokumenttyp> von <Sender> an <Empfänger> [<Tag>. <Monat> <Jahr>]
en: <Document type> from <Sender> to <Recipient>, <ISO-Datum>
```

- Dokumenttyp aus dem führenden Substantiv von `extent/span[@xml:lang="de"]`:
  Brief/Letter, Brieffragment/Letter, Ansichtspostkarte/Picture postcard,
  Postkarte/Postcard, Telegramm/Telegram, Kuvert/Envelope; alles andere Brief/Letter.
- Namen als `Vorname Nachname` aus `persName` (`forename` + `surname`), sonst der
  Elementtext; `orgName` nur, wenn die Handlung keine Person nennt.
- Mehrere Sender oder Empfänger stehen als mehrere `correspAction` desselben `@type` und
  werden mit `und` beziehungsweise `and` verbunden.
- Das Datum trägt allein `correspAction[@type="sent"]/date`. Der deutsche Titel nimmt es
  nur aus `@when` und schreibt es ausgeschrieben in eckige Klammern, der englische nimmt
  den ISO-Wert, ersatzweise den Anzeigetext, wenn der Eintrag kein `@when` hat.
  Ohne Datum entfällt der Datumsteil.
- `persName/name` mit dem zweisprachigen Wert `Unbekannt/Unidentified` wird je
  Titelsprache aufgelöst (`Unbekannt` / `Unidentified`). Die Zuordnung steht als
  ausdrückliche Tabelle im Skript, es wird kein Schrägstrich allgemein zerlegt.

`--verify` misst diese Regel gegen den Bestand: sie reproduziert die vorhandenen Titel in
Zielform bis auf die redaktionellen Namensvarianten (siehe unten).

## Reparierte Muster

1. **machine-date** — deutscher und englischer Titel identisch, ISO-Datum und/oder
   Signatur im Titeltext
   (`Walter Bauer an Stefan Zweig, 1933-01-07, SZ-SAM/AK.284`). Betroffen sind die
   Ansichtspostkarten der Signaturgruppe `SZ-SAM/AK`.
2. **mangled-partner** — der deutsche Titel trägt die unaufgelöste Quellzelle
   `Nachname, Vorname; Nachname, Vorname` statt der Partnernamen
   (`Brief von Lotte Zweig an Hannah; Altmann, Manfred Altmann [...]`). Der englische
   Titel derselben Einträge ist bereits richtig.

## Jahrhundertfehler im Datum

Bei den machine-date-Titeln trägt der Titel oft ein plausibles Jahr, während
`date/@when` die zweistellige Jahresangabe der Quelle in die 2000er expandiert hat
(`@when="2021-02-20"` zu `20. 2. 21`, Titel `1921-02-20`). Bevor das Datum aus dem Titel
entfernt wird, korrigiert das Skript `@when` aus dem Titel, sofern sich beide nur im
Jahrhundert unterscheiden und `@when` nach 1942 liegt. Jede andere Abweichung zwischen
Titeldatum und `@when` wird berichtet und nicht geändert.

## Aufruf

```bash
# 1) Trockenlauf: Vorher/Nachher je Eintrag plus Restliste, schreibt nichts
python scripts/korrespondenz_titel/fix_titles.py

# 2) Anwenden
python scripts/korrespondenz_titel/fix_titles.py --apply

# 3) Prüflauf
python scripts/korrespondenz_titel/fix_titles.py --verify
```

Der Prüflauf vergleicht den Arbeitsstand gegen `HEAD` und meldet einen Fehler, wenn die
Zahl der `biblFull` sich geändert hat, eine Datei nicht wohlgeformt ist, ein anderes
Element als `title` seinen Text oder ein anderes Attribut als `date/@when` seinen Wert
geändert hat, oder ein Altmuster außerhalb der dokumentierten Restliste geblieben ist.
Der Lauf ist idempotent, ein zweiter Trockenlauf meldet null Änderungen.

## Was das Skript bewusst nicht anfasst

- **Redaktionelle Namensvarianten.** Ein bereits in Zielform stehender deutscher Titel
  wird nie überschrieben, auch wenn er andere Namen nennt als `correspDesc`. Das betrifft
  vor allem die Briefe an Lotte Altmann, die vor der Heirat 1939 mit dem Mädchennamen
  angesprochen wird, während `correspAction` `Zweig, Lotte` führt.
- **Einträge mit leerem Sender oder Empfänger.** Wo `correspAction` keinen Namen enthält,
  wäre der erzeugte Titel unvollständig; solche Einträge stehen in der Restliste, ebenso
  die drei Ansichtskarten ohne Titeldatum, deren `@when` unplausibel ist und deren
  Jahrhundert sich aus dem Eintrag nicht belegen lässt.
- **Alles außerhalb von `titleStmt/title` und `correspAction/date/@when`.** Die
  Serialisierung ersetzt nur diese Stellen im Dateitext, Einrückung, Attributreihenfolge,
  fehlende XML-Deklaration und Zeilenenden bleiben unverändert.
- **Der Sammlungsindex `SZDKOR.xml`.** Dessen Titel beschreiben Bündel
  (`9 Korrespondenzstücke AN/VON Stefan Zweig`) und folgen einer anderen Konvention.
- **Vorhandene Mojibake.** Einige Dateien tragen doppelt kodierte Umlaute aus früheren
  Importen; das ist ein eigener Befund und kein Titelproblem.
