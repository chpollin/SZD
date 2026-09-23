---
title: Lebenskalender Lanes
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD.git
method:
  name: Promptotyping
  url: https://dhcraft.org/promptotyping
status: complete
created: 2026-09-11
updated: 2026-09-23
version: 1.0.0
tags: [data, lebenskalender, timeline, derived]
---

# Lebenskalender Lanes

The timeline view of the Lebenskalender shows several collections side by side as lanes that users switch on and off individually. So that the view can treat all collections alike, each lane is backed by its own JSON file in one shared event schema. The files are derived from the TEI sources of this repository by [`scripts/lebenskalender_lanes/build_lanes.py`](../scripts/lebenskalender_lanes/README.md). The view is integrated in the presentation layer in the repository `ZIMLAB/szd` under `mode=timeline`, and `mode=fancy` stays as a compatible alias. Its implementation and local testing are described there in `knowledge/UI-Ueberarbeitung.md`.

## Lanes and Sources

| Lane | Source | Object |
|------|--------|--------|
| `biography` | `docs/lebenskalender/SZDBIO.xml` | `o:szd.lebenskalender` |
| `correspondence` | `data/Correspondence/SZDKOR.xml` and `data/Correspondence/konvolute/` | `o:szd.korrespondenzen` and `o:szd.korrespondenzen.<person>` |
| `personal-documents` | `data/PersonalDocument/SZDLEB.xml` | `o:szd.lebensdokumente` |
| `autographs` | `data/Autograph/SZDAUT.xml` | `o:szd.autographen` |

The correspondence lane covers both levels of the two-level architecture described in [COLLECTIONS.md](COLLECTIONS.md#two-level-architecture), the aggregating index and the single letters of the konvolut objects.

`data/Index/Person/SZDPER.xml` resolves the person identifiers. The correspondence references persons by GND, the other collections by the SZDPER identifier in the `@ref` of `author`. The index is read on every run, so changes to it take effect without touching the script.

## Event Schema

Every event is a JSON object with the same fields, whatever the lane. The files are written compactly, and a field without a value is left out, except `date`, which the view reads as `null` for undated pieces.

`id`

Stable identifier, the `xml:id` of the source entry, for instance `SZDBIO.1`, `SZDKOR.127`, `SZDKOR.roth-joseph.1`, `SZDLEB.138` or `SZDAUT.720`.

`lane`

One of `biography`, `correspondence`, `personal-documents`, `autographs`.

`date`

Start of the dating as an ISO string in the granularity of the source, `YYYY`, `YYYY-MM` or `YYYY-MM-DD`. `null` for undated pieces.

`datePrecision`

One of `day`, `month`, `year`, `range`, `inferred`, `undated`. It is `undated` exactly when `date` is missing.

`dateEnd`

Present only for `range` and `inferred`, the end of the period as an ISO string.

`dateLabel`

Display text with the keys `de` and `en`, generated from the ISO value. German in the day form „7. Januar 1933“, English „7 January 1933“, with month precision „Januar 1933“ and „January 1933“, with year precision the number alone, for periods start and end joined. Where the source gives a dating only as display text and the parser does not resolve it, that source text stands in the label, because it is the only information the holdings give about the piece.

`title`

Title with the keys `de` and `en`. In the correspondence it is generated from `correspAction` after the pattern „Brief von X an Y“ and „Letter from X to Y“, with the names in reading order as in the title convention of the konvolut objects. In the personal documents and autographs it is the title of the `biblFull`, where an assigned title precedes an object title and that precedes the original title. A language-neutral title applies to both languages, and a language without a title of its own takes the other one. In the biography it is the text of the entry in both languages.

`place`

Place name, where the source gives one. In the biography from the heading before the date element, in the correspondence from `correspAction/placeName`, in the autographs from the acquisition note. The personal documents give no place.

`persons`

List of objects with `id` and `name`. The `id` is the SZDPER identifier, `null` where the reference of the source cannot be resolved. The `name` stands in index form, surname followed by forename, and comes from the person index as far as the identifier is there. In the biography these are the referenced persons of the entry, in the correspondence sender and recipient, in the other collections the author.

`signature`

Signature from `msIdentifier`, in the autographs from the provenance note.

`href`

Detail page as a relative path, built from the object PID of the source file and the entry identifier as fragment, `/<PID>/sdef:TEI/get#<id>`. The view resolves it on the host it runs on, so staging links stay on staging.

`facsimile`

PID of the METS object, where the entry carries one. The facsimile itself is at `https://stefanzweig.digital/<PID>`.

`dateOrigin`, `dateOriginPrecision`, `dateOriginEnd`, `dateOriginLabel`

Additional data for autographs on the creation of the piece, with the same dating forms as the acquisition. Without a creation date, `dateOrigin`, `dateOriginPrecision` and `dateOriginLabel` are absent, as in the other lanes. `dateOriginEnd` is set only when an end value exists. The view shows the creation text in the metadata, while placement on the timeline and the year scale use the acquisition in `date`.

## Dating Rules

The sources give their dates in machine-readable attributes and, where these are missing, as display text alone. Both paths lead to the same six values of `datePrecision`.

A `@when` yields day, month or year precision after the length of the value. A pair of `@from` and `@to` yields `range` with `date` as start, and a `@to` beside a `@when` is read as a period as well, because one heading of the biography gives its start that way. A pair of `@notBefore` and `@notAfter` yields `inferred`, again with `date` as start. A `@type="undated"` on an element that also carries a value does not count against it. In the correspondence index it marks bundles that hold undated pieces beside dated ones.

Dates given only as text are resolved by a narrow parser that knows the forms occurring in the sources, the German and English day form, the month form, the dotted form, the ISO form and the bare year. Two or more recognised values yield `range` from the earliest to the latest. Square brackets and any other wording beside the date, such as a circumstance or a reservation, lower the precision to `inferred`. What the parser does not resolve stays undated. A two-digit year receives no century, and a weekday without a date does not become a date.

The decision of 11 September 2026 sets the division of labour with the frontend. Pieces dated by year alone carry `year` and are gathered at the start of the year there. Undated pieces stay in the file, appear at the end of their lane and do not count on the scale.

## Event Date of the Autographs

The autographs carry two dates, the creation of the autograph in `summary` and its acquisition by Stefan Zweig in `acquisition`. The lane uses the acquisition, because the Lebenskalender shows the events of his life. The acquisition dates fall within his collecting years, while the creation dates reach back to the sixteenth century and would break the scale. Autographs without an acquisition note stay in the lane as `undated`.

## Duplicates and Coverage of the Correspondence

A letter to several recipients stands in the konvolut object of every correspondence partner involved. The facsimile PID is the identifier these copies share. The run merges such records when, in addition, their non-empty signature matches and their existing dates and places do not contradict each other. Missing dates or places may be supplied by another record of the same group. Contradictions produce separate events and a run message.

The main event takes the metadata of the record sorted first, and the persons of the other records join its person list. The optional field `sources` holds, for a merge, all original event objects including the main entry, with their own dates, titles, persons and permalinks. The contained objects carry no `sources` field of their own. Deviating source data and alternative detail pages thereby stay accessible. In the holdings of September 2026, some facsimile groups complete undated records with dated records carrying the place Salzburg.

The correspondence index carries no facsimile PIDs and therefore takes no part in this merge. Its entries and the letters of the konvolute relate as bundle and piece. Archival signatures and their prefixes are shared by different correspondence partners, however, and prove no complete coverage of an index entry. The generator therefore keeps every index entry. Entries covering several pieces keep the bundle title of the source. The number of events mixes catalogue levels and does not count physical letters.

An earlier version of the generator suppressed index entries whose signature occurred among the single letters. The check of 11 September 2026 showed that most of these entries point to a curated konvolut object missing from the local single-letter holdings and that others are only partly represented. For `SZDKOR.680`, five pieces in the index face two matching records in the linked Alfred Zweig object. For `SZDKOR.858` and `SZDKOR.899`, the person data of the only matching single record contradicts the index. An automatic suppression cannot be derived from such comparisons, and every lane file therefore holds all source records, directly or in `sources`.

`index.json` holds `mergedDuplicates` as the number of merged facsimile groups, `mergedRecords` as the number of additionally merged records, and the compatibility field `suppressedIndexEntries` with the numeric value `0`. The sources stay unchanged. The dates 2012-05-26, 2018-10-02 and 2030-09-23 of three `unidentified` records are output as in the source and need scholarly review.

## Generation

```
python scripts/lebenskalender_lanes/build_lanes.py
```

The lane files and `index.json` land in `data/derived/lebenskalender/`, a folder ignored by Git that the generator reproduces at any time. The same run puts a copy into `docs/lebenskalender/lanes/`, because GitHub Pages serves this repository from the `docs/` folder of the `master` branch and files outside it are not reachable there. It is a copy rather than a symlink, because the prototype in the same folder already handles `SZDBIO.xml` that way and a symlink is unreliable under Windows and Git. A build step is out of the question as long as the repository's only workflow generates the ontology documentation and the Pages delivery otherwise works without a build. Pages serves the copy only after the maintainer's push.

The lane files are byte-identical across two runs. The generation time lives only in the field `generated` of `index.json`, so that a comparison can leave it out. The corpus tests of the generator check the preservation of all source records, conflict handling and deterministic output.

The GAMS presentation layer holds a further copy of all lane files and `index.json` under `ZIMLAB/szd/data/lebenskalender/`. This copy is refreshed explicitly when the data changes, and the generator does not write it. `szd-Lebenskalender.xsl` passes the asset base from `$server` and `$gamsdev` to the client, so lane files and frontend follow the same staging and production path. The deferred Cirilo assignments are documented in the README of the frontend repository.

## Delivery State

Frontend commit `b616496` with the timeline and the lane copies was pushed to `ZIMLAB/szd` on 11 September 2026, and the following commit `3cb6596` fixes the filter links for GAMS. Filters live in the URL fragment, because GAMS rejects additional query parameters with HTTP 404. Both states are on staging. A server mirror comparison, HTTP checks of scripts, stylesheets and JSON files against the local content and a browser check of the previously shared Fancy URL in German and English confirmed the delivery.

The message about the new view went to the Literaturarchiv Salzburg on 11 September 2026, as confirmed by the operator. Partner review, acceptance and production publication are pending.

## Related

- [COLLECTIONS.md](COLLECTIONS.md) — structure of the collections and rendering contracts
- [DATA.md](DATA.md) — counting conventions and documented data gaps
- [DATA_MODEL.md](DATA_MODEL.md) — encoding patterns and bilingual encoding
- [scripts/lebenskalender_lanes/README.md](../scripts/lebenskalender_lanes/README.md) — run, options and tests
- [docs/lebenskalender/README.md](../docs/lebenskalender/README.md) — prototype of the view in the SZD design
