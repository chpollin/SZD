# Data corrections from the live-site audit of 2026-10-13

`fix_audit_findings.py` repairs four findings of the audit of the published site, each only
where the data itself evidences the value. Nothing is taken from outside the repository.

| Finding | File | Rule |
| --- | --- | --- |
| `misc-number` | `webpage/MISCELLANEOUS.xml` | The English news items numbered the item with `NEWS_IMG_3` `n="2"` a second time, so the page carried the id `miscellaneous.2` twice. Each English item takes the `n` of the German item that shows the same `NEWS_IMG` datastream. |
| `empty-prov` | `data/Autograph/SZDAUT.xml` | `SZDAUT.218` carried `<provenance type="provenance">` with a blank German span only. Entries without that value omit the element, so the empty one is removed with its line. |
| `essay-id` | `data/Aufsatzablage/SZDESS.xml` | The entry SZ-AAP/W-AA212.3 (`o:szd.2838`) had the id `SZDESS.`, because its row in the source table `essays.csv` (removed in `e1dd5d73`) had no ID. It is no duplicate, its signature and PID are its own. The ids run from 1 without gap or suffix and are never renumbered, so it takes the next free number. The script refuses when there is more than one empty id or the ids have a gap. |
| `empty-wikidata` | `data/Index/Person/SZDPER.xml` | `SZDPER.2299` carried an empty `<idno type="wikidata">`. Persons without a Wikidata identifier omit the element, so it is removed with its line. |

The audit also named `SZDPER.2143`. Its GND `@ref` is not empty but starts with a space, and
trimming whitespace in `@ref` waits for the operator's decision in the
[plan](../../knowledge/plan.md#person-index), so the script leaves it.

## Run

```bash
python scripts/datenkorrektur_2026_10_13/fix_audit_findings.py            # dry run
python scripts/datenkorrektur_2026_10_13/fix_audit_findings.py --apply
python scripts/datenkorrektur_2026_10_13/fix_audit_findings.py --verify
```

Files are read and written through [`scripts/_szd_io.py`](../_szd_io.py), so line endings stay
as they were, and every changed file is checked well formed before it is written. An applied
run appends one row per change to `audit_findings_log.csv` with finding, file, line, old and
new text. `--verify` checks that every file is well formed and that no rule would change it
any more. A second dry run after `--apply` reports nothing to do.
