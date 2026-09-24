# Stefan Zweig Digital (SZD)

Digital humanities project for the complete digitization and online availability of Stefan Zweig's works, correspondence, autographs, biographical materials, and personal library.

- Website: https://stefanzweig.digital
- Zenodo archive: https://zenodo.org/records/17421555

---

## Repository Structure

### Primary Data

The [data/](data/) directory contains the TEI-XML sources of the catalogue.

- Works (SZDMSK), manuscripts, typescripts, notebooks and proofs
- Correspondence (SZDKOR), the correspondence index with the per-person konvolut objects in `data/Correspondence/konvolute/`
- Autographs (SZDAUT), Zweig's collection of autographs by other hands
- Library (SZDBIB), the reconstructed private library
- Essays (SZDESS), the essay filing (Aufsatzablage)
- Personal Documents (SZDLEB), life documents
- Biography (SZDBIO), the Lebenskalender timeline
- Themes, curated thematic pages in `data/Issue/`
- Indices for persons (SZDPER), corporate bodies (SZDORG), repositories (SZDSTA) and works (SZDWRK), and the glossary

Files, PIDs and encoding are described in [knowledge/COLLECTIONS.md](knowledge/COLLECTIONS.md). The presentation layer (XSLT, JavaScript, CSS) that GAMS applies to these sources lives in the separate repository `ZIMLAB/szd`.

### Web Content

The [webpage/](webpage/) directory contains static page content and assets, including about pages, imprint, landing page content, audio files and images. [webpage/README.md](webpage/README.md) explains image linking and reference types.

### Zenodo Backup

The [szd-zenodo-backup/](szd-zenodo-backup/) directory holds the archival pipeline for long-term preservation on Zenodo. It contains only scripts and documentation. The data is generated locally and uploaded to Zenodo with DOI versioning. Usage is described in [szd-zenodo-backup/README.md](szd-zenodo-backup/README.md).

### Scripts

The [scripts/](scripts/) directory contains the data processing, repair and reconciliation scripts, each with its own README. The index is in [knowledge/README.md](knowledge/README.md#scripts).

### Estate ontology (SZDO)

The [ontology/](ontology/) directory contains the Stefan Zweig Digital Estate Ontology (Nachlass-Ontologie), a formal OWL ontology for the digital estate based on Records in Contexts (RiC-O), IFLA LRM and CIDOC-CRM.

- Live documentation: https://chpollin.github.io/SZD/ontology/
- Namespace: `https://gams.uni-graz.at/o:szd.ontology#`
- Version 2.0.0 with English identifiers and two layers, the generic `nachlass:` in `nachlass-ontology.ttl` (`https://w3id.org/nachlass#`), reusable for any estate project, and the SZD-specific `szdo:`
- The English v0.x terms used on GAMS are the canonical identifiers wherever the meaning is the same, so live GAMS data conforms without a mapping layer
- Validation with `python ontology/validate.py` (syntax, SHACL, OWL, OntoClean, competency questions)
- Design document: [knowledge/ONTOLOGY.md](knowledge/ONTOLOGY.md)

### GitHub Pages

The [docs/](docs/) directory serves the documentation site at https://chpollin.github.io/SZD/.

- https://chpollin.github.io/SZD/project/ with project description, collections, methodology and FAIR compliance
- https://chpollin.github.io/SZD/ontology/ with the bilingual class and property reference
- https://chpollin.github.io/SZD/downloads/ with TEI-XML, RDF, ontology, glossary, Klawiter bibliography and Zenodo
- https://chpollin.github.io/SZD/lebenskalender/ with the Lebenskalender prototype

### Knowledge Base

The [knowledge/](knowledge/) directory holds the project knowledge, covering collections and encoding, data gaps and checkup results, architecture, the ontology design and the work journal. [knowledge/README.md](knowledge/README.md) is the index.

---

## Technology Stack

The project uses TEI-XML (Text Encoding Initiative P5) as the primary data format. Facsimile objects carry METS/MODS metadata after the DFG-METS profile, and Zenodo deposits use DataCite Schema 4.0. The website runs on GAMS (Geisteswissenschaftliches Asset Management System) hosted at University of Graz, providing XML/TEI repository infrastructure, METS/MODS metadata support, and Blazegraph for SPARQL queries. Long-term archival storage is provided by Zenodo with DOI versioning. Data processing, validation, and ontology tooling are written in Python.

---

## Licence

- Code, ontology, scripts and tooling are licensed under [MIT](LICENSE).
- Documentation, knowledge documents and other textual content are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- Archival research data, the TEI-XML encoded estate materials and digital facsimiles originate from the Stefan Zweig collection held by the Literaturarchiv Salzburg (Paris Lodron University of Salzburg). Those rights remain with the archive.

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

