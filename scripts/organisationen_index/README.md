# Organisation index SZDORG

Two scripts built the organisation index on 11 September 2026 and moved the holdings onto it. Since 18 September 2026 [`data/Index/Organisation/SZDORG.xml`](../../data/Index/Organisation/SZDORG.xml) is maintained by hand, see [Maintenance after the migration](#maintenance-after-the-migration).

- `build_org_index.py` is historical. It wrote the index and beside it the decision table `organisation_decisions.csv`, it now refuses to run, and it stays as the provenance of the decisions of 11 September 2026.
- `migrate_org_references.py` stays in use. It removes the entries decided as corporate bodies from `SZDPER.xml`, rewrites the references of the holdings and appends every change to `migration_log.csv`.
- `reconcile_org_places.py` adds `country` and `settlement` from the GND record of each body (`geographicAreaCode` for the country, `placeOfBusiness` for the place), only where the record gives exactly one value, and never overwrites an existing one. It appends every written value to `reconcile_places_log.csv`, and `test_reconcile_org_places.py` checks its mapping rules. The GND code `XA-GB` becomes „Großbritannien“, the country name the organisation and location indexes share since 24 September 2026.

At the first run the order was fixed, because the second script uses the identifiers the first one assigned. Structure of the index, its relation to the location index, the reference form in the holdings and the way the RDF transformation resolves it are described in [`knowledge/COLLECTIONS.md`](../../knowledge/COLLECTIONS.md#organisation-index-szdorg).

## Two sources

1. `data/Index/Person/SZDPER.xml`, with the corporate bodies the person index carries as `person`. They are nowhere marked as such. The script finds them by two heuristics, a `persName` without `surname` or `forename` and a name pattern for corporate designations. What a hit turns out to be stands as a single decision in the table `DECISIONS` in the script.
2. Every `orgName/@ref` under `data/`, the corporate bodies the holdings already point to by authority number. All of them must resolve in the index, even without an entry in SZDPER.

The location index `SZDSTA.xml` is read as well, because the holdings point to most repositories through the same `orgName/@ref`, so they have to resolve here anyway. From SZDSTA they come in under their curated name with country, place and institution link instead of the spelling of a signature line, each with a reference to its `SZDSTA` identifier.

A candidate unknown to the table counts as a person if its GND number has the person format, otherwise as unclear. A corporate body newly entered in SZDPER thereby shows up in the report instead of slipping into the index unnoticed.

Authority numbers are never guessed. Where an SZDPER entry lacks a GND, the script takes one from the holdings only if exactly one `orgName` of the same name stands there.

## Editorial decisions of 11 September 2026

Both decisions are constants in the script, not hand corrections of the generated file.

`NON_CORPORATE_SZDSTA` keeps out of the index the SZDSTA entries that hold material without naming a corporate body, the entries „Privatbesitz, Land“ and „Erben Stefan Zweigs“. They stay in the location index, and the references of the holdings to them keep pointing to `o:szd.standorte`.

`MERGE_INTO` merges two SZDPER entries that name the same body under names too different for the name normalisation to catch. The value is the entry whose name and authority number lead the merged entry, and the key becomes a name variant with its own `idno` back-reference. This concerns `SZDPER.1735` „Home Office, Whitehall“, which merges into `SZDPER.2326` „Großbritannien. Home Office“ with GND 35565-3.

## Usage

```bash
# historical, stops with a message since the migration
python scripts/organisationen_index/build_org_index.py --dry-run

# clean SZDPER and rewrite the references of the holdings
python scripts/organisationen_index/migrate_org_references.py --dry-run
python scripts/organisationen_index/migrate_org_references.py

# country and place from the GND, cached lobid.org responses in the temp directory
python scripts/organisationen_index/reconcile_org_places.py --dry-run
python scripts/organisationen_index/reconcile_org_places.py
```

Both runs are deterministic, two runs on the same state yield the same files. The migration run is also idempotent, a second run finds nothing to do and leaves the log alone.

## Maintenance after the migration

At generation, the `SZDORG` identifiers followed from sorting by main name, and a rebuild would shift them. After the migration the index can no longer be generated from the sources, because the corporate bodies have left the person index. `build_org_index.py` then stops with a message instead of writing a truncated index, and the file is maintained by hand.

A new body receives the next free number, because the identifiers are part of the RDF URIs. If it comes from the person index, the decision table receives its row with `org` and the new identifier, and `migrate_org_references.py` then removes the person entry and rewrites the references. The script appends to its log under the existing header, so the rows of earlier runs stay. `SZDORG.67` Britain in Pictures was added this way on 23 September 2026.

## Form of the rewritten references

- The name element becomes `<orgName ref="http://d-nb.info/gnd/<number>">` where the index entry has an authority number, as SZDLEB and SZDKOR write throughout.
- Without an authority number it becomes `<orgName ref="https://gams.uni-graz.at/o:szd.organisation#SZDORG.<n>">`. `szd-TORDF.xsl` passes such a value through unchanged.
- The `@ref` of the enclosing `author` or `editor` is rewritten to the same form and not dropped, because `szd-Bibliothek.xsl` groups and sorts the library list by it and an empty attribute would collapse several titles under one heading.

Where a `persName` becomes an `orgName`, the attributes stay and the inner `<name>` is dropped, because the holdings give the corporate name directly in `orgName`.

## Columns of the decision table

| Column | Content |
|---|---|
| `szdper_id` | Identifier in the person index, empty for entries not from SZDPER |
| `name` | Name as spelled in the source |
| `gnd` | GND number without prefix |
| `entscheidung` | `org`, `person`, `unclear` or `keine-koerperschaft` |
| `grund` | Reason for the decision |
| `szdorg_id` | Identifier in the new index, empty except for `org` |
| `quelle` | `SZDPER`, `SZDSTA` or `Bestand` |

Unclear cases and the locations excluded as non-corporate stand in the table and not in the index.

## Columns of the migration log

| Column | Content |
|---|---|
| `datei` | Path relative to the repository root |
| `kontext` | `xml:id` of the enclosing `biblFull`, for SZDPER the removed identifier |
| `zeile` | Line in the file before the change |
| `alte_referenz` | Attribute and value before the change |
| `neue_referenz` | Attribute and value after it |
| `aktion` | `Verweis umgestellt` or `SZDPER-Eintrag entfernt` |

## Open findings in the source data

Two contradictions stay unchanged after the decision of 11 September 2026 and are recorded here for an editorial ruling.

GND 38379-X stands in the location index for two different bodies, `SZDSTA.37` „The British Museum“ and `SZDSTA.38` „David H. Lowenherz“. Because the index merges by authority number, both names stand in the entry `SZDORG.15`, the dealer's name as main name and the museum as variant, and only `SZDSTA.38` is referenced back. 38379-X is correct for the British Museum, and the autograph dealer needs a number of its own or none.

GND 117322695 stands in the holdings at an `orgName` „Schweizerisches Vereinssortiment Olten“ in `SZDKOR`, but is the number of a person in the person index. The number therefore does not enter the index, and this one reference in the holdings stays unresolved on purpose. The run reports it as a warning.

## Scope

The scripts leave the location index as it is, even where SZDORG names the same body. The presentation layer, `szd-TORDF.xsl` and the other stylesheets, lives in `ZIMLAB/szd`.
