---
doc: DATA
project: fix-szd
version: 0.5.0
updated: 2026-03-29
tags: [data, korrespondenzen, zweig]
---

# Correspondence corpus -- overview

## Snapshot (29 Mar 2026)

| Dataset            | Description                                                               | Records / Files | Format / Size |
|--------------------|---------------------------------------------------------------------------|-----------------|---------------|
| **TEI source**     | Correspondence register (`data/Correspondence/SZDKOR.xml`)                | 723 `<biblFull>` entries, 721 `<date>` elements | TEI-XML (~37 k lines) |

### Date quality

| Metric | Count |
|--------|------:|
| `<date>` with `@when`, `@notBefore`, or `@notAfter` | 702 (97 %) |
| `<date>` without machine-readable attribute (`n. d.`) | 19 (3 %) |

The 19 undated entries carry the text `n. d.` (no date) and cannot be normalized.

---

## Schema cheat-sheet

### TEI source

```
<TEI>
 └─ text
     └─ listBibl
         └─ biblFull*
             └─ idno type="signature"  →  SZ-…
```

A partner can have **multiple signatures** (e.g. one convolute plus standalone letters).

---

## Data gaps & clean-up queue

| Issue | Count | Remedy |
|-------|------:|--------|
| `n. d.` dates (no date available) | 19 entries | cannot be resolved without archival research |
| TEI signatures lacking external catalogue match | ~130 | create new catalogue rows or mark un-catalogued |

---

## Recommended access patterns

* **Filter by year** -- use `@notBefore` / `@notAfter` or `@when` on `<date>` elements.
* **Partner overview** -- group by `<biblFull>` and join to TEI signatures.
* **Item drill-down** -- join TEI signature for full physical & provenance data.

---

_Last refresh: 29 Mar 2026._
