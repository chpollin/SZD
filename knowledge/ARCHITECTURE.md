# Architecture - Stefan Zweig Digital

System architecture, component overview, and data flow for the Stefan Zweig Digital platform.

---

## System Overview

Stefan Zweig Digital is a distributed digital humanities platform combining multiple technologies for data encoding, transformation, presentation, search, and long-term preservation.

```
┌─────────────────────────────────────────────────────────────┐
│                   Stefan Zweig Digital                       │
│                  https://stefanzweig.digital                 │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼────┐          ┌─────▼─────┐         ┌────▼────┐
   │  GAMS   │          │ TEI-XML   │         │ Zenodo  │
   │Platform │          │   Data    │         │ Archive │
   └─────────┘          └───────────┘         └─────────┘
```

---

## Component Architecture

### Data Layer

**TEI-XML Source Files**
- Location: [data/](../data/)
- Format: TEI P5 XML
- Collections: Thematic collections and person index
- Encoding: UTF-8 with bilingual content

### Archival Layer

**Zenodo Pipeline**
- Location: [szd-zenodo-backup/](../szd-zenodo-backup/)
- Purpose: Long-term preservation with DOI versioning
- Format: TAR.GZ archives with DataCite metadata
- Archive Types: Facsimiles, correspondence, personal documents, essays

**FAIR Principles:** Findable, Accessible, Interoperable, Reusable

See [szd-zenodo-backup/README.md](../szd-zenodo-backup/README.md) for workflow details.

---

## Data Flow

### Publication Workflow

```
1. Data Creation/Encoding
   ├─ TEI-XML files created/edited in data/
   ├─ Validation with Python scripts
   └─ CSV catalogue updates

2. GAMS Ingestion
   ├─ TEI files uploaded to GAMS repository
   ├─ Metadata extracted to triple store
   └─ RDF graphs generated

3. Web Transformation
   ├─ XSL stylesheets transform TEI to HTML
   ├─ SPARQL queries provide search results
   └─ JavaScript adds interactivity

4. Public Access
   └─ https://stefanzweig.digital/
```

### Search Workflow

```
1. User Query
   └─ Search form on website

2. SPARQL Execution
   ├─ Query sent to Blazegraph
   ├─ Triple pattern matching
   └─ Bilingual filtering

3. Results Processing
   ├─ XML result set returned
   ├─ XSL transforms to HTML
   └─ JavaScript enhances display

4. Result Display
   └─ Formatted search results with links
```

### Archival Workflow

```
1. Archive Creation
   ├─ Python scripts download data from GAMS
   ├─ Split into manageable archives
   └─ DataCite metadata generated

2. Zenodo Upload
   ├─ TAR.GZ files uploaded
   ├─ Metadata attached
   └─ DOI assigned

3. Version Management
   ├─ New versions for updates
   └─ DOI versioning chain
```

---

## GAMS Platform Integration

**GAMS (Geisteswissenschaftliches Asset Management System)**
- Host: University of Graz
- URL: https://gams.uni-graz.at/
- SZD Context: https://gams.uni-graz.at/context:szd

### Platform Components

**Fedora Commons Repository**
- Digital object storage
- PID management (o:szd.*)
- Version control
- Access control

**Blazegraph Triple Store**
- RDF graph database
- SPARQL 1.1 endpoint
- Full-text indexing
- Bilingual content support

**METS/MODS Support**
- Structural metadata
- Descriptive metadata
- Administrative metadata
- Rights metadata

**XSL Transformation Pipeline**
- Server-side XSLT processing
- Template inheritance
- Dynamic content generation
- Format conversions

---

## Technology Stack Summary

### Data Encoding
- **TEI P5:** Primary data format
- **XML Schema:** Validation
- **UTF-8:** Character encoding
- **ISO 8601:** Date encoding

### Metadata Standards
- **METS/MODS:** GAMS structural metadata
- **DataCite 4.0:** Zenodo deposits
- **Dublin Core:** OAI-PMH harvesting
- **GND/Wikidata:** Authority files

### Web Technologies
- **XSLT 2.0/3.0:** XML transformations
- **CSS3:** Responsive styling
- **JavaScript ES6+:** Client interactivity
- **HTML5:** Semantic markup

### Database & Search
- **SPARQL 1.1:** Query language
- **Blazegraph:** Triple store
- **RDF:** Data model
- **Fedora Commons:** Repository backend

### Programming
- **Python 3:** Validation and archival scripts
- **lxml:** XML processing
- **requests:** HTTP operations
- **BeautifulSoup:** HTML parsing

### Infrastructure
- **GAMS:** Hosting platform (University of Graz)
- **Zenodo:** Long-term preservation
- **Git:** Version control
- **GitHub:** Code repository

---

## Integration Points

### External Authority Files

**GND (Gemeinsame Normdatei)**
- URL pattern: `http://d-nb.info/gnd/{ID}`
- Usage: Person, organization, place identifiers
- Integration: `@ref` attributes in TEI

**Wikidata**
- URL pattern: `https://www.wikidata.org/wiki/{ID}`
- Usage: Entity linking and enrichment
- Integration: `@corresp` attributes in TEI

**Wikipedia**
- URL pattern: `https://de.wikipedia.org/wiki/{TITLE}`
- Usage: Biographical context
- Integration: `@corresp` attributes in TEI

### Content Delivery

**IIIF (International Image Interoperability Framework)**
- Image delivery for high-resolution facsimiles
- Mirador viewer integration
- Zoom and pan functionality

**OAI-PMH (Open Archives Initiative Protocol)**
- Metadata harvesting
- Dublin Core exports
- Repository interoperability

---

## Bilingual Architecture

All system components support German and English:

**Data Level**
- `xml:lang="de"` and `xml:lang="en"` attributes in TEI

**Query Level**
- SPARQL FILTER clauses for language selection
- Bilingual result sets

**Display Level**
- XSL templates with language parameters
- JavaScript language switching
- CSS styling for both languages

**URL Level**
- Language parameter in URLs
- Content negotiation

---

## Performance Considerations

**Caching**
- XSL transformation results cached
- SPARQL query results cached
- Static asset caching (CSS, JS, images)

**Optimization**
- Lazy loading for images
- Minified CSS/JS
- Optimized SPARQL queries
- Index-based searches

---

## Security & Access Control

**Repository Access**
- GAMS authentication for editing
- Public read access for published content
- Role-based permissions

**Data Integrity**
- Git version control for source files
- GAMS object versioning
- Zenodo immutable archives

**Licensing**
- CC-BY 4.0 for most content
- License metadata in TEI headers
- Rights statements in web interface

---

## GitHub Pages — Design System

The `docs/` folder is deployed as GitHub Pages, serving the ontology documentation and project overview. The design is aligned to the Stefan Zweig Digital GAMS reference to form a visual family ("Zweig Forschungsverbund"):

**Shared palette (from GAMS):**
- Burgundy `#631a34` — header, links, primary accent
- Gold `#C2A360` — metadata labels, secondary accent
- Cream `#FAF8F3` — page background

**Typography (Google Fonts):**
- Source Serif 4 — headings, body text (serif)
- Source Sans 3 — UI elements, navigation (sans-serif)
- JetBrains Mono — ontology URIs, code (monospace)

**Design differentiation from Klawiter Bibliography:**
- Same palette, but "burgundy-forward" (section headings in burgundy, gold used sparingly for metadata)
- Klawiter is "gold-forward" (section headings in gold, more warm/inviting for browsing)
- Both share the GAMS color values exactly, creating unmistakable family cohesion

**Landing page:** Ontology-focused dashboard (not a portal). Stats row (72 Classes, 132 Properties, 7 Layers, v1.1.0), three primary cards (Reference, Visualization, Downloads), secondary links row. All pages in English.

**Verbund bar:** Slim navigation bar above header connecting Stefan Zweig Digital (GAMS), Klawiter Bibliography, and Ontology & Data (this site).

**Visualization:** Fullscreen force-directed D3.js graph at `ontology/visualize.html`. Sidebar controls with layer toggles, auto-fit zoom, hover-to-highlight, English labels.

**Files:** `docs/css/szd-ontology.css` (single stylesheet for all pages except visualize.html which has inline styles for fullscreen layout)

---

## Related Documentation

- [DATA_MODEL.md](DATA_MODEL.md) - TEI-XML structure and encoding
- [COLLECTIONS.md](COLLECTIONS.md) - Collection-specific details
- [../szd-zenodo-backup/README.md](../szd-zenodo-backup/README.md) - Archival pipeline

---

## External Resources

- **GAMS Platform:** https://gams.uni-graz.at/
- **GAMS Documentation:** https://gams.uni-graz.at/documentation
- **TEI Guidelines:** https://tei-c.org/guidelines/
- **Blazegraph:** https://github.com/blazegraph/database/wiki
- **Fedora Commons:** https://fedora.lyrasis.org/
- **Zenodo:** https://zenodo.org/

---

**Last Updated:** March 2026

**See also:** [ONTOLOGY.md](ONTOLOGY.md) for the formal data model, [PROJECT.md](PROJECT.md) for the full project description.
