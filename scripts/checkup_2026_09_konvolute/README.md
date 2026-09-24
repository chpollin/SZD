# Konvolut corrections from the September 2026 archive checkup

`fix_konvolut_defects.py` applies the corrections to `data/Correspondence/konvolute/*.xml`
that the archive checkup of 16 September 2026 diagnosed and that the archive-internal
verification notes establish beyond doubt. It complements
[`scripts/checkup_2026_09_korrespondenz/`](../checkup_2026_09_korrespondenz/), which corrects
the correspondence index `data/Correspondence/SZDKOR.xml`; this script never touches that file.

Until 24 September 2026 the individual correspondence konvolut objects existed only on GAMS,
apart from 42 person konvolut files generated in June 2026. Commit `e1b156fa` brought all 306
of them into `data/Correspondence/konvolute/` unchanged from production, which is what let this
script work on the objects directly.

## What it corrects

Wrong facsimile PIDs (five picture postcards in `SZ-SAM/AK`, misassigned to the facsimile of a
neighbouring signature), missing facsimile PIDs (fourteen pieces across the Fleischer, Freud,
Friedenthal, Kippenberg, Hertzka and Rolland konvolute), one dead facsimile PID corrected to the
live object (Specht Richard, `SZ-SEF/B9.1`), the `correspDesc/@type="byZweig"` of all 47 Sigmund
Freud letters (a value the presentation layer does not resolve, which is why every one of them
rendered its sender as "unbekannt" although the TEI already names Stefan Zweig correctly), two
title dates corrected from an internal contradiction with the entry's own `date` element
(`SZ-AAP/B2.50`, `SZ-AAP/B1.266–268`), two title dates added from the archive's stated
correction where none existed before (`SZ-LAS/B3.21–22`), a `persName` split into a structured
sender and recipient where it held the whole title phrase instead of a name
(`SZ-SEF/B3`, `SZ-SAH/B1.1`, `SZ-SHB/B6.2`), one wrongly signed entry deleted because no object
carries that signature (`SZ-SHB/B3`), doubly encoded umlauts repaired in the sibling entry
`SZ-SHB/B6.1`, and the Hirschfeld Eugenie duplicate `SZ_SEF_B5.1` merged into the canonical
`SZ-SEF/B5.1` and deleted.

Every correction is anchored to one `biblFull` entry by its `xml:id` and traced in the source
code to the archive-internal verification note it rests on (`verify-korrespondenz-daten.md` or
`verify-verknuepfung.md`, outside this repository). A fix that finds its target value already in
place is skipped, which is what makes a second run report nothing to do.

## What it deliberately leaves untouched

A number of items from the same defect list are not in the correction table, because the
correct value is not established from data and code alone, or because acting on it would need a
fact, a ruling or a write outside this script's scope:

- Specht Richard `SZ-SEF/B9.1`: the entry's own title ("Brief an Lotte Altmann") contradicts its
  `correspAction` (Richard Specht), an internal contradiction the verification note leaves open
  ("decide from the original whether the recipient is Richard Specht or Lotte Altmann"). Only
  the dead facsimile PID is corrected; the duplicate entry and the recipient dispute stay.
- `SZ-SAM/B18.1–3` (Rieger to Meingast): the verification note establishes that the three
  incomplete item-level entries must take their data from the three complete bundle-level
  entries in the same file, but not which of the three dates belongs to which item. Assigning a
  specific date to a specific item without that mapping would be a guess, so the entries are
  left as they are.
- `SZ-LAS/B3.33–35`: the two konvolut objects that both carry this signature (`fleischer-max`
  and `fleischer-victor`) disagree with each other, one partially filled, one empty. Which
  object is canonical is an open editorial question the verification note defers, so no
  `correspDesc` is written in either.
- Thalhuber `SZ-SAM/B17`: the konvolut already correctly names Anna Meingast as recipient. The
  defect the archive reports lives in the index `SZDKOR.xml`, which this script's write scope
  excludes.
- Everything the verification notes classify `needs-archive` (a date, a century, a recipient
  identity, whether a piece was ever scanned) or `needs-operator` (a merge ruling, a duplicate
  object, a wording decision). These are listed in the operator report of the run that produced
  this script, not repeated here to avoid drifting out of sync with it.
- The 221 konvolut objects that still exist only on GAMS and not in this repository. Most of
  the reported defects live there; they can be corrected here only once the objects are ingested
  into `data/Correspondence/konvolute/`, matching commit `e1b156fa`'s own scope.
- Two items where the current production download already carries the corrected value, found
  during this run (`SZ-AAL/B1.110a` in `altmann-hannah.xml`/`altmann-manfred.xml`, and
  `SZ-AAL/B3.48` in `geiringer-josef.xml`): both were diagnosed as broken in the verification
  notes of 17 September 2026 and are already fixed in the 24 September 2026 download, evidently
  by an upstream correction between the two dates. No action was needed.

## Evidence

Wrong- and missing-PID corrections rest on a live re-check against GAMS production, one read-only
`GET` of the object's `DC` datastream per PID (`https://gams.uni-graz.at/archive/objects/<pid>/datastreams/DC/content`),
confirming the shelfmark in `dc:title`/`dc:source`, and one check of `RELS-EXT` confirming
context membership, run sequentially with a pause between requests. The rest rest on the
archive-internal verification notes, which already carried this evidence at the time they were
written; where this run's snapshot of the konvolut files (24 September) differed from what a
verification note described (17 September), the correction was checked against the current file
before being applied, and left out where the current state no longer matched what the note
established (see above).

## Run

```bash
# 1) dry run, showing what would be written
python scripts/checkup_2026_09_konvolute/fix_konvolut_defects.py

# 2) apply
python scripts/checkup_2026_09_konvolute/fix_konvolut_defects.py --apply

# 3) check: every fix applied, every touched file well formed
python scripts/checkup_2026_09_konvolute/fix_konvolut_defects.py --verify
```

The run is idempotent: a fix already in place is reported and skipped, not reapplied, so a
second `--apply` writes nothing. Every file is checked well formed with
`xml.etree.ElementTree` before it is written; if the result would not be, that file is not
written and the run reports the error.

## Serialisation

Files are read and written through [`scripts/_szd_io.py`](../_szd_io.py), byte-preserving:
the text is read and written with `newline=""`, so the file's own line terminators pass through
unchanged (these konvolut files carry LF, matching the download in commit `e1b156fa`; a
`git checkout` on a machine with `core.autocrlf=true` silently turns that into CRLF on write,
which is why this script's own testing restored files with `git show HEAD:<path>` rather than
`git checkout --` where it needed a clean baseline). Edits are exact string anchors and
substitutions scoped to one `biblFull` entry by its `xml:id`, following the style of
[`scripts/checkup_2026_09_korrespondenz/add_bundle_signatures.py`](../checkup_2026_09_korrespondenz/add_bundle_signatures.py),
not a round trip through an XML serialiser that would rewrite indentation or attribute order
across the whole file.

## Log

Every applied correction is appended to `corrections_log.csv` (shelfmark, konvolut file,
field, old value, new value, evidence, date), committed alongside the data as provenance. The
log is append-only; a fix already logged from an earlier run is not logged again because it is
not re-applied.
