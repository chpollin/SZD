# Validation Tools

TEI/CSV validation and data quality assurance scripts for the Stefan Zweig Digital correspondence corpus.

## Overview

These scripts validate, clean, and synchronize TEI-XML files against CSV catalogue data. They help maintain data quality across the 245+ correspondence partners and 2,200+ catalogue entries.

---

## Scripts

### Core Validation

#### `validate_tei_csv.py`
**Offline validator for Zweig correspondence corpus (TEI/CSV validation)**

- Validates TEI XML structure and content
- Cross-references with CSV catalogue metadata
- Checks for completeness and consistency
- Version: 0.7+ (updated April 2025)

**Usage:**
```bash
python validate_tei_csv.py
```

#### `validate_tei_against_csv.py`
**Compare CSV rows (authoritative) with corresponding <biblFull> in TEI files**

- CSV is treated as authoritative source
- Logs discrepancies between TEI and CSV
- Identifies missing or inconsistent data
- Generates detailed comparison reports

**Usage:**
```bash
python validate_tei_against_csv.py
```

---

### Data Cleaning

#### `clean_tei_with_csv.py`
**Align TEI <biblFull> nodes with catalogue data in CSV files**

- Removes duplicate entries
- Enforces proper ordering
- Synchronizes TEI with CSV data
- Preserves TEI structure while updating content

**Dependencies:** Requires `tei_csv_mapping.py`

**Usage:**
```bash
python clean_tei_with_csv.py
```

#### `fix_mojibake.py`
**Repair UTF-8 mojibake encoding issues**

- Fixes character encoding corruption
- Removes trailing context markers from titles
- Cleans empty identifiers
- Standardizes character encodings

**Usage:**
```bash
python fix_mojibake.py
```

---

### Data Extraction

#### `fetch_korrespondenzen.py`
**Extract signatures from TEI XMLs and link them to CSV records**

- Offline version (reads from local ./tei/ directory)
- Extracts all `<idno type="signature">` values
- Links signatures to CSV catalogue rows
- Generates correspondence dataset overview

**Current Status:** 127/259 signatures (49%) have CSV matches

**Usage:**
```bash
python fetch_korrespondenzen.py
```

**Output:** Logs signature extraction and CSV matching results

---

### Comparison Tools

#### `compare_tei_bodies.py`
**Compare text and attribute differences in <body> elements between two TEI folders**

- Compares two versions of TEI files
- Identifies text differences
- Tracks attribute changes
- Useful for version control and migration validation

**Usage:**
```bash
python compare_tei_bodies.py <folder1> <folder2>
```

---

### Configuration

#### `tei_csv_mapping.py`
**Define OrderedDict mapping between TEI elements and CSV columns**

- Shared configuration file
- Defines 41-column schema mapping
- Used by `clean_tei_with_csv.py` and other scripts
- See [../../docs/MAPPING.md](../../docs/MAPPING.md) for full schema

**Usage:** Import as module, not standalone script

```python
from tei_csv_mapping import get_mapping
mapping = get_mapping()
```

---

## Data Sources

### TEI XML Files
Location: Various collections in `../../data/Correspondence/`
- One TEI per correspondence partner
- Contains `<biblFull>` entries with signatures
- 245 partners, 13 missing (5%)

### CSV Catalogue Files
Location: `../data/*.csv` (6 files)
- `Other.csv` - Assorted single items
- `SZ_AAP_Reichner.csv` - Autograph Album Reichner
- `SZ_SAM_Meingast.csv` - Sammlung Meingast
- (3 additional CSV files)
- 2,200+ total rows

---

## Known Issues

See [../../docs/DATA.md](../../docs/DATA.md) for complete data quality documentation:

| Issue | Count | Status |
|-------|------:|--------|
| Missing TEI files | 13 partners (5%) | Needs investigation |
| TEI signatures lacking CSV | ~130 signatures | Needs cataloguing |
| `@bound="false"` contributors | 55 XML nodes | Treat as NULL |
| Non-ISO dates in CSV | 47 cells | Needs normalization |

---

## Dependencies

```
lxml
requests
beautifulsoup4
```

Install via:
```bash
pip install lxml requests beautifulsoup4
```

---

## Documentation

- **[DATA.md](../../docs/DATA.md)** - Correspondence corpus overview
- **[MAPPING.md](../../docs/MAPPING.md)** - Complete 41-column TEI-CSV schema
- **[Correspondence Preprocessing](../../data/Correspondence/preprocessing/)** - Collection-specific scripts

---

## Version History

- **v3.1** (April 2025) - Latest validation suite
- **v0.7** (April 2025) - Updated fetch_korrespondenzen.py
- **v0.4** (April 2025) - Offline validation mode

---

**Last Updated:** October 2025
**Maintainer:** Stefan Zweig Digital Team
