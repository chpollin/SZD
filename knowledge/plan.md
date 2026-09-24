---
title: Plan
project:
  name: Stefan Zweig Digital, data repository
  repository: https://github.com/chpollin/SZD
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: active
created: 2026-09-24
updated: 2026-09-24
---

# Plan

Open technical work on the data repository and the questions that need a decision by the operator or the archive. A finished item leaves this list, and its outcome goes into the [journal](journal.md). The presentation layer keeps its own plan in `ZIMLAB/szd` (`knowledge/plan.md`), which also lists the Cirilo reference readings of staging.

## Staging ingest

The data changes of 2026-09-22 to 2026-09-24 are in the repository and not yet on staging. The ingest runs from a package that `scripts/staging_package/build_staging_package.py --out <folder>` writes outside the repository from the current `HEAD`. The operator ingests it with Cirilo.

1. Folder `1-index` first, meaning organisation, person, location and work index, because `szd-TORDF.xsl` resolves persons, repositories and corporate bodies against the index objects at ingest time.
2. Folder `2-bestaende` with the holdings. `o:szd.korrespondenzen` needs this renewed ingest so that its RDF carries the corporate bodies.
3. Folder `3-konvolute`. Cirilo creates a missing Konvolut from the PID in its file, which concerns the three new Konvolute `berger-gisela-von`, `ferencak-mirko` and `oppeln-bronikowski-friedrich-von` and every Konvolut that exists in production but not on staging.

Every object needs `STYLESHEET` and `TORDF` pointing to the gamsdev mirror, and nothing may follow `.xsl` in either reference. The package README lists the references still to set, read live from staging when the package is built.

Before the package is built:


On staging after the ingest:

- Delete `o:szd.375`, `o:szd.263`, the two sister Konvolute, `o:szd.publikation` and `o:szd.korrespondenzen.ferencak-mirko-m.`, and carry signature and date into `o:szd.2939` (decisions of 2026-09-22 and 2026-09-23).
- Re-ingest the prepared book sources of `scripts/iiif_structure_labels/prepared/` into `o:szd.174`, `o:szd.67`, `o:szd.939`, `o:szd.2935`, `o:szd.2409` and `o:szd.2291`, then check that each manifest is valid JSON.
- Once the fix of the autograph RDF in `szd-TORDF.xsl` (absolute `//t:textClass` path, `ZIMLAB/szd`) is on the mirror, ingest `o:szd.autographen` again, because GAMS derives the RDF only at ingest.

## Production ingest

The corrections reach production only after the archive has approved them on staging, in the same order as on staging. Until then `o:szd.personen` in production keeps the persons removed from the repository on 2026-09-24, and the production Konvolute keep the defects corrected here. Partner review and publication of the timeline are pending as well, see [Lebenskalender-Lanes](Lebenskalender-Lanes.md#delivery-state).

## Konvolute

- Three production objects are defective and stay out of the staging package, because their files do not name their own PID. `o:szd.korrespondenzen.judischer-jugendverein` and `o:szd.korrespondenzen.judischer-jugendverein-dusseldorf` are two objects for one body, and both name the obsolete PID `o:szd.korrespondenzen.judischer-jugendverein-(dusseldorf)`. `o:szd.korrespondenzen.rascher-und-cie` carries the content of `alberts-margot` and no PID of its own. Operator question, which of the two Jugendverein objects stays, and where the correct content of the Rascher Konvolut can be recovered from.
- Left untouched by `scripts/checkup_2026_09_konvolute/fix_konvolut_defects.py` because the correct value is not established. Specht Richard `SZ-SEF/B9.1` (recipient Richard Specht or Lotte Altmann, archive at the original). `SZ-SAM/B18.1–3` (which date belongs to which piece, archive). `SZ-LAS/B3.33–35`, carried by both `fleischer-max` and `fleischer-victor` with diverging content (which object is canonical, operator). The remaining `needs-archive` and `needs-operator` items of the archive-internal operator report.
- Thalhuber `SZ-SAM/B17`. The defect lies in the correspondence index `SZDKOR.xml`, which the Konvolut script does not write. Technical, a correction with evidence in the index scripts.
- Dates after 1950. The imported Konvolute `bahr-hermann`, `feld-leo`, `freud-sigmund`, `heidelbach-paul`, `jeanrenaud`, `kaemmerer-ami`, `kaemmerer-maria`, `kubin-alfred`, `mees-friedrich-siegbert`, `unidentified` and `winternitz-friderike-von` carry `@when` values after 1950 (read on 2026-09-24). Most look like the century error of two-digit years described in [DATA](DATA.md#century-error-in-two-digit-years), while family letters may genuinely be later. Where title or display text proves the year, `scripts/korrespondenz_titel/` corrects it, the rest needs an editorial decision.
- The `dc:title` values of the Konvolut objects follow several patterns (frontend `knowledge/Facsimiles-Korrespondenzen.md`). The header titles of the Konvolut files are their source.

## Timeline lanes

The lanes are generated from the complete Konvolute, and the corpus tests pin that state. The run messages leave editorial work in the Konvolut data.

- Facsimile groups whose records conflict and therefore stay separate, listed in `CONFLICTING_FACSIMILES` of the test. About half concern places that the Konvolut `zweig-friderike` gives as Salzburg against the sender's place in `fleischer-victor` and `fleischer-max`. Others involve the pairs `glucksmann-heinrich` and `gluecksmann-heinrich` or `meulenhoff` and `meulenhoff-johannes-marius`, which look like duplicate objects, and coarser dates in `reichner-herbert` and `meingast-anna` against day dates of the partner's record. In the two Jugendverein files one copy of `SZDKOR.judischer-jugendverein.1` carries a date as its place. `o:szd.3204` and `o:szd.3317` stand at records with different signatures and dates, and at `o:szd.909` one record dates 2019 for 1919 and one sits in the file `masereel-frans` with a `reichner-herbert` identifier.
- Konvolut dates after 1950 whose display text gives a two-digit year that `@when` places in the twenty-first century.
- `SZDKOR.696` names `o:szd.korrespondenzen.unbekannt` and `SZDKOR.857` names `o:szd.korrespondenzen.podbielski-gert-rene`, while the repository holds the probable counterparts `unidentified` and `podbieliki-gert-rene`. Which spelling is the correct PID is an operator question, and until then the two index entries carry no `konvolut` link.
- Konvolut files that reuse the `xml:id` values of another Konvolut, which the run lists and the lanes resolve with a file suffix. The largest group is `friedenthal-richard`, `masereel-frans` and `reichner-herbert`, the others involve `czech-suzanne`, `suzanne-czech`, `international-copyright-bureau-ltd.-the`, `heilbron-george`, `fleischer-max`, `fleischer-victor` and `max-und-victor-fleischer`, and the pairs `judischer-jugendverein` and `judischer-jugendverein-dusseldorf`, `meulenhoff` and `meulenhoff-johannes-marius`, `muller` and `muller-einigen-hans`, `weisflog` and `weisflog-heinrich`. Correcting the ids in the Konvolut files is editorial work.
- The three defective production objects of the import README give dead `href` values in the lanes until their `teiHeader` PID is corrected.

## Person index

- `scripts/checkup_2026_09_index/find_unlinked_persons.py` classified 45 persons as "Kandidat gefunden" and 68 as "nur Nachname" in the run of 2026-09-24. The review list is archive-internal and stays outside the repository. A person is linked only where the text hit identifies the index entry unambiguously.
- Operator decisions on the colour-coded archive list. The entries "Filed as …", "Unidentified signatures" and "Zweig Family", the names marked bold, and whether unlinked names the archive wants removed leave the index beyond the certainly unreferenced persons removed on 2026-09-24. Also with the operator are the divergent forenames between holdings and index (Altmann, Miller, Bischoff), persons named only in titles and running text, and Kuro Masu and Králík, whose envelope already points to another entry.
- Archive question, whether the entry for Neumann means the writer or the architect of that name.
- `SZDPER.1026` (Neydisser) has been a name variant of `SZDPER.818` (Lernet-Holenia) since `a108c6f3`, while the library still names the pseudonym's own GND. `SZDPER.1304` never existed, and the body it means, the Selbsthilfevereinigung der jüdischen Blinden in Deutschland, has no entry in the organisation index.
- Correspondence partners whose GND in `SZDKOR.xml` is missing from their index entry, and person references in `SZDKOR.xml` that carry `gnd/placeholder`.
- The check scripts do not read identifiers with a letter suffix such as `SZDPER.2080a` as references.

## Organisation and location index

- Entries still without country or place after the GND reconciliation, because their GND record gives no geographic code, names several places (Herbert Reichner Verlag, `SZDORG.24`) or is missing.
- `SZDORG.15` joins the British Museum and the dealer David H. Lowenherz under GND 38379-X, which belongs to the museum. The dealer needs a number of its own or none. GND 117322695 at "Schweizerisches Vereinssortiment Olten" in `SZDKOR.xml` is a person's number. Both are recorded in [scripts/organisationen_index/](../scripts/organisationen_index/README.md#open-findings-in-the-source-data) for an editorial ruling.
- `SZDSTA.xml` has had no `geo` elements since the data update of June 2021 (`1ed133c2`), so the location RDF carries no coordinates.

## Reconciliation

- A reconciliation script adds Wikidata identifiers through the GND (Wikidata property P227) and writes only unambiguous hits, each with its provenance. It checks the existing GND numbers against the German National Library (DNB) or lobid for existence and redirects and reports contradictions to Wikidata. Persons without GND receive only a suggestion list. Corporate bodies carry no Wikidata identifier yet, and `szd-TORDF.xsl` has no `szd:wikidata` output for them (presentation layer).
- A place list with GeoNames identifiers as the first step of a places index, starting with the autographs (proposed 2026-09-18, not begun).
- The Klawiter links in `ontology/reconciliation.ttl` rest on title matching with a percentage score. A reconciliation of the works by authority numbers is open.

## Operator questions

- Ontology identifiers. The namespace `https://w3id.org/nachlass#` keeps its German name, and `szd:glossar`, the hybrid `szd:objecttyp` and glossary concepts such as `szdg:DatumEvidenz` keep German-derived identifiers, because they belong to the live GAMS vocabulary and the glossary. Rename them together with the glossary and the presentation layer, or keep them?
- Einheitssachtitel. The former repository rules required `title[@type="Einheitssachtitel"]` in German and English, while the renderer groups a language-neutral one correctly in both languages ([COLLECTIONS](COLLECTIONS.md#rendering-contract-grouped-lists)). Is the bilingual form an editorial obligation?
- Rights. Every TEI header states CC BY 4.0 in `availability`, while the [README](../README.md#licence) says the rights of the archival research data remain with the archive. Which statement applies, and does the other change?
- Glossary. The German and English definitions of `Enclosures` and `AdditionalMaterial` are crossed ([DATA](DATA.md#glossary)). Which language version is canonical?
- Editorial rulings from the archive checkup. Whether an index entry counts an archival bundle or a correspondence relationship, what bracketed title dates mean, one notation for unidentified senders, and the classification vocabulary of the Aufsatzablage.
- Archive questions on missing scans and on dates only the originals can supply.
- The root file `mail.md`, a mail text of July 2026 on the SZ-AAL/B correspondence, has no function in the repository. Remove it?

## Scripts and documentation

- `reconcile_klawiter.py` and `generate_instances.py` with `reconciliation_report.md` and `reconciliation_results.json` stay at the top level of `scripts/`. They belong with the ontology, and a move changes the generator comments of `ontology/reconciliation.ttl` and `ontology/sample-instances.ttl`, `ontology/README.md` and [ONTOLOGY](ONTOLOGY.md), so it goes together with the next ontology regeneration.
- `scripts/SZ-AAL-Pipeline/` holds a second, diverging `szd_pipeline.py` beside `scripts/Processing Pipeline/` and has no README. Which one stays?
- The README of `scripts/checkup_2026_09_index/` does not yet describe `verify_orphan_persons.py` and `remove_orphan_persons.py`, and the README of `scripts/checkup_2026_09_konvolute/` still speaks of Konvolute that exist only on GAMS.
