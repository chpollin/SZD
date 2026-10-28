---
title: Project
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: complete
language: en
created: 2026-03-29
updated: 2026-10-28
authors: [Christopher Pollin]
generated-with: Claude Code (Claude Opus 5.5)
related: [INDEX, data, architecture, specification, governance]
---

# Project

Stefan Zweig Digital (SZD) is the information and research portal on the life and work of the Austrian writer Stefan Zweig (1881–1942), published at <https://stefanzweig.digital/> and served from <https://gams.uni-graz.at/szd/>. It is a research project on the digital reconstruction of Stefan Zweig's estate from the perspective of the Digital Humanities and research data management. This document is the charter of both repositories, the data repository with the TEI sources, the ontology and the scripts, and gams-www with the presentation layer, the XSLT, JavaScript and CSS with which the GAMS repository of the University of Graz renders the portal and derives the RDF of its search.

## 1. Context

### The estate of Stefan Zweig

Stefan Zweig is among the most widely read and most translated German-language authors of the twentieth century. Exile, flight and posthumous dispersal have spread his estate across several public and private collections worldwide, which puts considerable obstacles in the way of research.

Since 2014 the Literaturarchiv Salzburg has held one of the largest collections from Zweig's literary estate, including manuscripts and typescripts, notebooks and all known diaries. The portal brings it together with the manuscripts and typescripts of the Stefan Zweig Collection at the Daniel A. Reed Library of the State University of New York at Fredonia (USA) and of the National Library of Israel (Jerusalem).

### Aim

Stefan Zweig Digital brings the scattered estate together in digital form and opens it to a scholarly audience. The result is a structured body of digital objects, represented for long-term preservation and accessible independent of place and time. The project is laid out so that later enrichment of the sources, for instance by digital editions, remains possible at any time.

## 2. Collections

The core consists of six estate collections, the works (manuscripts, typescripts, notebooks, bundles, proofs), the correspondence with its person konvolute, Zweig's autograph collection, the reconstructed private library with provenance features, the personal documents (Lebensdokumente) and the essay filing (Aufsatzablage). Digital facsimiles, indices of persons, corporate bodies (organisations), repositories and works, a controlled vocabulary (glossary) and the Lebenskalender with the biographical timeline open them up and complement them. Thematic pages (Themenseiten) present selected holdings. Files, PIDs and encoding of each collection are in [collections](collections.md).

All collection objects have high-resolution facsimiles. They can be browsed through IIIF in the Mirador viewer and are preserved on Zenodo.

The description of the subject in the presentation layer follows the About and Imprint datastreams of `context:szd`, of which [local-test-build/fixtures/](../local-test-build/fixtures/) keeps read-only copies.

## 3. Method

The project rests on four methodological pillars.

1. Archival description after the Regeln zur Erschließung von Nachlässen und Autographen (RNA) and international archival standards.
2. Semantic modelling in a formal ontology (SZDO) based on Records in Context (RiC-O), IFLA LRM and CIDOC-CRM.
3. Linked Open Data with links to authority files (GND, Wikidata, VIAF, GeoNames) and controlled vocabularies (SKOS).
4. Long-term preservation in GAMS and as a Zenodo backup with DOI versioning.

The data model follows TEI P5 and is bilingual throughout (German and English). Persons, corporate bodies, places and works are identified through GND and Wikidata. The work model has three layers, the work index as intellectual level, the manuscript witnesses as physical level and the facsimiles as digital level. For the library reconstruction, changes of ownership and provenance features (stamps, bookplates, marginalia) are recorded. [data-model](data-model.md) describes the encoding patterns, [ontology](ontology.md) the ontology, with the live documentation at https://chpollin.github.io/SZD/ontology/.

## 4. Material basis and infrastructure

The primary data are curated TEI files, one per holding, maintained in this data repository and ingested into GAMS (Fedora Commons). Index objects, the Lebenskalender, the theme pages, the glossary as SKOS and the METS objects of the facsimiles complete the material. Objects, identifiers and the derived datastreams are described in [data](data.md), the TEI to RDF mapping in [rdf-mapping](rdf-mapping.md).

GAMS (Geisteswissenschaftliches Asset Management System) is the Fedora-based repository infrastructure of the University of Graz. It stores the SZD objects and runs the stylesheets of gams-www on the server, the page stylesheets whenever a page is called and the ingest stylesheets whenever an object is ingested. gams-www therefore holds transformation and presentation logic, while data, translation catalogue, executed search queries and runtime environment live on the GAMS server. XSLT turns the data into HTML and RDF, Blazegraph answers the SPARQL queries of the search, Zenodo holds the preservation copy, and GitHub Pages documents ontology and project. [architecture](architecture.md) describes components, the split and the data flow, [deployment-architecture](deployment-architecture.md) the route from a commit or a data change to the published site.

## 5. Standards

- TEI P5 (Text Encoding Initiative) for the catalogue, the indexes, the Lebenskalender and the theme pages
- METS with embedded MODS for structural and descriptive metadata (DFG-METS), compatible with the DFG Viewer, for the facsimile objects
- DataCite 4.0 for the Zenodo metadata
- Dublin Core over OAI-PMH for harvesting
- IIIF Presentation API for image delivery and viewer, with IIIF Image API derivatives for the gallery cards and IIIF manifests for the viewer and the image download
- RNA for the description of estates and autographs
- Records in Context (RiC-O), IFLA LRM and CIDOC-CRM for the ontology
- RDF/XML in the project ontology `szd:` with the controlled vocabulary of the SKOS glossary `szdg:` for the search, described in [rdf-mapping](rdf-mapping.md)
- GND and Wikidata for persons, GND for organisations and repositories, WGS84 coordinates for repositories and the ISO 639-2 language codes of the Library of Congress
- SPARQL against the two triplestores of GAMS, described in [search-architecture](search-architecture.md)

## 6. Research Data Management

| Principle | Measures |
|-----------|----------|
| Findable | DOI (Zenodo), ORCID, GND, Wikidata, PIDs in GAMS |
| Accessible | Open access through GAMS and Zenodo, OAI-PMH |
| Interoperable | TEI P5, METS/MODS, RDF and SPARQL, controlled vocabularies |
| Reusable | CC BY 4.0, documented provenance, community standards |

An object passes through digitisation, cataloguing in bilingual TEI linked to authority data, transformation into HTML and RDF, publication in GAMS with PIDs and a SPARQL endpoint, preservation on Zenodo and finally reuse through ontology, Linked Data and downloads.

Citation:

```
Zweig, Stefan: [Werktitel], [Dokumenttyp]. Literaturarchiv Salzburg,
[Signatur]. In: Stefan Zweig digital, Hrsg. Literaturarchiv Salzburg,
URL: https://stefanzweig.digital/o:szd.werke#[ID]
```

## 7. Licences

All content of the portal, data and texts, is published under Creative Commons BY 4.0, and the code of gams-www under the MIT licence (`LICENSE` in gams-www), as decided on 2026-10-09. The Imprint datastream of `context:szd`, the licence badge in the page footer (`szd-static.xsl`) and the Dublin Core crosswalk ([szd-MODStoDC_MAPPING.xsl](../gams/szd-MODStoDC_MAPPING.xsl)), which writes `dc:rights`, state CC BY 4.0, as do the data repository in its `CITATION.cff` and the sources of the static pages in its `webpage/` folder. The crosswalk is a documented copy that neither GAMS instance references (read on 2026-10-28), see [deployment-architecture](deployment-architecture.md#ingest-stylesheets-in-cirilo). The production datastreams `STARTSEITE`, `ABOUT` and `MISCELLANEOUS` of `context:szd` still declared CC BY-NC-SA 4.0 in their TEI headers on 2026-10-09, and their replacement is tracked in the [plan](plan.md#production).

The TEI files carry CC BY 4.0 in their `availability` element. The licences of code, documentation and archival data of the data repository are stated in its [README](../README.md#licence). Whether the archival research data fall under CC BY 4.0 or remain with the archive is an [operator question](plan.md#data-questions).

## 8. Connected Projects

The Klawiter bibliography adds the reception and publication history to Stefan Zweig Digital, with first editions, translations, secondary literature and film adaptations. It is connected through the work layer of the SZDO. Repository https://github.com/chpollin/klawiter-rescue, website https://chpollin.github.io/klawiter-rescue/.

The ontology thereby joins three perspectives, the archival perspective of SZD with physical objects, repositories and provenance, the bibliographic perspective of Klawiter with publications, translations and reception, and the biographical perspective of the Lebenskalender with life events, encounters and places. GND numbers and Wikidata entities serve as shared identifiers.

## 9. Chronology

| Date | Milestone |
|------|-----------|
| 2014 | The Literaturarchiv Salzburg acquires Stefan Zweig holdings |
| 2016–2021 | Development of the portal at the Zentrum für Informationsmodellierung, University of Graz |
| 2017–2025 | Ongoing digitisation and cataloguing |
| June 2018 | Launch of version 1 (stefanzweig.digital) |
| December 2019 | Version 2 with the English version |
| July 2020 | Version 3 with the autograph collection and extended data |
| 2022 | Digital Humanities Craft OG takes over project lead and development of the portal, as the presentation-layer knowledge states (see the [plan](plan.md#data-questions)) |
| October 2025 | Zenodo archive of the digitised objects |
| March 2026 | SZDO v1.0.0, formal Nachlass-Ontologie and GitHub Pages |
| March 2026 | SZDO v1.1.0 with date evidence, person role hierarchy, RiC alignments and Klawiter corrections |
| March 2026 | SZDO v1.2.0 with the generic Nachlass-Ontologie (`nachlass:`) and two-layer architecture, date normalisation in SZDBIB, SZDAUT and SZDKOR |
| March 2026 | GAMS frontend (`gamsdev/`) removed from this repository, it lives in `ZIMLAB/szd` (gams-www) since |
| June 2026 | SZ-AAL correspondence as person konvolute and SZ-AAL personal documents in TEI, rendering contract for grouped lists documented |
| September 2026 | Facsimile links for Notizbuch Paris 1936 and Register der Aufsätze, Lebenskalender prototype in the SZD design under `docs/lebenskalender/` |
| 11 September 2026 | Timeline with derived lanes in the GAMS frontend on staging, state and acceptance in [lebenskalender-lanes](lebenskalender-lanes.md#delivery-state) |
| September 2026 | Archive checkup of the catalogue views evaluated and applied to the data, result in [data-quality](data-quality.md#archive-checkup-september-2026). Corporate bodies moved from the person index to the organisation index. The first editions, never published productively, removed from the repository |
| 24 September 2026 | Every correspondence Konvolut of production in the repository, organisation index with country and place from the GND, certainly unreferenced persons removed from the person index, SZDO 2.0.0 with English identifiers, staging ingest package generated from the repository |
| 9 October 2026 | Production goes live with the frontend overhaul of September 2026, the multi-holding timeline switched off, CC BY 4.0 for all content and MIT for the code of gams-www decided |
| October 2026 | Everything GAMS does not serve moves from gams-www into this repository, and the two knowledge bases become one (2026-10-28) |

## 10. Participants

The website (https://stefanzweig.digital) names the participants, this document lists roles and institutions.

| Role | Institution |
|------|-------------|
| Project lead | Literaturarchiv Salzburg, as the former data-repository knowledge stated, and Digital Humanities Craft OG since 2022, as the former presentation-layer knowledge stated following the About and Imprint datastreams, see the [plan](plan.md#data-questions) |
| Data entry | Literaturarchiv Salzburg |
| Data modelling (Christopher Pollin, ORCID 0000-0002-4879-129X) | Digital Humanities Craft OG |

| Institution | Role |
|-------------|------|
| Literaturarchiv Salzburg (LAS), Paris Lodron University of Salzburg | Academic publisher of the portal, administration of the domain, sources, digitisation, cataloguing and curation of the catalogue data |
| Zentrum für Informationsmodellierung (Centre for Information Modelling, ZIM), University of Graz | Provider of the information and services, digital infrastructure and operator of the GAMS platform, development of the portal from 2016 to 2021 |
| Digital Humanities Craft OG (DHCraft) | Project lead and development since 2022, data modelling, ontology, technical implementation |
| Fotohof Salzburg | Production of the digital facsimiles of the Salzburg holdings |
| Daniel A. Reed Library (SUNY Fredonia) | Partner, holdings |
| National Library of Israel (Jerusalem) | Partner, holdings |

The project is funded from the budget of the Literaturarchiv Salzburg. Who decides what inside the repositories is laid down in [governance](governance.md).

## References

- Website: https://stefanzweig.digital
- GAMS context: https://gams.uni-graz.at/context:szd
- Ontology: https://chpollin.github.io/SZD/ontology/
- Zenodo archive: https://zenodo.org/records/17421555
- GitHub: https://github.com/chpollin/SZD
- gams-www: https://zimlab.uni-graz.at/gams/projects/szd/gams-www
- Klawiter bibliography: https://github.com/chpollin/klawiter-rescue
