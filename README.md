# Stefan Zweig Digital (SZD)

Digital humanities project for the complete digitization and online availability of Stefan Zweig's works, correspondence, autographs, biographical materials, and personal library.

**Website:** https://stefanzweig.digital
**GAMS Collection:** https://gams.uni-graz.at/context:szd
**GND:** https://d-nb.info/gnd/118637479
**Wikidata:** https://www.wikidata.org/wiki/Q78491

---

## Repository Structure

### Primary Data

The [data/](data/) directory contains TEI-XML encoded archival data organized by collection type. The main collections include correspondence, works, autographs, library materials, biographical information, essays, personal documents, and authority files for persons and subject terminology. Each collection maintains its own preprocessing scripts within collection-specific subdirectories.

### GAMS Frontend

The [gamsdev/](gamsdev/) directory contains the complete frontend codebase for https://stefanzweig.digital/ running on the GAMS platform at University of Graz. This includes XSL transformations for converting TEI-XML to HTML, SPARQL queries for database searches, CSS stylesheets, JavaScript for interactivity, and various web assets. The [sparql/](gamsdev/sparql/) subdirectory provides fulltext search capabilities via Blazegraph, along with location-based, person-based, and category-based search queries with bilingual result sets in German and English.

See [gamsdev/README.md](gamsdev/README.md) for technical details on the GAMS platform integration.

### Web Content

The [webpage/](webpage/) directory contains static page content and assets including about pages, imprint information, landing page content, audio files, and images used throughout the website. See [webpage/README.md](webpage/README.md) for details on image linking and reference types.

### Zenodo Backup

The [szd-zenodo-backup/](szd-zenodo-backup/) directory provides an automated archival pipeline for long-term preservation on Zenodo. This directory contains only scripts and documentation. The actual data is generated locally and uploaded to Zenodo with DOI versioning. The pipeline handles complete backup of digitized objects including high-resolution images with FAIR-compliant metadata.

Documentation includes quick start guides, technical details, FAIR principles analysis, and data quality assessments. See [szd-zenodo-backup/README.md](szd-zenodo-backup/README.md) for usage instructions.

### Validation Tools

The [scripts/](scripts/) directory contains cross-cutting data validation and quality assurance utilities. The [validation/](scripts/validation/) subdirectory provides a suite of tools for TEI-XML and CSV validation, including offline validators, synchronization utilities, character encoding cleanup, signature extraction, and version comparison tools. The [data/](scripts/data/) subdirectory contains catalogue CSV files used for validation purposes.

See [scripts/validation/README.md](scripts/validation/README.md) for detailed documentation on each validation tool.

### Documentation

The [docs/](docs/) directory contains technical documentation and specifications. This includes correspondence corpus overviews and TEI-CSV schema mapping documentation describing the data structure and validation requirements.

---

## Technology Stack

### Data Formats and Standards

The project uses TEI-XML (Text Encoding Initiative P5) as the primary data format. Metadata follows METS/MODS and DFG-METS library standards. Zenodo deposits use DataCite Schema 4.0 for metadata description.

### Frontend Technologies

The web frontend uses XSL/XSLT for server-side XML transformations, JavaScript for client-side interactivity, and CSS for responsive web design. Database queries are implemented using SPARQL against a Blazegraph triple store.

### Platform and Infrastructure

The project runs on GAMS (Geisteswissenschaftliches Asset Management System) hosted at University of Graz, providing XML/TEI repository infrastructure, METS/MODS metadata support, and Blazegraph for SPARQL queries. Long-term archival storage is provided by Zenodo with DOI versioning. Data processing and validation scripts are written in Python.

---

## License

All content in this repository is licensed under CC-BY 4.0 (Creative Commons Attribution 4.0 International).

---

## Contributors

### Creators

Lina Maria Zangerl (Literaturarchiv Salzburg) - https://orcid.org/0000-0001-9709-3669
Julia Rebecca Glunk (Literaturarchiv Salzburg) - https://orcid.org/0000-0001-6647-9729
Oliver Matuschek (Literaturarchiv Salzburg)
Christopher Pollin (Digital Humanities Craft OG) - https://orcid.org/0000-0002-4879-129X

### Institutions

Literaturarchiv Salzburg at Paris Lodron University of Salzburg provides the original materials and digitization. GAMS at University of Graz provides the digital infrastructure and hosting platform. Zenodo serves as the long-term preservation platform.

---

## Contact

**Email:** info@stefanzweig.digital
**Project Website:** https://stefanzweig.digital
**GAMS Context:** https://gams.uni-graz.at/context:szd

---

**Last Updated:** October 2025
**Repository Status:** Active development and maintenance
