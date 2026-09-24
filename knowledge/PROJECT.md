---
title: Stefan Zweig Digital — Project
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD.git
method:
  name: Promptotyping
  url: https://dhcraft.org/promptotyping
status: complete
created: 2026-03-29
updated: 2026-09-23
---

# Stefan Zweig Digital — Project

Research project on the digital reconstruction of Stefan Zweig's estate from the perspective of the Digital Humanities and research data management.

## 1. Context

### The estate of Stefan Zweig

Stefan Zweig (1881–1942) is among the most widely read and most translated German-language authors of the twentieth century. Exile, flight and posthumous dispersal have spread his estate across several public and private collections worldwide, which puts considerable obstacles in the way of research.

Since 2014 the Literaturarchiv Salzburg has held one of the largest collections from Zweig's literary estate, including manuscripts and typescripts, notebooks and all known diaries. Holdings of the Daniel A. Reed Library (SUNY Fredonia, USA) and the National Library of Israel (Jerusalem) complement it.

### Aim

Stefan Zweig Digital brings the scattered estate together in digital form and opens it to a scholarly audience. The result is a structured body of digital objects, represented for long-term preservation and accessible independent of place and time. The project is laid out so that later enrichment of the sources, for instance by digital editions, remains possible at any time.

## 2. Collections

The core consists of six estate collections, the works (manuscripts, typescripts, notebooks, bundles, proofs), the correspondence with its person konvolute, Zweig's autograph collection, the reconstructed private library with provenance features, the personal documents (Lebensdokumente) and the essay filing (Aufsatzablage). Indices of persons, corporate bodies, repositories and works, a controlled vocabulary (glossary) and the Lebenskalender with the biographical timeline open them up. Thematic pages present selected holdings. Files, PIDs and encoding of each collection are in [COLLECTIONS.md](COLLECTIONS.md).

All collection objects have high-resolution facsimiles. They can be browsed through IIIF in the Mirador viewer and are preserved on Zenodo.

## 3. Method

The project rests on four methodological pillars.

1. Archival description after the Regeln zur Erschließung von Nachlässen und Autographen (RNA) and international archival standards.
2. Semantic modelling in a formal ontology (SZDO) based on Records in Context (RiC-O), IFLA LRM and CIDOC-CRM.
3. Linked Open Data with links to authority files (GND, Wikidata, VIAF, GeoNames) and controlled vocabularies (SKOS).
4. Long-term preservation in GAMS and as a Zenodo backup with DOI versioning.

The data model follows TEI P5 and is bilingual throughout (German and English). Persons, corporate bodies, places and works are identified through GND and Wikidata. The work model has three layers, the work index as intellectual level, the manuscript witnesses as physical level and the facsimiles as digital level. For the library reconstruction, changes of ownership and provenance features (stamps, bookplates, marginalia) are recorded. [DATA_MODEL.md](DATA_MODEL.md) describes the encoding patterns, [ONTOLOGY.md](ONTOLOGY.md) the ontology, with the live documentation at https://chpollin.github.io/SZD/ontology/.

## 4. Infrastructure

The data lives as TEI P5 in this repository and is ingested into GAMS (Fedora Commons). XSLT turns it into HTML and RDF, Blazegraph answers the SPARQL queries of the search, Zenodo holds the preservation copy, and GitHub Pages documents ontology and project. [ARCHITECTURE.md](ARCHITECTURE.md) describes components and data flow.

Standards in use:

- TEI P5 (Text Encoding Initiative)
- METS/MODS for structural and descriptive metadata (DFG-METS)
- DataCite 4.0 for the Zenodo metadata
- Dublin Core for OAI-PMH harvesting
- IIIF Presentation API for image delivery and viewer
- RNA for the description of estates and autographs
- Records in Context (RiC-O), IFLA LRM and CIDOC-CRM for the ontology

## 5. Research Data Management

| Principle | Measures |
|-----------|----------|
| Findable | DOI (Zenodo), ORCID, GND, Wikidata, PIDs in GAMS |
| Accessible | Open access through GAMS and Zenodo, OAI-PMH |
| Interoperable | TEI P5, METS/MODS, RDF and SPARQL, controlled vocabularies |
| Reusable | CC BY 4.0, documented provenance, community standards |

An object passes through digitisation, cataloguing in bilingual TEI linked to authority data, transformation into HTML and RDF, publication in GAMS with PIDs and a SPARQL endpoint, preservation on Zenodo and finally reuse through ontology, Linked Data and downloads.

The TEI files carry CC BY 4.0 in their `availability` element. The licences of code, documentation and archival data of the repository are stated in the [README](../README.md#licence).

Citation:

```
Zweig, Stefan: [Werktitel], [Dokumenttyp]. Literaturarchiv Salzburg,
[Signatur]. In: Stefan Zweig digital, Hrsg. Literaturarchiv Salzburg,
URL: https://stefanzweig.digital/o:szd.werke#[ID]
```

## 6. Connected Projects

The Klawiter bibliography adds the reception and publication history to Stefan Zweig Digital, with first editions, translations, secondary literature and film adaptations. It is connected through the work layer of the SZDO. Repository https://github.com/chpollin/klawiter-rescue, website https://chpollin.github.io/klawiter-rescue/.

The ontology thereby joins three perspectives, the archival perspective of SZD with physical objects, repositories and provenance, the bibliographic perspective of Klawiter with publications, translations and reception, and the biographical perspective of the Lebenskalender with life events, encounters and places. GND numbers and Wikidata entities serve as shared identifiers.

## 7. Chronology

| Date | Milestone |
|------|-----------|
| 2014 | The Literaturarchiv Salzburg acquires Stefan Zweig holdings |
| 2017–2025 | Ongoing digitisation and cataloguing |
| June 2018 | Launch of version 1 (stefanzweig.digital) |
| December 2019 | Version 2 with the English version |
| July 2020 | Version 3 with the autograph collection and extended data |
| October 2025 | Zenodo archive of the digitised objects |
| March 2026 | SZDO v1.0.0, formal Nachlass-Ontologie and GitHub Pages |
| March 2026 | SZDO v1.1.0 with date evidence, person role hierarchy, RiC alignments and Klawiter corrections |
| March 2026 | SZDO v1.2.0 with the generic Nachlass-Ontologie (`nachlass:`) and two-layer architecture, date normalisation in SZDBIB, SZDAUT and SZDKOR |
| March 2026 | GAMS frontend (`gamsdev/`) removed from this repository, it lives in `ZIMLAB/szd` since |
| June 2026 | SZ-AAL correspondence as person konvolute and SZ-AAL personal documents in TEI, rendering contract for grouped lists documented |
| September 2026 | Facsimile links for Notizbuch Paris 1936 and Register der Aufsätze, Lebenskalender prototype in the SZD design under `docs/lebenskalender/` |
| 11 September 2026 | Timeline with derived lanes in the GAMS frontend on staging, state and acceptance in [Lebenskalender-Lanes.md](Lebenskalender-Lanes.md#delivery-state) |
| September 2026 | Archive checkup of the catalogue views evaluated and applied to the data, result in [DATA.md](DATA.md#archive-checkup-september-2026). Corporate bodies moved from the person index to the organisation index. The first editions, never published productively, removed from the repository |

## 8. Participants

The website (https://stefanzweig.digital) names the participants, this document lists roles and institutions.

| Role | Institution |
|------|-------------|
| Project lead | Literaturarchiv Salzburg |
| Data entry | Literaturarchiv Salzburg |
| Data modelling (Christopher Pollin, ORCID 0000-0002-4879-129X) | Digital Humanities Craft OG |

| Institution | Role |
|-------------|------|
| Literaturarchiv Salzburg (Paris Lodron University of Salzburg) | Sources, digitisation, cataloguing |
| Zentrum für Informationsmodellierung (University of Graz) | Digital infrastructure, GAMS platform |
| Digital Humanities Craft OG | Data modelling, ontology, technical implementation |
| Daniel A. Reed Library (SUNY Fredonia) | Partner, holdings |
| National Library of Israel (Jerusalem) | Partner, holdings |

## References

- Website: https://stefanzweig.digital
- GAMS context: https://gams.uni-graz.at/context:szd
- Ontology: https://chpollin.github.io/SZD/ontology/
- Zenodo archive: https://zenodo.org/records/17421555
- GitHub: https://github.com/chpollin/SZD
- Klawiter bibliography: https://github.com/chpollin/klawiter-rescue
