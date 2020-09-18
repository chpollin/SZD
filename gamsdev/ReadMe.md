# gamsdev

### szd-static
* defines header, body and footer. is included in all xslt for webdev
* JS and CSS
* icons - img
* meta tags
* templates, which are used everywhere (like t:p->p)

### szd-context
* databasket, memory, map, about, imprint, home

### szd-Templates
* contains templates that are reused in different xslt (like print EN/DE)
* is inclued in most of the xslt

### szd-TORDF
* extracts semantic structures from TEI-Files and transforms it to RDF

### szd-

this templates have a primary data stream (https://github.com/chpollin/SZD/tree/master/data) and create the HTML presentation of it.

* szd-Autographen (SZDAUT)
* szd-Bibliothek (SZDBIB)
* szd-Werke (SZDMSK)
* szd-Lebenskalender (SZDLEB)
* szd-Standortliste (SZDSTA)
* szd-Personenliste  (SZDPER)

### szd-Suche
* transforms a SPARQL XML-Result to HTML

### templates not used in live system
* szd-Ontology
* szd-Collage (scan-image collage)
* szd-Collection
* szd-tei-hssf (Excel export for TEI data)
* szd-TOTEI
* szd-Publikationenliste  (SZDPUB)

