---
title: TEI-XML Data Overview
project:
  name: Stefan Zweig Digital, data repository
  repository: https://github.com/chpollin/SZD
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: complete
created: 2025-10-23
updated: 2026-09-24
version: 1.0.0
tags: [data, zweig, tei, statistics]
---

# TEI-XML Data Overview

Coverage of the TEI sources, their documented data gaps and the results of the archive checkups of September 2026. Files, PIDs and encoding of the collections are in [COLLECTIONS.md](COLLECTIONS.md), the open corrections and decisions in the [plan](plan.md).

## Counting conventions

The TEI files are the source of truth for every size figure, so this document keeps none. Counts are taken from the files with these units.

- An entry is a `biblFull` in the collections, an `event` in the biography and a `person` or `org` in the indices.
- The correspondence index `SZDKOR.xml` counts archival bundles. The konvolut files under `data/Correspondence/konvolute/` count individual letters, one `biblFull` per letter with its facsimile PID.
- A date is machine-readable when the `date` element carries `@when`, `@notBefore`, `@notAfter`, `@from` or `@to`.

## Dates

On 29 March 2026 machine-readable date attributes were added systematically to three collections.

| File | Method |
|------|--------|
| `SZDKOR.xml` | `@notBefore`/`@notAfter` for year ranges, `cert="low"` for uncertain dates |
| `SZDBIB.xml` | `@when` for years, `s.d.` skipped |
| `SZDAUT.xml` | `@when` for years, `@notBefore`/`@notAfter` for ranges, mojibake dashes repaired |

Since then the collections carry machine-readable dates almost throughout. The remaining gaps are the `n. d.` entries of `SZDKOR.xml`, the `s.d.` entries (sine dato) of `SZDBIB.xml` and one autograph dated `24. April` without a year. The Works, Essays and Personal Documents date their entries in `history/origin/origDate`, where machine-readable attributes are only partly set and many dates stand as display text alone.

## Correspondence

A correspondence partner can have several signatures, for instance a bundle and single letters, and therefore several index entries. Undated pieces (`n. d.`) can be dated only by archival research. Some TEI signatures have no counterpart in the archive catalogue and need either a new catalogue entry or a mark as uncatalogued.

### Century error in two-digit years

For the picture postcards of the signature group `SZ-SAM/AK` in the konvolut objects, an earlier import expanded the two-digit year of the source (`20. 2. 21`) into the 2000s and set `when="2021-02-20"` instead of `1921-02-20`. The display text of the `date` element and, where present, the date in the former title carry the right value. Where the title proved the year, `@when` has been corrected from it ([scripts/korrespondenz_titel/](../scripts/korrespondenz_titel/README.md)). Where the title carried no date, the error stands and needs an editorial decision. A `@when` after 1942 on a piece with Zweig as sender or recipient is impossible and serves as the search criterion, while the family correspondence of the konvolute reaches beyond 1942. Since the import of all production Konvolute on 24 September 2026 the criterion also finds entries outside `SZ-SAM/AK`, listed in the [plan](plan.md#konvolute).

Related but independent, single entries carry a `date` without `@when`, one with a different granularity between the German and the English version, and some `correspAction` elements name no person. These cases are in the residual list of the title script and are not changed automatically.

## Glossary

In `data/Glossary/szd-Glossary.xml` the German and the English `skos:definition` of two neighbouring SKOS concepts are crossed.

| Concept (`prefLabel`) | German definition describes | English definition describes |
|-----------------------|-----------------------------|------------------------------|
| `Enclosures` (Beilagen) | added by Zweig himself or during his lifetime | added by third parties after his death |
| `AdditionalMaterial` (Zusatzmaterial) | added by third parties after his death | added by Zweig himself or during his lifetime |

The `prefLabel` values are correct in both languages. The German reading is the semantically plausible one (Beilage from Zweig or his lifetime, Zusatzmaterial from third parties or posthumous), and the fix would swap the two English definitions. Which language version is canonical is an editorial decision. The swap was found on 11 June 2026 while checking the SZDLEB display fields against the glossary.

## Personal Documents facsimile checkup (10 September 2026)

An archive-side checkup list against the catalogue view of `o:szd.lebensdokumente` was checked against the TEI source, the facsimile context and the GAMS datastreams.

| Signature | Reported | Finding | Remedy |
|---|---|---|---|
| SZ-AP2/L-S1.1 Adressbuch | viewer broken | `o:szd.174` complete, IIIF manifest invalid because of quotes in a structure label | repaired book source prepared, re-ingest open |
| SZ-AAP/L2 Tagebuch 1914 | viewer broken | `o:szd.67` complete, same manifest defect | same |
| SZ-AAP/L11 Notizbuch Paris 1936 | facsimile link missing | `o:szd.76` exists in the facsimile context, TEI entry SZDLEB.12 had no PID | PID added, index re-ingested on 10 September 2026, link live |
| SZ-AP2/L-S12 Register der Aufsätze | facsimile link missing | `o:szd.175` exists, TEI entry SZDLEB.71 had no PID | PID added, index re-ingested on 10 September 2026, link live |
| SZ-AAP/L2 [Beilage] K. u. k. Kriegsarchiv Offene Order | no facsimile | no facsimile source anywhere, neither in the Tagebuch book structure nor as a `SZ_AAP_L2_Beilage` folder | the archive checks the server files |

A Beilage object follows the Works pattern, a separate object that keeps the main signature in `dc:source` and marks itself with "[Beilage]" in the title (as `o:szd.234` for SZ-AAP/W45), so no new signature suffix is needed. The delivery of the two PIDs was confirmed on 17 September 2026 against the production `TEI_SOURCE` and the rendered catalogue. The manifest defect and the prepared repairs are described in [COLLECTIONS.md](COLLECTIONS.md#iiif-structure-labels-in-book-sources) and [scripts/iiif_structure_labels/](../scripts/iiif_structure_labels/README.md).

## Archive checkup (September 2026)

On 16 September 2026 the archive delivered a defect list for all catalogue views, compiled against the productive instance. The list was verified item by item on 17 September 2026 against the working tree, the productive datastreams and the presentation layer. The verification notes are archive-internal and stay outside the repository.

Almost every reported symptom traces back to one of five causes.

- Aggregate index entries of the SZ-AAL/B ingest (`SZDKOR.928` to `SZDKOR.970`) carried no signature, named Stefan Zweig in a fixed counter-role whether or not a piece involves him, and added the suffix "u. a." or "aus dem Nachlass Stefan Zweigs" to every title. This one generator defect produced the duplicate correspondent headings, the wrong piece counts, the contradictions between overview and entry page and the unjustified "u. a.".
- Catalogue entries referenced a facsimile object that does not exist or belongs to another signature, while the correct object exists and is a member of its facsimile context. The index encoded konvolut PIDs with a slug normalisation that differs from the live objects.
- Straight quotes in structure labels of book sources make the IIIF manifest unparsable.
- Every `author/@ref` in the Aufsatzablage repeated the essay number instead of naming the author. This stayed invisible in the published view because the RDF mapping prefers the GND on the inner `persName`, and misled every script that reads the attribute. Person references written without the fragment marker, and `term[@type='person_affected']` in the Personal Documents, never reached the person view.
- The presentation layer did not handle corporate bodies as correspondents, sorted undated pieces first, and the search query objects did not read the Themen graphs.

Corrected in the working tree, each with a script that logs every change and verifies the written state:

- bundle signatures where the konvolut proves them ([scripts/checkup_2026_09_korrespondenz/](../scripts/checkup_2026_09_korrespondenz/README.md)),
- counter-roles and konvolut pointers in the correspondence index,
- the essay author references, the reference form across all holdings and the duplicate person entries ([scripts/checkup_2026_09_index/](../scripts/checkup_2026_09_index/README.md)),
- the facsimile PIDs of the Works and Aufsatzablage entries the archive reported,
- further prepared IIIF label repairs ([scripts/iiif_structure_labels/](../scripts/iiif_structure_labels/README.md)),
- the evidenced defects of the Konvolut files, once all of them were in the repository ([scripts/checkup_2026_09_konvolute/](../scripts/checkup_2026_09_konvolute/README.md)).

The corporate bodies left the person index for the organisation index ([COLLECTIONS.md](COLLECTIONS.md#organisation-index-szdorg)). The presentation-layer causes were fixed in `ZIMLAB/szd` (frontend commit `8ec067b` and later). None of the data corrections reaches production before the affected index objects, the konvolut files and the prepared book sources are re-ingested. The ingest steps are in the [plan](plan.md#staging-ingest).

### Colour-coded person index list

The archive's list for the person index carries a colour coding that the text export lost. On 23 September 2026 it was read from the Word original, which supersedes the earlier reconstruction from the export. Red marks a duplicate or faulty entry, yellow a person wrongly left unlinked, green a corporate body, and bold a name where the archive asks whether a connection is artificial. The list is archive-internal. What the data settle unambiguously is carried out.

- Kesten (`SZDPER.1935` into `SZDPER.1574`) and Pilnjak (`SZDPER.1099` into `SZDPER.1581`) are merged with `merge_person_duplicates.py` after a check against the German National Library (DNB). GND 1185617155 does not exist, and 1089928157 redirects to 118594397. The Kesten reference in `SZDKOR.xml` carried the non-existent number and now carries 118561715.
- Frenkel (`SZDPER.2299`) is linked in the konvolute `frenkel-lotte` and `zweig-lotte`, Kaufmann (`SZDPER.2296`) in `kaufmann-charlotte` and `zweig-lotte`, Tomaselli (`SZDPER.2212`) in `SZDKOR.xml`, where the reference previously read `gnd/placeholder`. Kaufmann appears as Charlotte in the holdings and as Lotte in the index, and the identification follows the archive's marking.
- Britain in Pictures moved from the person index to the organisation index as `SZDORG.67`, added by hand with the next free number. `migrate_org_references.py` removed `SZDPER.1899`.

### Dead references and unlinked correspondence partners

Four author references in `SZDAUT.xml` carried, beside the valid identifier, a second one that had been removed from the index as a GND duplicate in 2022 (commit `c1a9a34e`), `SZDPER.1579` beside `SZDPER.194` (twice), `SZDPER.1623` beside `SZDPER.1009` and `SZDPER.1617` beside `SZDPER.1588`. The dead identifiers are deleted.

A `persName` without reference is linked only where forename and surname equal an index entry exactly and no other entry carries the same name. This linked seven correspondence partners in the collective line of `SZDKOR.xml` and in their own konvolut, and single pieces in `altmann-eva` and `zweig-lotte`.

[find_unlinked_persons.py](../scripts/checkup_2026_09_index/README.md#find_unlinked_personspy) lists the index persons the person search cannot find and the places in the holdings where they are named without a link. Its output is an archive-internal review list outside the repository.

A person without any reference and without any text hit is certainly unreferenced when, in addition, its identifier occurs nowhere else in the data and the presentation layer, none of its GND numbers occurs outside its own entry, and the person search of production and staging finds nothing (`verify_orphan_persons.py`). On 24 September 2026 `remove_orphan_persons.py` removed the persons that pass all these checks. They are kept unchanged in `scripts/checkup_2026_09_index/removed_persons.xml`, outside `data/` so that no later scan counts them as references, and their identifiers are never assigned again.

## Related

- [COLLECTIONS.md](COLLECTIONS.md), files, PIDs, encoding and rendering contracts
- [Lebenskalender-Lanes.md](Lebenskalender-Lanes.md), derived timeline data, its coverage and delivery
- [plan](plan.md), open corrections, ingest steps and decisions
- [journal](journal.md), work sessions and decisions
