---
title: Search architecture
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
related: [rdf-mapping, rendering-architecture, deployment-architecture, specification]
---

# Search architecture

How the content search of SZD runs, from the search link or form through the five SPARQL query objects to the result page rendered by `szd-Suche.xsl`. The RDF it searches is described in [rdf-mapping](rdf-mapping.md), the parameterisation of the query templates in [gams/query/README.md](../gams/query/README.md). Stylesheets, scripts, styles and assets named in code formatting without a link lie in gams-www (https://zimlab.uni-graz.at/gams/projects/szd/gams-www).

## Request flow

The five query objects `query:szd.*` run against the `szd:` RDF in Blazegraph. Every request is a full navigation to `/archive/objects/query:<query>/methods/sdef:Query/get?params=…&locale=…`, whose result XML `szd-Suche.xsl` renders. `sdef:Query/getXML` with the same `params`, but without `locale`, returns the unrendered SPARQL result; with `locale` it answers HTTP 500. The search uses no client-side AJAX and no DataTables.

- The full-text search is a form in the navigation bar of `szd-static.xsl`. `js/buildquery.js` serialises the input of `#fulltext_search` to `$1|value;$2|locale` and navigates through `window.location`.
- Person, repository, category and work searches are links built by the page stylesheets through `fn:query-href` in `szd-Templates.xsl`. The function takes query object, index PID, entry identifier and locale and encodes the parameter `$1|<https://gams.uni-graz.at/<index>#<id>>;$2|<locale>` with `encode-for-uri`. The helpers `createPersonSearchHREF`, `LocationSearch` and `WorkSearch` wrap it, glossary and search page call it directly, and the page shell calls it for person names in TEI text (`t:name[@type='person']` in `szd-static.xsl`).

GAMS substitutes `$1`, the search object, and `$2`, the language tag `de` or `en`, at runtime into the query of the datastream `QUERY`.

## Query objects

All five queries read the graphs `o:szd.bibliothek`, `o:szd.autographen`, `o:szd.werke`, `o:szd.personen`, `o:szd.lebenskalender`, `o:szd.lebensdokumente` and `o:szd.korrespondenzen`. The table names the further graphs.

| Query object | Template | Parameter `$1` | Binding | Further graphs |
|---|---|---|---|---|
| `query:szd.fulltext` | [fulltext_search.sparql](../gams/query/fulltext_search.sparql) | string | `?text bds:search "$1"` on `gams:textualContent`, with `bds:` = `http://www.bigdata.com/rdf/search#` | `o:szd.aufsatzablage`, `o:szd.organisation`, `o:szd.thema.1` to `o:szd.thema.8` |
| `query:szd.person_search` | [person_search.sparql](../gams/query/person_search.sparql) | URI `…/o:szd.personen#SZDPER.n` or `…/o:szd.organisation#SZDORG.n` | `?re ?hasrole $1`, any predicate, name through `szd:surname` or `szd:name` | `o:szd.aufsatzablage`, `o:szd.organisation`, `o:szd.thema.1` to `o:szd.thema.8` |
| `query:szd.standort_search` | [standort_search.sparql](../gams/query/standort_search.sparql) | URI `…/o:szd.standorte#SZDSTA.n` | `?re szd:location $1` | `o:szd.aufsatzablage`, `o:szd.organisation`, `o:szd.standorte` |
| `query:szd.category_search` | [category_search.sparql](../gams/query/category_search.sparql) | glossary URI `…/o:szd.glossar#…` | `?re szd:glossar $1` or through `szd:provenanceCharacteristic` | `o:szd.organisation` |
| `query:szd.work_search` | [work_search.sparql](../gams/query/work_search.sparql) | URI `…/o:szd.werkindex#SZDWRK.n` | `?re szd:relationToWork $1` | `o:szd.aufsatzablage` |

The files in [gams/query/](../gams/query/README.md) of this repository, formerly `query/` of gams-www, are the templates of the `QUERY` datastreams. GAMS executes the version the operator has copied into Cirilo, and every query object references `szd-Suche.xsl` as its stylesheet, see [deployment-architecture](deployment-architecture.md#query-datastreams). A new collection or theme page is found only after a `FROM` line for its graph has been added to every query that should read it.

## Renderer

`szd-Suche.xsl` recognises the search type from the URI in `s:query/@uri`, shows search term and hit count, builds the filter bar and renders the hits as Bootstrap collapse cards with a data basket button and a link to the catalogue view. The work search returns no work title, so its header names the search type only.

The table `SearchCollections` at the top of the file lists the holdings, one row per holding in the order of the filter buttons. `@match` is the PID fragment by which a hit is recognised, `@id` the target of the filter button, `@radio` the `id` of the button, and the label comes from `@i18n` or from `@de` and `@en`. `list="no"` marks holdings with their own block above the result lists, namely themes, persons and biography. The filter bar tests `@match` against all collection URIs of the result, a result list tests `/` plus `@match` against its own collection URI, and the first matching row wins, which is why `o:szd.korrespondenzen.` for the pieces precedes `o:szd.korrespondenzen` for the Konvolute. The result lists follow the descending order of the collection URIs. A new holding needs only a new row.

Each object gets one card, even when the query returns it in several rows, one per language or per person. `SearchListGroup` reduces the rows by the fragment of the hit URI, preferring a row with `s:a='T'` that names an author, and the header counts the objects that receive a card or a block entry. A result without hits gets a neutral heading, because the query type cannot be read from an empty result. A full-text result at the `LIMIT` of its query (10000 rows, 20000 for the person search) carries a notice that the list is truncated.

The filter buttons are visibility switches in the browser, radio buttons with the inline function `filter()`, and trigger no new query. On the server only the language tag `$2` narrows the result.

Hits with a URI under `o:szd.organisation#` stand in the block "Organisationen" (`id="organisation_search"`) after the person block, one entry per organisation with the name from `s:s`, linked relatively to its entry in the organisation index. Before 2026-10-21 the renderer had no row for this collection and dropped them.

Hits with a URI under `o:szd.thema.` stand in the block "Themen" (i18n key `subjects`, `id="thema_search"`) before the person block. Every theme page appears once with its title, sorted alphabetically, and links relatively to `/o:szd.thema.<n>/sdef:TEI/get?locale=<de|en>`, so that staging points to staging and not to the production URI from the RDF. Because the URI of a theme page has no fragment, the filter bar groups hits without `#` by the full URI.

## Assessment of the queries

This assessment of 2026-09-23 rests on reading the queries and has not been tested against a SPARQL endpoint.

- The language ranking through `COALESCE` works only through errors. `IF(lang(?x)='$2', …)` raises an error on an unbound field, and only this makes `COALESCE` fall through to the next level.
- Literals without a language tag never receive `?a='T'`.
- The `FILTER` with `|| ?t || ?s` hardly filters, because every row with a title or name passes.
- `?s` is bound in three `OPTIONAL` blocks, at the hit itself, at the author and at the sender. A sender with a surname different from the author's is therefore probably lost.
- `LIMIT` can cut off silently for frequent search terms. The work search has no `LIMIT`.

The queries stay unchanged by operator decision of 2026-09-23, see [specification](specification.md#theme-pages-and-search).

## Open findings in the renderer

These findings come from the structure-preserving refactoring of 2026-09-23 and are not fixed.

- The filter button "Korrespondenz" has no target section when the result holds only pieces, because `o:szd.korrespondenzen` also matches the URIs of the pieces.
- The branches for `s:spi` and `s:fpi` are dead, because no query binds these variables. `s:ss` and `s:sf` are bound for the sender by `gams/query/work_search.sparql`, so their branches apply to hits of the work search.
- `lang="ger"` in the sort instructions is not a valid language code.
