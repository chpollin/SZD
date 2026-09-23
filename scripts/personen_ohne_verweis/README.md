# Persons without a reference from the holdings

Determines which entries of [`data/Index/Person/SZDPER.xml`](../../data/Index/Person/SZDPER.xml) no other TEI file under `data/` references, and writes the result as `unlinked_persons.csv` beside the script.

The result is a candidate list. Whether an entry is removed, kept for a coming delivery or linked somewhere is the project's decision. The script changes no TEI file.

[`scripts/checkup_2026_09_index/find_unlinked_persons.py`](../checkup_2026_09_index/README.md#find_unlinked_personspy) complements it for the checkup of September 2026. It reads every reference token, also scans not yet ingested bundles, and searches the element text for places where the unlinked persons are named. Its output stays outside the repository.

The two scripts read references differently and do not replace each other. This one follows `GetPersonlist` and counts only the first token of `@ref`. `find_unlinked_persons.py` counts every token of `@ref`, `@key` and `@corresp`, so a person on its shorter list is reached by no reference of any form, while a person only on this list is referenced, but in a place the mapping does not read.

## Reference patterns

A reference counts when the RDF mapping reads it, not when it looks like one. `GetPersonlist` in `szd-TORDF.xsl` produces a triple for these spellings:

```
ref="#SZDPER.42"
ref="https://gams.uni-graz.at/o:szd.personen#SZDPER.42"
ref="http://d-nb.info/gnd/118637479"   (only on persName, resolved through the index)
```

Since the checkup of September 2026 the script follows four reading rules derived from this.

- `ref="SZDPER.42"` without the fragment marker does not count. The mapping drops the value, the person view stays empty, and the entry belongs on the list as long as the spelling is not normalised. [`scripts/checkup_2026_09_index/normalize_person_refs.py`](../checkup_2026_09_index/README.md#normalize_person_refspy) does that.
- An authority number on a `persName` counts wherever it stands under `data/`, because the mapping resolves it through the index. The same number on a `repository` or `orgName` names an institution and does not count.
- In `data/Aufsatzablage/SZDESS.xml`, `author/@ref` is ignored where the inner `persName` carries a reference of its own, because the essay template reads the `persName` first and falls back to the attribute on `author` only without it.
- With several identifiers in one attribute, `ref="#SZDPER.42 #SZDPER.43"`, the committed `GetPersonlist` reads only the first token. Identifiers that stand only behind it are reported separately, because they stay invisible in the person view.

References inside `SZDPER.xml` do not count as use by the holdings but have a column of their own in the CSV.

## Columns

| Column | Content |
|---|---|
| `id` | Identifier `SZDPER.N` |
| `name` | Name as spelled in the file, `Surname, Forename` |
| `normdaten` | `persName/@ref` (GND), Wikidata and Wikipedia identifiers, space-separated |
| `verweis_innerhalb_szdper` | whether the person index itself refers to the entry |

The former column `gnd_sonst_verwendet` has been dropped. An authority number used elsewhere on a `persName` is a reference, so such entries no longer appear on the list, and the column would carry the same value in every row.

## Usage

```bash
# dry run with figures, dead references and the first rows, no CSV
python scripts/personen_ohne_verweis/list_unlinked_persons.py --dry-run

# write the CSV
python scripts/personen_ohne_verweis/list_unlinked_persons.py
```

The run also reports references to identifiers that do not exist in the person index, and identifiers that stand only behind the first token of a multiple reference. Both are findings of their own and no candidates for removal.

## Scope

The script leaves the person index untouched and deletes, adds or reorders nothing. It recognises only identifier and GND references, so a person named elsewhere only in running text counts as unlinked here. Work, place and subject references are out of its view.
