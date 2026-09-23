# Check and complete the Aufsatzablage classification

Repairs the outer grouping key `term[@type="classification"]` in [`data/Aufsatzablage/SZDESS.xml`](../../data/Aufsatzablage/SZDESS.xml) and surveys, for the grouped lists, which entries lack a key the renderer needs. Why the key must exist in both languages and in one spelling is part of the rendering contract in [`knowledge/COLLECTIONS.md`](../../knowledge/COLLECTIONS.md#rendering-contract-grouped-lists).

## Rules

- missing-language. An entry carries the classification in one language only. The pair is taken from the entries with the same object type (`extent/span/term[@type="objecttyp"]`, German and English) and a complete classification, but only if all of them point to exactly one pair. Otherwise the entry stays unchanged and appears in the residual list.
- case-variant. A value differs from the prevailing spelling of the same language only by capitalisation and is moved to that spelling.

The script creates no new categories. The vocabulary stays closed, and only pairs fully attested in the holdings are used.

## Usage

```bash
# 1) dry run with planned changes, residual list and survey of the grouped lists
python scripts/essay_klassifikation/fix_classification.py

# 2) apply
python scripts/essay_klassifikation/fix_classification.py --apply

# 3) check
python scripts/essay_klassifikation/fix_classification.py --verify
```

The check fails when the number of entries differs from `HEAD`, the order has shifted, an element other than `term[@type="classification"]` has changed its text, an entry without complete classification remains, or spelling variants of the same category still stand side by side. A second dry run plans zero changes.

## Scope

- `SZDMSK.xml` and `SZDLEB.xml` are only read. The survey shows missing facsimile PIDs there, which are no grouping problem and only prevent the Mirador link.
- The object type describes the piece, the classification places it in the navigation, and the script changes only the latter.
- `Druckfahnen` and `Korrekturfahnen` both map to `Galley proofs`, one category in the English output and two in the German. This is an editorial question.
- Existing mojibake and the CRLF line endings of the file stay. Only the affected `term` elements are written.
