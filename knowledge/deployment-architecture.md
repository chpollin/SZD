---
title: Deployment architecture
project:
  name: Stefan Zweig Digital
  repository: https://github.com/chpollin/SZD  # the served files it describes are in https://zimlab.uni-graz.at/gams/projects/szd/gams-www
method:
  name: Promptotyping
  url: https://dhcraft.org/Promptotyping/
status: complete
language: en
created: 2026-10-09
updated: 2026-10-28
authors: [Christopher Pollin]
generated-with: Claude Code (Claude Opus 5.5)
related: [architecture, governance, testing, search-architecture, rdf-mapping]
---

# Deployment architecture

How a commit of gams-www and a data change of this repository reach staging and production, and which references in Cirilo, the GAMS client for ingest and object maintenance, must be set for a page to render. Stylesheets, scripts, styles and assets named in code formatting without a link lie in gams-www (https://zimlab.uni-graz.at/gams/projects/szd/gams-www). Who may carry out each step is laid down in [governance](governance.md).

## Environments

The served code of gams-www exists in four places that do not synchronise by themselves. The data repository [chpollin/SZD](https://github.com/chpollin/SZD) on GitHub holds data, knowledge, harness, ingest stylesheet copies and query templates. GAMS does not read it. The operator ingests from its `data/` and copies the query templates of its `gams/query/` into Cirilo.

| Place | Role |
|---|---|
| Local working copy | development and checks with the harness in [local-test-build/](../local-test-build/README.md), which lies in the data repository since October 2026 |
| ZimLab, `https://zimlab.uni-graz.at/gams/projects/szd/gams-www.git` | Git remote `origin` of gams-www and source of truth of the served files, reachable from the university network or over VPN |
| gamsdev mirror on the staging server | checkout of `origin/develop`, served at `https://gams-staging.uni-graz.at/gamsdev/pollin/szd/gams-www/` |
| Production checkout | checkout of `origin/main`, served at `https://gams.uni-graz.at/szd/` and through the public domain `https://stefanzweig.digital/` |

Staging (`gams-staging.uni-graz.at`) is reachable only from the university network or over VPN and appends the watermark "preliminary test version" to every page. Production went live with the full frontend overhaul on 2026-10-09.

## Branches

Development of gams-www runs on `develop`. `main` carries only the published state. The data repository works on `master`, from which GitHub Pages serves `docs/`. The gamsdev mirror follows `develop`, the production checkout follows `main`.

The gamsdev mirror is never edited. Its synchronisation, run in the mirror checkout, is

```
git fetch origin
git reset --hard origin/develop
```

The server checkout belongs to another user account, so Git needs a one-time `safe.directory` exception for its path. The state the mirror carried before its first clean-up is kept on ZimLab in the branch `server-gamsdev-snapshot-2026-09-11`.

## Release flow

The GAMS updater on the production server pulls ZimLab `main` by fast-forward into the checkout served under `/szd/` and cannot deliver any other branch. A release merges `develop` into `main`. A single feature that has to go online without the rest of `develop` goes in as a commit on `main` that applies only its changes to the published state. Because the updater only fast-forwards, `main` is never rewritten. The update is a publication for every user of the site and follows the approval of the state by the project partners.

The production objects reference their stylesheets under `https://gams.uni-graz.at/szd/`, so a release needs no change of references.

A feature that spans several files arrives complete or not at all. The Konvolut mode of the correspondence gallery, for instance, needs `szd-Facsimiles.xsl`, `szd-static.xsl`, `szd-Templates.xsl` and `js/facsimiles-konvolut.js` together, otherwise the page renders half a state.

## Asset releases and cache headers

Project CSS, JavaScript and timeline JSON use the release value in `$asset-version` in `szd-static.xsl`. Change it whenever one of these assets changes. `fn:asset-url` builds the XSLT links; the download loader and timeline pass the same value to their deferred requests. Tokens load as an explicit versioned stylesheet after `szd.css`, whose Bootstrap import stays in the `legacy` layer. Its unversioned tokens import remains as a compatibility fallback for cached old HTML; the later versioned link overrides those values in new pages. Remove the fallback only when old page heads no longer need it. Release URLs must never be added to Cirilo `STYLESHEET` or `TORDF` references, which still end in `.xsl`.

Deploy the XSLT and its assets as one consistent state. The current mutable filenames do not retain immutable release contents, so do not give them `immutable` or a long freshness lifetime just because they carry a query parameter. For HTML and mutable project assets, the GAMS operators should configure the effective response header `Cache-Control: no-cache`, retaining the existing asset `ETag` and `Last-Modified` validators. This includes CSS, JavaScript and timeline JSON on production and staging, and the SZD aliases. Check the actual response headers through both the GAMS and SZD hosts after configuration. Neither gams-www nor the data repository contains the production nginx/Cocoon configuration, so neither can apply that change.

The first versioned release escapes pre-existing unversioned CSS/JS caches. Header changes alone do not reach a client while it continues to reuse an old fresh response. Existing open pages can keep their loaded state until navigation or reload. A deployment check must include a returning browser as well as a fresh one, menu operation and a complete image ZIP download.

## Staging workflow

1. Check the change locally as [testing](testing.md#rule) requires and commit it on `develop` of gams-www.
2. Push to `origin`.
3. Synchronise the gamsdev mirror with the two commands above.
4. Set or correct the Cirilo references the change needs, see [Cirilo references](#cirilo-references).
5. Ingest the objects whose RDF or TEI changed. An ingest runs the `szd-TORDF.xsl` that lies in the mirror at that moment, so an object ingested before step 3 carries the old RDF and must be ingested again.
6. Review the result on staging in both languages, with the keyboard and at narrow width. A local preview never replaces this review.

## Data ingest

A change of the TEI sources reaches GAMS by ingest, independently of a release of gams-www.

### Publication workflow of the data

1. TEI files are edited in `data/`. Repairs run as scripts with a dry run, an `--apply` step and a `--verify` step that checks the written state against `HEAD`. Every correspondence Konvolut of production is in the repository since 24 September 2026, so Konvolut corrections happen here too.
2. `scripts/staging_package/build_staging_package.py --out <folder>` copies the files to ingest from `HEAD` into a package outside the repository, in three folders for indexes, holdings and Konvolute, with checksums and a README. Uncommitted changes under `data/` stay out and are named, and an `--out` inside the repository is refused. Before it writes, the script runs `scripts/check_data.py` over the same files and stops on a file that is not well formed or on a new finding of a decided check. The README lists per object the `STYLESHEET` and `TORDF` references it still needs, read live from the datastream redirects of staging. Both references point to the gamsdev mirror of the presentation layer, and a character after `.xsl` makes a reference unusable. A Konvolut whose file does not name its own PID stays out, because Cirilo takes the PID of a new object from the file. A staging answer other than a redirect, 400 or 404 is listed in the README as unreadable and ends the run with exit code 1, so that a server error never passes for a new object.
3. The operator ingests the package with Cirilo in folder order, first on GAMS staging and, after approval by the archive, on the productive instance. At ingest, GAMS derives the RDF with the `TORDF` stylesheet the object points to, so the indexes go in before the holdings that reference them.
4. The gams-www XSLT renders the TEI to HTML. Search pages run SPARQL query objects against Blazegraph and render the XML result sets.

### Ingesting TEI with Cirilo

Every TEI document of the data repository, holdings, indexes, Konvolute and theme pages, goes in through the same dialog.

1. In Cirilo open the dialog "Ingest objects".
2. Choose the content model "TEI Object | cirilo:TEI.szd". The owner is `szd`. Leave the PID box unticked.
3. Press "From filesystem" and select the files of one package folder. Cirilo takes the PID of each object from `<idno type="PID">` in the TEI header, so an existing object is updated and a missing one is created. A file with a wrong PID creates or overwrites the wrong object.
4. "Show log" lists what was created or refreshed. The dialog also offers "Simulate ingest".

Context objects, query objects, the SKOS glossary and the facsimile book objects have content models of their own and do not go through this dialog.

A new object takes its datastream references from the content model object `cirilo:TEI.szd`. Its `TORDF` points to the gamsdev mirror and its `STYLESHEET` to the generic GAMS TEI stylesheet, which every Konvolut created by the staging ingest of 2026-09-24 received, so a newly created Konvolut needs `szd-Konvolut.xsl` set afterwards. Setting the `STYLESHEET` of `cirilo:TEI.szd` to `szd-Konvolut.xsl` before a folder of new Konvolute would give them the right reference at creation, an inference from this inheritance that no ingest has tested yet. An updated object keeps the references it already has. Cirilo logs an object as refreshed even when its `TORDF` reference is unusable, and the RDF of such objects on staging then differs from the RDF the current stylesheet builds locally, so the log proves the TEI update, not the RDF.

Facsimiles are separate `cm:dfgMETS` book objects (`o:szd.<number>`) whose IIIF manifests feed the Mirador viewer. Catalogue entries link them through `altIdentifier/idno[@type="PID"]`, see [collections.md](collections.md#rendering-contract-grouped-lists).

## Cirilo references

Three kinds of settings in Cirilo decide whether a page renders on an instance as intended. [local-test-build/gams-objects.toml](../local-test-build/gams-objects.toml) records the expected values in machine-readable form for a read-only check against staging or production. Deviations read on staging are listed in [plan](plan.md#staging-reading-of-2026-09-24).

### Stylesheet references

Every TEI, context and query object carries in its datastream `STYLESHEET` an external reference to its page stylesheet. A new object created in Cirilo receives the generic GAMS TEI stylesheet from its content model, recognisable by the heading "A TEI Project". An updated object keeps its old reference. Old references on staging point to the retired host `glossa.uni-graz.at` or to the SVN path `trunk/www`, which no longer exists. The target value is the base of the instance plus the file name, `https://gams-staging.uni-graz.at/gamsdev/pollin/szd/gams-www/` on staging and `https://gams.uni-graz.at/szd/` in production.

| Object | Stylesheet |
|---|---|
| `o:szd.werke`, `o:szd.lebensdokumente`, `o:szd.nli` | `szd-Werke.xsl` |
| `o:szd.werkindex`, `o:szd.personen`, `o:szd.standorte`, `o:szd.organisation` | `szd-Index.xsl` |
| `o:szd.bibliothek` | `szd-Bibliothek.xsl` |
| `o:szd.autographen` | `szd-Autographen.xsl` |
| `o:szd.glossar` | `szd-Glossar.xsl` |
| `o:szd.lebenskalender` | `szd-Lebenskalender.xsl` |
| `o:szd.korrespondenzen` | `szd-Korrespondenzen.xsl` |
| `o:szd.korrespondenzen.<person>`, every Personen-Konvolut | `szd-Konvolut.xsl` |
| `o:szd.aufsatzablage` | `szd-Essays.xsl` |
| `o:szd.thema.<n>`, every theme page | `szd-Thema.xsl` |
| `o:szd.SZDBRI.1`, prototype of the letter edition | `szd-Briefedition.xsl` |
| `context:szd` | `szd-context.xsl` |
| `context:szd.facsimiles`, `context:szd.facsimiles.korrespondenzen`, `context:szd.facsimiles.lebensdokumente`, `context:szd.facsimiles.aufsatz` | `szd-Facsimiles.xsl` |
| `query:szd.person_search`, `query:szd.fulltext`, `query:szd.standort_search`, `query:szd.category_search`, `query:szd.work_search` | `szd-Suche.xsl` |

`o:szd.ontology` renders through the GAMS stylesheet `cirilo:Backbone/datastreams/ONTOLOGYtoHTML`.

The four indexes render from the shared file `szd-Index.xsl`. `szd-Personenliste.xsl`, `szd-Standortliste.xsl`, `szd-Werkliste.xsl` and `szd-Organisationen.xsl` only include it, so that references set earlier keep working. They can be deleted once all four index objects reference `szd-Index.xsl` on both instances.

A reference to an include file has a side effect. After the release of 2026-10-09 exactly the three production objects whose `STYLESHEET` still named an include file (`o:szd.werkindex` with `szd-Werkliste.xsl`, `o:szd.personen` with `szd-Personenliste.xsl`, `o:szd.standorte` with `szd-Standortliste.xsl`) kept serving the output from before the release, with the old menu and without digit jump links, while every object whose referenced stylesheet had changed or that references a stylesheet directly showed the new code. This suggests that GAMS caches a transformation by its top-level file and does not notice changes in included stylesheets while the referenced file is unchanged. The remedy is to point these references at `szd-Index.xsl`, see [plan](plan.md#production).

The reference of an object can be read without login from the redirect of `https://<host>/archive/objects/<pid>/datastreams/STYLESHEET/content`. A reference with a trailing illegal character answers there with HTTP 400 and the message "Illegal character in path", although the page itself may still render.

### Context membership of the facsimile objects

The galleries list the METS objects whose datastream `RELS-EXT` carries an `isMemberOf` to the gallery context. A METS object ingested in Cirilo lacks this relation at first and is missing from the gallery until it is assigned. Personal documents (shelfmarks `SZ-AAP/L`, `SZ-AP2/L`) belong in `context:szd.facsimiles.lebensdokumente`, correspondence and picture postcards (`SZ-LAS/B`, `SZ-SAM/B`, `SZ-SAM/AK`) in `context:szd.facsimiles.korrespondenzen`.

### Query datastreams

The result schema of a gallery is fixed by the SPARQL query in the datastream `QUERY` of its context object. The correspondence gallery needs `creator`, `contributor` and `date` in the result, see [correspondence-gallery-architecture](correspondence-gallery-architecture.md#data-flow). The production query is the template and lies at `https://gams.uni-graz.at/archive/objects/context:szd.facsimiles.korrespondenzen/datastreams/QUERY/content`. The other galleries run with the GAMS default query.

The content search runs through the `QUERY` datastreams of the five query objects. The operator copies a changed template from [gams/query/](../gams/query/README.md) of this repository into the datastream, as done for all five in production on 2026-10-09. GAMS never reads the templates from a repository, neither formerly from `query/` of gams-www nor now from `gams/query/`.

| Query object | Datastream `QUERY` from |
|---|---|
| `query:szd.person_search` | `gams/query/person_search.sparql` |
| `query:szd.fulltext` | `gams/query/fulltext_search.sparql` |
| `query:szd.category_search` | `gams/query/category_search.sparql` |
| `query:szd.standort_search` | `gams/query/standort_search.sparql` |
| `query:szd.work_search` | `gams/query/work_search.sparql` |

### RDF ingest reference

`szd-TORDF.xsl` produces the RDF of a TEI object at ingest. The datastream `TORDF` of every TEI object names the stylesheet copy to run, `https://gams-staging.uni-graz.at/gamsdev/pollin/szd/gams-www/szd-TORDF.xsl` on staging and `https://gams.uni-graz.at/szd/szd-TORDF.xsl` in production. A new TEI object inherits this reference from the content model `cirilo:TEI.szd`, whose `TORDF` redirects to the served copy of `szd-TORDF.xsl` of its instance, the gamsdev mirror on staging and `https://gams.uni-graz.at/szd/szd-TORDF.xsl` in production (read on 2026-10-28), so the file must stay in gams-www. Every object needs a valid reference before it is ingested.

The ingest resolves person, repository and organisation references against the index objects, so `o:szd.personen`, `o:szd.standorte` and `o:szd.organisation` are ingested before the holdings. Nothing enforces this order. `o:szd.organisation` was ingested in production only on 2026-10-09, after the holdings, so the production RDF of the holdings carries the `SZDORG` references only after their renewed ingest, see [plan](plan.md#production). How the RDF transformation finds the organisation index on each instance is explained in [rdf-mapping](rdf-mapping.md#index-hosts).

### Ingest stylesheets in Cirilo

A reading of the Cirilo datastreams on staging and production on 2026-10-28 established which ingest stylesheets each instance runs.

- `cirilo:TEI.szd/TORDF` redirects to the served copy of `szd-TORDF.xsl` of its instance, the gamsdev mirror on staging and `https://gams.uni-graz.at/szd/szd-TORDF.xsl` in production, so that file must stay in gams-www.
- `cirilo:szd/TOMETS` is an inline value on both instances. The production value equals the former gams-www `szd-TOMETS.xsl` plus one `xsl:value-of select="vi:category"`, and [gams/szd-TOMETS.xsl](../gams/szd-TOMETS.xsl) is a byte copy of the production datastream as served on 2026-10-28. The staging value differs from both.
- `cirilo:szd/DC_MAPPING` is a short generic mm:metadata-mapping, identical on staging and production. Neither instance references `szd-MODStoDC_MAPPING.xsl`, which [gams/szd-MODStoDC_MAPPING.xsl](../gams/szd-MODStoDC_MAPPING.xsl) keeps as a documented copy.
- `HSSF_STYLESHEET` and `TEItoHSSF` of `cirilo:szd` are generic inline Gnumeric templates on staging, and `HSSF_STYLESHEET` answers 404 on production. Neither instance references `szd-tei-hssf.xsl`, which [gams/szd-tei-hssf.xsl](../gams/szd-tei-hssf.xsl) keeps as an editorial export tool.
- The operator copies the five query templates into the `QUERY` datastreams, see [Query datastreams](#query-datastreams). GAMS never reads them from gams-www.

Because GAMS serves none of these files from gams-www, the three stylesheets and the query templates moved into [gams/](../gams/) of the data repository in October 2026, while `szd-TORDF.xsl` stays in gams-www.

## Checking an instance

After a change, call the page at `https://<host>/<pid>/sdef:TEI/get?locale=de`, or `/archive/objects/<pid>/methods/sdef:Context/get?locale=de` for a context, in both languages, and compare staging with production. The symptoms point to their cause.

| Symptom | Cause |
|---|---|
| HTTP 500 with "Error getting http://glossa…", or a 404 target of the stylesheet redirect | dead stylesheet reference |
| heading "A TEI Project" | generic GAMS stylesheet instead of the project stylesheet |
| empty gallery | missing context membership or a `QUERY` without the grouping fields |

Every object exposes its datastreams at `https://<host>/archive/objects/<PID>/datastreams/<DSID>/content`, among them `DC`, `RELS-EXT`, `QUERY`, `METADATA` (the SPARQL result of a context object), `TEI_SOURCE`, `STYLESHEET`, `TORDF` and `RDF`. Comparing these datastreams between staging and production is the quickest diagnosis of a deviating page.

`local-test-build/check-instance.py` reads the references, the queries, the `RDF` presence and, with `--data`, the currency of every `TEI_SOURCE` against the data repository for a whole instance and ends with the operator checklist, see the [harness README](../local-test-build/README.md#instance-check). Use it for instance configuration changes and before and after an ingest. Frontend-only releases use the page, asset and download checks in [testing](testing.md#rule).
