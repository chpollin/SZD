# Import the correspondence konvolute from GAMS production

Brings every correspondence konvolut that GAMS production publishes as `o:szd.korrespondenzen.<slug>` into [`data/Correspondence/konvolute/`](../../data/Correspondence/konvolute/). Before 2026-09-24 the repository held only the konvolute that had been edited here, the others existed only as GAMS objects.

## Behaviour

- The PID list comes from the Fedora search of `gams.uni-graz.at`, so a konvolut created later is picked up by a rerun.
- A file that already exists is never overwritten. The repository copy is the edited one and may be ahead of production.
- The datastream `TEI_SOURCE` is written byte for byte as production serves it. Local copies on the operator's disk (the ingest folder of May 2025 and the per-person export) were not used, a sample comparison showed them equal to production or older.
- A download that is not well-formed or has no TEI root is skipped. One that does not name its own PID is skipped too, unless `KNOWN_DEFECTS` in the script records the production object as defective.
- Every run appends to [`fetch_log.csv`](fetch_log.csv).

## Known defects of production objects

Taken over unchanged and to be corrected in the repository copy:

- `o:szd.korrespondenzen.judischer-jugendverein` and `o:szd.korrespondenzen.judischer-jugendverein-dusseldorf` are two objects for the same body, and both name the obsolete PID `o:szd.korrespondenzen.judischer-jugendverein-(dusseldorf)`.
- `o:szd.korrespondenzen.rascher-und-cie` carries the content of another konvolut (`alberts-margot`) and no PID of its own.

The three konvolute of the staging package of 2026-09-23 (`berger-gisela-von`, `ferencak-mirko`, `oppeln-bronikowski-friedrich-von`) came from that package, not from production, whose objects carry placeholder titles.

## Superseded objects

`berger-gisela`, `oppeln-bronikowski-friedrich` and `ferencak-mirko-m.` are replaced by the merged Konvolute `berger-gisela-von`, `oppeln-bronikowski-friedrich-von` and `ferencak-mirko`. They came in with the first import run, were removed again on 2026-09-24 and are skipped by `SUPERSEDED` in the script until the operator deletes them on GAMS.

## Usage

```bash
python scripts/konvolute_import/fetch_konvolute.py          # dry run, lists missing konvolute
python scripts/konvolute_import/fetch_konvolute.py --apply  # download and write
```
