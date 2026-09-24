---
title: Architecture
project:
  name: Stefan Zweig Digital, data repository
  repository: https://github.com/chpollin/SZD
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: complete
created: 2025-10-23
updated: 2026-09-24
---

# Architecture

Stefan Zweig Digital is published on GAMS (Geisteswissenschaftliches Asset Management System) at the University of Graz. Its sources and presentation are split across two Git repositories, with Zenodo for long-term preservation and GitHub Pages for the ontology and project documentation.

## Two Repositories

| Repository | Role |
|------------|------|
| `chpollin/SZD` (this repository) | Curated TEI sources in `data/`, the Nachlass-Ontologie in `ontology/`, the scripts that turn partner deliveries into TEI and repair the catalogue data, the GitHub Pages site in `docs/`, the Zenodo pipeline in `szd-zenodo-backup/` |
| `ZIMLAB/szd` (gams-www) | Presentation layer, meaning the XSLT, JavaScript, CSS and SPARQL query templates that GAMS applies, including the RDF transformation `szd-TORDF.xsl` |

The repositories do not see each other automatically. Their cross-references stand in both `CLAUDE.md` files. The operator pushes and ingests. Scripts that must read the presentation layer, such as `scripts/checkup_2026_09_index/verify_orphan_persons.py`, expect its checkout at `ZIMLAB/szd` beside this repository.

```
TEI in chpollin/SZD
  └─ Cirilo ingest ──► GAMS object (Fedora, PID o:szd.*)
                         ├─ TEI_SOURCE datastream
                         ├─ RDF via szd-TORDF.xsl ──► Blazegraph triple store
                         └─ rendering via gams-www XSLT ──► https://stefanzweig.digital
```

## Publication Workflow

1. TEI files are edited in `data/`. Repairs run as scripts with a dry run, an `--apply` step and a `--verify` step that checks the written state against `HEAD`. Every correspondence Konvolut of production is in the repository since 24 September 2026, so Konvolut corrections happen here too.
2. `scripts/staging_package/build_staging_package.py --out <folder>` copies the files to ingest into a package outside the repository, in three folders for indexes, holdings and Konvolute, with checksums and a README. The README lists per object the `STYLESHEET` and `TORDF` references it still needs, read live from the datastream redirects of staging. Both references point to the gamsdev mirror of the presentation layer, and a character after `.xsl` makes a reference unusable. A Konvolut whose file does not name its own PID stays out, because Cirilo takes the PID of a new object from the file.
3. The operator ingests the package with Cirilo in folder order, first on GAMS staging and, after approval by the archive, on the productive instance. At ingest, GAMS derives the RDF with the `TORDF` stylesheet the object points to, so the indexes go in before the holdings that reference them.
4. The gams-www XSLT renders the TEI to HTML. Search pages run SPARQL query objects against Blazegraph and render the XML result sets.

### Ingesting TEI with Cirilo

Every TEI document of this repository, holdings, indexes, Konvolute and theme pages, goes in through the same dialog.

1. In Cirilo open the dialog "Ingest objects".
2. Choose the content model "TEI Object | cirilo:TEI.szd". The owner is `szd`. Leave the PID box unticked.
3. Press "From filesystem" and select the files of one package folder. Cirilo takes the PID of each object from `<idno type="PID">` in the TEI header, so an existing object is updated and a missing one is created. A file with a wrong PID creates or overwrites the wrong object.
4. "Show log" lists what was created or refreshed. The dialog also offers "Simulate ingest".

Context objects, query objects, the SKOS glossary and the facsimile book objects have content models of their own and do not go through this dialog.

A new object takes its datastream references from the content model object `cirilo:TEI.szd`. Its `TORDF` points to the gamsdev mirror and its `STYLESHEET` to the generic GAMS TEI stylesheet, which every Konvolut created by the staging ingest of 2026-09-24 received, so a newly created Konvolut needs `szd-Konvolut.xsl` set afterwards. Setting the `STYLESHEET` of `cirilo:TEI.szd` to `szd-Konvolut.xsl` before a folder of new Konvolute would give them the right reference at creation, an inference from this inheritance that no ingest has tested yet. An updated object keeps the references it already has. Cirilo logs an object as refreshed even when its `TORDF` reference is unusable, and the RDF of such objects on staging then differs from the RDF the current stylesheet builds locally, so the log proves the TEI update, not the RDF.

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

- [DATA_MODEL.md](DATA_MODEL.md), encoding patterns and authority references
- [COLLECTIONS.md](COLLECTIONS.md), collections and rendering contracts
- [ONTOLOGY.md](ONTOLOGY.md), the formal ontology and its documentation site
- [PROJECT.md](PROJECT.md), project context and standards
- [plan](plan.md), the pending staging and production ingest
