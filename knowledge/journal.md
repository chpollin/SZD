---
title: Journal
project:
  name: Stefan Zweig Digital, data repository
  repository: https://github.com/chpollin/SZD
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: active
created: 2026-09-18
updated: 2026-09-24
---

# Journal

Work diary of the data repository, one short entry per substantive session, newest first. It records what changed, what was decided and what stayed open at the time. Durable findings stand in the documents listed in the [index](INDEX.md), current open work in the [plan](plan.md). The entries up to the organisation places of 2026-09-24 were written in German and translated on 2026-09-24, and Git keeps their wording.

## 2026-09-24, staging ingest of the data package

Checked. The operator ingested the whole package on staging, and Cirilo created the Konvolute missing there. Indexes and Konvolute on staging match the repository in content, the person index without the removed persons and the organisation index with places and "Großbritannien". The RDF of the holdings still lacks the corporate bodies, because they went in before the organisation fallback of `szd-TORDF.xsl` reached the mirror, and many objects carry `TORDF` references that end in an illegal character. The package README now lists the references per object, treats the include stylesheets of the registers as valid and leaves the Cirilo log in the package folder alone when the package is rebuilt (`faeda672`). The renewed ingest is in the [plan](plan.md#staging-ingest).

## 2026-09-24, timeline lanes on the complete Konvolute

Changed. `build_lanes.py` ran on the complete Konvolute, and the corpus tests pin the new state with values read from the run. Correspondence events from the index carry three new fields, `konvolut` with the detail page of the named Konvolut where its file exists, `repository` for bundles held outside the Literaturarchiv Salzburg and `extent` with the pieces per direction ([Lebenskalender-Lanes](Lebenskalender-Lanes.md#event-schema)). `extent` is a list, because some bundles carry a measure for letters sent and one for letters received. Event ids are unique across all lanes, because several Konvolut files reuse the `xml:id` values of another Konvolut and the view uses ids as DOM ids and fragments. Such an id carries the file slug after a tilde in every occurrence, unique ids stay unchanged. The `href` of a Konvolut record takes its PID from the file name, so the defective Jugendverein and Rascher objects link to the objects GAMS holds. The lane files went to `docs/lebenskalender/lanes/` and to `ZIMLAB/szd/data/lebenskalender/`.

Open. The conflicting facsimile groups, the Konvolut files with shared ids, the two index entries whose Konvolut PID has no file and the Konvolut dates after 1950 are in the [plan](plan.md#timeline-lanes).

## 2026-09-24, complete Konvolute, person index clean-up, staging package

Changed.

- Every correspondence Konvolut of GAMS production is in `data/Correspondence/konvolute/` (`e1b156fa`), taken over byte for byte from `TEI_SOURCE` by `scripts/konvolute_import/fetch_konvolute.py`, and the three new Konvolute of the staging package of 2026-09-23 from that package. Before, the repository held only the Konvolute edited here. Three defective production objects are recorded in the import README.
- 41 corrections of the Konvolut files that the archive checkup reported and that the verification notes or the facsimile objects on GAMS prove (`2d085b98`, `scripts/checkup_2026_09_konvolute/`), among them wrong and missing facsimile PIDs, the `correspDesc/@type` of the Freud letters, title dates and a duplicate entry in the Hirschfeld Konvolut. Cases without an established value stay unchanged.
- Person index. `verify_orphan_persons.py` (`81a56e58`) takes the persons without text hit from `find_unlinked_persons.py` and checks identifier, GND and the person search on production and staging. `remove_orphan_persons.py` (`f2bb270c`) removed the 230 persons that pass every check. The removed entries stay unchanged in `scripts/checkup_2026_09_index/removed_persons.xml`, and their identifiers are never assigned again.
- Organisation index with country and place from the GND (`82da76ee`, entry below). Afterwards "England" became "Großbritannien" in the organisation and the location index (`c63379f6`), because the country switch of the index pages showed two groups for one country, and the script writes "Großbritannien" for `XA-GB` throughout.
- `scripts/staging_package/build_staging_package.py` (`0b1328e7`) writes the staging ingest package outside the repository, in the order indexes, holdings, Konvolute, with checksums and the `STYLESHEET` and `TORDF` references each object still needs, read live from staging. A Konvolut whose file does not name its own PID stays out.
- SZDO 2.0.0 with English identifiers (`8f54aeed`, entry below).
- Documentation refactored after the model of the frontend knowledge base. `knowledge/README.md` became the [index](INDEX.md) with a glossary, the [plan](plan.md) and the [handoff](handoff.md) inbox are new, the journal is English throughout, the open lists of DATA.md and of the journal moved into the plan, and CLAUDE.md became a compact rules file. `reconcile_org_places.py` and its test moved into `scripts/organisationen_index/`.

Found. The import brought back the sister Konvolute decided for deletion on 2026-09-22 and 2026-09-23, and several imported Konvolute carry dates after 1950. Four corpus tests of the timeline lanes pin the corpus before the import and fail since `e1b156fa`. All three are in the plan.

Presentation layer. `szd-TORDF.xsl` read the autograph classification with the absolute path `//t:textClass` and is being fixed in `ZIMLAB/szd` the same day. `o:szd.autographen` needs a renewed ingest afterwards.

## 2026-09-24, SZDO 2.0.0 with English identifiers

Changed. The ontology uses English identifiers only, as the operator decided on
2026-09-23 and 2026-09-24. `szdo:` moves to 2.0.0 and `nachlass:` to 0.2.0. Wherever the
GAMS vocabulary of `szd-TORDF.xsl` already has an English term with the same meaning,
that term is canonical, so live GAMS data conforms unchanged. Shapes, sample instances,
Klawiter links, the documentation site and both generating scripts use the new names.
`ontology/migration-v2.csv` maps every retired identifier to its successor.

Decided. The German v1.2.0 identifiers are dropped without deprecated aliases, because
aliases would keep German identifiers in the ontology and no live data uses v1.x. The
missing shelfmark on a record became a SHACL warning, since privately held books have
inventory numbers only.

Found and fixed. Sample instances and Klawiter links wrote entry IRIs as prefixed names
with `#`, which Turtle reads as a comment, so every entry collapsed onto its collection
node and the instance shapes never fired. Both scripts now write full IRIs, the instance
generator reads the untyped shelfmark of SZDBIB and the GND-referenced correspondents of
SZDKOR, and `validate.py` now validates the sample instances with SHACL and fails on any
retired identifier. `reconciliation.ttl` was regenerated from the stored results, which
also applies the script's `isSubjectOf` for secondary literature.

Open. `szd:glossar`, the hybrid `szd:objecttyp` and the glossary concepts of
`szdg:DatumEvidenz` keep German-derived identifiers, because they belong to the live GAMS
vocabulary and glossary. The namespace `https://w3id.org/nachlass#` keeps its name.

## 2026-09-24, country and place in the organisation index from the GND

Changed. `scripts/reconcile_org_places.py` adds `<country>` and `<settlement>` to `SZDORG.xml` from the GND record of each corporate body, `placeOfBusiness` for the place and `geographicAreaCode` for the country, never estimated and never combined across levels. 42 values were added, both fields for 16 of the 32 entries that had been incomplete since the migration from the person index, and the country alone for 10 more, because their GND record names no place. For the GND code `XA-GB` the script followed the split already present in the data, "England" where a city is known and "Großbritannien" otherwise (SZDORG.32/49 against SZDSTA.15), a setting the script derived from the data. Five entries give no geographic code in their GND record, three have no GND reference at all, and for Herbert Reichner Verlag (SZDORG.24) country and place stay open, because the record lists Wien, Zürich and Leipzig with equal rank. The log `scripts/organisationen_index/reconcile_places_log.csv` records only values actually written, and `scripts/test_reconcile_org_places.py` accompanies the script.

Checked. The known contradiction at SZDORG.15 (David H. Lowenherz, the GND points to London, the data carry USA/New York) is unchanged and was not overwritten. No further contradiction between data and GND turned up among the entries that already carried country and place. Well-formedness, an unchanged number of `<org>` entries, a purely additive diff and a second run without effect are checked, as are `pytest scripts/test_reconcile_org_places.py` and `ruff check`.

Open. The organisation index must be ingested again after the change. 16 entries stay without place, six of them without country or place, because their GND record gives nothing or stays ambiguous.

## 2026-09-23, review list of unlinked persons, staging package, knowledge documents

Changed. `scripts/checkup_2026_09_index/find_unlinked_persons.py` (`10728679`) lists the index persons the person search does not find because no object references them, and searches the element text of the holdings for places that name them without a reference, on request also in the Konvolute of the staging package not yet ingested. The output is an archive-internal review list under `Documents/PROJECTS/szd/checkup-2026-09/` outside the repository.

The staging package under `Documents/PROJECTS/szd/ingest_staging_2026-09-23/` stands at `aac08670`. Since the merges of the day it again contains the person index and in addition the Konvolute of the newly linked correspondence partners. The Masereel theme page is now on staging, and its `TEI_SOURCE` there carries the tagged person references.

Integrated. The knowledge documents are brought to this state and deduplicated, with `10728679` as predecessor. The organisation index is described in [COLLECTIONS.md](COLLECTIONS.md) instead of DATA.md, and delivery state and coverage of the Lebenskalender lanes stand only in [Lebenskalender-Lanes.md](Lebenskalender-Lanes.md). [DATA.md](DATA.md) carries the counting conventions, the findings of the day and the collected open points instead of the collection statistics. Examples in COLLECTIONS and DATA_MODEL now come from the data, and invented signatures and date forms are replaced. ARCHITECTURE describes the two-repository topography instead of general platform details. The licence statement in PROJECT follows the README (code MIT), and the Zenodo link points to the public record. Outside the journal no document names the first editions as a collection any more. At the operator's request the knowledge documents and script READMEs that had been German were translated into English, as CLAUDE.md provides, while the journal stayed German.

Presentation layer. The organisation page links every corporate body, repositories to the location search and the others to the person search, and shows place and country in the heading line (`ZIMLAB/szd` `e7acd7d`).

Open. The RDF transformation in `ZIMLAB/szd` is being adapted for several identifiers in one `@ref` and for GND references with `https`. Until then `GetPersonlist` reads only the first token, and a corporate-body reference resolves only if it matches the index character for character. ONTOLOGY.md and `ontology/README.md` are revised in a separate session with English identifiers, and there the organisation index is still missing from the mapping of the TEI files. The root document `mail.md`, a mail text on the SZ-AAL/B correspondence from July 2026, has no function in the repository.

## 2026-09-23, dead person references and unlinked correspondence partners

Changed. In `SZDAUT.xml` four author references carried, beside the valid identifier, a second one that `c1a9a34e` had removed from the index as a GND duplicate in 2022, namely Michelangelo twice (1579 beside 194), Joachim Murat (1623 beside 1009) and Gounod (1617 beside 1588). The dead identifiers are deleted. From the candidate list of unlinked persons only the unambiguous cases are linked, meaning a `persName` without reference whose surname and forename equal the index entry exactly while no other entry carries the same name. This applies to the correspondence partners Kahn, Mayer, Süssland, Birman, Monath, Sambat and Garcés, each in the collective line of `SZDKOR.xml` and in their own Konvolut, plus pieces in `altmann-eva` and `zweig-lotte`. The persons without reference thereby go down from 354 to 347. Birman and Sambat stand in index and holdings with an initial only, and their entries are the only ones of that surname.

Open. Neydisser (`SZDPER.1026`) has been only a name variant of Lernet-Holenia (`SZDPER.818`) since `a108c6f3` of April 2025, but the library names the pseudonym's own GND. `SZDPER.1304` never existed, and what is meant is the Selbsthilfevereinigung der jüdischen Blinden in Deutschland, a corporate body without an entry in the organisation index. Seven correspondence partners carry a GND in `SZDKOR.xml` that their index entry lacks. Also with the operator are divergent forenames (Altmann, Miller, Bischoff), mentions in titles and running text, and Kuro Masu and Králík, whose envelope already points to another entry. The check script does not recognise identifiers with a letter suffix such as `SZDPER.2080a` as references.

## 2026-09-23, colour coding of the person index list evaluated

Changed. The colour coding of the archive list for the person index is read from the Word original, because it was lost in the text export. What follows unambiguously from the data is carried out. Kesten and Pilnjak are each merged into the entry with the valid GND after a check with the DNB (`merge_person_duplicates.py`, log extended), because 1185617155 does not exist and 1089928157 redirects to 118594397. The non-existent Kesten GND in `SZDKOR.xml` is replaced by 118561715. The persons Frenkel, Kaufmann and Tomaselli, marked yellow by the archive as wrongly unlinked, now point to their index entry in the Konvolute `frenkel-lotte`, `kaufmann-charlotte` and `zweig-lotte` and in `SZDKOR.xml`. Kaufmann appears in the data as Charlotte and in the index as Lotte, and the identification follows the archive's marking.

"Britain in Pictures", marked green by the archive as a corporate body, is added by hand to the organisation index as `SZDORG.67` and removed from the person index by `migrate_org_references.py`. The numbering continues instead of restarting, because the identifiers are part of the RDF URIs. Because the script rewrote its migration log, the older rows are put back in front from the Git history.

The knowledge documents are updated. [DATA.md](DATA.md) carries the colour coding as a source, the results and the open points in the section on the archive checkup, and the statements on organisation and person index in COLLECTIONS, PROJECT, README and the README of the organisation script are brought up to date. The organisation section in DATA.md still described `GetOrglist` as never called, which frontend commit `ef9a4ce` had made obsolete.

Open. Neumann, writer or architect, remains a question for the archive. With the operator are the entries "Filed as …", "Unidentified signatures" and "Zweig Family", the names marked bold and the question whether the unlinked names the archive wants removed leave the person index. `SZDKOR.xml` carries further person references with the placeholder `gnd/placeholder`. `SZDSTA.xml` has had no `geo` data since the data update of June 2021 (`1ed133c2`), so the new RDF of the locations has no coordinates. `ontology/reconciliation.ttl` for Klawiter rests on title matching with percentage values.

Open and planned as the next step, at the operator's suggestion, is a reconciliation script of its own. It adds Wikidata identifiers through the GND, meaning Wikidata P227, and writes only unambiguous hits automatically. It checks the existing GNDs at DNB or lobid for existence and redirects and reports contradictions to Wikidata. Entries without GND receive only a suggestion list, written hits carry their provenance, and places follow later. As of that day 521 persons have a GND but no Wikidata identifier, 220 persons have no GND, and none of the 67 corporate bodies carries a Wikidata identifier. For corporate bodies `szd-TORDF.xsl` also still lacks the output of `szd:wikidata`.

## 2026-09-23, first editions removed, staging ingest prepared

Decided. The operator abandoned the first editions (SZDPUB). Both versions, `data/Publication/SZDPUB.xml` and `data/Index/Erstveröffentlichungen/SZDPUB.xml`, are removed and remain in the Git history. They carried the same PID `o:szd.publikation`, differed in content and named no source. The object never existed in production, and the RDF transformation had no branch for it. The references in COLLECTIONS, DATA, ONTOLOGY and PROJECT are deleted. The total row of the collection statistics in DATA.md and the description of DATA.md in the README still contained SZDPUB and were corrected the same day.

Changed. The element-level comparison between this repository and `TEI_SOURCE` on staging gave the objects for the next staging ingest, the six holdings, the organisation index, three Konvolute and three new Konvolute from the source folder outside the repository. The package with checksums lies outside the repository under `Documents/PROJECTS/szd/ingest_staging_2026-09-23/`. Persons, locations, work index, Lebenskalender and the other Konvolute match staging.

Open. On staging `o:szd.publikation` can be deleted, and so can the orphaned `o:szd.korrespondenzen.ferencak-mirko-m`, whose only piece the new Konvolut `ferencak-mirko` carries more completely. The tagged Masereel theme page is not yet ingested on staging.

## 2026-09-22, duplicate pairs of the checkup decided

Decided. On 22 September 2026 the main agent instance decided the four open duplicate pairs of the checkup after delegation by the operator, revisably. For SZ-SHB/W3 `o:szd.359` stays and the byte-identical `o:szd.375` is deleted. For SZ-AP2/W-H206 `o:szd.2939` stays as the object in the newer cataloguing standard, and `o:szd.263` becomes dispensable once its signature and date are taken over. For Berger and Oppeln-Bronikowski the Konvolut identifier with `-von`, to which the index points, stays in each case and takes up the curated content of the sister identifier.

Changed. In the work index SZDMSK.299 points to `o:szd.359` instead of "Amerigo" `o:szd.358`, and SZDMSK.201 to `o:szd.2939`. The merged Konvolute lie, as with Ferenčak, in the source folder outside the repository, with direction `fromZweig`, titles after the title convention and, for Berger, signature SZ-SEF/B1 and facsimile `o:szd.1384`. Index and gallery anchors already point to the remaining identifiers.

Open. On GAMS the ingest of both Konvolute and of the work index, the deletion of `o:szd.375`, `o:szd.263` and of both sister Konvolute, and signature and date in `o:szd.2939` are pending. The sheet of SZ-AP2/W-H206 also lies as the first two images in `o:szd.220`.

## 2026-09-18, superseded person identifiers, checkup notes moved out

Changed. The sixteen back-references of the organisation index to former entries of the person index carry `subtype="superseded"`, so that they can be told apart from the live cross-references `idno type="SZDSTA"`. `build_org_index.py` writes this form, and the README of the script folder explains it. The RDF transformation of the presentation layer outputs `dcterms:replaces` from it, pointing to the old person resource.

Decided. The archive-internal verification notes of the checkup of September 2026 lie under `Documents/PROJECTS/szd/checkup-2026-09/` outside the repository, and the pattern `reports/checkup-*/` is ignored. The durable result stands in [DATA.md](DATA.md) in the section on the archive checkup.

Checked. Person, location, work and organisation index were ingested on GAMS staging the same day. No holding points to a superseded person identifier any more, and the migration log of the organisation index matches the targets that the RDF harness of the presentation layer resolves for the library.

Open. The organisation index must be ingested again after the change. Most corporate bodies lack country and place, because they come from the person index. Proposed and not begun are a GND-to-Wikidata reconciliation for persons with a GND and without a Wikidata identifier, and a place list with GeoNames identifiers as a first step towards a places index, with the autographs as the starting holding. `data/derived/lebenskalender/` is untracked although the lanes contract provides the files there, and the delivered copy under `docs/lebenskalender/lanes/` has the same content.
