# GAMS ingest material

Files that the operator copies into Cirilo and that GAMS therefore never reads from the served folder of gams-www. `szd-TORDF.xsl` is the exception and stays in gams-www, because the datastream `TORDF` of `cirilo:TEI.szd` redirects to its served copy on staging and in production.

| File | Cirilo datastream | State read on 2026-10-28 |
|---|---|---|
| [query/](query/README.md) | `QUERY` of the five objects `query:szd.*` | copied by the operator, compared by `local-test-build/check-instance.py` |
| `szd-TOMETS.xsl` | `TOMETS` of `cirilo:szd` | byte copy of the production datastream, which is inline; the staging value differs |
| `szd-MODStoDC_MAPPING.xsl` | none | `DC_MAPPING` of `cirilo:szd` is a short generic metadata mapping on both instances, so this file is a kept copy of an earlier mapping |
| `szd-tei-hssf.xsl` | none | `HSSF_STYLESHEET` and `TEItoHSSF` of `cirilo:szd` are generic Gnumeric templates on staging and `HSSF_STYLESHEET` is missing in production, so this file serves as an editorial export tool |

A changed file here takes effect only when the operator copies it into the datastream. The values are read without login from `https://<host>/archive/objects/<pid>/datastreams/<dsid>/content`, one request after the other.
