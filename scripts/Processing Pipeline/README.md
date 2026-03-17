# SZD Pipeline

Unified processing pipeline for the Stefan Zweig Digital Archive (Literaturarchiv Salzburg).

Converts Lightroom scan exports into METS viewer XML files (`Result_*.xml`) for the GAMS viewer at `gams.uni-graz.at`, using metadata from a CSV file provided by colleagues and an XSLT stylesheet.

---

## Overview

```text
Lightroom export
      │
      ▼
 1. sort         Normalize filenames, sort TIFF/RAW into subfolders
      │
      ▼
 2. generate     CSV metadata → intermediate XML, written into each signature folder
      │
      ▼
  ── MANUAL ──   Open each XML, fill in the page number ranges for each section
      │
      ▼
 3. transform    Validates XMLs, then applies XSLT → final METS viewer XML (Result_*.xml)

 status          Check the current stage of every folder at any point
```

All steps are subcommands of a single script:

```bash
python szd_pipeline.py <step> [options]
```

---

## Prerequisites

```bash
pip install pandas saxonche
```

- **pandas** — used in the `generate` step to read the CSV file
- **saxonche** — Saxon-C Python wrapper, required only for the `transform` step

---

## Folder structure

Each letter has its own signature folder under the base directory:

```text
<base-dir>/
├── SZ_AAL_B2.1/
│   ├── SZ_AAL_B2.1_001.jpg       ← regular scan pages (stay in root)
│   ├── SZ_AAL_B2.1_002.jpg
│   ├── SZ_AAL_B2.1_003.jpg
│   ├── SZ_AAL_B2.1_TIFF/         ← created by sort
│   │   └── SZ_AAL_B2.1_001.tif
│   ├── SZ_AAL_B2.1_RAW/          ← created by sort
│   │   └── SZ_AAL_B2.1_RAW_001.jpg
│   ├── SZ_AAL_B2.1.xml           ← created by generate, edited manually
│   └── Result_SZ_AAL_B2.1.xml    ← created by transform (final output)
├── SZ_AAL_B2.2/
│   └── ...
```

---

## Step 1 — `sort`

**When:** Right after exporting scans from Lightroom.

Normalizes all filenames to 3-digit numbering (`1` → `001`, `22` → `022`, etc.) and moves files into type subfolders:

| File type | Destination |
| --- | --- |
| `*.tif`, `*.tiff` | `<signature>_TIFF/` subfolder |
| `*_RAW_*.jpg` | `<signature>_RAW/` subfolder |
| Regular `*.jpg` | Stays in the signature folder root |

**Defaults to dry-run** — no files are changed until you add `--apply`.

```bash
# Preview what would happen (safe, no changes)
python szd_pipeline.py sort --root ./scans --series SZ_AAL_B2

# Apply changes
python szd_pipeline.py sort --root ./scans --series SZ_AAL_B2 --apply

# Process a single folder only
python szd_pipeline.py sort --root ./scans --series SZ_AAL_B2 --folder SZ_AAL_B2.5 --apply
```

| Argument | Default | Description |
| --- | --- | --- |
| `--root DIR` | `.` | Root directory containing the signature folders |
| `--series PREFIX` | `SZ_AAL_B2` | Signature series prefix (e.g. `SZ_AAL_B1`, `SZ_AAL_B2`) |
| `--folder NAME` | *(all)* | Process only this one subfolder |
| `--apply` | *(dry-run)* | Actually apply changes; without this flag nothing is modified |

---

## Step 2 — `generate`

**When:** After the colleague provides the updated CSV metadata file.

Reads the CSV and generates one intermediate XML file per letter, written directly into the matching signature folder. Skips rows whose signature folder does not exist yet, and skips XMLs that already exist.

```bash
python szd_pipeline.py generate metadata.csv --base-dir ./scans

# Preview without writing any files
python szd_pipeline.py generate metadata.csv --base-dir ./scans --dry-run

# Limit to the first 10 rows (useful for testing)
python szd_pipeline.py generate metadata.csv --base-dir ./scans --batch 10
```

| Argument | Default | Description |
| --- | --- | --- |
| `csv_file` | *(required)* | Path to the CSV metadata file |
| `--base-dir DIR` | *(required)* | Root directory containing the signature folders |
| `--batch N` | `0` (all) | Process only the first N rows |
| `--dry-run` | off | Preview which XMLs would be created without writing any files |

**Expected CSV columns:**

| Column | Content |
| --- | --- |
| `Signatur SPÄTER FELD AF!!` | Signature, e.g. `SZ-AAL/B2.1` |
| `Verfasser*in` | Sender, in `Last, First` format |
| `Adressat*in` | Recipient, in `Last, First` format |
| `Datum normalisiert` | Date in `YYYY-MM-DD`, `YYYY-MM`, or `YYYY` format |

**Generated XML structure:**

```xml
<root>
  <author>Zweig, Stefan</author>
  <contributor>Zweig, Lotte</contributor>
  <titel>Brief von Stefan Zweig an Lotte Zweig [1. Mai 1934], SZ-AAL/B2.1</titel>
  <signatur>SZ-AAL/B2.1</signatur>
  <datum>1934-05-01</datum>
  <filename>SZ_AAL_B2.1_</filename>
  <category></category>
  <structure>
    <chapter>
      <title>Textseiten</title>
      <from></from>   ← fill in manually
      <to></to>       ← fill in manually
    </chapter>
    <chapter>
      <title>Farbreferenz</title>
      <from></from>   ← fill in manually
      <to></to>       ← fill in manually
    </chapter>
  </structure>
</root>
```

---

## Manual step — fill in page numbers

**Before running `transform`**, open each `<signature>.xml` and fill in the `<from>` and `<to>` values for each chapter section.

These correspond to the scan page numbers (as integers). The XSLT uses them to generate the list of `<page xlink:href="...">` entries.

**Example:** if `Textseiten` covers pages 1–4 and `Farbreferenz` is page 5:

```xml
<chapter>
  <title>Textseiten</title>
  <from>1</from>
  <to>4</to>
</chapter>
<chapter>
  <title>Farbreferenz</title>
  <from>5</from>
  <to>5</to>
</chapter>
```

Check the JPG files in the folder to determine the correct page ranges.

---

## Step 3 — `transform`

**When:** After all XMLs have been reviewed and page numbers filled in.

Before running the XSLT, the script **validates every XML** automatically. It checks that all `<from>` and `<to>` values are filled in as integers, and that every referenced JPG file actually exists in the folder. If any folder fails validation, the transformation is aborted and the issues are listed — so nothing gets transformed until everything is correct.

After a successful transformation, source XMLs are deleted (use `--no-delete` to keep them).

The XSLT also fetches remote TEI sources from `stefanzweig.digital` to resolve `<relation>` links — an internet connection is required.

```bash
python szd_pipeline.py transform --base-dir ./scans --xslt szd-JPGtoMETS.xsl

# Transform only one folder (e.g. after fixing a single XML)
python szd_pipeline.py transform --base-dir ./scans --xslt szd-JPGtoMETS.xsl --folder SZ_AAL_B2.5

# Keep source XMLs after transformation
python szd_pipeline.py transform --base-dir ./scans --xslt szd-JPGtoMETS.xsl --no-delete
```

| Argument | Default | Description |
| --- | --- | --- |
| `--base-dir DIR` | *(required)* | Directory containing the signature subfolders |
| `--xslt FILE` | *(required)* | Path to the XSLT stylesheet |
| `--folder NAME` | *(all)* | Transform only this one folder |
| `--no-delete` | off | Keep source XML after transformation instead of deleting it |

Folders are skipped if:

- `Result_<signature>.xml` already exists
- No `<signature>.xml` input file is found

---

## `status` — check pipeline progress

Run at any time to see where each folder stands:

```bash
python szd_pipeline.py status --base-dir ./scans
python szd_pipeline.py status --base-dir ./scans --series SZ_AAL_B1
```

Each folder is classified into one of these stages:

| Stage | Meaning |
| --- | --- |
| `✓ done` | `Result_*.xml` exists — fully processed |
| `◉ ready` | XML exists and all page numbers are filled in — ready to transform |
| `✎ needs review` | XML exists but page numbers are still empty |
| `○ no xml` | JPGs present but no XML generated yet |
| `! no jpgs` | Folder exists but contains no JPG files |

A summary count is printed at the end.

---

## Full example

```bash
# 1. Sort after Lightroom export (dry-run first, then apply)
python szd_pipeline.py sort --root C:/Scans/SZ_AAL_B2 --series SZ_AAL_B2
python szd_pipeline.py sort --root C:/Scans/SZ_AAL_B2 --series SZ_AAL_B2 --apply

# Check status after sorting
python szd_pipeline.py status --base-dir C:/Scans/SZ_AAL_B2

# 2. Preview XML generation, then run for real
python szd_pipeline.py generate C:/Metadata/SZ_AAL_B2.csv --base-dir C:/Scans/SZ_AAL_B2 --dry-run
python szd_pipeline.py generate C:/Metadata/SZ_AAL_B2.csv --base-dir C:/Scans/SZ_AAL_B2

# Check which folders still need page numbers filled in
python szd_pipeline.py status --base-dir C:/Scans/SZ_AAL_B2

# -- manually review and fill in page ranges in each XML --

# 3. Transform to METS
python szd_pipeline.py transform \
  --base-dir C:/Scans/SZ_AAL_B2 \
  --xslt C:/Repos/SZ_AAL_B2_Results/szd-JPGtoMETS.xsl
```

---

## Output

The final output for each letter is `Result_<signature>.xml`, a METS-style viewer XML in the format expected by the GAMS viewer:

```xml
<book xmlns="http://gams.uni-graz.at/viewer" xmlns:xlink="http://www.w3.org/1999/xlink">
  <title>Brief von Stefan Zweig an Lotte Zweig [1. Mai 1934], SZ-AAL/B2.1</title>
  <author>Zweig, Stefan</author>
  <date>1.5.1934</date>
  <category/>
  <owner>
    <name>Literaturarchiv Salzburg, https://stefanzweig.digital, CC-BY</name>
  </owner>
  <structure>
    <div type="Textseiten">
      <page xlink:href="SZ_AAL_B2.1_001.jpg"/>
      <page xlink:href="SZ_AAL_B2.1_002.jpg"/>
    </div>
    <div type="Farbreferenz">
      <page xlink:href="SZ_AAL_B2.1_003.jpg"/>
    </div>
  </structure>
</book>
```
