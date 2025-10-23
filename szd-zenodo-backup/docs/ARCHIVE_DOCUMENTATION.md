# Stefan Zweig Digital - Archive Backup

**Complete archive of digital facsimiles from the Stefan Zweig Digital collection**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## Overview

This archive contains a complete backup of digital facsimiles from the **Stefan Zweig Digital** collection, hosted by the Literaturarchiv Salzburg and made available through GAMS (Geisteswissenschaftliches Asset Management System) at the University of Graz.

The collection includes manuscripts, correspondence, essays, and biographical documents from the Austrian writer **Stefan Zweig (1881-1942)**, one of the most widely read authors of the early 20th century.

### Collection Statistics

- **Total Objects**: 2,107
- **Complete Objects**: 2,085 (99.0%)
- **Total Images**: 18,719 high-resolution scans
- **Image Resolution**: 4912 x 7360 pixels (JPEG)
- **Archive Date**: October 22, 2025
- **Data Size**: 24.7 GB
- **Version**: 1.0.0

### Source Information

- **Institution**: Literaturarchiv Salzburg
- **Platform**: GAMS, University of Graz
- **Website**: https://stefanzweig.digital
- **License**: CC-BY (Creative Commons Attribution)
- **Rights Holder**: Literaturarchiv Salzburg

---

## Archive Structure

```
szd-backup/
│
├── README.md                          # This file
├── LICENSE.txt                        # CC-BY license
├── data.md                            # Detailed technical documentation
│
├── metadata/                          # Container metadata
│   ├── context_szd_facsimiles.xml
│   ├── context_szd_facsimiles_aufsatz.xml
│   ├── context_szd_facsimiles_lebensdokumente.xml
│   ├── context_szd_facsimiles_korrespondenzen.xml
│   └── object_ids_summary.txt
│
├── data/                              # Main archive data
│   ├── facsimiles/                    # 169 objects
│   ├── aufsatz/                       # 625 objects (Essays)
│   ├── lebensdokumente/               # 127 objects (Life documents)
│   └── korrespondenzen/               # 1,186 objects (Correspondence)
│
├── logs/                              # Download logs and progress tracking
│   ├── download_progress.json
│   └── validation_report.json
│
└── scripts/                           # Archive creation scripts
    ├── fetch_metadata.py
    ├── download_archive.py
    └── validate_downloads.py
```

### Data Organization

Each object is organized in its own folder with the following structure:

```
data/{container}/{object_id}/
├── mets.xml              # Original METS metadata
├── metadata.json         # Parsed metadata (human-readable)
└── images/
    ├── IMG_1.jpg
    ├── IMG_2.jpg
    └── ...
```

---

## Collection Contents

### 1. Facsimiles (169 objects)
Main facsimile collection including various manuscripts and documents.

**Completeness**: 161/169 complete (95.3%)

### 2. Aufsatz - Essays (625 objects)
Collection of Stefan Zweig's essays and articles in manuscript form.

**Completeness**: 619/625 complete (99.0%)

**Notable works include**:
- Literary essays on Goethe, Hölderlin, Tolstoy
- Historical essays
- Cultural criticism

### 3. Lebensdokumente - Life Documents (127 objects)
Biographical materials and personal documents.

**Completeness**: 123/127 complete (96.9%)

**Contents**:
- Personal correspondence
- Travel documents
- Official papers
- Photographs

### 4. Korrespondenzen - Correspondence (1,186 objects)
Extensive collection of letters and correspondence.

**Completeness**: 1,182/1,186 complete (99.7%)

**Correspondents include**:
- Fellow writers and intellectuals
- Publishers
- Friends and family
- Political figures

---

## Metadata

Each object includes comprehensive metadata in both METS/MODS XML format and a simplified JSON format.

### Metadata Fields

- **Object ID**: Unique identifier (e.g., o:szd.199)
- **URN**: Persistent identifier (info:fedora/o:szd.XXX)
- **Title**: Document title
- **Signature**: Archive signature (e.g., SZ-AAP/W20.1)
- **Author**: Stefan Zweig
- **Language**: German (Deutsch) - de
- **Created Date**: Object creation date in GAMS
- **Modified Date**: Last modification date
- **Owner**: Literaturarchiv Salzburg
- **Rights**: CC-BY
- **Image Count**: Number of page scans
- **Image Information**: URLs, dimensions, order

### Example Metadata (JSON)

```json
{
  "object_id": "o:szd.199",
  "urn": "info:fedora/o:szd.199",
  "title": "Goethe und Hölderlin",
  "signature": "SZ-AAP/W20.1",
  "author": "Zweig, Stefan",
  "language": "de",
  "language_text": "Deutsch",
  "created": "2024-07-20T09:29:25.456Z",
  "modified": "2024-08-06T16:35:20.506Z",
  "owner": "Literaturarchiv Salzburg",
  "rights": "CC-BY",
  "image_count": 13,
  "images": [...]
}
```

---

## Using This Archive

### Browsing the Collection

1. Navigate to the `data/` directory
2. Choose a container (facsimiles, aufsatz, lebensdokumente, or korrespondenzen)
3. Each object folder contains:
   - `metadata.json` - Quick overview of the object
   - `mets.xml` - Full METS metadata
   - `images/` - All page scans in order

### Searching

The archive includes several ways to search:

1. **By Object ID**: Check `metadata/object_ids_summary.txt`
2. **By Title**: Search through `metadata.json` files
3. **Full-text search**: Use tools like `jq` or custom scripts on JSON metadata

Example search for a specific title:
```bash
# Find all objects containing "Goethe" in the title
find data/ -name "metadata.json" -exec grep -l "Goethe" {} \;
```

### Validation

To verify the integrity and completeness of the archive:

```bash
python validate_downloads.py
```

This script checks:
- All METS files are present
- All metadata.json files are present
- Image counts match METS specifications
- No missing or corrupted files

---

## Technical Details

### Image Specifications

- **Format**: JPEG
- **Resolution**: 4912 x 7360 pixels (typically)
- **Color Space**: RGB
- **File Size**: ~1-2 MB per image (average)
- **DPI**: Suitable for high-quality reproduction and OCR

### METS Format

All objects use the **DFG-METS** (Deutsche Forschungsgemeinschaft - METS) data model, a standardized format for digital collections used by German research institutions.

**Namespace**: `info:fedora/cm:dfgMETS`

### Data Standards

- **METS**: Metadata Encoding & Transmission Standard (v1.x)
- **MODS**: Metadata Object Description Schema (v3.x)
- **DFG-Viewer**: Compliant metadata for German digital libraries
- **EXIF**: Embedded image metadata (dimensions)

---

## Scripts and Tools

This archive includes Python scripts used for creation and validation:

### 1. fetch_metadata.py

Downloads container metadata and extracts all object IDs from GAMS.

**Usage**:
```bash
python fetch_metadata.py
```

**Output**: `metadata/*.xml` and `metadata/object_ids_summary.txt`

### 2. download_archive.py

Main download script for METS and images.

**Features**:
- Rate limiting (server-friendly)
- Resume capability
- Progress tracking
- Error handling with retries
- Detailed logging

**Usage**:
```bash
# Test mode (10 objects per container)
python download_archive.py

# Full download (edit TEST_MODE = False in script)
python download_archive.py
```

**Configuration**:
- `TEST_MODE`: Set to `False` for full download
- `DELAY_BETWEEN_REQUESTS`: Adjust rate limiting (default: 1.5s)
- `MAX_RETRIES`: Number of retry attempts (default: 3)

### 3. validate_downloads.py

Validates completeness and integrity of downloaded data.

**Usage**:
```bash
python validate_downloads.py
```

**Checks**:
- METS files present
- metadata.json present
- Image count matches METS
- No missing images
- File sizes valid
- Cross-validation between METS and JSON

**Output**: Console summary and `logs/validation_report.json`

---

## Citation

If you use this archive in your research, please cite:

```
Stefan Zweig Digital Archive (2025).
Digital facsimiles from the Stefan Zweig Collection.
Literaturarchiv Salzburg.
Available through GAMS, University of Graz.
https://stefanzweig.digital
[Accessed: YYYY-MM-DD]
```

BibTeX:
```bibtex
@misc{szd_archive_2025,
  title = {Stefan Zweig Digital Archive},
  author = {{Literaturarchiv Salzburg}},
  year = {2025},
  url = {https://stefanzweig.digital},
  note = {Digital facsimiles, CC-BY license}
}
```

---

## License

This archive is licensed under **CC-BY 4.0** (Creative Commons Attribution 4.0 International).

**You are free to**:
- Share — copy and redistribute the material
- Adapt — remix, transform, and build upon the material
- For any purpose, even commercially

**Under the following terms**:
- **Attribution** — You must give appropriate credit to Literaturarchiv Salzburg and Stefan Zweig Digital, provide a link to the license, and indicate if changes were made.

Full license text: https://creativecommons.org/licenses/by/4.0/

### Original Rights Statement

```
Owner: Literaturarchiv Salzburg
Website: https://stefanzweig.digital
License: CC-BY
```

---

## Preservation Notes

### Archive Creation

- **Method**: Automated download via Python scripts
- **Date**: October 2025
- **Source URLs**: GAMS archive (gams.uni-graz.at)
- **Validation**: All downloads verified against METS specifications
- **Checksums**: See `checksums_sha256.txt` and `checksums_md5.txt`

### Data Integrity

To verify data integrity, checksums are provided:

```bash
# Verify SHA-256 checksums
sha256sum -c checksums_sha256.txt

# Verify MD5 checksums
md5sum -c checksums_md5.txt
```

### Format Migration

Original formats are preserved:
- METS XML (future-proof, standardized)
- JPEG images (widely supported)
- JSON metadata (human-readable, machine-parsable)

No proprietary formats are used.

---

## Contact & Support

### For questions about this archive:
- **Archive Creator**: [Your Contact Information]
- **Archive Date**: October 2025

### For questions about the collection:
- **Institution**: Literaturarchiv Salzburg
- **Website**: https://stefanzweig.digital
- **Platform**: GAMS, University of Graz
- **Email**: [Contact via website]

### For technical issues:
- Check `logs/download.log` for detailed information
- Run `validate_downloads.py` to diagnose problems
- Review `data.md` for technical documentation

---

## Acknowledgments

This archive was created using data from:

- **Literaturarchiv Salzburg** - Collection ownership and curation
- **GAMS (University of Graz)** - Digital infrastructure and hosting
- **Stefan Zweig Digital** - Project coordination and digitization

Special thanks to all institutions and individuals who made Stefan Zweig's works freely available under a CC-BY license, enabling research and preservation.

---

## Known Issues

**22 objects (1.0%) are incomplete** due to server-side metadata issues. 729 images (3.7% of total) referenced in METS files do not exist on the source server.

For detailed information about missing images and affected objects, see [DATA_QUALITY_ISSUES.md](DATA_QUALITY_ISSUES.md).

The most affected objects are:
- o:szd.939: 328 missing images
- o:szd.268: 230 missing images
- o:szd.267: 125 missing images

**Important**: These missing images are due to source data problems, not download errors. All available images have been successfully archived.

---

## Version History

- **v1.0.0** (October 22, 2025): Initial archive creation
  - 2,107 objects downloaded
  - 18,719 high-resolution images
  - 24.7 GB total size
  - 99.0% completeness rate
  - Complete METS metadata
  - Validation completed

---

## About Stefan Zweig

**Stefan Zweig** (1881-1942) was an Austrian novelist, playwright, journalist, and biographer. At the height of his literary career in the 1920s and 1930s, he was one of the most popular writers in the world.

**Notable works**:
- *The World of Yesterday* (autobiography)
- *Beware of Pity* (novel)
- *Chess Story* (novella)
- *Marie Antoinette* (biography)
- *Confusion* (novella)

Zweig was a passionate advocate for European unity and humanism. He fled Nazi-occupied Europe and eventually settled in Brazil, where he and his wife took their own lives in 1942.

His extensive correspondence, manuscripts, and personal papers preserved in this archive provide invaluable insight into European intellectual life during a tumultuous period of the 20th century.

---

## Further Reading

- **Stefan Zweig Digital**: https://stefanzweig.digital
- **GAMS**: https://gams.uni-graz.at
- **Literaturarchiv Salzburg**: https://www.literaturarchiv-salzburg.at
- **DFG-METS Guidelines**: [DFG Viewer Documentation]
- **CC-BY 4.0 License**: https://creativecommons.org/licenses/by/4.0/

---

*Last Updated: October 2025*

*This README is part of the Stefan Zweig Digital Archive preservation project.*
