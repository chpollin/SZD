# Repair IIIF structure labels

The three GAMS manifests below failed JSON parsing on 11 September 2026 because
`sdef:IIIF/getManifest` inserts straight quotes from book `div/@type` into range
labels without JSON escaping. The local book sources reproduce every offending
label. The prepared copies replace only those quotation pairs with typographic
quotes. Their other bytes, including metadata and image references, are preserved.

| Object | Prepared source | Changed labels | Pages |
|---|---|---:|---:|
| `o:szd.174` | [Result_SZ_AP2_L_S1.1.xml](prepared/Result_SZ_AP2_L_S1.1.xml) | 1 | 122 |
| `o:szd.67` | [Result_SZ_AAP_L2.xml](prepared/Result_SZ_AAP_L2.xml) | 1 | 237 |
| `o:szd.314` | [Result_SZ_AP2_W_G104.1.xml](prepared/Result_SZ_AP2_W_G104.1.xml) | 4 | 55 |

[repairs.json](prepared/repairs.json) records the exact replacements and SHA-256
checksums of each original and prepared file. The rule for ingest sources that follows
from the defect is in
[`knowledge/COLLECTIONS.md`](../../knowledge/COLLECTIONS.md#iiif-structure-labels-in-book-sources).

The archive checkup of September 2026 found four further objects with the same defect,
`o:szd.939`, `o:szd.2935`, `o:szd.2409` and `o:szd.2291`. Their prepared sources lie in
the same folder, recorded in
[repairs-checkup-2026-09.json](prepared/repairs-checkup-2026-09.json), and were produced
by [`scripts/checkup_2026_09_index/prepare_iiif_repairs.py`](../checkup_2026_09_index/README.md#prepare_iiif_repairspy),
which reuses `prepare_source` from this script. The ingest procedure below applies to
them as well. None of the prepared sources has been ingested yet.

## Reproduce

`prepare_repairs.py` is a standalone Python 3.11+ script with no dependencies.
Run from the repository root with the source tree and a separate output directory:

```powershell
uv run scripts/iiif_structure_labels/prepare_repairs.py --source-root C:/Users/Chrisi/Documents/PROJECTS/szd/done --out-dir scripts/iiif_structure_labels/prepared
```

Plain `python` works with the same arguments. The script requires exactly one
source per filename, the recorded PID, page count and quoted labels. It rejects
unexpected input or differing existing output. A repeated run keeps identical
output files. It never edits the source tree or contacts GAMS.

## Verification

Both the original and prepared XML parsed strictly. A structural comparison
allowed only the listed `div/@type` changes. Two preparation runs produced
byte-identical XML and reports. Wrong PIDs and unexpected labels were rejected.

The three live manifests were retrieved and parsed locally. All failed at an
unescaped structure label. Applying the exact listed label replacements to copies
of those responses made all three valid JSON, with 122, 237 and 55 canvases
respectively. This verifies the identified escaping defect and the prepared
workaround. The files have not been ingested, and post-ingest viewer behaviour
remains to be checked. The shared manifest generator belongs to GAMS and is
outside this data repository.

## Manual ingest

The relative JPEG references still point into the original source directories.
Use each prepared XML beside its existing images, preserving the existing PID:

| Prepared filename | Original directory below `C:/Users/Chrisi/Documents/PROJECTS/szd/done/` |
|---|---|
| `Result_SZ_AP2_L_S1.1.xml` | `Lebensdokumente/10/SZ_AP2_L_S1.1/SZ_AP2_L_S1.1/` |
| `Result_SZ_AAP_L2.xml` | `Lebensdokumente/1/SZ_AAP_L2/` |
| `Result_SZ_AP2_W_G104.1.xml` | `Werke/12/SZ_AP2_W_G104.1/` |

1. Compare the original file's SHA-256 with `sourceSha256` in `repairs.json`. If it
   differs, recheck the later source changes before replacing anything. Preserve
   the original XML as a backup outside the ingest directory, then place the
   corresponding prepared XML beside the existing images.
2. Re-ingest these book sources through Cirilo into their existing objects
   `o:szd.174`, `o:szd.67` and `o:szd.314`, using the established book workflow.
3. Fetch each `https://gams.uni-graz.at/<PID>/sdef:IIIF/getManifest`, require valid
   JSON and the canvas count listed above, then open its Mirador view and check
   the corrected structure labels and images.

The durable server repair is correct JSON escaping of every range label in the
GAMS manifest generator. The prepared sources provide the documented workaround
while that generator remains unchanged.
