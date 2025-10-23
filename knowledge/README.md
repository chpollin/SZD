# Knowledge Vault - Stefan Zweig Digital

Central documentation hub for understanding the Stefan Zweig Digital project architecture, data structures, and workflows.

---

## Core Documentation

### Data & Structure
- [DATA_MODEL.md](DATA_MODEL.md) - TEI-XML structure, bilingual architecture, and encoding patterns
- [COLLECTIONS.md](COLLECTIONS.md) - Detailed overview of all archival collections
- [DATA.md](DATA.md) - Correspondence corpus statistics and known data quality issues
- [MAPPING.md](MAPPING.md) - Complete TEI-CSV schema mapping

### System Architecture
- [ARCHITECTURE.md](ARCHITECTURE.md) - System components, data flow, and platform integration

---

## Quick Reference

### What is Stefan Zweig Digital?

A complete digital edition of Stefan Zweig's works, correspondence, autographs, and personal library hosted at https://stefanzweig.digital/

**Key Technologies:**
- TEI-XML P5 for data encoding
- GAMS platform for hosting and infrastructure
- XSL/XSLT for transformations
- SPARQL/Blazegraph for search
- Zenodo for long-term preservation

**Collections:**
- Correspondence - Letters and exchanges
- Works - Published writings
- Autographs - Handwritten manuscripts
- Library - Personal book collection
- Biography - Life calendar timeline
- Essays - Articles and academic pieces
- Personal Documents - Life documents
- Person Index - Authority file with GND/Wikidata links
- Glossary - Subject terminology

---

## Navigation by Topic

### Understanding the Data
Start with [DATA_MODEL.md](DATA_MODEL.md) to understand TEI-XML structure and bilingual architecture, then explore [COLLECTIONS.md](COLLECTIONS.md) for collection-specific details.

### Working with the Data
See [MAPPING.md](MAPPING.md) for TEI-CSV schema mapping and [DATA.md](DATA.md) for data quality documentation.

### System Integration
Read [ARCHITECTURE.md](ARCHITECTURE.md) for overall system design and platform integration details.

---

## External Documentation

### Frontend & Queries
- [gamsdev/README.md](../gamsdev/README.md) - XSL transformations and frontend code
- [gamsdev/sparql/README.md](../gamsdev/sparql/README.md) - SPARQL query documentation

### Validation & Quality
- [scripts/validation/README.md](../scripts/validation/README.md) - TEI-CSV validation tools

### Archival Pipeline
- [szd-zenodo-backup/README.md](../szd-zenodo-backup/README.md) - Zenodo backup automation

---

## Standards & References

**TEI Guidelines:** https://tei-c.org/guidelines/
**GAMS Documentation:** https://gams.uni-graz.at/documentation
**METS/MODS:** Library metadata standards
**DataCite Schema 4.0:** Zenodo metadata format

---

**Last Updated:** October 2025
