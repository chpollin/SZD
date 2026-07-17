# CLAUDE.md — Stefan Zweig Digital (SZD) · Daten-Repo

Arbeitsanleitung für die Zusammenarbeit in diesem Repository.

## Was das ist

Daten- und Preprocessing-Repo für [stefanzweig.digital](https://stefanzweig.digital):
kuratierte **TEI-P5-Quellen** (`data/`), die **Nachlass-Ontologie** (`ontology/`, SZDO)
und die Skripte, die Partner-Lieferungen in TEI überführen. Was nach GAMS ingestiert und
dort gerendert wird, entsteht hier. Die Präsentationsschicht (XSLT/JS/CSS) liegt im
separaten Repo `ZIMLAB/szd` (`gams-www`).

## Zwei-Repo-Topographie

SZD verteilt sich auf zwei getrennte Git-Repos mit klarer Rollenteilung:

- **`chpollin/SZD`** (GitHub) — **Daten + Preprocessing.** Kuratierte TEI-Quellen
  (`data/`), Nachlass-Ontologie, Partner-Lieferungen → TEI. Was ingestiert wird, entsteht
  hier.
- **`ZIMLAB/szd`** = `gams-www` (Asset-Basis im Code: `$gamsdev`) —
  **Präsentationsschicht.** XSLT/JS/CSS, die GAMS rendert.

Datenfluss: TEI in `chpollin/SZD` → Cirilo-Ingest → GAMS (Fedora) → gams-www-XSLT →
[stefanzweig.digital](https://stefanzweig.digital). Die Repos sehen sich nicht automatisch
— Querverweise stehen in beiden CLAUDE.md und im Vault-`Repo-Verzeichnis`.

## Render-Vertrag (vor dem Bearbeiten von Listen-TEI beachten)

Einträge der **gruppierten Listen** (Lebensdokumente `SZDLEB`, Werke `SZDMSK`) erscheinen
im Frontend nur, wenn sie die Gruppierungsschlüssel tragen, die die gams-www-XSLT
(`szd-Werke.xsl`) erwartet:

- `term[@type="classification"]` (de+en) — h2-Navbar-Kategorie,
- `title[@type="Einheitssachtitel"]` (de+en) — h3-Dokumenttyp,
- PID als `msIdentifier/altIdentifier/idno[@type="PID"]` (nicht bare) — sonst kein
  Faksimile-Link.

`for-each-group` wirft schlüssellose Einträge lautlos aus der ganzen Ausgabe —
„ingestiert, aber unsichtbar". Navbar-Kategorien sind ein geschlossenes Set; bestehende
`Einheitssachtitel` exakt (de+en) wiederverwenden. Details:
[knowledge/COLLECTIONS.md](knowledge/COLLECTIONS.md); Renderer-Seite in gams-www
`knowledge/Rendering-and-Search.md`.

**Zweiter Vertrag — Korrespondenz-Faksimile-Galerie**
(`context:szd.facsimiles.korrespondenzen`, `szd-Facsimiles.xsl`): gruppiert nach
Korrespondenzpartner = `dc:creator` (außer exakt `Zweig, Stefan`) ∪ gebundenem
`dc:contributor`. Von Stefan Zweig verfasste Briefe **ohne `dc:contributor`** (Empfänger)
fallen aus der Gruppierung und bleiben unsichtbar. Im `<book>`-Quellformat wird `<author>`
→ dc:creator, `<contributor>` → dc:contributor; der Empfänger muss also als `<contributor>`
gesetzt sein. Die gerenderte `sdef:Context/get`-Seite ist zudem **gecacht** (Membership
via `risearch` ist live). Details: [knowledge/COLLECTIONS.md](knowledge/COLLECTIONS.md).

## Dokumentation zuerst lesen

- [knowledge/PROJECT.md](knowledge/PROJECT.md) — Forschungsprojekt, Kontext, Chronologie.
- [knowledge/COLLECTIONS.md](knowledge/COLLECTIONS.md) — Sammlungen, TEI-Encoding, Render-Vertrag.
- [knowledge/DATA_MODEL.md](knowledge/DATA_MODEL.md) — TEI-Encoding-Muster, bilinguale Architektur.
- [knowledge/ONTOLOGY.md](knowledge/ONTOLOGY.md) — Nachlass-Ontologie (SZDO).
- [knowledge/ARCHITECTURE.md](knowledge/ARCHITECTURE.md) — Systemarchitektur, Datenfluss.
- [knowledge/README.md](knowledge/README.md) — Index aller Wissensdateien.

## Konventionen

- Knowledge-Dokumente in diesem Repo: **Englisch** (bestehende Konvention).
  Commits/Journal/Mails: **Deutsch**. Code-Kommentare: **Englisch**, knapp.
- TEI bilingual de/en; bestehende Schreibung von Normvokabular exakt spiegeln.
- **Kein `git push`** — Push und GAMS-Ingest macht der Maintainer manuell.
