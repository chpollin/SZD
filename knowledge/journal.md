# Journal

Arbeitstagebuch des Datenrepos, ein kurzer Eintrag je substanzieller Session, jüngster
zuerst. Festgehalten wird, was sich geändert hat, was entschieden wurde und was offen
bleibt. Dauerhafte Befunde stehen in den Wissensdokumenten, hier steht der Weg dorthin.

## 2026-09-24 — Land und Ort im Organisationenindex aus der GND ergänzt

Geändert. `scripts/reconcile_org_places.py` ergänzt in `SZDORG.xml` `<country>` und
`<settlement>` aus dem GND-Datensatz jeder Körperschaft, `placeOfBusiness` für den Ort,
`geographicAreaCode` für das Land, nie geschätzt und nie über eine Stufe hinweg
kombiniert. 42 Werte wurden ergänzt, bei 16 der 32 seit der Migration aus dem
Personenindex unvollständigen Einträge beide Felder, bei 10 weiteren nur das Land, weil
der GND-Datensatz keinen Ort führt. Für den GND-Code `XA-GB` folgt das Skript der im
Bestand schon angelegten Trennung, „England" wenn eine Stadt bekannt ist, sonst
„Großbritannien" (SZDORG.32/49 gegen SZDSTA.15), eine aus dem Bestand abgeleitete
Setzung, keine GND-eigene. Fünf Einträge liefern im GND-Datensatz keinen geografischen
Code, drei haben keinen GND-Verweis überhaupt, und bei Herbert Reichner Verlag
(SZDORG.24) bleiben Land und Ort offen, weil der Datensatz Wien, Zürich und Leipzig
gleichrangig führt. Das Log `scripts/organisationen_index/reconcile_places_log.csv`
hält nur tatsächlich geschriebene Werte fest, dazu `scripts/test_reconcile_org_places.py`.

Geprüft. Der bekannte Widerspruch bei SZDORG.15 (David H. Lowenherz, GND zeigt auf
London, der Bestand trägt USA/New York) besteht unverändert und wurde nicht
überschrieben, kein weiterer Widerspruch zwischen Bestand und GND fand sich unter den
Einträgen, die schon Land und Ort trugen. Wohlgeformtheit, unveränderte Zahl der
`<org>`-Einträge, ein rein additiver Diff und ein zweiter, folgenloser Lauf des Skripts
sind geprüft, ebenso `pytest scripts/test_reconcile_org_places.py` und `ruff check`.

Offen. Der Organisationenindex muss nach der Änderung erneut ingestiert werden. 16
Einträge bleiben ohne Ort, sechs davon ganz ohne Land oder Ort, weil ihr GND-Datensatz
dazu nichts hergibt oder mehrdeutig bleibt.

## 2026-09-23 — Prüfliste unverknüpfter Personen, Stagingpaket, Wissensdokumente

Geändert. `scripts/checkup_2026_09_index/find_unlinked_persons.py` (`10728679`) listet die
Indexpersonen, die die Personensuche nicht findet, weil kein Objekt auf sie verweist, und
sucht im Elementtext der Bestände nach Stellen, die sie ohne Verweis nennen, auf Wunsch
auch in den noch nicht ingestierten Konvoluten des Stagingpakets. Die Ausgabe ist eine
archivinterne Prüfliste unter `Documents/PROJECTS/szd/checkup-2026-09/` außerhalb des Repos.

Das Stagingpaket unter `Documents/PROJECTS/szd/ingest_staging_2026-09-23/` steht auf
`aac08670`. Seit den Zusammenführungen des Tages enthält es wieder den Personenindex und
zusätzlich die Konvolute der neu verknüpften Korrespondenzpartner. Die Masereel-Themenseite
ist inzwischen auf Staging, ihr `TEI_SOURCE` dort trägt die getaggten Personenverweise.

Integriert. Die Wissensdokumente sind auf diesen Stand gebracht und entdoppelt, Vorgänger
ist `10728679`. Der Organisationenindex ist in [COLLECTIONS.md](COLLECTIONS.md) beschrieben
statt in DATA.md, Auslieferungsstand und Abdeckung der Lebenskalender-Lanes stehen nur noch
in [Lebenskalender-Lanes.md](Lebenskalender-Lanes.md). [DATA.md](DATA.md) führt statt der
Bestandsstatistik die Zählkonventionen, die heutigen Befunde und die gesammelten offenen
Punkte. Beispiele in COLLECTIONS und DATA_MODEL stammen jetzt aus den Daten, erfundene
Signaturen und Datumsformen sind ersetzt. ARCHITECTURE beschreibt die Zwei-Repo-Topographie
statt allgemeiner Plattformangaben. Die Lizenzangabe in PROJECT folgt dem README (Code MIT),
der Zenodo-Link zeigt auf den öffentlichen Datensatz. Außerhalb des Journals nennt kein
Dokument mehr die Erstveröffentlichungen als Bestand. Auf Wunsch des Operators sind die
bisher deutschen Wissensdokumente und Skript-READMEs ins Englische übertragen, wie
CLAUDE.md es vorsieht, das Journal bleibt deutsch.

Präsentationsschicht. Die Organisationenseite verlinkt jede Körperschaft, Aufbewahrungsorte
auf die Standortsuche und die übrigen auf die Personensuche, und zeigt Ort und Land in der
Kopfzeile (`ZIMLAB/szd` `e7acd7d`).

Offen. Die RDF-Transformation in `ZIMLAB/szd` wird für mehrere Kennungen in einem `@ref`
und für GND-Verweise mit `https` angepasst. Bis dahin liest `GetPersonlist` nur das erste
Token, und ein Körperschaftsverweis löst nur zeichengleich zum Index auf. ONTOLOGY.md und
`ontology/README.md` überarbeitet eine eigene Sitzung mit englischen Bezeichnern, dort fehlt
der Organisationenindex noch in der Zuordnung der TEI-Dateien. Das Wurzeldokument `mail.md`,
ein Mailtext zur SZ-AAL/B-Korrespondenz aus dem Juli 2026, hat im Repo keine Funktion.

## 2026-09-23 — Tote Personenverweise und unverknüpfte Korrespondenzpartner

Geändert. In `SZDAUT.xml` trugen vier Autorverweise neben der gültigen Kennung eine zweite,
die `c1a9a34e` im Jahr 2022 als GND-Dublette aus dem Index entfernt hatte, nämlich
zweimal Michelangelo (1579 neben 194), Joachim Murat (1623 neben 1009) und Gounod (1617 neben 1588).
Die toten Kennungen sind gestrichen. Aus der Kandidatenliste der unverknüpften Personen ist
nur verknüpft, was eindeutig ist, also ein `persName` ohne Verweis, dessen Nach- und Vorname
dem Indexeintrag exakt gleicht, während kein anderer Eintrag denselben Namen führt. Das
trifft die Korrespondenzpartner Kahn, Mayer, Süssland, Birman, Monath, Sambat und Garcés, je
in der Sammelzeile von `SZDKOR.xml` und im eigenen Konvolut, dazu Stücke in `altmann-eva` und
`zweig-lotte`. Die Personen ohne Referenz gehen damit von 354 auf 347 zurück. Birman und
Sambat stehen in Index und Bestand nur mit Initiale, ihre Einträge sind die einzigen dieses
Nachnamens.

Offen. Neydisser (`SZDPER.1026`) ist seit `a108c6f3` vom April 2025 nur noch Namensvariante von
Lernet-Holenia (`SZDPER.818`), die Bibliothek nennt aber die eigene GND des
Pseudonyms. `SZDPER.1304` gab es nie, gemeint ist die Selbsthilfevereinigung der jüdischen
Blinden in Deutschland, eine Körperschaft ohne Eintrag im Organisationenindex. Sieben
Korrespondenzpartner tragen in `SZDKOR.xml` eine GND, die ihrem Indexeintrag fehlt. Beim
Operator liegen außerdem abweichende Vornamen (Altmann, Miller, Bischoff), Nennungen in Titeln
und Fließtext sowie Kuro Masu und Králík, deren Hülle schon auf einen anderen Eintrag zeigt.
Das Prüfskript erkennt Kennungen mit Buchstabensuffix wie `SZDPER.2080a` nicht als Verweis.

## 2026-09-23 — Farbcodierung des Personenindex ausgewertet

Geändert. Die Farbcodierung der Archivliste zum Personenindex ist aus dem Word-Original
gelesen, sie war im Textexport verloren. Daraus ist umgesetzt, was aus den Daten eindeutig
folgt. Kesten und Pilnjak sind nach Prüfung bei der DNB je auf den Eintrag mit gültiger GND
zusammengeführt (`merge_person_duplicates.py`, Protokoll ergänzt), weil 1185617155 nicht
existiert und 1089928157 auf 118594397 umleitet. Die nicht existierende Kesten-GND in
`SZDKOR.xml` ist durch 118561715 ersetzt. Die vom Archiv gelb markierten, fälschlich
unverknüpften Personen Frenkel, Kaufmann und Tomaselli zeigen jetzt in den Konvoluten
`frenkel-lotte`, `kaufmann-charlotte`, `zweig-lotte` und in `SZDKOR.xml` auf ihren
Indexeintrag. Kaufmann steht in den Daten als Charlotte, im Index als Lotte, die
Gleichsetzung folgt der Markierung des Archivs.

„Britain in Pictures“, vom Archiv grün als Körperschaft markiert, ist von Hand als
`SZDORG.67` in den Organisationenindex nachgetragen und über `migrate_org_references.py` aus
dem Personenindex entfernt. Die Zählung läuft weiter statt neu, weil die Kennungen Teil der
RDF-URIs sind. Weil das Skript sein Migrationsprotokoll neu schreibt, sind die älteren
Zeilen aus der Git-Historie wieder vorangestellt.

Die Wissensdokumente sind nachgezogen. [DATA.md](DATA.md) führt die Farbcodierung als
Quelle, die Ergebnisse und die offenen Punkte im Abschnitt zum Archiv-Checkup, die
Aussagen zu Organisationenindex und Personenindex in COLLECTIONS, PROJECT, README und der
README des Organisationsskripts sind auf den Stand gebracht. Der Organisationsabschnitt in
DATA.md beschrieb `GetOrglist` noch als unaufgerufen, das ist seit dem Frontendcommit
`ef9a4ce` überholt.

Offen. Neumann, Schriftsteller oder Architekt, bleibt eine Frage an das Archiv. Beim
Operator liegen die Einträge „Filed as …“, „Unidentified signatures“ und „Zweig Family“,
die fett markierten Namen und die Frage, ob die unverknüpften Namen, die das Archiv
entfernt haben will, den Personenindex verlassen. `SZDKOR.xml` trägt weitere
Personenverweise mit dem Platzhalter `gnd/placeholder`. `SZDSTA.xml` hat seit dem
Datenupdate vom Juni 2021 (`1ed133c2`) keine `geo`-Angaben mehr, das neue RDF der
Standorte hat deshalb keine Koordinaten. `ontology/reconciliation.ttl` für Klawiter beruht
auf Titelabgleich mit Prozentwerten.

Offen und als nächster Schritt geplant ist, auf Anregung des Operators, ein eigenes
Reconciliation-Skript. Es ergänzt Wikidata-Kennungen über die GND, also über Wikidata P227,
und schreibt nur eindeutige Treffer automatisch. Die vorhandenen GNDs prüft es bei DNB oder lobid auf Existenz und
Umleitung und meldet Widersprüche zu Wikidata. Einträge ohne GND bekommen nur eine
Vorschlagsliste, geschriebene Treffer tragen ihre Herkunft, Orte folgen nachrangig. Zum
Stand dieses Tages haben 521 Personen eine GND, aber keine Wikidata-Kennung, 220 Personen
haben keine GND, und keine der 67 Körperschaften trägt eine Wikidata-Kennung. Für
Körperschaften fehlt in `szd-TORDF.xsl` außerdem noch die Ausgabe von `szd:wikidata`.

## 2026-09-23 — Erstveröffentlichungen entfernt, Staging-Ingest vorbereitet

Entschieden. Der Operator hat die Erstveröffentlichungen (SZDPUB) aufgegeben. Beide
Fassungen, `data/Publication/SZDPUB.xml` und `data/Index/Erstveröffentlichungen/SZDPUB.xml`,
sind entfernt und bleiben in der Git-Historie. Sie trugen dieselbe PID `o:szd.publikation`,
wichen inhaltlich voneinander ab und nannten keine Quelle. Produktiv gab es das Objekt nie,
die RDF-Transformation hatte keinen Zweig dafür. Die Verweise in COLLECTIONS, DATA, ONTOLOGY
und PROJECT sind gestrichen. Die Summenzeile der Bestandsstatistik in DATA.md und die
Beschreibung von DATA.md im README enthielten SZDPUB noch und sind am selben Tag
nachgezogen.

Geändert. Der Vergleich auf Elementebene zwischen diesem Repo und `TEI_SOURCE` auf Staging
ergab die Objekte für den nächsten Staging-Ingest, die sechs Bestände, den
Organisationenindex, drei Konvolute und drei neue Konvolute aus der Quellablage. Das Paket mit
Prüfsummen liegt außerhalb des Repos unter `Documents/PROJECTS/szd/ingest_staging_2026-09-23/`.
Personen, Standorte, Werkindex, Lebenskalender und die übrigen Konvolute stimmen mit Staging
überein.

Offen. Auf Staging können `o:szd.publikation` und das verwaiste
`o:szd.korrespondenzen.ferencak-mirko-m` gelöscht werden, dessen einziges Stück das neue
Konvolut `ferencak-mirko` vollständiger führt. Die getaggte Masereel-Themenseite ist noch
nicht auf Staging ingestiert.

## 2026-09-22 — Dublettenpaare des Checkups entschieden

Entschieden. Die Hauptinstanz hat am 22. September 2026 nach Delegation durch den
Operator die vier offenen Dublettenpaare des Checkups entschieden, revidierbar. Für
SZ-SHB/W3 bleibt `o:szd.359`, das byteidentische `o:szd.375` wird gelöscht. Für
SZ-AP2/W-H206 bleibt `o:szd.2939` als Objekt im neueren Aufnahmestandard, `o:szd.263`
wird nach Übernahme von Signatur und Datum entbehrlich. Bei Berger und
Oppeln-Bronikowski bleibt jeweils die Konvolutkennung mit `-von`, auf die der Index
zeigt, und nimmt den kuratierten Inhalt der Schwesterkennung auf.

Geändert. Im Werkindex zeigt SZDMSK.299 auf `o:szd.359` statt auf „Amerigo“
`o:szd.358`, SZDMSK.201 auf `o:szd.2939`. Die zusammengeführten Konvolute liegen wie bei
Ferenčak in der Quellablage außerhalb des Repos, mit Richtung `fromZweig`, Titeln nach der
Titelkonvention und bei Berger mit Signatur SZ-SEF/B1 und Faksimile `o:szd.1384`. Index
und Galerieanker zeigen bereits auf die bleibenden Kennungen.

Offen. Auf GAMS stehen Ingest der beiden Konvolute und des Werkindex, das Löschen von
`o:szd.375`, `o:szd.263` und der beiden Schwesterkonvolute sowie Signatur und Datum in
`o:szd.2939` aus. Das Blatt von SZ-AP2/W-H206 liegt zusätzlich als erste zwei Bilder in
`o:szd.220`.

## 2026-09-18 — Abgelöste Personenkennungen, Checkup-Notizen ausgelagert

Geändert. Die sechzehn Rückverweise des Organisationenindex auf frühere Einträge des
Personenindex tragen `subtype="superseded"`, damit sie von den lebenden Querverweisen
`idno type="SZDSTA"` unterscheidbar sind. `build_org_index.py` schreibt diese Form, die
README des Skriptordners erklärt sie. Die RDF-Transformation der Präsentationsschicht
gibt daraus `dcterms:replaces` auf die alte Personenressource aus.

Entschieden. Die archivinternen Verifikationsnotizen des Checkups vom September 2026
liegen unter `Documents/PROJECTS/szd/checkup-2026-09/` außerhalb des Repos, das Muster
`reports/checkup-*/` ist ignoriert. Das dauerhafte Ergebnis steht in
[DATA.md](DATA.md) im Abschnitt zum Archiv-Checkup.

Geprüft. Personen-, Standort-, Werk- und Organisationenindex sind am selben Tag auf
GAMS Staging ingestiert. Kein Bestand verweist mehr auf eine abgelöste Personenkennung,
das Migrationsprotokoll des Organisationenindex deckt sich mit den Zielen, die das
RDF-Harness der Präsentationsschicht für die Bibliothek auflöst.

Offen. Der Organisationenindex muss nach der Änderung erneut ingestiert werden. Der
Mehrheit der Körperschaften fehlen Land und Ort, weil sie aus dem Personenindex stammen.
Vorgeschlagen und nicht begonnen sind ein Abgleich GND zu Wikidata für Personen mit GND
ohne Wikidata-Kennung und eine Ortsliste mit GeoNames-Kennungen als Vorstufe eines
Orteindex, mit den Autographen als Startbestand. `data/derived/lebenskalender/` ist
untracked, obwohl der Lanes-Vertrag die Dateien dort vorsieht, die ausgelieferte Kopie
unter `docs/lebenskalender/lanes/` ist inhaltsgleich.
