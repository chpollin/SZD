# Stefan Zweig Digital (SZD)

Digital humanities project for the complete digitization and online availability of Stefan Zweig's works, correspondence, autographs, biographical materials, and personal library.

- Website: https://stefanzweig.digital
- Zenodo Archive: https://zenodo.org/uploads/17421555

---

## Repository Structure

### Primary Data

The [data/](data/) directory contains TEI-XML encoded archival data and digital facsimiles organized by collection type:

- Correspondence (SZDKOR) - Letters and correspondence
- Works (SZDWRK) - Published writings and literary works
- Autographs (SZDAUT) - Handwritten manuscripts
- Library (SZDBIB) - Personal book collection
- Biography (SZDBIO) - Life calendar and biographical timeline
- Essays (SZDESS) - Articles and academic essays
- Personal Documents (SZDLEB) - Life documents
- Index (SZDPER) - Person authority file
- Glossary (SZDGLR) - Subject terminology

### Web Content

The [webpage/](webpage/) directory contains static page content and assets including about pages, imprint information, landing page content, audio files, and images used throughout the website. See [webpage/README.md](webpage/README.md) for details on image linking and reference types.

### Zenodo Backup

The [szd-zenodo-backup/](szd-zenodo-backup/) directory provides an automated archival pipeline for long-term preservation on Zenodo. This directory contains only scripts and documentation. The actual data is generated locally and uploaded to Zenodo with DOI versioning. The pipeline handles complete backup of digitized objects including high-resolution images with FAIR-compliant metadata.

Documentation includes quick start guides, technical details, FAIR principles analysis, and data quality assessments. See [szd-zenodo-backup/README.md](szd-zenodo-backup/README.md) for usage instructions.

### Scripts

The [scripts/](scripts/) directory contains data processing and reconciliation tools, including instance data generation (`generate_instances.py`) and Klawiter bibliography reconciliation (`reconcile_klawiter.py`).

### Nachlass-Ontologie (SZDO)

The [ontology/](ontology/) directory contains the **Stefan Zweig Digital Nachlass-Ontologie** — a formal OWL ontology for the digital estate based on Records in Context (RiC-O), IFLA LRM, and CIDOC-CRM.

- **Live Documentation:** https://chpollin.github.io/SZD/ontology/
- **Namespace:** `https://gams.uni-graz.at/o:szd.ontology#`
- **Version:** 1.2.0 (two-layer architecture: generic `nachlass:` + SZD-specific `szdo:`)
- **Generic Ontology:** `nachlass-ontology.ttl` (`https://w3id.org/nachlass#`) -- reusable for any estate project
- **GAMS Compatibility:** Full backward-compatible mapping from English v0.x names via `owl:equivalentClass/Property`
- **Validation:** 6-stage pipeline (Syntax, SHACL, OWL, OntoClean, 22 Competency Questions) -- run `python ontology/validate.py`
- **Design Document:** [knowledge/ONTOLOGY.md](knowledge/ONTOLOGY.md)

### GitHub Pages

The [docs/](docs/) directory serves the project documentation site at https://chpollin.github.io/SZD/:

- **Project:** https://chpollin.github.io/SZD/project/ — DH project description, collections, methodology, FAIR compliance
- **Ontology:** https://chpollin.github.io/SZD/ontology/ — Bilingual (DE/EN) class/property reference, vocabulary badges
- **Downloads:** https://chpollin.github.io/SZD/downloads/ — TEI-XML, RDF, Ontologie, Glossar, Klawiter-Bibliographie, Zenodo

### Knowledge Vault

The [knowledge/](knowledge/) directory provides comprehensive technical documentation including TEI-XML data models, collection overviews, system architecture, correspondence corpus statistics, TEI-CSV schema mapping, and the ontology design document. See [knowledge/README.md](knowledge/README.md) for navigation.

---

## Technology Stack

The project uses TEI-XML (Text Encoding Initiative P5) as the primary data format with metadata following METS/MODS and DFG-METS library standards, while Zenodo deposits use DataCite Schema 4.0 for metadata description. The website runs on GAMS (Geisteswissenschaftliches Asset Management System) hosted at University of Graz, providing XML/TEI repository infrastructure, METS/MODS metadata support, and Blazegraph for SPARQL queries. Long-term archival storage is provided by Zenodo with DOI versioning. Data processing, validation, and ontology tooling are written in Python.

---

## License

All content in this repository is licensed under CC-BY 4.0 (Creative Commons Attribution 4.0 International).

---

## Contributors

### Creators

- Lina Maria Zangerl (Literaturarchiv Salzburg) - https://orcid.org/0000-0001-9709-3669
- Julia Rebecca Glunk (Literaturarchiv Salzburg) - https://orcid.org/0000-0001-6647-9729
- Oliver Matuschek
- Christopher Pollin (Digital Humanities Craft OG) - https://orcid.org/0000-0002-4879-129X

### Institutions

- Literaturarchiv Salzburg (Paris Lodron University of Salzburg) - Original materials and digitization
- GAMS (University of Graz) - Digital infrastructure and hosting platform
- Zenodo - Long-term preservation platform

---

## Contact

Email: 

- info@stefanzweig.digital
- christopher.pollin@dhcraft.org

---

**Last Updated:** March 2026
