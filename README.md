# Stefan Zweig Digital (SZD)

Digital humanities project for the complete digitization and online availability of Stefan Zweig's works, correspondence, autographs, biographical materials, and personal library.

**Website:** https://stefanzweig.digital
**GAMS Collection:** https://gams.uni-graz.at/context:szd
**GND:** https://d-nb.info/gnd/118637479
**Wikidata:** https://www.wikidata.org/wiki/Q78491

---

## 📁 Repository Structure

### Primary Data ([data/](data/))
TEI-XML encoded archival data organized by collection type:

- **[Correspondence](data/Correspondence/)** (SZDKOR) - Letters and correspondence with 245+ partners
- **[Works](data/Work/)** (SZDWRK) - Published writings and literary works
- **[Autographs](data/Autograph/)** (SZDAUT) - Handwritten manuscripts
- **[Library](data/Library/)** (SZDLIB) - Stefan Zweig's personal book collection
- **[Biography](data/Biography/)** (SZDBIO) - Life calendar and biographical timeline
- **[Essays](data/Aufsatzablage/)** (SZDESS) - Articles and academic essays (625 objects)
- **[Personal Documents](data/PersonalDocument/)** (SZDDOC) - Life documents (127 objects)
- **[Index](data/Index/)** (SZDPER) - Person authority file with GND links
- **[Glossary](data/Glossary/)** (SZDGLR) - Subject terminology and thematic index

Each collection contains preprocessing scripts in their respective `preprocessing/` subdirectories.

### GAMS Frontend ([gamsdev/](gamsdev/))
Complete frontend codebase for https://stefanzweig.digital/ running on the GAMS platform:

- **XSL Transformations** (26+ stylesheets) - TEI-XML to HTML conversion
  - `szd-Korrespondenzen.xsl`, `szd-Autographen.xsl`, `szd-Bibliothek.xsl`, etc.
- **[sparql/](gamsdev/sparql/)** - Database queries
  - Fulltext search (Blazegraph)
  - Location, person, category searches
  - Bilingual result sets (German/English)
- **[css/](gamsdev/css/)** - Stylesheets and responsive design
- **[js/](gamsdev/js/)** - JavaScript interactivity and features
- **[MemoryGame/](gamsdev/MemoryGame/)** - Educational game component
- **fonts/**, **icons/** - Web assets

### Web Content ([webpage/](webpage/))
Static page content and assets:
- **ABOUT.xml**, **IMPRINT.xml**, **MISCELLANEOUS.xml** - Static pages
- **STARTSEITE.xml** - Landing page content
- **audio/** - Audio files (interviews, readings)
- **img/** - Images for news, landing page, etc.

See [webpage/README.md](webpage/README.md) for details on image linking and reference types.

### Zenodo Backup ([szd-zenodo-backup/](szd-zenodo-backup/))
Automated archival pipeline for long-term preservation on Zenodo:

**Archive Statistics:**
- 2,107 digitized objects
- 18,719 high-resolution images (~4912×7360 pixels)
- 24.7 GB uncompressed (22.3 GB compressed)
- 99.0% completeness
- FAIR compliance: 92%

**Documentation:**
- [README.md](szd-zenodo-backup/README.md) - Quick start guide
- [DOCUMENTATION.md](szd-zenodo-backup/DOCUMENTATION.md) - Technical details
- [FAIR_COMPLIANCE.md](szd-zenodo-backup/docs/FAIR_COMPLIANCE.md) - FAIR principles analysis
- [DATA_QUALITY_ISSUES.md](szd-zenodo-backup/docs/DATA_QUALITY_ISSUES.md) - Known limitations

### Validation Tools ([scripts/](scripts/))
Cross-cutting data validation and quality assurance utilities:

**[validation/](scripts/validation/)** - TEI/CSV validation suite:
- `validate_tei_csv.py` - Offline TEI/CSV validator
- `validate_tei_against_csv.py` - Compare CSV against TEI
- `clean_tei_with_csv.py` - Synchronize TEI with CSV data
- `fix_mojibake.py` - Character encoding cleanup
- `fetch_korrespondenzen.py` - Extract correspondence signatures
- `compare_tei_bodies.py` - Compare TEI versions
- `tei_csv_mapping.py` - Schema mapping definitions

**[data/](scripts/data/)** - Catalogue CSV files (2,200+ rows):
- `Other.csv`, `SZ_AAP_Reichner.csv`, `SZ_SAM_Meingast.csv`, etc.

### Documentation ([docs/](docs/))
Technical documentation and specifications:
- **[DATA.md](docs/DATA.md)** - Correspondence corpus overview (245 partners, 1,201 records)
- **[MAPPING.md](docs/MAPPING.md)** - TEI-CSV schema mapping (41 columns)

---

## 🔧 Technology Stack

**Data Formats & Standards:**
- **TEI-XML** - Text Encoding Initiative P5 (primary data format)
- **METS/MODS** - Library metadata standards
- **DFG-METS** - Deutsche Forschungsgemeinschaft standard
- **DataCite Schema 4.0** - Zenodo metadata

**Frontend Technologies:**
- **XSL/XSLT** - Server-side XML transformations
- **JavaScript** - Client-side interactivity
- **CSS** - Responsive web design
- **SPARQL** - RDF database queries (Blazegraph)

**Platform & Infrastructure:**
- **GAMS** - Geisteswissenschaftliches Asset Management System (University of Graz)
- **Zenodo** - Long-term archival storage with DOI versioning
- **Python 3.11+** - Data processing and validation scripts

---

## 📊 Project Statistics

- **2,107 objects** digitized across 4 collections
- **18,719 images** at high resolution
- **245 correspondence partners** with TEI encoding
- **2,200+ catalogue entries** in CSV format
- **26+ XSL stylesheets** for frontend rendering
- **99% data completeness**

---

## 📄 License

- **Code & Scripts:** MIT License
- **Data & Content:** CC-BY 4.0 (Creative Commons Attribution 4.0 International)

---

## 👥 Contributors

**Creators:**
- [Lina Maria Zangerl](https://orcid.org/0000-0001-9709-3669) (Literaturarchiv Salzburg)
- [Julia Rebecca Glunk](https://orcid.org/0000-0001-6647-9729) (Literaturarchiv Salzburg)
- Oliver Matuschek (Literaturarchiv Salzburg)
- [Christopher Pollin](https://orcid.org/0000-0002-4879-129X) (Digital Humanities Craft OG)

**Institutions:**
- **Literaturarchiv Salzburg** - Paris Lodron University of Salzburg
- **GAMS** - University of Graz (digital infrastructure and hosting)
- **Zenodo** - Long-term preservation platform

---

## 📞 Contact

- **Email:** info@stefanzweig.digital
- **Project Website:** https://stefanzweig.digital
- **GAMS Context:** https://gams.uni-graz.at/context:szd

---

## 🔗 External Identifiers

- **GND (Stefan Zweig):** https://d-nb.info/gnd/118637479
- **Wikidata:** https://www.wikidata.org/wiki/Q78491
- **ORCID (Team Members):** See Contributors section above

---

**Last Updated:** October 2025
**Repository Status:** Active development and maintenance
