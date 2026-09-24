# Build the timeline lanes of the Lebenskalender

Derives one JSON file per lane of the integrated timeline view from the TEI sources, in one event schema shared by all collections. The presentation layer in the repository `ZIMLAB/szd` switches the lanes on and off and needs events in a form that is the same for every collection.

Schema, dating rules, coverage and delivery state are described in [`knowledge/Lebenskalender-Lanes.md`](../../knowledge/Lebenskalender-Lanes.md). This file describes the run.

## Usage

```
python scripts/lebenskalender_lanes/build_lanes.py
```

Standard library only, no manifest, no installation. The run only reads the sources and writes only into the two target folders.

| Option | Effect |
|--------|--------|
| `--out-dir` | Target folder of the lane files, default `data/derived/lebenskalender` |
| `--docs-dir` | Copy target below `docs/`, default `docs/lebenskalender/lanes` |
| `--no-docs` | skips the copy below `docs/` |

## Sources

| Lane | Source |
|------|--------|
| `biography` | `docs/lebenskalender/SZDBIO.xml` |
| `correspondence` | `data/Correspondence/SZDKOR.xml` and the konvolut objects in `data/Correspondence/konvolute/` |
| `personal-documents` | `data/PersonalDocument/SZDLEB.xml` |
| `autographs` | `data/Autograph/SZDAUT.xml` |

`data/Index/Person/SZDPER.xml` resolves the person identifiers, GND references by number and direct references by SZDPER identifier. The index is read fresh on every run, so changes to it take effect without touching the script.

The object PID of the index and the other holdings comes from `teiHeader/publicationStmt/idno[@type="PID"]`. A Konvolut takes its PID from the file name, `o:` followed by the stem, because the teiHeader of a few defective production objects names another PID.

## Output

`<lane>.json` per lane as a list of events, plus `index.json` with the lane list, the event counts per lane and per `datePrecision`, the number of merged facsimile groups and the generation time in the field `generated`.

The correspondence keeps all index entries, because shared signatures prove no complete coverage by single letters. Merged records keep their original metadata in the field `sources`. `mergedDuplicates` counts the facsimile groups, `mergedRecords` the additionally merged records. `suppressedIndexEntries` stays for existing readers as the numeric value `0`.

The lane files are byte-identical across two runs. The only changing value is `generated`, which a comparison leaves out. Events are sorted by ISO date and identifier, undated events come last. Files are written through a temporary file and a rename, as UTF-8 with LF.

## Reports on the sources

The run reports on `stderr` the date texts it could not resolve, the irregularities it meets in the headings of the biography, the facsimile groups whose records conflict, the Konvolut files that share `xml:id` values and the index entries that name a Konvolut missing from the repository. Both are a work list for the editors and trigger no change in the sources.

## Tests

The generator parses all sources and reports unresolvable dates. The corpus tests also check that all correspondence records including their metadata and permalinks are preserved. They cover incomplete konvolute, shared signatures, contradictory facsimile metadata, ids unique across all lanes, the dates after 1950 and the Konvolut links, repositories and extents of the index entries. They further check the deterministic export and the identical copy below `docs/`.

```
python -m pytest scripts/lebenskalender_lanes/test_build_lanes.py -q
```

```
python -m ruff check --select E,F,W,I,UP,B,C4,SIM,PTH,RUF --ignore E501 scripts/lebenskalender_lanes/build_lanes.py
```
