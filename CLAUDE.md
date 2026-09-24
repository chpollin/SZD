# CLAUDE.md

Arbeitsregeln für Agenten im Datenrepository von Stefan Zweig Digital. Beschreibendes, also Bestände, Encoding, Architektur, Ingest und offene Arbeit, steht in der [README](README.md) und unter `knowledge/`. Hier stehen nur Regeln.

## Zuerst lesen

1. [knowledge/INDEX.md](knowledge/INDEX.md) als Einstieg mit Dokumentliste, Skriptübersicht und Glossar.
2. [knowledge/plan.md](knowledge/plan.md) für die offene technische Arbeit und die offenen Fragen an Operator und Archiv.
3. [knowledge/journal.md](knowledge/journal.md) für Verlauf und Entscheidungsgründe, [knowledge/handoff.md](knowledge/handoff.md) für offene Übergaben aus anderen Sessions.
4. Je nach Aufgabe [COLLECTIONS](knowledge/COLLECTIONS.md) vor jeder Änderung an TEI-Listen und Indizes, [DATA](knowledge/DATA.md) für Datenlücken und Checkup-Ergebnisse, [ARCHITECTURE](knowledge/ARCHITECTURE.md) für Ingest und Veröffentlichung, [ONTOLOGY](knowledge/ONTOLOGY.md) für SZDO.

## Zwei Repositories

- Dieses Repository `chpollin/SZD` hält die TEI-Quellen in `data/`, die Ontologie in `ontology/` und die Skripte in `scripts/`.
- Die Präsentationsschicht mit XSLT, JavaScript, CSS, der RDF-Transformation `szd-TORDF.xsl` und den Query-Vorlagen liegt in `ZIMLAB/szd` (gams-www), lokal unter `GitHub/ZIMLAB/szd`. Arbeit dort folgt deren eigener CLAUDE.md, Befunde für sie gehen in deren Plan oder Handoff.

## Sprache

- Wissensdokumente unter `knowledge/`, README und Skript-READMEs sind Englisch. Deutsche Projektbegriffe bleiben, wo das Glossar in `knowledge/INDEX.md` sie definiert.
- Commit-Messages sind Deutsch.
- Code-Kommentare sind Englisch, knapp und nennen das Warum, das der Code nicht zeigt.
- TEI ist zweisprachig de/en. Bestehende Schreibungen von Normvokabular werden exakt gespiegelt.

## Daten

- Einträge der gruppierten Listen (Werke, Lebensdokumente, Aufsatzablage) folgen dem Render-Vertrag in [COLLECTIONS](knowledge/COLLECTIONS.md#rendering-contract-grouped-lists), weil ein Eintrag ohne Gruppierungsschlüssel ingestiert, aber nirgends gerendert wird. Die Navbar-Kategorien sind ein geschlossenes Set, bestehende Werte von `classification` und `Einheitssachtitel` werden wörtlich wiederverwendet.
- Ein von Zweig verfasster Brief trägt in seiner `<book>`-Quelle den Empfänger als `<contributor>`, sonst fehlt er in der Korrespondenz-Faksimile-Galerie ([COLLECTIONS](knowledge/COLLECTIONS.md#rendering-contract-correspondence-facsimile-gallery)).
- Kennungen von SZDPER, SZDORG und SZDSTA sind Teil der RDF-URIs. Sie werden nie umnummeriert und nie neu vergeben, auch nach dem Entfernen oder Zusammenführen eines Eintrags nicht. Ein neuer Eintrag erhält die nächste freie Nummer.
- Datenänderungen laufen als Skript mit Trockenlauf, einem schreibenden Lauf und, wo vorgesehen, `--verify`. Sie lesen und schreiben über `scripts/_szd_io.py` und protokollieren jede Änderung im CSV-Log neben dem Skript. `_szd_io.py` bleibt in `scripts/`, weil die Skripte es über seinen Pfad laden.
- Werte werden nie geraten. GND, Wikidata, Datum und Ort kommen aus der Quelle, einem Normdatensatz oder einem belegten Befund. Ein mehrdeutiger Fall bleibt unverändert und kommt in den Plan.
- Archivinterne Prüfnotizen, Prüflisten und Operator-Berichte des Checkups liegen unter `Documents/PROJECTS/szd/checkup-2026-09/` außerhalb des Repositories und werden nie committet. Im Repository steht nur das dauerhafte Ergebnis.

## Prüfen

- `python -m pytest -q scripts` läuft vor jedem Commit, der Skripte berührt.
- Jede geschriebene TEI-Datei ist wohlgeformt, bevor sie committet wird.
- Nach Änderungen an `ontology/` läuft `python ontology/validate.py`.
- Ein Umzug eines Skripts zieht jede Referenz nach, in Dokumenten, in Pfaden über `parents[...]` und in Generator-Kommentaren, und das Skript läuft danach.

## Git, Staging und Produktion

- Branch `master`. Vor größerer Arbeit wird `origin` abgeholt und abgeglichen.
- Gestaget werden nur konkrete Pfade, nie `git add -A`, weil parallele Instanzen im selben Working Tree arbeiten.
- Commits entstehen nach jeder abgeschlossenen, geprüften Einheit. Gepusht wird nur auf ausdrückliches Go des Operators.
- Der Staging-Ingest läuft über ein Paket von `scripts/staging_package/build_staging_package.py --out <Ordner außerhalb des Repositories>`. Der Operator spielt es mit Cirilo in der Ordnerreihenfolge ein, Indizes vor Beständen vor Konvoluten.
- Die Verweise `STYLESHEET` und `TORDF` zeigen auf den gamsdev-Spiegel und enden unmittelbar mit `.xsl`. Ein Zeichen danach macht den Verweis unbrauchbar.
- Cirilo-Einstellungen setzt der Operator. Agenten lesen Datenströme nur über die Datenstrom-URLs von Staging und Produktion, nacheinander und mit Pause.
- Der Ingest auf die Produktivinstanz ist eine Publikation und folgt erst der Freigabe durch das Archiv.
