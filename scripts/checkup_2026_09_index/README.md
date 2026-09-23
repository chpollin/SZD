# Person index and linkage repairs, checkup 2026-09

Four scripts that carry out the `confirmed-data` findings of the 2026-09 checkup
verification that concern the person index and the way the holdings reference it. The
diagnoses are archive-internal verification notes that stay outside the repository; the
durable summary is the section "Archive checkup (September 2026)" of
[`knowledge/DATA.md`](../../knowledge/DATA.md).

Each script defaults to a dry run, writes with `--apply` and checks the written state with
`--verify`. Each writes a CSV log of every change, in the columns of
[`scripts/organisationen_index/migration_log.csv`](../organisationen_index/migration_log.csv).

## Order

`merge_person_duplicates.py` runs first. It removes index entries, and the other two
resolve persons against the index, so an ambiguity it clears is one they no longer meet.
Concretely, GND 118535579 stands at two Friedenthal entries until the merge, and
`fix_essay_author_refs.py` leaves that one essay alone while it does.

```bash
python scripts/checkup_2026_09_index/merge_person_duplicates.py --apply
python scripts/checkup_2026_09_index/normalize_person_refs.py --apply
python scripts/checkup_2026_09_index/fix_essay_author_refs.py --apply
```

## merge_person_duplicates.py

Merges eleven duplicate pairs and triples into the entry the report names as the survivor,
rewrites every reference to a removed id, moves life dates out of the forename field into
`birth` and `death`, and carries over an authority number or variant note the survivor
lacks. Modelled on `scripts/organisationen_index/migrate_org_references.py`, which does the
same job for corporate bodies.

Kesten and Pilnjak followed on 2026-09-23 after a check against the DNB: GND 1185617155
does not exist, and 1089928157 redirects to 118594397. Left untouched on purpose: Neumann,
where writer and architect of the same name make the identity an archive question, and Geiringer, Meiler and the Przeworskiego
publishing house, which an earlier commit and the organisation migration already settled.
A removed record whose authority number differs from the survivor's is not copied over the
survivor's; the log records the dropped number so that the contradiction stays visible.

## normalize_person_refs.py

Writes every person reference in the form the RDF mapping reads. `GetPersonlist` in
`szd-TORDF.xsl` emits a triple only for a value containing `#SZDPER.` or a GND, so
`ref="SZDPER.1315"` is dropped and the person looks unlinked although the holdings name
her. The script adds the fragment marker, and it lifts the reference of an inner `persName`
onto a `term[@type='person']` that carries none, because `Work_RDF` reads the term attribute
and not the inner name.

A term reference is lifted only where the inner name resolves to exactly one index entry.
The run lists what it leaves alone: names with no reference at all, an authority number
several index entries share, and a reference sitting on a nested `name` element.

## fix_essay_author_refs.py

Sets `author/@ref` in `data/Aufsatzablage/SZDESS.xml` to the person the inner `persName`
names. All 403 values repeated the sequence number of their own entry, so SZDESS.28 pointed
at SZDPER.28, Hanns Arens, while naming Stefan Zweig. Two entries carry the name
"Zweig, Stefan" in the attribute meant for an identifier and get the authority number of the
index entry as well.

## prepare_iiif_repairs.py

Prepares four further book sources whose structure labels break the IIIF manifest, the same
defect and the same remedy as [`scripts/iiif_structure_labels`](../iiif_structure_labels),
whose `prepare_source` this script imports rather than copies. The prepared files and their
record land beside the existing ones in `scripts/iiif_structure_labels/prepared/`.

```bash
python scripts/checkup_2026_09_index/prepare_iiif_repairs.py \
    --source-root C:/Users/Chrisi/Documents/PROJECTS/szd --apply
python scripts/checkup_2026_09_index/prepare_iiif_repairs.py --verify
```

The objects are `o:szd.939` (SZ-SAM/W2), `o:szd.2935` (SZ-AP2/W-H172.4), `o:szd.2409`
(SZ-AAP/W-AA135.1) and `o:szd.2291` (SZ-AAP/W-AA183.2). Ingest follows the manual procedure
of the neighbouring README: place the prepared XML beside the existing images, re-ingest
into the existing object, then fetch the manifest and require valid JSON with the recorded
canvas count.

## What these scripts do not touch

- The presentation layer. `szd-TORDF.xsl` and `query/person_search.sparql` live in the
  `ZIMLAB/szd` repository, and the mapping gaps the report lists for
  `term[@type='person_affected']` and for the missing Aufsatzablage graph belong there.
- Anything the report classifies `needs-archive` or `needs-operator`, above all whether
  unlinked index entries are removed at all.
- The derived data under `data/derived/`, which its own generator reproduces.
