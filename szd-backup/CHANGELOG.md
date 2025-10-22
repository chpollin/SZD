# Changelog - Stefan Zweig Digital Archive

All notable changes to this archive will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-10-22

### Initial Release

Complete backup of the Stefan Zweig Digital collection from GAMS (Geisteswissenschaftliches Asset Management System, University of Graz).

### Added

- **2,107 objects** across 4 containers downloaded and validated
- **18,719 high-resolution images** (JPEG format, ~4912x7360 pixels)
- **24.7 GB** of archival data
- Complete METS/MODS metadata for all objects
- JSON metadata files for human-readable access
- Comprehensive validation report

#### Containers

- `szd.facsimiles`: 169 objects (161 complete)
- `szd.facsimiles.aufsatz`: 625 objects (619 complete)
- `szd.facsimiles.lebensdokumente`: 127 objects (123 complete)
- `szd.facsimiles.korrespondenzen`: 1,186 objects (1,182 complete)

#### Documentation

- README.md with complete usage instructions
- DATA_QUALITY_ISSUES.md documenting known server-side problems
- ZENODO_VERSIONING_STRATEGY.md for future updates
- Validation report (logs/validation_report.json)
- Download progress tracking (logs/download_progress.json)

#### Scripts

- `fetch_metadata.py`: Download container metadata from GAMS
- `download_archive.py`: Main download script with resume capability
- `validate_downloads.py`: Validation and integrity checking
- `upload_to_zenodo.py`: Zenodo upload automation

### Known Issues

**22 objects (1.0%) incomplete** due to server-side metadata issues:

#### Critical Cases (>100 missing images)
- `o:szd.939`: 328 missing images (76.8% incomplete)
- `o:szd.268`: 230 missing images (71.7% incomplete)
- `o:szd.267`: 125 missing images (53.9% incomplete)

#### Minor Cases
- `facsimiles`: 5 additional objects with 1-2 missing images each
- `aufsatz`: 6 objects with 1-6 missing images each
- `lebensdokumente`: 4 objects with 1-6 missing images each
- `korrespondenzen`: 4 objects with 1-6 missing images each

**Total missing images**: 729 out of 19,448 (3.7%)

**Root cause**: Invalid URLs or non-existent resources in source METS metadata. See DATA_QUALITY_ISSUES.md for detailed analysis.

### Statistics

- **Success rate**: 99.0% (objects with all available images)
- **Downloaded images**: 18,719
- **Total download time**: ~48 hours (Oct 20-22, 2025)
- **Average download rate**: ~8-12 objects per hour
- **Data integrity**: 100% (all downloaded files validated)

### Technical Details

- **Source**: https://gams.uni-graz.at (University of Graz)
- **Collection**: Stefan Zweig Digital (https://stefanzweig.digital)
- **License**: CC-BY 4.0 (Creative Commons Attribution)
- **Metadata standard**: DFG-METS (Deutsche Forschungsgemeinschaft)
- **Download method**: Automated Python scripts with rate limiting
- **Resume capability**: Yes (via logs/download_progress.json)
- **Validation**: Complete cross-check against METS specifications

---

## [Unreleased]

### Planned

- Monitor source for updates quarterly
- Re-download if missing images become available on server
- Add OCR text layer if source provides it
- Create derivative formats (thumbnail collections, optimized web versions)

---

## Version History

- **1.0.0** (2025-10-22): Initial release with 2,107 objects

---

**Maintained by**: Archive Curator
**Last updated**: 2025-10-22
