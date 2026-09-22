# Journal

Arbeitstagebuch des Datenrepos, ein kurzer Eintrag je substanzieller Session, jüngster
zuerst. Festgehalten wird, was sich geändert hat, was entschieden wurde und was offen
bleibt. Dauerhafte Befunde stehen in den Wissensdokumenten, hier steht der Weg dorthin.

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
