# SPARQL templates

The files in this folder are the templates of the `QUERY` datastreams of the five query objects `query:szd.*`. GAMS executes the version the operator has copied into Cirilo. Which graphs each query reads, what it binds and which object carries it is listed in [knowledge/search-architecture.md](../../knowledge/search-architecture.md#query-objects), the Cirilo target values in [knowledge/deployment-architecture.md](../../knowledge/deployment-architecture.md#query-datastreams).

## Parameters

`$1` and `$2` are placeholders that GAMS fills at runtime from the `params` of the request. `$1` is the search object, `$2` the language tag (`de`, `en`).

## Selecting graphs

Every collection is a named graph whose URI is its PID. A query selects its graphs with `FROM` lines.

```
FROM <o:szd.bibliothek>
FROM <o:szd.autographen>
FROM <o:szd.werke>
FROM <o:szd.personen>
FROM <o:szd.organisation>
FROM <o:szd.lebenskalender>
FROM <o:szd.lebensdokumente>
FROM <o:szd.korrespondenzen>
```

A new collection or theme page is found only after its graph has been added to the queries that should read it.

## Marking the language of a result

A quick hack marks the rows whose title matches the requested language, and the result stylesheet filters on `?a`. Its weaknesses are assessed in [knowledge/search-architecture.md](../../knowledge/search-architecture.md#assessment-of-the-queries).

```
BIND
(
  COALESCE(
    IF(lang(?t)='$2' && lang(?ex)='$2', "T", ""),
      IF(lang(?t)='$2', "T", "")
        ,"") AS ?a
)
FILTER(lang(?h) = '$2'  && lang(?co) = '$2' || ?t || ?s)
```

## Queries

- Full text (`fulltext_search.sparql`) selects every resource whose `gams:textualContent` contains the string `$1`, through the Blazegraph full-text search (`bds:`, <https://github.com/blazegraph/database/wiki/FullTextSearch>).
- Person (`person_search.sparql`) selects every resource connected to the person or organisation `$1` by any predicate, for instance `<https://gams.uni-graz.at/o:szd.personen#SZDPER.1>`. Results are works, books, events, correspondence and theme pages.
- Repository (`standort_search.sparql`) selects every resource whose `szd:location` is the repository `$1`, for instance `<https://gams.uni-graz.at/o:szd.standorte#SZDSTA.2>`.
- Category (`category_search.sparql`) selects every resource connected to a glossary concept `$1`, for instance `<https://gams.uni-graz.at/o:szd.glossar#Insertion>`.
- Work (`work_search.sparql`) selects every resource related to the work index entry `$1` through `szd:relationToWork`, for instance `<https://gams.uni-graz.at/o:szd.werkindex#SZDWRK.1>`.
