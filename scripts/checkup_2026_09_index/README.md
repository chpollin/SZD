# Person index and linkage repairs, checkup 2026-09

Scripts that carry out the `confirmed-data` findings of the 2026-09 checkup verification
that concern the person index and the way the holdings reference it, a preparation script
for further IIIF label repairs and a read-only survey of unlinked persons. The diagnoses
are archive-internal verification notes that stay outside the repository. The durable
summary is the section "Archive checkup (September 2026)" of
[`knowledge/DATA.md`](../../knowledge/DATA.md#archive-checkup-september-2026).

Each writing script defaults to a dry run, writes with `--apply` and checks the written
state with `--verify`. Each appends a row for every change to its CSV log, in the columns of
[`scripts/organisationen_index/migration_log.csv`](../organisationen_index/migration_log.csv).
A later run adds to the log and never replaces the rows of an earlier one.

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

Merges the duplicate pairs and triples listed in `MERGES` into the entry the report names as the survivor,
rewrites every reference to a removed id, moves life dates out of the forename field into
`birth` and `death`, and carries over an authority number or variant note the survivor
lacks. Modelled on `scripts/organisationen_index/migrate_org_references.py`, which does the
same job for corporate bodies.

Kesten and Pilnjak followed on 2026-09-23 after a check against the German National
Library (DNB), because GND 1185617155 does not exist and 1089928157 redirects to 118594397.
Neumann stays untouched on purpose, because writer and architect of the same name make the
identity an archive question. Geiringer, Meiler and the Przeworskiego publishing house are
left out as well, because an earlier commit and the organisation migration settled them.
A removed record whose authority number differs from the survivor's is not copied over the
survivor's. The log records the dropped number so that the contradiction stays visible.

## normalize_person_refs.py

Writes every person reference in the form the RDF mapping reads. `GetPersonlist` in
`szd-TORDF.xsl` emits a triple only for a value containing `#SZDPER.` or a GND, so
`ref="SZDPER.1315"` is dropped and the person looks unlinked although the holdings name
her. The script adds the fragment marker, and it lifts the reference of an inner `persName`
onto a `term[@type='person']` that carries none, because `Work_RDF` reads the term attribute
and not the inner name.

A term reference is lifted only where the inner name resolves to exactly one index entry.
The run lists what it leaves alone, meaning names with no reference at all, an authority number
several index entries share, and a reference sitting on a nested `name` element.

## fix_essay_author_refs.py

Sets `author/@ref` in `data/Aufsatzablage/SZDESS.xml` to the person the inner `persName`
names. Every value repeated the sequence number of its own entry, so SZDESS.28 pointed
at SZDPER.28 while naming Stefan Zweig. Two entries carry the name
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
of the neighbouring README. The prepared XML is placed beside the existing images and
re-ingested into the existing object, and the fetched manifest must then be valid JSON with
the recorded canvas count.

## find_unlinked_persons.py

Read-only. Lists the index persons the person search of the website cannot find, because no
object references them, and searches the element text of the holdings for places where they
are named without a link. A reference counts in the two forms `szd-TORDF.xsl` resolves, a
token containing `#SZDPER.n` and a GND that `GetPersonlist` finds in the index by substring
match, and every `@ref`, `@key` and `@corresp` token of the scanned files is read, which is
more than the mapping reads. It therefore complements
[`scripts/personen_ohne_verweis/list_unlinked_persons.py`](../personen_ohne_verweis/README.md),
which counts only what the mapping reads, and does not replace it. The scan covers the
object holdings under `data/` without `data/Index/`, plus optionally the not yet ingested bundles of a staging folder. Persons
whose only reference was the essay numbering error recorded in `essay_author_log.csv` are
marked as such.

```bash
python scripts/checkup_2026_09_index/find_unlinked_persons.py \
    --staging C:/Users/Chrisi/Documents/PROJECTS/szd/ingest_staging_2026-09-23/konvolute_neu \
    --out-dir C:/Users/Chrisi/Documents/PROJECTS/szd/checkup-2026-09
```

The output is archive-internal and stays outside the repository, a candidate CSV with one
row per text hit (`unverknuepfte_personen_kandidaten.csv`) and a German summary with method,
class counts, the most promising candidates and the limits of the text search
(`unverknuepfte_personen_zusammenfassung.md`).

## verify_orphan_persons.py and remove_orphan_persons.py

`verify_orphan_persons.py` takes the class "kein Treffer im Text" of `find_unlinked_persons.py` and adds three independent checks: the identifier `SZDPER.n` occurs nowhere else (other index entries, the organisation index, any data file, the presentation layer), none of the person's GND numbers occurs in the data, and the person search of GAMS production and staging returns no hit. Only a person that passes all of them counts as certainly unreferenced. The result is an archive-internal CSV.

`remove_orphan_persons.py` removes exactly these persons from `data/Index/Person/SZDPER.xml`, after checking each one again against the current repository. The removed entries are kept unchanged in `removed_persons.xml` beside the script, outside `data/` so that no later scan counts them, and their identifiers are never assigned again. The run of 2026-09-24 is logged in `remove_orphan_persons_log.csv`.

```bash
python scripts/checkup_2026_09_index/verify_orphan_persons.py --candidates <out-dir>/unverknuepfte_personen_kandidaten.csv --out <out-dir>/sicher_unverknuepft.csv
python scripts/checkup_2026_09_index/remove_orphan_persons.py --verified <out-dir>/sicher_unverknuepft.csv --apply
```

A name that the holdings carry only in another spelling, transliteration or inflection is not found by the text search, so "certainly unreferenced" means no reference and no occurrence of the name in the spelling of the index.

## Scope

- The presentation layer stays untouched. `szd-TORDF.xsl` and `query/person_search.sparql` live in the
  `ZIMLAB/szd` repository, and the mapping gaps the report lists for
  `term[@type='person_affected']` and for the missing Aufsatzablage graph belong there.
- Anything the report classifies `needs-archive` or `needs-operator` stays open, above all
  whether unlinked index entries are removed at all.
- The derived data under `data/derived/` is reproduced by its own generator.
