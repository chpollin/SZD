---
title: Architecture - Stefan Zweig Digital
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD.git
method:
  name: Promptotyping
  url: https://dhcraft.org/promptotyping
status: complete
created: 2025-10-23
updated: 2026-09-23
---

# Architecture - Stefan Zweig Digital

Stefan Zweig Digital is published on GAMS (Geisteswissenschaftliches Asset Management System) at the University of Graz. Its sources and presentation are split across two Git repositories, with Zenodo for long-term preservation and GitHub Pages for the ontology and project documentation.

## Two Repositories

| Repository | Role |
|------------|------|
| `chpollin/SZD` (this repository) | Curated TEI sources in `data/`, the Nachlass-Ontologie in `ontology/`, the scripts that turn partner deliveries into TEI and repair the catalogue data, the GitHub Pages site in `docs/`, the Zenodo pipeline in `szd-zenodo-backup/` |
| `ZIMLAB/szd` (gams-www) | Presentation layer, meaning the XSLT, JavaScript, CSS and SPARQL query templates that GAMS applies, including the RDF transformation `szd-TORDF.xsl` |

The repositories do not see each other automatically. Their cross-references stand in both `CLAUDE.md` files. Push and GAMS ingest are done manually by the maintainer.

```
TEI in chpollin/SZD
  └─ Cirilo ingest ──► GAMS object (Fedora, PID o:szd.*)
                         ├─ TEI_SOURCE datastream
                         ├─ RDF via szd-TORDF.xsl ──► Blazegraph triple store
                         └─ rendering via gams-www XSLT ──► https://stefanzweig.digital
```

## Publication Workflow

1. TEI files are edited in `data/`. Repairs run as scripts with a dry run, an `--apply` step and a `--verify` step that checks the written state against `HEAD`.
2. The maintainer ingests the changed objects with Cirilo, first on GAMS staging and then on the productive instance. At ingest, GAMS derives the RDF with the `TORDF` stylesheet the object points to, so the indices `o:szd.personen` and `o:szd.organisation` go in before the holdings that reference them.
3. The gams-www XSLT renders the TEI to HTML. Search pages run SPARQL query objects against Blazegraph and render the XML result sets.

Facsimiles are separate `cm:dfgMETS` book objects (`o:szd.<number>`) whose IIIF manifests feed the Mirador viewer. Catalogue entries link them through `altIdentifier/idno[@type="PID"]`, see [COLLECTIONS.md](COLLECTIONS.md#rendering-contract-grouped-lists).

## Derived Timeline Assets

The timeline of the Lebenskalender adds a static JSON delivery path beside the GAMS ingest. `scripts/lebenskalender_lanes/build_lanes.py` derives the lane files from the TEI sources and writes identical copies to `data/derived/lebenskalender/` (ignored by Git, reproduced by the generator) and `docs/lebenskalender/lanes/`. The presentation repository carries a further copy under `data/lebenskalender/`, refreshed explicitly. Schema, dating rules and delivery state are in [Lebenskalender-Lanes.md](Lebenskalender-Lanes.md).

## Long-term Preservation

The pipeline in [szd-zenodo-backup/](../szd-zenodo-backup/README.md) downloads the digitised objects from GAMS, packs them into TAR.GZ archives with DataCite metadata and uploads them to Zenodo with DOI versioning. The data itself is generated locally and never committed. The deposit is https://zenodo.org/records/17421555.

## GitHub Pages

The `docs/` folder is served from the `master` branch at https://chpollin.github.io/SZD/ without a build step. The only workflow, `.github/workflows/deploy-ontology-docs.yml`, regenerates the ontology documentation from `ontology/szd-ontology.ttl`. The site holds the ontology reference, the project page, downloads and the Lebenskalender prototype.

The design is aligned to the Stefan Zweig Digital GAMS site as one visual family with the Klawiter Bibliography.

- Palette from GAMS, burgundy `#631a34` for header, links and primary accent, gold `#C2A360` for metadata labels, cream `#FAF8F3` as page background. The ontology site is burgundy-forward with section headings in burgundy, the Klawiter site gold-forward.
- Typography Source Serif 4 for headings and body, Source Sans 3 for UI elements and navigation, JetBrains Mono for URIs and code.
- The landing page is an ontology dashboard with a stats row, three primary cards (reference, visualisation, downloads) and a row of secondary links. All pages are in English.
- A slim bar above the header connects Stefan Zweig Digital (GAMS), the Klawiter Bibliography and this site.
- `ontology/visualize.html` is a fullscreen force-directed D3.js graph with layer toggles and hover highlighting.
- `docs/css/szd-ontology.css` is the stylesheet for all pages except `visualize.html`, which carries inline styles for its fullscreen layout.

## Related

- [DATA_MODEL.md](DATA_MODEL.md) — encoding patterns and authority references
- [COLLECTIONS.md](COLLECTIONS.md) — collections and rendering contracts
- [ONTOLOGY.md](ONTOLOGY.md) — the formal ontology and its documentation site
- [PROJECT.md](PROJECT.md) — project context and standards
