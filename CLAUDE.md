# CLAUDE.md

Arbeitsregeln für Agenten im Datenrepository von Stefan Zweig Digital. Beschreibendes, also Bestände, Encoding, Architektur, Ingest und offene Arbeit, steht in der [README](README.md) und unter `knowledge/`. Hier stehen nur Regeln.

## Zuerst lesen

1. [knowledge/INDEX.md](knowledge/INDEX.md) als Einstieg mit Dokumentliste, Skriptübersicht und Glossar.
2. [knowledge/plan.md](knowledge/plan.md) für die offene technische Arbeit und die offenen Fragen an Operator und Archiv.
3. [knowledge/journal.md](knowledge/journal.md) für Verlauf und Entscheidungsgründe, [knowledge/handoff.md](knowledge/handoff.md) für offene Übergaben aus anderen Sessions.
4. Je nach Aufgabe [collections](knowledge/collections.md) vor jeder Änderung an TEI-Listen und Indizes, [data-quality](knowledge/data-quality.md) für Datenlücken und Checkup-Ergebnisse, [architecture](knowledge/architecture.md) für den Aufbau beider Repositories, [deployment-architecture](knowledge/deployment-architecture.md) für Ingest und Veröffentlichung, [testing](knowledge/testing.md) vor jeder Prüfung, [ontology](knowledge/ontology.md) für SZDO.

## Zwei Repositories

- Dieses Repository `chpollin/SZD` hält die TEI-Quellen in `data/`, die Ontologie in `ontology/`, die Skripte in `scripts/`, das Ingest-Material für Cirilo in `gams/` (Query-Vorlagen und die Ingest-Stylesheets, die GAMS nicht aus gams-www liest), die Testumgebung in `local-test-build/` und das Projektwissen beider Repositories in `knowledge/`.
- Das ZimLab-Repository gams-www (https://zimlab.uni-graz.at/gams/projects/szd/gams-www), lokal unter `GitHub/ZIMLAB/szd`, hält nur, was GAMS ausliefert, die Seiten-Stylesheets, `szd-TORDF.xsl`, `js/`, `css/`, `fonts/`, `icons/`, `img/` und `data/lebenskalender/`. Es hat keine eigene Agentendatei, diese Datei gilt für beide Repositories.

## Präsentationsschicht in gams-www

- Den Stil der geänderten Datei spiegeln, ihre Einrückung, Benennung und Idiome.
- Eine neue Seite ist ein Stylesheet mit `<xsl:include href="szd-static.xsl"/>`, `<xsl:include href="szd-Templates.xsl"/>` und einem Template `content`. Der Seitenrahmen kommt aus `szd-static.xsl` und wird nie neu gebaut. Eine neue PID braucht ihren Zweig in den PID-Fallunterscheidungen von `szd-Templates.xsl`, deren sämtliche Zweige bei einer Änderung im Blick bleiben.
- `$locale` wird durchgereicht. Jeder neue Text existiert deutsch und englisch über `<xsl:choose>` oder einen `<i18n:text>`-Schlüssel, TEI-Inhalt läuft über `printEnDe`, und jeder Link trägt `?locale={$locale}`.
- Projekt-Assets werden unter `$gamsdev` adressiert, Fremdbibliotheken unter `/lib/…` auf dem Server. URLs bleiben hostrelativ.
- Keine neue Fremdbibliothek und kein CSS-Framework. Die vorhandenen werden in der Reihenfolge des Plans entfernt.
- Suchlinks entstehen nur über `fn:query-href` und die Helfer `createPersonSearchHREF`, `LocationSearch` und `WorkSearch` in `szd-Templates.xsl`.
- Namen und Signaturen der globalen JavaScript-Funktionen bleiben, wie sie in der Rendering-Architektur unter `knowledge/` verzeichnet sind.
- Vor einer Änderung die Dublettenliste der Architektur unter „known debt“ prüfen und beide Seiten einer Dublette ändern.
- Eine JavaScript-Datei, die kein Stylesheet einbindet, wird erst geändert oder gelöscht, wenn feststeht, dass kein GAMS-Datenstrom sie nutzt.
- Faksimile-Metadaten und TEI-Quellen bleiben in gams-www unberührt. Datenkorrekturen gehören in dieses Repository.
- Jede Änderung an einem Seiten-Stylesheet, an JavaScript oder an `szd-TORDF.xsl` läuft vor einem Push durch `local-test-build/` mit den Prüfungen, die `knowledge/testing.md` für ihre Art nennt. Ein Fehler im RDF lässt sich erst mit dem nächsten Ingest korrigieren.
- Ein Refactoring ohne Verhaltensänderung wird byteweise mit `node snapshot.mjs --rev HEAD --compare worktree` geprüft.
- Testauswahl nach Änderungsumfang: CSS, JavaScript und Seiten-XSLT mit `npm run test:frontend`, RDF-Erzeugung mit `npm run test:data`, gemeinsame Rendering-Infrastruktur mit `npm test`, Änderungen am Routing mit `npm run test:scope`. Reine Dokumentation braucht kein Rendering, und für eine reine Frontend-Änderung wird kein RDF neu gebaut.
- Die Commit-Message nennt den Testlauf.
- Die letzte Prüfung vor einem Release ist der lokale Build im Browser in beiden Sprachen, nach dem Release `check-instance.py` gegen Produktion und ein Blick auf die geänderten Seiten dort.
- In gams-www wird auf `develop` gearbeitet. `main` trägt den veröffentlichten Stand und wird nie umgeschrieben.
- Push nach `origin` und das Nachziehen des gamsdev-Spiegels nur auf ausdrückliches Go. Der Spiegel wird mit `git fetch` und `git reset --hard origin/develop` nachgezogen und nie bearbeitet.
- Merge nach `main`, Push von `main`, das GAMS-Update der Produktion, jede Cirilo-Einstellung und jeder Ingest liegen beim Operator. Zielwerte stehen in der Deployment-Dokumentation unter `knowledge/` und werden über die Datenstrom-URLs gelesen.
- Alles, was nach `main` gemergt ist, ist unter `https://gams.uni-graz.at/szd/` öffentlich. Dritte stehen mit Rolle und Institution, ohne E-Mail-Adressen, Telefonnummern, Geldbeträge oder Zugangsdaten.

## Sprache

- Wissensdokumente unter `knowledge/`, README und Skript-READMEs sind Englisch. Deutsche Projektbegriffe bleiben, wo das Glossar in `knowledge/INDEX.md` sie definiert.
- Commit-Messages sind in diesem Repository Deutsch, in gams-www Englisch und imperativ.
- Code-Kommentare sind Englisch, knapp und nennen das Warum, das der Code nicht zeigt.
- TEI ist zweisprachig de/en. Bestehende Schreibungen von Normvokabular werden exakt gespiegelt.

## Daten

- Einträge der gruppierten Listen (Werke, Lebensdokumente, Aufsatzablage) folgen dem Render-Vertrag in [collections](knowledge/collections.md#rendering-contract-grouped-lists), weil ein Eintrag ohne Gruppierungsschlüssel ingestiert, aber nirgends gerendert wird. Die Navbar-Kategorien sind ein geschlossenes Set, bestehende Werte von `classification` und `Einheitssachtitel` werden wörtlich wiederverwendet.
- Ein von Zweig verfasster Brief trägt in seiner `<book>`-Quelle den Empfänger als `<contributor>`, sonst fehlt er in der Korrespondenz-Faksimile-Galerie ([collections](knowledge/collections.md#rendering-contract-correspondence-facsimile-gallery)).
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
