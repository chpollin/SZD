---
title: TEI-XML Data Overview
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD.git
method:
  name: Promptotyping
  url: https://dhcraft.org/promptotyping
status: complete
created: 2025-10-23
updated: 2026-09-23
version: 1.0.0
tags: [data, zweig, tei, statistics]
---

# TEI-XML Data Overview

Bestandsuebersicht der TEI-XML-Sammlungen mit Umfangs- und Datumsstatistiken sowie dokumentierten Datenluecken.

## Collection Statistics (24 Jun 2026)

| Collection | File | Lines | Size | Entries | Dates | Machine-readable |
|------------|------|------:|-----:|--------:|------:|-----------------:|
| Korrespondenz (Index) | `data/Correspondence/SZDKOR.xml` | 39,649 | 1.28 MB | 765 | 760 | 741 (98%) |
| Korrespondenz-Konvolute | `data/Correspondence/konvolute/` (42 Dateien) | 69,461 | 3.0 MB | 904 | 1,720 | 1,629 (95%) |
| Autographen | `data/Autograph/SZDAUT.xml` | 58,718 | 3.1 MB | 997 | 1,250 | 1,248 (100%) |
| Bibliothek | `data/Library/SZDBIB.xml` | 103,319 | 4.2 MB | 1,303 | 1,304 | 1,281 (98%) |
| Aufsaetze | `data/Aufsatzablage/SZDESS.xml` | 56,284 | 2.9 MB | 624 | 1 | 1 (100%) |
| Werke/Manuskripte | `data/Work/SZDMSK.xml` | 33,015 | 2.1 MB | 352 | 1 | 1 (100%) |
| Lebensdokumente | `data/PersonalDocument/SZDLEB.xml` | 13,728 | 711 KB | 156 | 1 | 1 (100%) |
| Biographie | `data/Biography/SZDBIO.xml` | 1,614 | 87 KB | 104 | 208 | 208 (100%) |
| Glossar | `data/Glossary/szd-Glossary.xml` | 442 | 58 KB | -- | 0 | -- |
| **Gesamt** | | **376,230** | **17.4 MB** | **5,205** | **5,245** | **5,110 (97%)** |

**Entries** = `<biblFull>` (Sammlungen), `<event>` (Biographie), oder `<person>` (Index).

**Korrespondenz-Konvolute** = die per-Person-Objekte `o:szd.korrespondenzen.<person>` (zweite Ebene, ein `biblFull` pro Einzelbrief mit Faksimile-PID); der Index SZDKOR aggregiert pro Bündel. Im Juni 2026 um die SZ-AAL/B-Korrespondenz erweitert (42 Konvolute, ~480 Briefe; 30 neu, 12 erweitert). Siehe [COLLECTIONS.md](COLLECTIONS.md) und [DATA_MODEL.md](DATA_MODEL.md).
**Machine-readable** = `<date>` mit `@when`, `@notBefore`, `@notAfter`, `@from`, oder `@to`.

### Index-Dateien (nicht in Tabelle)

| File | Lines | Purpose |
|------|------:|---------|
| `data/Index/Person/SZDPER.xml` | 21,814 | Personen-Normdaten (GND, Wikidata, VIAF) |
| `data/Index/SZDWRK.xml` | 5,422 | Werkindex (WEMI-Ebene) |
| `data/Index/Location/SZDSTA.xml` | 303 | Standorte/Aufbewahrungsorte |
| `data/Issue/szd-thema*.xml` (7 Dateien) | ~4,593 | Thematische Sammlungen |
| `data/Index/Organisation/SZDORG.xml` | 433 | Koerperschaften (GND), seit 18. Sep 2026 auf Staging |

### Organisationenindex SZDORG

`data/Index/Organisation/SZDORG.xml` fuehrt die Koerperschaften des Nachlasses als
`listOrg/org` mit `orgName/@ref` auf die GND, in der Bauform von
[`SZDSTA.xml`](../data/Index/Location/SZDSTA.xml). Zweck ist die Aufloesung der
Koerperschaftsverweise, die der Bestand schon traegt. Verlage, Banken, Behoerden,
Zeitungen und Vereine standen bisher teils als `person` im Personenindex, teils nur als
`orgName/@ref` in den Sammlungen, ohne eigene Normdatenliste.

Die Datei traegt die PID `o:szd.organisation`. `o:szd.standorte` bleibt daneben bestehen
und bleibt die kuratierte Sicht auf die Aufbewahrungsorte, `o:szd.organisation` fuehrt alle
Koerperschaften einschliesslich dieser Aufbewahrungsorte. Nicht aufgenommen sind die
SZDSTA-Eintraege, die zwar Material verwahren, aber keine Koerperschaft benennen, also die
Privatbesitz-Eintraege und die Erbengemeinschaft. Sie bleiben im Standortindex, und die
Verweise des Bestands auf sie zeigen weiter auf `o:szd.standorte`.

`szd-TORDF.xsl` im Repo `ZIMLAB/szd` laedt das Objekt in die Variable `$OrganisationList`
und loest dort `t:org[t:orgName[@ref = …]]` zu einer internen `SZDORG`-Kennung auf. Die
`@ref`-Schreibung `http://d-nb.info/gnd/<Nummer>` muss deshalb zeichengleich zu der im
Bestand sein. Das `document()` steht in einer globalen Variablen, ein Fehlen des Objekts
auf einer Instanz wirkt also auf die ganze Transformation, nicht nur auf die
Koerperschaften. Seit dem Frontendcommit `ef9a4ce` vom 20. September 2026 rufen die
Bestandszweige das Template `GetOrglist` auf, das die Aufloesung leistet und auf
`o:szd.organisation` zielt. Der Zweig fuer das Objekt selbst gibt Name, GND, Ort, Land und
die Rueckverweise aus, aber noch kein `szd:wikidata`, und der Index traegt bisher auch keine
Wikidata-Kennungen.

Jeder Eintrag traegt `idno type="SZDPER"` auf den Personenindex-Eintrag, aus dem er stammt,
und `idno type="SZDSTA"` auf den Standortindex, wo die Koerperschaft dort bereits steht.
Wo zwei Personeneintraege dieselbe Koerperschaft unter verschiedenen Namen fuehrten, stehen
beide Rueckverweise im selben Eintrag und der zweite Name als `orgName type="variant"`.

### Koerperschaften aus SZDPER heraus

Die als Koerperschaft entschiedenen Eintraege sind aus `SZDPER.xml` entfernt, und die
Verweise des Bestands auf ihre Kennungen zeigen auf den Organisationenindex. Die
Verweisform folgt der, die der Bestand fuer Koerperschaften schon verwendet, also `orgName`
mit `@ref` auf die GND, wo eine GND vorliegt, und sonst mit `@ref` auf
`https://gams.uni-graz.at/o:szd.organisation#SZDORG.<n>`, gebaut wie der bestehende
Standortverweis `https://gams.uni-graz.at/o:szd.standorte#SZDSTA.<n>`. Das `@ref` des
umgebenden `author`- oder `editor`-Elements wird mit umgestellt und nicht gestrichen, weil
`szd-Bibliothek.xsl` die Bibliotheksliste ueber dieses Attribut gruppiert und sortiert.

Erzeugt und reproduzierbar aus den Quellen mit
`scripts/organisationen_index/build_org_index.py`, die Umstellung mit
`scripts/organisationen_index/migrate_org_references.py`. Nach dem Migrationslauf ist der
Index nicht mehr aus den Quellen erzeugbar und wird von Hand gepflegt. Das Bauskript bricht
in diesem Fall ab, statt einen verkuerzten Index zu schreiben. Eine neue Koerperschaft
erhaelt die naechste freie `SZDORG`-Nummer, weil die Kennungen Teil der RDF-URIs sind und
stehen bleiben. Kommt sie aus dem Personenindex, stellt `migrate_org_references.py` die
Verweise um, das Verfahren beschreibt die README des Skriptordners. Die offenen Befunde in
den Quelldaten, eine GND mit zwei Koerperschaften und eine Personen-GND an einem `orgName`,
stehen in der README des Skriptordners.

Beim Ingest gehen `o:szd.personen` und `o:szd.organisation` den Bestaenden voraus, weil
TORDF die Verweise zur Ingest-Zeit gegen diese Objekte aufloest.

---

## Date Normalization History

Maschinenlesbare Datumsattribute wurden am 29. Maerz 2026 systematisch nachgetragen:

| Datei | Vorher | Nachher | Methode |
|-------|-------:|--------:|---------|
| SZDKOR.xml | 60% | 97% | `@notBefore`/`@notAfter` fuer Jahresbereiche; `cert="low"` fuer unsichere Daten |
| SZDBIB.xml | 2% | 98% | `@when` fuer Jahresangaben; `s.d.` uebersprungen |
| SZDAUT.xml | 58% | 100% | `@when` fuer Jahre; `@notBefore`/`@notAfter` fuer Bereiche; Mojibake-Dashes repariert |

**Verbleibende Luecken:**
- 19 `n. d.`-Eintraege in SZDKOR (kein Datum verfuegbar)
- 19 `s.d.`-Eintraege in SZDBIB (sine dato)
- 1 unvollstaendiges Datum in SZDAUT (`24. April` ohne Jahr)

---

## Glossar -- Datenqualitaet

### DE/EN-Definitionen vertauscht (Beilagen vs. Zusatzmaterial)

Im Glossar (`data/Glossary/szd-Glossary.xml`) widersprechen sich bei zwei benachbarten SKOS-Konzepten die deutsche und die englische `skos:definition` -- die Definitionstexte sind ueberkreuz vergeben:

| Konzept (`prefLabel`) | DE-Definition beschreibt | EN-Definition beschreibt |
|-----------------------|--------------------------|--------------------------|
| `Enclosures` (Beilagen) | von Zweig selbst / zu Lebzeiten beigelegt | von Dritten / nach seinem Tod hinzugefuegt |
| `AdditionalMaterial` (Zusatzmaterial) | von Dritten / nach seinem Tod hinzugefuegt | von Zweig selbst / zu Lebzeiten |

Die `prefLabel` (DE/EN) sind in beiden Faellen korrekt; nur die Definitionstexte stehen ueber Kreuz. Innerhalb jedes Konzepts widersprechen sich DE und EN, ueber beide Konzepte hinweg passen sie kreuzweise zusammen. Die semantisch plausible Lesart ist die deutsche (Beilage = von Zweig/zu Lebzeiten, Zusatzmaterial = von Dritten/posthum); welche Sprachfassung kanonisch ist, muss aber redaktionell entschieden werden. **Fix:** die beiden englischen `skos:definition` gegeneinander tauschen.

_Gefunden 11. Juni 2026 beim Abgleich der SZDLEB-Anzeigefelder gegen das Glossar._

---

## Korrespondenz-Details

### Struktur

```
<TEI>
 +-- text
     +-- listBibl
         +-- biblFull*
             +-- idno type="signature"  ->  SZ-...
```

Ein Korrespondenzpartner kann **mehrere Signaturen** haben (z.B. ein Konvolut plus Einzelbriefe).

### Offene Datenluecken

| Issue | Count | Remedy |
|-------|------:|--------|
| `n. d.` Daten (kein Datum vorhanden) | 19 | Nur durch Archivrecherche loesbar |
| TEI-Signaturen ohne Katalog-Zuordnung | ~130 | Neue Katalogeintraege oder Markierung als unkatalogisiert |

### Jahrhundertfehler bei zweistelligen Jahresangaben

Bei den Ansichtskarten der Signaturgruppe `SZ-SAM/AK` in den Konvolut-Objekten hat ein
frueherer Import die zweistellige Jahresangabe der Quelle (`20. 2. 21`) in die 2000er
expandiert, also `when="2021-02-20"` statt `1921-02-20` gesetzt. Der Anzeigetext des
`date`-Elements und, wo vorhanden, das Datum im damaligen Titel tragen den richtigen Wert.
Wo der Titel das Jahr belegte, ist `@when` daraus korrigiert worden
(`scripts/korrespondenz_titel/`); wo der Titel kein Datum trug, bleibt der Fehler stehen
und ist nur redaktionell zu entscheiden. Merkmal fuer die Suche: ein `@when` nach 1942 an
einem Stueck mit Stefan Zweig als Sender oder Empfaenger ist unmoeglich, weil er 1942
gestorben ist; die Familienkorrespondenz der Konvolute reicht dagegen ueber 1942 hinaus.

Verwandt, aber davon unabhaengig: einzelne Eintraege tragen ein `date` ohne `@when`, eines
mit abweichender Granularitaet zwischen der deutschen und der englischen Fassung, und
einzelne `correspAction` ohne Personennamen. Diese Faelle stehen in der Restliste des
Skripts und werden nicht automatisch geaendert.

## Lebensdokumente facsimile checkup (10 Sep 2026)

Archive-side checkup list against the catalogue view of `o:szd.lebensdokumente`, checked
against the TEI source, the facsimile context and the GAMS datastreams:

| Signature | Reported | Finding | Remedy |
|---|---|---|---|
| SZ-AP2/L-S1.1 Adressbuch | viewer broken | `o:szd.174` complete (122 images); IIIF manifest invalid because of quotes in a structure label | fix label in the book source, re-ingest; see COLLECTIONS.md |
| SZ-AAP/L2 Tagebuch 1914 | viewer broken | `o:szd.67` complete (237 images); same manifest defect | same |
| SZ-AAP/L11 Notizbuch Paris 1936 | facsimile link missing | `o:szd.76` exists in the facsimile context, TEI entry SZDLEB.12 had no PID | PID added in `data/PersonalDocument/SZDLEB.xml`, index re-ingested on 10 September 2026, link live |
| SZ-AP2/L-S12 Register der Aufsätze | facsimile link missing | `o:szd.175` exists, TEI entry SZDLEB.71 had no PID | PID added, index re-ingested on 10 September 2026, link live |
| SZ-AAP/L2 [Beilage] K. u. k. Kriegsarchiv Offene Order | no facsimile | no facsimile source anywhere: not in the Tagebuch book structure, no `SZ_AAP_L2_Beilage` folder | archive checks the server files. A Beilage object follows the Werke pattern, a separate object that keeps the main signature in `dc:source` and marks itself with "[Beilage]" in the title (as `o:szd.234` for SZ-AAP/W45), so no new signature suffix is needed |

The local TEI matched the GAMS `TEI_SOURCE` entry for entry before the two PID additions.
The delivery of the two PIDs was confirmed on 17 September 2026 against the production
`TEI_SOURCE` and the rendered catalogue.

On 11 September 2026, repaired book sources were prepared for `o:szd.174`, `o:szd.67`
and `o:szd.314`. The last object belongs to the works collection and has four affected
structure labels. These prepared copies have not been ingested. Their checksums and
the recorded XML and manifest checks are maintained in
[the IIIF repair documentation](../scripts/iiif_structure_labels/README.md).

## Derived Lebenskalender data (11 Sep 2026)

The corrected generator output contains 2,663 events across biography, correspondence,
personal documents and autograph acquisitions. Four lane files and `index.json` are
present in `data/derived/lebenskalender/` and `docs/lebenskalender/lanes/`; identical
copies are included in frontend commit `b616496`, pushed to `ZIMLAB/szd`.
The correspondence lane contains 1,406 events representing all 765 index records and
904 records from 42 konvolut files. The former suppression of 180 index records has
been removed. Merging 188 compatible facsimile groups folds 263 additional records
into events whose `sources` preserve the original metadata and permalinks.
Eleven corpus tests verify source coverage, conflict handling and deterministic output.

The source dates 2012-05-26, 2018-10-02 and 2030-09-23 remain unchanged and require
scholarly review. The event schema, dating rules and coverage evidence are documented
in [Lebenskalender-Lanes.md](Lebenskalender-Lanes.md). Staging delivery was confirmed
with a clean server mirror at `b616496` and identical HTTP-delivered JSON content.
Production publication, partner review and acceptance remain open
after the message sent to Salzburg on 11 September 2026.

## Archive checkup (September 2026)

On 16 September 2026 the archive delivered a defect list for all catalogue views, compiled
against the productive instance. The list was verified item by item on 17 September 2026
against the working tree, the productive datastreams and the presentation layer. The
verification notes are archive-internal and stay outside the repository; what follows is
the durable result.

Almost every reported symptom traces back to one of five causes.

- Aggregate index entries of the SZ-AAL/B ingest (`SZDKOR.928` to `SZDKOR.970`) carry no
  signature, name Stefan Zweig in a fixed counter-role whether or not a piece involves him,
  and add the suffix "u. a." or "aus dem Nachlass Stefan Zweigs" to every title. This one
  generator defect produces the duplicate correspondent headings, the wrong piece counts,
  the contradictions between overview and entry page, and the unjustified "u. a.".
- Catalogue entries reference a facsimile object that does not exist or belongs to another
  signature, while the correct object exists and is a member of its facsimile context. The
  index encodes konvolut PIDs with a slug normalisation that differs from the live objects.
- Straight quotes in structure labels of book sources make the IIIF manifest unparsable, so
  the viewer stays empty although every image is intact.
- Every `author/@ref` in the Aufsatzablage repeated the essay number instead of naming the
  author, invisible in the published view because the RDF mapping prefers the GND on the
  inner `persName`, but misleading for every script that reads the attribute. Person
  references written without the fragment marker, and `term[@type='person_affected']` in
  the personal documents, never reached the person view.
- The presentation layer does not handle corporate bodies as correspondents, sorts undated
  pieces first, and the search query objects do not read the Themen graphs.

Corrected in the working tree, each with a script that logs every change and verifies the
written state: bundle signatures where the konvolut proves them
(`scripts/checkup_2026_09_korrespondenz/`), counter-roles and konvolut pointers in the
correspondence index, the essay author references, the reference form across all holdings,
eleven duplicate person entries, the facsimile PIDs of the Werke and Aufsatzablage entries
the archive reported, and four further prepared IIIF label repairs
(`scripts/checkup_2026_09_index/`, `scripts/iiif_structure_labels/`). None of it reaches
production before the affected index objects, the konvolut files and the prepared book
sources are re-ingested.

The archive's list for the person index carries a colour coding that the text export lost.
On 23 September 2026 it was read from the Word original, which supersedes the earlier
reconstruction from the export. Red marks a duplicate or faulty entry, yellow a person
wrongly left unlinked, green a corporate body, and bold a name where the archive asks
whether a connection is artificial. The list itself is archive-internal and stays outside
the repository. What the data settle unambiguously is carried out.

- Kesten (`SZDPER.1935` into `SZDPER.1574`) and Pilnjak (`SZDPER.1099` into
  `SZDPER.1581`) are merged with `scripts/checkup_2026_09_index/merge_person_duplicates.py`
  after a check against the German National Library (DNB). GND 1185617155 does not exist,
  and 1089928157 redirects to 118594397. The Kesten reference in `SZDKOR.xml` carried the
  non-existent number and now carries 118561715.
- Frenkel (`SZDPER.2299`) is linked in the konvolute `frenkel-lotte` and `zweig-lotte`,
  Kaufmann (`SZDPER.2296`) in `kaufmann-charlotte` and `zweig-lotte`, Tomaselli
  (`SZDPER.2212`) in `SZDKOR.xml`, where the reference previously read `gnd/placeholder`.
  Kaufmann appears as Charlotte in the holdings and as Lotte in the index. The
  identification follows the archive's marking.
- Britain in Pictures moved from the person index to the organisation index as
  `SZDORG.67`, added by hand with the next free number, since the identifiers are part of
  the RDF URIs. `migrate_org_references.py` removed `SZDPER.1899`. Its migration log is
  rewritten on each run, so the earlier rows were restored from the Git history.

Not decidable from data or code, and therefore still open:

- The editorial rulings on whether an index entry counts an archival bundle or a
  correspondence relationship, on the meaning of bracketed title dates, on one notation for
  unidentified senders, on the Aufsatzablage classification vocabulary and on the person
  markup convention for Themen pages.
- The archive questions on missing scans, on dates the originals must supply, and on
  whether the index entry for Neumann means the writer or the architect of that name.
- The operator decisions on the colour-coded list, namely the person index entries
  "Filed as …", "Unidentified signatures" and "Zweig Family", the names marked bold, and
  whether the unlinked names the archive wants removed leave the person index.
- Further person references in `SZDKOR.xml` that carry `gnd/placeholder`.
- The missing coordinates of the locations. `SZDSTA.xml` has had no `geo` elements since
  the data update of June 2021, so the location RDF carries none.
- The Klawiter reconciliation. `ontology/reconciliation.ttl` links Klawiter entries to
  works by exact, normalised and fuzzy title matching with a percentage confidence, not by
  authority numbers.

---

_Statistics retain their stated collection dates; project-specific findings updated 23 Sep 2026._
