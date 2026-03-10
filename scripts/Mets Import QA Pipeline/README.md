# GAMS Viewer Import QA Pipeline

Pre-ingest validation and cleanup for digitized object metadata (GAMS Viewer XML + page images).

## Dataset: SZ-AAL/B2

Stefan Zweig → Lotte Zweig correspondence (1934–1935), Literaturarchiv Salzburg.
49 objects (`SZ_AAL_B2.1`–`SZ_AAL_B2.50`, B2.40 missing), each containing a `Result_*.xml` and JPEG page images.

## Scripts

| Script | Purpose |
|--------|---------|
| `validate_results.py` | Validates XML well-formedness, image references, naming conventions, metadata completeness, and structural consistency |
| `fix_issues.py` | Applies automated fixes (see below) |

Run: `python validate_results.py` / `python fix_issues.py`

## Fixed Issues

| Issue | Folders | Fix |
|-------|---------|-----|
| Duplicate/misnamed XML files | B2.1–5 | Renamed to `Result_SZ_AAL_B2.{N}.xml`, deleted duplicates |
| Extensionless XML duplicates | B2.1–5 | Deleted |
| Extraneous `xmlns:file` namespace | B2.1–5 | Removed |
| `Farbreferenzen` (plural typo) | B2.14 | Corrected to `Farbreferenz` |
| `Textseite`/`Adressseite` (singular) | B2.50 | Corrected to plural form |

## Open Issues (require manual intervention)

| Issue | Folder |
|-------|--------|
| Empty XML (0 bytes) | B2.16 |
| Missing image `_004.jpg` + empty `<date/>` | B2.33 |
| Missing folder | B2.40 |

## XML Structure

```xml
<book xmlns="http://gams.uni-graz.at/viewer">
  <title>Brief/Postkarte/Kuvert von Stefan Zweig an Lotte Zweig [Datum], SZ-AAL/B2.N</title>
  <author>Zweig, Stefan</author>
  <date>D.M.YYYY</date>
  <category/>
  <owner><name>Literaturarchiv Salzburg, https://stefanzweig.digital, CC-BY</name></owner>
  <structure>
    <div type="Textseiten">...</div>       <!-- letter pages -->
    <div type="Kuvert">...</div>           <!-- envelope, if present -->
    <div type="Adressseiten">...</div>     <!-- postcard address side -->
    <div type="Ansichtsseite">...</div>    <!-- postcard view side -->
    <div type="Farbreferenz">...</div>     <!-- color reference chart -->
  </structure>
</book>
```
