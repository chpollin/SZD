# Stefan Zweig Digital Archive - Complete Documentation

**Version:** 1.0.0
**Date:** October 22, 2025
**Zenodo DOI:** [10.5281/zenodo.XXXXXX](https://doi.org/10.5281/zenodo.XXXXXX)
**Project:** https://stefanzweig.digital

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Archive Contents](#archive-contents)
3. [Technical Specifications](#technical-specifications)
4. [Installation & Usage](#installation--usage)
5. [Data Quality](#data-quality)
6. [FAIR Compliance](#fair-compliance)
7. [Metadata](#metadata)
8. [Versioning Strategy](#versioning-strategy)
9. [Project Timeline](#project-timeline)
10. [Contributors](#contributors)

---

## Project Overview

### Purpose

Complete backup and long-term preservation of the Stefan Zweig Digital collection from GAMS (Geisteswissenschaftliches Asset Management System, University of Graz) for archival purposes on Zenodo.

### Results

- **2,107 digitized objects** (99.0% complete)
- **18,719 high-resolution images** (4912×7360 pixels, JPEG)
- **24.7 GB uncompressed** (22.3 GB compressed)
- **4 collections:** Facsimiles, Essays, Life Documents, Correspondence
- **FAIR-compliant metadata:** 92% score

### Institutions

- **Literaturarchiv Salzburg** - Original materials holder and digitization
- **GAMS, University of Graz** - Digital infrastructure and hosting
- **Digital Humanities Craft OG** - Technical implementation

---

## Archive Contents

### Collections

| Collection | Objects | Complete | Incomplete | Success Rate |
|------------|---------|----------|------------|--------------|
| **Facsimiles** | 169 | 161 | 8 | 95.3% |
| **Essays (Aufsatz)** | 625 | 619 | 6 | 99.0% |
| **Life Documents** | 127 | 123 | 4 | 96.9% |
| **Correspondence** | 1,186 | 1,182 | 4 | 99.7% |
| **TOTAL** | **2,107** | **2,085** | **22** | **99.0%** |

### File Structure

```
stefan-zweig-digital-v1.0.0/
├── data/                              # 24.7 GB
│   ├── facsimiles/                    # 169 objects
│   │   └── o_szd_XXX/
│   │       ├── mets.xml               # METS/MODS metadata
│   │       ├── metadata.json          # Parsed JSON
│   │       └── images/
│   │           ├── IMG_1.jpg
│   │           └── ...
│   ├── aufsatz/                       # 625 objects
│   ├── lebensdokumente/               # 127 objects
│   └── korrespondenzen/               # 1,186 objects
│
├── metadata/
│   └── container_metadata/            # 4 XML files
│       ├── context_szd_facsimiles.xml
│       ├── context_szd_facsimiles_aufsatz.xml
│       ├── context_szd_facsimiles_lebensdokumente.xml
│       └── context_szd_facsimiles_korrespondenzen.xml
│
├── logs/
│   ├── download_progress.json         # Progress tracking (2,107 objects)
│   └── validation_report.json         # Validation results
│
└── docs/
    ├── README.md
    ├── CHANGELOG.md
    ├── CITATION.cff
    ├── DATA_QUALITY_ISSUES.md
    ├── ZENODO_VERSIONING_STRATEGY.md
    └── FAIR_COMPLIANCE.md
```

---

## Technical Specifications

### Images

- **Format:** JPEG
- **Resolution:** Typically 4912×7360 pixels
- **Color Space:** RGB
- **Average Size:** 1-2 MB per image
- **Total Images:** 18,719

### Metadata Standards

- **METS/MODS:** Metadata Encoding & Transmission Standard
- **DFG-METS:** Deutsche Forschungsgemeinschaft standard
- **DataCite:** Metadata Schema 4.0 (Zenodo)
- **Citation File Format:** CITATION.cff included

### Archive Format

- **Compression:** tar.gz (gzip)
- **Uncompressed:** 24.7 GB
- **Compressed:** 22.3 GB
- **Compression Ratio:** ~10% reduction

---

## Installation & Usage

### Prerequisites

```bash
Python 3.11+
pip
Internet connection
```

### Installation

```bash
git clone https://github.com/YOUR_ORG/szd-backup.git
cd szd-backup
pip install -r requirements.txt
```

### Scripts

#### 1. fetch_metadata.py

Download container metadata from GAMS.

```bash
python scripts/fetch_metadata.py
```

**Output:** `metadata/container_metadata/*.xml`

#### 2. download_archive.py

Main download script with resume capability.

```bash
python scripts/download_archive.py
```

**Features:**
- Rate limiting (1.5s between images, 2s between objects)
- Resume capability via `logs/download_progress.json`
- Automatic retry on failures (max 3 attempts)
- Progress tracking

**Configuration:**
- `TEST_MODE = False` (set in script for full download)
- `DELAY_BETWEEN_IMAGES = 1.5` seconds
- `DELAY_BETWEEN_OBJECTS = 2.0` seconds
- `MAX_RETRIES = 3`

#### 3. validate_downloads.py

Validate completeness against METS specifications.

```bash
python scripts/validate_downloads.py
```

**Checks:**
- METS files present
- metadata.json present
- Image count matches METS
- No corrupted files

**Output:** `logs/validation_report.json`

#### 4. zenodo_upload_simple.py

Upload archive to Zenodo.

```bash
# Test on Sandbox
python scripts/zenodo_upload_simple.py --sandbox --token YOUR_SANDBOX_TOKEN

# Upload to Production (draft)
python scripts/zenodo_upload_simple.py --token YOUR_PROD_TOKEN

# Upload and publish
python scripts/zenodo_upload_simple.py --token YOUR_PROD_TOKEN --publish
```

---

## Data Quality

### Known Limitations

**22 objects (1.0%) incomplete** due to server-side METS metadata issues.

**729 images (3.7%) missing** - referenced in METS but not available on source server.

### Most Affected Objects

| Object ID | Missing Images | Total Expected | % Missing |
|-----------|----------------|----------------|-----------|
| o:szd.939 | 328 | 427 | 76.8% |
| o:szd.268 | 230 | 321 | 71.7% |
| o:szd.267 | 125 | 232 | 53.9% |

**Root Cause:** Invalid URLs or non-existent resources in source METS metadata.

**Impact:** All available images successfully archived. Missing images are source-side issues, not download errors.

**Detailed Analysis:** See [docs/DATA_QUALITY_ISSUES.md](docs/DATA_QUALITY_ISSUES.md)

---

## FAIR Compliance

### FAIR Score: 92%

| Principle | Score | Status |
|-----------|-------|--------|
| **Findable** | 100% | ✅ |
| **Accessible** | 100% | ✅ |
| **Interoperable** | 83% | ✅ |
| **Reusable** | 100% | ✅ |

### Key FAIR Features

**F - Findable:**
- ✅ Persistent DOI (Zenodo Concept + Version DOIs)
- ✅ ORCID IDs for all creators
- ✅ GND identifier: https://d-nb.info/gnd/118637479
- ✅ Wikidata: https://www.wikidata.org/wiki/Q78491
- ✅ OECD subject classification

**A - Accessible:**
- ✅ Open Access via Zenodo
- ✅ HTTPS protocol
- ✅ Metadata accessible even if data unavailable

**I - Interoperable:**
- ✅ METS/MODS (standardized XML)
- ✅ DFG-METS standard
- ✅ DataCite Metadata Schema
- ✅ Controlled vocabularies (GND, Wikidata)

**R - Reusable:**
- ✅ Clear license: CC-BY 4.0
- ✅ Detailed provenance
- ✅ Community standards (DFG-METS)
- ✅ Contact information

**Detailed Analysis:** See [docs/FAIR_COMPLIANCE.md](docs/FAIR_COMPLIANCE.md)

---

## Metadata

### Creators

1. **Zangerl, Lina Maria** ([ORCID: 0000-0001-9709-3669](https://orcid.org/0000-0001-9709-3669))
   - Literaturarchiv Salzburg, Paris Lodron Universität Salzburg

2. **Glunk, Julia Rebecca** ([ORCID: 0000-0001-6647-9729](https://orcid.org/0000-0001-6647-9729))
   - Literaturarchiv Salzburg, Paris Lodron Universität Salzburg

3. **Matuschek, Oliver**
   - Literaturarchiv Salzburg, Paris Lodron Universität Salzburg

4. **Pollin, Christopher** ([ORCID: 0000-0002-4879-129X](https://orcid.org/0000-0002-4879-129X))
   - Digital Humanities Craft OG

### License

- **Code/Scripts:** MIT License
- **Data:** CC-BY 4.0 (Creative Commons Attribution 4.0 International)

### Identifiers

- **Zenodo DOI:** 10.5281/zenodo.XXXXXX (to be updated)
- **GND (Stefan Zweig):** https://d-nb.info/gnd/118637479
- **Wikidata:** https://www.wikidata.org/wiki/Q78491
- **Source Collection:** https://gams.uni-graz.at/context:szd
- **Project Website:** https://stefanzweig.digital

### Temporal Coverage

- **Content Creation:** 1881-1942 (Stefan Zweig's lifetime)
- **Digitization:** 2017-2025 (Literaturarchiv Salzburg)
- **Archive Creation:** October 22, 2025

### Geographic Coverage

- **Location:** Salzburg, Austria
- **Institution:** Literaturarchiv Salzburg, Paris Lodron Universität Salzburg

---

## Versioning Strategy

### Current Version: 1.0.0

### Semantic Versioning (MAJOR.MINOR.PATCH)

**MAJOR (x.0.0):** Breaking changes
- Complete restructuring
- Metadata format changes
- Incompatible structural changes

**MINOR (1.x.0):** Feature updates
- New containers added
- Significant object additions (>50)
- New metadata fields
- Improved image quality

**PATCH (1.0.x):** Bug fixes
- Missing images corrected
- Metadata corrections
- Small object additions (<50)

### Future Update Scenarios

**v1.0.1 - Patch Update:**
- Missing images from o:szd.267, o:szd.268, o:szd.939 become available
- Metadata corrections
- Individual object updates

**v1.1.0 - Minor Update:**
- New objects added to existing containers
- Additional metadata fields
- Improved documentation

**v2.0.0 - Major Update:**
- New METS format
- Complete re-download
- Structural changes

**Detailed Strategy:** See [docs/ZENODO_VERSIONING_STRATEGY.md](docs/ZENODO_VERSIONING_STRATEGY.md)

---

## Project Timeline

### Phase 1: Planning & Setup (Oct 19-20, 2025)
- Project scope defined
- Scripts developed
- Infrastructure tested

### Phase 2: Download (Oct 20-22, 2025)
- **Duration:** 48 hours
- **Start:** Oct 20, 19:43
- **End:** Oct 22, 18:06
- **Throughput:** 8-12 objects/hour
- **Result:** 2,107 objects, 18,719 images, 24.7 GB

### Phase 3: Validation (Oct 22, 2025)
- Complete validation against METS
- 99.0% success rate confirmed
- Data quality issues documented

### Phase 4: Archive Creation (Oct 22, 2025)
- **Duration:** ~2.5 hours
- **Compression:** 24.7 GB → 22.3 GB
- **Format:** tar.gz

### Phase 5: Zenodo Upload (Oct 22, 2025)
- FAIR metadata prepared (92% compliance)
- Sandbox test successful
- Production upload initiated

---

## Contributors

### Project Team

**Creators:**
- Lina Maria Zangerl (Literaturarchiv Salzburg)
- Julia Rebecca Glunk (Literaturarchiv Salzburg)
- Oliver Matuschek (Literaturarchiv Salzburg)
- Christopher Pollin (Digital Humanities Craft OG)

**Institutions:**
- Literaturarchiv Salzburg - Original materials, digitization
- GAMS, University of Graz - Digital infrastructure, hosting
- Digital Humanities Craft OG - Technical implementation

### Contact

- **Email:** info@stefanzweig.digital
- **Website:** https://stefanzweig.digital
- **GAMS:** https://gams.uni-graz.at/context:szd

---

## Citation

### Recommended Citation

```
Zangerl, L. M., Glunk, J. R., Matuschek, O., & Pollin, C. (2025).
Stefan Zweig Digital - Complete Archive Backup (v1.0.0) [Data set].
Zenodo. https://doi.org/10.5281/zenodo.XXXXXX
```

### BibTeX

```bibtex
@dataset{szd_archive_2025,
  author    = {Zangerl, Lina Maria and
               Glunk, Julia Rebecca and
               Matuschek, Oliver and
               Pollin, Christopher},
  title     = {Stefan Zweig Digital - Complete Archive Backup},
  year      = {2025},
  publisher = {Zenodo},
  version   = {v1.0.0},
  doi       = {10.5281/zenodo.XXXXXX},
  url       = {https://doi.org/10.5281/zenodo.XXXXXX}
}
```

See [CITATION.cff](CITATION.cff) for machine-readable citation information.

---

## Additional Resources

### Documentation

- **README.md** - Quick start guide
- **CHANGELOG.md** - Version history
- **DATA_QUALITY_ISSUES.md** - Known limitations
- **ZENODO_VERSIONING_STRATEGY.md** - Version management
- **FAIR_COMPLIANCE.md** - FAIR principles analysis
- **ARCHIVE_DOCUMENTATION.md** - Original detailed docs

### External Links

- **Stefan Zweig Digital:** https://stefanzweig.digital
- **GAMS Collection:** https://gams.uni-graz.at/context:szd
- **Zenodo Deposit:** https://doi.org/10.5281/zenodo.XXXXXX
- **GND Entry:** https://d-nb.info/gnd/118637479
- **Wikidata:** https://www.wikidata.org/wiki/Q78491

---

## Technical Notes

### Download Process

- **Method:** Automated Python scripts
- **Rate Limiting:** Server-friendly (1.5s between images)
- **Resume:** Checkpoint-based via JSON
- **Validation:** Complete METS cross-check
- **Error Handling:** 3 retry attempts per file
- **Logging:** Comprehensive download.log

### System Requirements

**For Download:**
- Python 3.11+
- 30 GB free disk space
- Stable internet (48h runtime)
- 4 GB RAM minimum

**For Archive:**
- 50 GB free disk space (archive + data)
- tar/gzip tools

---

## Acknowledgments

This archive was created using data from:
- **Literaturarchiv Salzburg** - Collection ownership and curation
- **GAMS, University of Graz** - Digital infrastructure and hosting
- **Stefan Zweig Digital Project** - Digitization coordination

Special thanks to all institutions and individuals who made Stefan Zweig's works freely available under CC-BY license, enabling research and preservation.

---

**Documentation Version:** 1.0
**Last Updated:** October 22, 2025
**Status:** Production
**Zenodo Upload:** In Progress (Deposit ID: 17418961)
