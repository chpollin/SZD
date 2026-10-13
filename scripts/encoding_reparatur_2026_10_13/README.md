# Reverse the remaining double-encoded UTF-8

Repairs the mojibake that [`datenkorrektur_2026_09_29/fix_mojibake.py`](../datenkorrektur_2026_09_29/fix_mojibake.py) left in place. That script reversed the damage per whole text node and skipped every node that mixes a correct character with a damaged one, and it excluded `szd.korrespondenzen.rascher-und-cie.xml`. This script reverses the damage per character run, so the correct characters beside a damaged one stay as they are.

## Damage and reversal

A text read as cp1252 or latin-1 although it was UTF-8 and then written as UTF-8 turns every non-ASCII character into two to four characters (`ü` into `Ã¼`). The header of the Rascher file went through this twice (`Ã\x83Â¼` for `ü`).

- A cluster is a maximal run of at least two characters that each stand for one byte 0x80–0xFF under cp1252 or latin-1.
- The bytes of a cluster are decoded as UTF-8, repeatedly while that succeeds, so a doubled damage takes two steps.
- A cluster whose bytes are no valid UTF-8 stays as written. Correct text such as `Château`, `Sterngewölbe`, `– ` or `CIVILIZAÇÃO` never forms a valid cluster and is untouched.
- A cluster that would decode to a control character is ambiguous, stays unchanged and is reported for the [plan](../../knowledge/plan.md).
- Before a file is written, every repaired span is damaged again and put back, and the result must equal the original file. The file must also be well-formed.

## Usage

```bash
# 1) dry run, lists every repair with file, line, old and new text, writes nothing
python scripts/encoding_reparatur_2026_10_13/fix_double_encoding.py

# 2) apply
python scripts/encoding_reparatur_2026_10_13/fix_double_encoding.py --apply

# 3) check
python scripts/encoding_reparatur_2026_10_13/fix_double_encoding.py --verify
```

An applied run appends one row per repaired run to `encoding_log.csv` beside the script, with date, file, line, old and new text and the number of decoding steps. The log is provenance and is committed with the data.

The check fails when a file in scope is not well-formed, a repairable cluster remains, or a read-only file carries one. A second dry run reports zero repairs.

## Scope

- Every XML file under `data/` except `data/Library/`, which an operator ingest holds.
- `data/Issue/` and `data/Correspondence/SZDKOR.xml` are scanned and reported, never written.
- Reading and writing go through [`_szd_io.py`](../_szd_io.py), so line terminators, the XML declaration and all text outside the repaired runs stay byte for byte.
- The run of 2026-10-13 repaired `freud-sigmund`, `unidentified` and `rascher-und-cie`. The repair of the Rascher file touches only its header text; the question of its content and PID stays in the [plan](../../knowledge/plan.md#konvolute).
