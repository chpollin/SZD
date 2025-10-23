# GAMS Frontend

Frontend codebase for **https://stefanzweig.digital/** running on the GAMS (Geisteswissenschaftliches Asset Management System) platform at University of Graz.

---

## Overview

This directory contains all XSL transformations, CSS stylesheets, JavaScript, and SPARQL queries necessary for rendering the Stefan Zweig Digital website from TEI-XML source data.

---

## Directory Structure

### XSL Transformations (26+ files)
Transform TEI-XML to HTML for web display:

**Collection Displays:**
- `szd-Korrespondenzen.xsl` - Correspondence display with annotations
- `szd-Autographen.xsl` - Autographed manuscripts
- `szd-Bibliothek.xsl` - Library catalog display
- `szd-Werke.xsl` - Works list and display
- `szd-Briefedition.xsl` - Letter edition rendering

**Index & Navigation:**
- `szd-Personenliste.xsl` - Person directory with biographical links
- `szd-Standortliste.xsl` - Location/repository information
- `szd-Lebenskalender.xsl` - Biographical timeline
- `szd-Glossar.xsl` - Subject terminology browser
- `szd-Thema.xsl` - Theme/topic display

**Functionality:**
- `szd-Suche.xsl` - Search interface
- `szd-Collection.xsl` - Collection browsing
- `szd-static.xsl` - Static page templates
- `szd-Templates.xsl` - Shared template library

**Export Formats:**
- `szd-TORDF.xsl` - RDF export format
- `szd-tei-hssf.xsl` - Manuscript-specific display

### [sparql/](sparql/)
SPARQL queries for database searches:

**Query Types:**
- `fulltext_search.sparql` - Full-text search via Blazegraph
- `person_search.sparql` - Resources connected to specific people
- `standort_search.sparql` - Location-based searches
- `category_search.sparql` - Subject/theme filtering
- `glossary_search.sparql` - Terminology searches

**Features:**
- Bilingual results (German/English via language tags)
- Parameterized queries ($1, $2 parameters)
- Multiple data sources (bibliothek, autographen, werke, personen, etc.)

See [sparql/README.md](sparql/README.md) for details.

### [css/](css/)
Stylesheets and responsive design:
- Layout and typography
- Responsive breakpoints
- Collection-specific styles
- Print styles

### [js/](js/)
JavaScript interactivity:
- Search functionality
- Image viewers (Mirador integration)
- Navigation and UI components
- Interactive features

### [MemoryGame/](MemoryGame/)
Educational memory game component with Stefan Zweig imagery.

See [MemoryGame/ReadMe.md](MemoryGame/ReadMe.md) for details.

### Other Assets
- **fonts/** - Web fonts
- **icons/** - UI icons and graphics
- **img/** - Images for landing page and UI elements

---

## Technology Stack

- **XSLT 2.0/3.0** - XML transformations
- **CSS3** - Styling and responsive design
- **JavaScript (ES6+)** - Client-side interactivity
- **SPARQL 1.1** - Database queries (Blazegraph)
- **TEI P5** - Source data format

---

## GAMS Platform

GAMS (Geisteswissenschaftliches Asset Management System) provides:
- XML/TEI repository infrastructure
- METS/MODS metadata support
- Blazegraph triple store for SPARQL
- Fedora Commons repository backend
- XSL transformation pipeline

**Platform:** https://gams.uni-graz.at/
**SZD Context:** https://gams.uni-graz.at/context:szd

---

## Data Flow

```
TEI-XML (data/)
    → XSL Transformation (*.xsl)
    → HTML/CSS/JS
    → https://stefanzweig.digital/

SPARQL Queries (sparql/)
    → Blazegraph Triple Store
    → Search Results (XML)
    → Display via XSL
```

---

## Development

### Testing XSL Transformations
```bash
# Use Saxon or similar XSLT processor
saxon -s:input.xml -xsl:szd-Korrespondenzen.xsl -o:output.html
```

### Testing SPARQL Queries
Access GAMS Blazegraph endpoint:
```
https://gams.uni-graz.at/blazegraph/namespace/NAMESPACE/sparql
```

---

## Documentation

- **[Root README](../README.md)** - Repository overview
- **[webpage/README.md](../webpage/README.md)** - Static content documentation
- **[sparql/README.md](sparql/README.md)** - SPARQL query documentation

---

## External Resources

- **GAMS Documentation:** https://gams.uni-graz.at/documentation
- **TEI Guidelines:** https://tei-c.org/guidelines/
- **Blazegraph:** https://github.com/blazegraph/database/wiki

---

**Platform:** GAMS (University of Graz)
**Website:** https://stefanzweig.digital/
**Last Updated:** October 2025
