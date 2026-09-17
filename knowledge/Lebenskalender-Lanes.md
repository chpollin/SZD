---
title: Lebenskalender-Lanes
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD.git
method:
  name: Promptotyping
  url: https://dhcraft.org/promptotyping
status: complete
created: 2026-09-11
updated: 2026-09-11
version: 1.0.0
tags: [data, lebenskalender, timeline, derived]
---

# Lebenskalender-Lanes

Die Zeitleisten-Ansicht des Lebenskalenders zeigt mehrere Bestände nebeneinander als
Lanes, die Nutzerinnen einzeln ein- und ausschalten. Damit die Ansicht alle Bestände gleich
behandeln kann, liegt jeder Lane eine eigene JSON-Datei im selben Ereignisschema zugrunde.
Die Dateien entstehen aus den TEI-Quellen dieses Repos durch
[`scripts/lebenskalender_lanes/build_lanes.py`](../scripts/lebenskalender_lanes/build_lanes.py);
die Ansicht ist in der Präsentationsschicht im Repo `ZIMLAB/szd` unter
`mode=timeline` integriert; `mode=fancy` bleibt als kompatibler Alias erhalten.
Ihre Implementierung und lokale Prüfung beschreibt dort
`knowledge/UI-Ueberarbeitung.md`. Frontendcommit `b616496` wurde am 11. September 2026
nach `ZIMLAB/szd` gepusht. Der erste Serverabgleich bestätigte denselben Implementierungsstand. Der anschließende Frontendcommit `3cb6596` korrigiert die Filterlinks für GAMS und ist ebenfalls auf Staging übernommen. Filter werden im URL-Fragment gespeichert, weil GAMS zusätzliche Queryparameter mit HTTP 404 zurückweist. HTTP-Prüfungen bestätigten die Auslieferung
der JavaScript- und CSS-Dateien samt Tokens sowie aller fünf JSON-Dateien mit identischem
Inhalt zum lokalen Stand. Standardansicht, `mode=fancy` und `mode=timeline` antworteten
in Deutsch und Englisch mit HTTP 200; die beiden Modi laden das neue Timeline-Skript.
Die Browserprüfung der bereits versendeten Fancy-URL zeigte die neue Ansicht mit allen
vier Lanes und den Quellenlisten. Fachliche Abnahme und Produktionsveröffentlichung
stehen aus.

Die Nachricht zur neuen Ansicht an das Literaturarchiv Salzburg wurde laut
Nutzerbestätigung am 11. September 2026 gesendet. Sie verweist auf die Fancy-Ansicht
und die Werkliste als Beispiel für die Navigation. Die fachliche Partnerprüfung und
Abnahme stehen aus.

Die frühere HTTP-Prüfung vom selben Tag fand unter der versendeten Staging-URL die ältere
Ansicht mit `lebenskalender-fancy.js`. Das neue `lebenskalender-timeline.js` und
`data/lebenskalender/index.json` antworteten dort mit HTTP 404. Auch der saubere
Stagingspiegel und `origin/main` der Präsentationsschicht standen damals auf `06382eb6`.
Der inzwischen gepushte Commit `b616496` enthält die neue Integration und die korrigierten
Lane-Dateien. Der bestätigte Mailversand belegt die Übergabe des zuvor verlinkten Stands.

## Lanes und Quellen

| Lane | Quelle | Objekt |
|------|--------|--------|
| `biography` | `docs/lebenskalender/SZDBIO.xml` | `o:szd.lebenskalender` |
| `correspondence` | `data/Correspondence/SZDKOR.xml` und `data/Correspondence/konvolute/` | `o:szd.korrespondenzen` und `o:szd.korrespondenzen.<person>` |
| `personal-documents` | `data/PersonalDocument/SZDLEB.xml` | `o:szd.lebensdokumente` |
| `autographs` | `data/Autograph/SZDAUT.xml` | `o:szd.autographen` |

Die Korrespondenz-Lane deckt beide Ebenen der Zwei-Ebenen-Architektur ab, die
[COLLECTIONS.md](COLLECTIONS.md) beschreibt, den aggregierenden Index und die
Einzelbriefe der Konvolut-Objekte.

Die Personenkennungen löst `data/Index/Person/SZDPER.xml` auf. Die Korrespondenz verweist
über die GND, die übrigen Bestände über die SZDPER-Kennung im `@ref` des `author`. Der
Index wird bei jedem Lauf gelesen, sodass Änderungen an ihm ohne Eingriff ins Skript
wirken.

## Ereignisschema

Jedes Ereignis ist ein JSON-Objekt mit denselben Feldern, unabhängig von der Lane.

`id`
Stabile Kennung, die `xml:id` des Quelleintrags, also etwa `SZDBIO.1`, `SZDKOR.127`,
`SZDKOR.roth-joseph.1`, `SZDLEB.138` oder `SZDAUT.720`.

`lane`
Einer der Werte `biography`, `correspondence`, `personal-documents`, `autographs`.

`date`
Beginn der Datierung als ISO-String in der Granularität der Quelle, `YYYY`, `YYYY-MM` oder
`YYYY-MM-DD`. Bei undatierten Stücken `null`.

`datePrecision`
Einer der Werte `day`, `month`, `year`, `range`, `inferred`, `undated`. Genau dann
`undated`, wenn `date` fehlt.

`dateEnd`
Nur bei `range` und `inferred` vorhanden, das Ende des Zeitraums als ISO-String.

`dateLabel`
Anzeigetext mit den Schlüsseln `de` und `en`, erzeugt aus dem ISO-Wert. Deutsch in der
Tagesform „7. Januar 1933“, englisch „7 January 1933“, bei Monatsgenauigkeit „Januar 1933“
beziehungsweise „January 1933“, bei Jahresgenauigkeit die Zahl allein, bei Zeiträumen
Beginn und Ende verbunden. Wo die Quelle eine Datierung nur als Anzeigetext führt und der
Parser sie nicht auflöst, steht dieser Quelltext im Label, weil er die einzige Auskunft
ist, die der Bestand über das Stück gibt.

`title`
Titel mit den Schlüsseln `de` und `en`. In der Korrespondenz aus `correspAction` erzeugt
nach dem Muster „Brief von X an Y“ beziehungsweise „Letter from X to Y“, mit den Namen in
Lesereihenfolge wie in der Titelkonvention der Konvolut-Objekte. In den Lebensdokumenten
und Autographen der Titel des `biblFull`, wobei ein zugewiesener Titel vor einem
Objekttitel und dieser vor dem Originaltitel steht; ein sprachneutraler Titel gilt für
beide Sprachen, und eine Sprache ohne eigenen Titel übernimmt den der anderen. In der
Biographie der Text des Eintrags in beiden Sprachen.

`place`
Ortsname, wenn die Quelle einen führt. In der Biographie aus der Kopfzeile vor dem
Datumselement, in der Korrespondenz aus `correspAction/placeName`, in den Autographen aus
dem Erwerbungsvermerk. Die Lebensdokumente führen keinen Ort.

`persons`
Liste von Objekten mit `id` und `name`. Die `id` ist die SZDPER-Kennung, `null` wo der
Verweis der Quelle sich nicht auflösen lässt. Der `name` steht in Indexform,
Nachname gefolgt vom Vornamen, und stammt aus dem Personenindex, soweit die Kennung dort
steht. In der Biographie sind es die referenzierten Personen des Eintrags, in der
Korrespondenz Absender und Empfänger, in den übrigen Beständen der Verfasser.

`signature`
Signatur aus `msIdentifier`, in den Autographen aus dem Provenienzvermerk.

`href`
Detailseite auf stefanzweig.digital, gebildet aus der Objekt-PID der Quelldatei und der
Kennung des Eintrags als Fragment, also
`https://stefanzweig.digital/<PID>/sdef:TEI/get#<id>`.

`facsimile`
PID des METS-Objekts, wo der Eintrag eines trägt. Das Faksimile selbst liegt unter
`https://stefanzweig.digital/<PID>`.

`dateOrigin`, `dateOriginPrecision`, `dateOriginEnd`, `dateOriginLabel`
Zusätzliche Angaben bei Autographen zur Entstehung des Stücks, mit denselben
Datierungsformen wie die Erwerbsangabe. Ohne ermittelte Entstehungsdatierung bleiben
`dateOrigin`, `dateOriginPrecision` und `dateOriginLabel` auf `null`, ebenso bei den übrigen
Lanes. `dateOriginEnd` wird nur bei einem vorhandenen Endwert gesetzt. Die Ansicht zeigt den Entstehungstext in den Metadaten; die zeitliche
Einordnung und die Jahresskala verwenden weiterhin den Erwerb aus `date`.

## Datierungsregeln

Die Quellen führen ihre Datierungen in maschinenlesbaren Attributen und, wo diese fehlen,
allein als Anzeigetext. Beide Wege münden in dieselben sechs Werte von `datePrecision`.

Ein `@when` ergibt Tages-, Monats- oder Jahresgenauigkeit nach der Länge des Werts. Ein
Paar aus `@from` und `@to` ergibt `range` mit `date` als Beginn, und ein `@to` neben einem
`@when` wird ebenso als Zeitraum gelesen, weil eine Kopfzeile der Biographie ihren Beginn
so führt. Ein Paar aus `@notBefore` und `@notAfter` ergibt `inferred`, ebenfalls mit `date`
als Beginn. Ein `@type="undated"` an einem Element, das zugleich einen Wert trägt, gilt
nicht als Gegenanzeige; im Korrespondenzindex markiert es Bündel, die neben datierten auch
undatierte Stücke enthalten.

Datierungen, die nur als Text vorliegen, löst ein enger Parser auf, der die in den Quellen
vorkommenden Formen kennt, die deutsche und englische Tagesform, die Monatsform, die
Punktschreibung, die ISO-Schreibung und die nackte Jahreszahl. Zwei oder mehr erkannte
Werte ergeben `range` von der frühesten zur spätesten Angabe. Eckige Klammern und jeder
sonstige Wortlaut neben der Datumsangabe, etwa eine Umstandsangabe oder ein Vorbehalt,
senken die Genauigkeit auf `inferred`. Was der Parser nicht auflöst, bleibt undatiert; für
eine zweistellige Jahresangabe wird kein Jahrhundert ergänzt, und ein Wochentag ohne Datum
wird nicht zu einem Datum.

Aus der Entscheidung vom 11. September 2026 folgt die Arbeitsteilung mit dem Frontend.
Stücke mit reiner Jahresdatierung tragen `year` und werden dort am Jahresanfang gesammelt.
Undatierte Stücke bleiben in der Datei, erscheinen am Ende ihrer Lane und zählen in der
Skala nicht mit.

## Ereignisdatum der Autographen

Die Autographen tragen zwei Datierungen, die Entstehung des Autographs im `summary` und den
Erwerb durch Stefan Zweig im `acquisition`. Die Lane führt den Erwerb, weil der
Lebenskalender die Ereignisse seines Lebens zeigt. Die Erwerbsdaten liegen innerhalb seiner
Sammlertätigkeit, während die Entstehungsdaten bis ins 16. Jahrhundert zurückreichen und
die Skala sprengen würden. Autographen ohne Erwerbsvermerk bleiben mit `undated` in der
Lane.

## Dubletten und Abdeckung der Korrespondenz

Ein Brief an mehrere Empfänger steht im Konvolut-Objekt jedes beteiligten
Korrespondenzpartners. Die PID des Faksimiles ist die Kennung, die diese Ausfertigungen
teilen. Der Lauf führt diese Records zusammen, wenn zusätzlich ihre nichtleere Signatur
übereinstimmt und ihre vorhandenen Datierungen und Orte einander nicht widersprechen.
Fehlende Datierungen oder Orte dürfen durch einen anderen Record derselben Gruppe
vertreten sein. Widersprüche führen zu getrennten Ereignissen und einer Laufmeldung.

Das Hauptereignis übernimmt die Metadaten des zuerst sortierten Records; die Personen
der übrigen Records treten zu seiner Personenliste hinzu. Das optionale Feld `sources`
enthält bei einer Zusammenführung sämtliche ursprünglichen Ereignisobjekte einschließlich
des Haupteintrags, mit ihren eigenen Datierungen, Titeln, Personen und Permalinks.
Die enthaltenen Objekte haben selbst kein Feld `sources`. Dadurch bleiben auch abweichende
Quellangaben und alternative Detailseiten zugänglich. Im aktuellen Bestand ergänzen
zwei Faksimilegruppen undatierte Records durch datierte Records mit dem Ort Salzburg.

Der Korrespondenzindex trägt keine Faksimile-PIDs und nimmt an dieser Zusammenführung
deshalb nicht teil. Seine Einträge und die Einzelbriefe der Konvolute stehen zueinander im
Verhältnis von Bündel und Stück. Archivsignaturen und ihre Präfixe werden jedoch von
verschiedenen Korrespondenzpartnern gemeinsam verwendet und belegen keine vollständige
Abdeckung eines Indexeintrags. Deshalb erhält der Generator sämtliche Indexeinträge.
Mehrere Stücke umfassende Einträge behalten den Bündeltitel der Quelle. Die Ereigniszahl
mischt Katalogebenen und ist keine Zählung physischer Briefe.

Die Prüfung vom 11. September 2026 ergab für die zuvor unterdrückten 180 Indexeinträge,
dass 172 auf ein kuratiertes Konvolutobjekt verweisen, das im lokalen Einzelbriefbestand
fehlt. Drei weitere sind nur teilweise vertreten. Für `SZDKOR.680` stehen fünf Stücke im
Index zwei passenden Records im verlinkten Alfred-Zweig-Objekt gegenüber; für
`SZDKOR.800` sind es 52 gegenüber 19 und für `SZDKOR.840` 28 gegenüber 19.
Fünf Einträge haben je einen passenden Einzelrecord; bei `SZDKOR.858` und `SZDKOR.899`
widersprechen dessen Personenangaben denen des Index. Eine automatische Unterdrückung
wird aus diesen Vergleichen nicht abgeleitet.

Die korrigierte Ausgabe umfasst 765 Indexrecords und 904 Records aus 42 Konvolutdateien.
188 Faksimilegruppen vereinigen 263 zusätzliche Records. Die 1.406 Ereignisse enthalten
somit alle 1.669 Quellenrecords, unmittelbar oder in `sources`. `index.json` hält
`mergedDuplicates` als Zahl der Gruppen, `mergedRecords` als Zahl der zusätzlich
vereinigten Records und das kompatible Feld `suppressedIndexEntries` mit dem numerischen
Wert `0`. Die Quellen bleiben unverändert. Die Datierungen 2012-05-26,
2018-10-02 und 2030-09-23 aus den drei betreffenden `unidentified`-Records werden weiterhin
quellengetreu ausgegeben und bedürfen fachlicher Prüfung.

## Erzeugung und Auslieferung

Erzeugt wird mit

```
python scripts/lebenskalender_lanes/build_lanes.py
```

Die Lane-Dateien und `index.json` landen in `data/derived/lebenskalender/`. Derselbe Lauf
legt eine Kopie nach `docs/lebenskalender/lanes/`, weil GitHub Pages dieses Repo aus dem
Ordner `docs/` des Branches `master` ausliefert und Dateien außerhalb davon dort nicht
erreichbar sind. Eine Kopie und kein Symlink, weil der Prototyp im selben Ordner mit
`SZDBIO.xml` bereits so verfährt und ein Symlink unter Windows und Git unzuverlässig ist.
Ein Build-Schritt kommt nicht in Frage, solange der einzige Workflow des Repos die
Ontologie-Dokumentation erzeugt und die Pages-Auslieferung sonst ohne Build arbeitet.

Die Auslieferung geschieht durch den Push des Maintainers. Solange ein Commit lokal bleibt,
liefert Pages die Datei nicht aus, auch wenn sie unter `docs/` liegt.

Die Lane-Dateien sind über zwei Läufe byteidentisch. Der Erzeugungszeitpunkt liegt allein
im Feld `generated` von `index.json`, damit ein Vergleich ihn ausklammern kann.

Die GAMS-Präsentationsschicht enthält zusätzlich eine Kopie aller vier Lane-Dateien und
der `index.json` unter `ZIMLAB/szd/data/lebenskalender/`. Diese Kopie wird beim Aktualisieren
des Datenstands ausdrücklich nachgeführt; der Generator schreibt sie bislang nicht.
`szd-Lebenskalender.xsl` übergibt dem Client die Assetbasis aus `$server` und `$gamsdev`.
Damit folgen Lane-Dateien und Frontend demselben Staging- und Produktionspfad.

Die fünf am 11. September 2026 übernommenen Dateien wurden byteweise mit
`data/derived/lebenskalender/` verglichen. Der Frontend-Test gegen die lokal gerenderte
GAMS-Seitenhülle verwendet diese Kopien als Fixtures. Er belegt die lokale Integration,
Filterung und Ausgabe in beiden Sprachen. Der Generator besteht elf Korpustests für die
Erhaltung aller Quellenrecords, Konfliktbehandlung und deterministische Ausgabe.
Die Frontendkopien gehören zum gepushten Commit `b616496`; die Staging-Auslieferung
wurde anschließend unabhängig durch Serverabgleich, HTTP- und Browserprüfung bestätigt.
Die auf Nutzerwunsch zurückgestellten Cirilo-Zuordnungen sind in der README des
Frontendrepos `ZIMLAB/szd` kanonisch dokumentiert. Fachliche Freigabe und
Produktionsveröffentlichung stehen aus.

## Related

- [COLLECTIONS.md](COLLECTIONS.md) — Aufbau der Bestände und der Render-Vertrag
- [DATA.md](DATA.md) — Bestandsübersicht und dokumentierte Datenlücken
- [DATA_MODEL.md](DATA_MODEL.md) — Encoding-Muster und bilinguale Architektur
- [scripts/lebenskalender_lanes/README.md](../scripts/lebenskalender_lanes/README.md) — Lauf, Optionen und Prüfung
- [docs/lebenskalender/README.md](../docs/lebenskalender/README.md) — Prototyp der Ansicht im SZD-Design
