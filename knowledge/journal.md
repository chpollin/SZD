# Journal

Arbeitstagebuch des Datenrepos, ein kurzer Eintrag je substanzieller Session, jüngster
zuerst. Festgehalten wird, was sich geändert hat, was entschieden wurde und was offen
bleibt. Dauerhafte Befunde stehen in den Wissensdokumenten, hier steht der Weg dorthin.

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
