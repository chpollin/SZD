# SPARQL

### Selecting data sources in DB via PID:

```
FROM <o:szd.bibliothek>
FROM <o:szd.autographen>
FROM <o:szd.werke>
FROM <o:szd.personen>
FROM <o:szd.lebenskalender>
FROM <o:szd.lebensdokumente>
```

### Marking the SPARQL XML-Output for language tag 

(*quick-and-dirty hack*)

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

### Param: $1, $2

$n is placeholder for param for query object.
$2 contains language tag ("de", "en")

## Fulltext

- selects: all resources containing the sting (param) in gams:textualContent data property
- param: a string
- bds:blazegraph specific namespace - https://github.com/blazegraph/database/wiki/FullTextSearch

## Location

+ selects: all resources connected to a location (=standort)
+ param: <https://gams.uni-graz.at/o:szd.standorte#SZDSTA.2>
+ return: resource like a szd:Work or szd:Book

## Person

+ selects: all resources connected to a person
+ param: <https://gams.uni-graz.at/o:szd.personen#SZDPER.1>
+ return: resource like a szd:Work, szd:Book, or szd:Event

## Category

+ selects: all resources connected to a category (http://gams.uni-graz.at/o:szd.glossar/ONTOLOGY)
+ param: <https://gams.uni-graz.at/o:szd.glossar#Insertion>
+ return: resource like a szd:Work or szd:Book