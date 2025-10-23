# Stefan Zweig Digital Archive - Backup Pipeline

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXX)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data License: CC BY 4.0](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Automated download and archival pipeline for the [Stefan Zweig Digital](https://stefanzweig.digital) collection from GAMS (Geisteswissenschaftliches Asset Management System, University of Graz).

## 📦 Complete Archive on Zenodo

**Full archive available at:** [DOI: 10.5281/zenodo.XXXXXX](https://doi.org/10.5281/zenodo.XXXXXX)

- **2,107 objects** across 4 collections
- **18,719 high-resolution images** (~4912×7360 pixels)
- **22.3 GB** compressed (24.7 GB uncompressed)
- **99.0% complete** (22 objects with known server-side issues)
- **FAIR-compliant** metadata (92% score)

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/YOUR_ORG/szd-backup.git
cd szd-backup
pip install -r requirements.txt
```

### Usage

**1. Download metadata from GAMS:**
```bash
python scripts/fetch_metadata.py
```

**2. Download complete archive:**
```bash
python scripts/download_archive.py
```

**3. Validate downloaded data:**
```bash
python scripts/validate_downloads.py
```

**4. Upload to Zenodo:**
```bash
python scripts/zenodo_upload_simple.py --token YOUR_TOKEN
```

## 📋 Features

- ✅ **Resume-capable downloads** - Continue after interruptions
- ✅ **Rate limiting** - Server-friendly (1.5s between images)
- ✅ **Automatic validation** - Cross-check with METS metadata
- ✅ **Progress tracking** - JSON-based state management
- ✅ **FAIR-compliant** - Rich metadata with ORCID, GND, Wikidata IDs
- ✅ **Zenodo integration** - Automated upload with DOI versioning

## 📚 Collections

| Collection | Objects | Completeness |
|------------|---------|--------------|
| Facsimiles | 169 | 95.3% |
| Essays (Aufsatz) | 625 | 99.0% |
| Life Documents (Lebensdokumente) | 127 | 96.9% |
| Correspondence (Korrespondenzen) | 1,186 | 99.7% |

## 🗂️ Archive Structure

```
data/
├── facsimiles/           # Manuscripts and documents
├── aufsatz/              # Essays and articles
├── lebensdokumente/      # Biographical materials
└── korrespondenzen/      # Correspondence

Each object contains:
├── mets.xml              # Original METS metadata (DFG-METS)
├── metadata.json         # Parsed metadata (JSON)
└── images/               # High-resolution JPEG images
    ├── IMG_1.jpg
    ├── IMG_2.jpg
    └── ...
```

## ⚠️ Known Limitations

22 objects (1.0%) are incomplete due to server-side METS metadata issues:
- 729 images (3.7%) referenced in METS do not exist on source server
- Most affected: o:szd.939 (328 missing), o:szd.268 (230 missing), o:szd.267 (125 missing)

See [docs/DATA_QUALITY_ISSUES.md](docs/DATA_QUALITY_ISSUES.md) for details.

## 📖 Documentation

- **[Data Quality Issues](docs/DATA_QUALITY_ISSUES.md)** - Known problems and validation results
- **[Zenodo Versioning Strategy](docs/ZENODO_VERSIONING_STRATEGY.md)** - Version management plan
- **[FAIR Compliance](docs/FAIR_COMPLIANCE.md)** - FAIR principles analysis (92% score)

## 🔬 Technical Details

**Standards:**
- **Metadata:** DFG-METS (Deutsche Forschungsgemeinschaft), MODS, DataCite
- **Images:** JPEG, ~4912×7360 pixels, RGB
- **Archive:** tar.gz compression

**FAIR Compliance:**
- **F** (Findable): 100% - DOI, ORCID, GND, Wikidata
- **A** (Accessible): 100% - Open Access via Zenodo
- **I** (Interoperable): 83% - METS/MODS, controlled vocabularies
- **R** (Reusable): 100% - CC-BY 4.0, detailed provenance

## 📄 Citation

If you use this data or scripts, please cite:

```bibtex
@dataset{szd_archive_2025,
  author    = {Zangerl, Lina Maria and Glunk, Julia Rebecca and
               Matuschek, Oliver and Pollin, Christopher},
  title     = {Stefan Zweig Digital - Complete Archive Backup},
  year      = {2025},
  publisher = {Zenodo},
  version   = {v1.0.0},
  doi       = {10.5281/zenodo.XXXXXX},
  url       = {https://doi.org/10.5281/zenodo.XXXXXX}
}
```

See [CITATION.cff](CITATION.cff) for citation details.

## 👥 Contributors

**Creators:**
- [Zangerl, Lina Maria](https://orcid.org/0000-0001-9709-3669) - Literaturarchiv Salzburg
- [Glunk, Julia Rebecca](https://orcid.org/0000-0001-6647-9729) - Literaturarchiv Salzburg
- Matuschek, Oliver - Literaturarchiv Salzburg
- [Pollin, Christopher](https://orcid.org/0000-0002-4879-129X) - Digital Humanities Craft OG

**Institutions:**
- **Literaturarchiv Salzburg** - Original materials and digitization
- **GAMS, University of Graz** - Digital infrastructure and hosting

## 📞 Contact

- **Project:** https://stefanzweig.digital
- **Email:** info@stefanzweig.digital
- **GAMS:** https://gams.uni-graz.at/context:szd

## 🔗 Related Resources

- **GND:** https://d-nb.info/gnd/118637479
- **Wikidata:** https://www.wikidata.org/wiki/Q78491
- **Stefan Zweig Digital:** https://stefanzweig.digital

## 📜 License

- **Scripts/Code:** MIT License (see [LICENSE](LICENSE))
- **Data:** CC-BY 4.0 (Creative Commons Attribution 4.0) - see Zenodo deposit

## 🙏 Acknowledgments

This archive was created using data from:
- **Literaturarchiv Salzburg** - Collection ownership and curation
- **GAMS (University of Graz)** - Digital infrastructure and hosting
- **Stefan Zweig Digital Project** - Digitization and coordination

---

**Version:** 1.0.0 | **Date:** October 22, 2025 | **Archive Size:** 22.3 GB
