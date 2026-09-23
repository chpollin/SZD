# Journal

Arbeitstagebuch des Datenrepos, ein kurzer Eintrag je substanzieller Session, jüngster
zuerst. Festgehalten wird, was sich geändert hat, was entschieden wurde und was offen
bleibt. Dauerhafte Befunde stehen in den Wissensdokumenten, hier steht der Weg dorthin.

## 2026-09-23 — Tote Personenverweise und unverknüpfte Korrespondenzpartner

Geändert. In `SZDAUT.xml` trugen vier Autorverweise neben der gültigen Kennung eine zweite,
die `c1a9a34e` im Jahr 2022 als GND-Dublette aus dem Index entfernt hatte, nämlich
Michelangelo (1579 neben 194), Joachim Murat (1623 neben 1009) und Gounod (1617 neben 1588).
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
