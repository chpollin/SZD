---
doc: DATA
project: fix-szd
version: 0.3.0
updated: 2025‑04‑22
tags: [data]
---

### Datasets at a Glance

| Dataset            | Description                                                   | Records / Files                    | Format  |
|--------------------|---------------------------------------------------------------|------------------------------------|---------|
| SPARQL result set  | Fedora RISearch rows for `szd.facsimiles.korrespondenzen`     | 1 201 rows (259 partners)          | XML     |
| TEI sources        | TEI XML per partner (`…/o:{slug}/TEI_SOURCE`)                 | 246 found / 13 missing (~5 %)      | TEI XML |
| Convolute map      | Signatures (`SZ‑…`) extracted from every TEI and grouped      | 246 partners → > 250 signatures    | in log |

### Schema Outline

* **`sparql`** (root)  
  * `head` – nine `variable @name` nodes (column list).  
  * `results/result` – 1 201 records containing:  
    `cid`, `container`, `pid`, `model`, `title`, `identifier`,  
    `creator`, `contributor [@bound]`, `date`.  
* **TEI sources** – `<listBibl>/<biblFull>/<idno type="signature">` holds one
  **convolute signature** such as `SZ‑SAM/AK.12`.  
  Multiple `<biblFull>` ⇒ multiple signatures for a partner.

### Access Patterns

* Look up a metadata row by `pid`.  
* Filter rows by `date` year.  
* Aggregate by `container` to map sub‑collections.  
* Resolve TEI source with ASCII‑only slug formula  
  (strip diacritics, `ß→ss`, spaces/commas → `-`).  
* Harvest all signatures from each TEI and build a partner → convolute list
  (now logged).

### Data Gaps

* 13 partners still lack a TEI file (mostly corporate names with punctuation).  
* Some `contributor`/`date` nodes have `@bound="false"` → treat as **NULL**.  
* A handful of dates deviate from ISO 8601; normalise on ingest.

_Last crawl: 22 Apr 2025 — 246 / 259 TEI sources parsed; signature grouping
written to **fetch_korrespondenzen.log**._ :contentReference[oaicite:0]{index=0}&#8203;:contentReference[oaicite:1]{index=1}
