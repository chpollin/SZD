# SZ-AAL personal documents to SZDLEB.xml

Workflow that turns personal documents from a Google Sheets export (CSV) into the TEI collection [`data/PersonalDocument/SZDLEB.xml`](../../data/PersonalDocument/SZDLEB.xml). It is reusable for any later batch with the same column layout.

## Scope

The script handles personal documents (SZDLEB, `<biblFull>`) only. The letter series `SZ-AAL/B2.N` belongs to the correspondence (SZDKOR), which follows another schema.

## CSV format

38 columns in fixed order (see the `C_*` constants in `csv_to_szdleb.py`), the first row is the header. The script expects these conventions.

- Several persons per cell are separated by semicolon (`Zweig, Stefan; Hollander, Barnett`). The comma separates only `Surname, Forename` within one person.
- GND as URL, in the same order as the name column, empty slots as an empty semicolon segment.
- Person names preferably as `Surname, Forename`, split into `surname` and `forename`.
- Dating in an original, a supplied and a normalised column. The script shows the original wording, supplied dates in `[…]`, and sets `@when` from the ISO column (`YYYY`, `YYYY-MM`, `YYYY-MM-DD`).

## Run

```bash
# 1) dry run, produces the XML block and a report, writes nothing
python scripts/szaal_lebensdokumente/csv_to_szdleb.py --csv <export.csv> \
    --gesamttitel "Stefan Zweig - <Bestandsname>"

# 2) check the report (see below), then apply
python scripts/szaal_lebensdokumente/csv_to_szdleb.py --csv <export.csv> \
    --gesamttitel "Stefan Zweig - <Bestandsname>" --apply
```

Parameters are `--csv` (required), `--szdleb` and `--szdper` (default the repository paths), `--gesamttitel` (default a placeholder that must be replaced by the written-out collection name), `--start-id` (0 continues the numbering of the file) and `--apply` (without it only a dry run).

Built-in safeguards stop the run when the first signature already stands in SZDLEB, check the well-formedness of the block and of the whole file after writing, and resolve GND to SZDPER live from the person index without hard-coded person identifiers.

## Manual follow-up

The report lists the places the script cannot settle.

- „Personen OHNE SZDPER-Verknüpfung“ lists persons missing from [`SZDPER.xml`](../../data/Index/Person/SZDPER.xml). Create them with GND where one exists, otherwise with `surname` and `forename` only and never a guessed GND, then add `ref="#SZDPER.N"` on `editor` or `author` in the SZDLEB entry.
- „Personen ohne 'Nachname, Vorname'-Form“ lists names taken over as full `persName` text, to be checked.
- „Als Körperschaft (orgName) modelliert“ lists institutions recorded as `<editor><orgName>` by the keyword heuristic `ORG_KEYWORDS`. Check that nothing was classed as a corporate body by mistake. Corporate bodies belong to the organisation index, see [`knowledge/COLLECTIONS.md`](../../knowledge/COLLECTIONS.md#organisation-index-szdorg).
- The Gesamttitel must be the written-out collection name, uniform across all entries (as in `Stefan Zweig - Alberman Papers 2`).
- A comma instead of a semicolon in the CSV glues two persons together, which the report shows as an unstructured name. Correct it in the CSV or in the XML.

PIDs (`o:szd.*`) are not assigned locally but at the GAMS ingest.

## First application

SZ-AAL/L1–L13 became SZDLEB.144–156 in June 2026. The person index received SZDPER.2314 Hollander (GND), 2315 Altmann (GND), 2316 Geiringer, 2317 Meiler and 2318 Ullmann (the last three without GND). 2316 and 2317 turned out to be duplicates of existing entries and were merged into them (commit `ce23ddad`). SZDLEB.51 (title and dating of the birth certificate photocopy) and SZDLEB.137 (`ana` to `xml:id`) were corrected at the same time.
