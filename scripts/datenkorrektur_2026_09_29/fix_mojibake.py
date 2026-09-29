#!/usr/bin/env python3
"""Repair double-encoded umlauts in the text nodes of the correspondence konvolut files.

Some konvolut text went through a UTF-8 file read as cp1252 or latin-1 and back to UTF-8 once,
which turns "Österreich" into "Ã\x96sterreich": every non-ASCII character becomes two or three
characters that each start with "Ã" or "Â". The round trip that produced the defect also
reverses it, encode the text as cp1252 or latin-1 to get the original bytes back, then decode
those bytes as UTF-8.

The round trip is attempted for each text node in isolation and applied only where it succeeds
outright, the repaired text differs from the original and no "Ã" or "Â" is left in it. A text
node that mixes an already correct character with a double-encoded one fails this test, because
encoding the whole node in one pass either raises or produces further mojibake, and it is left
untouched. Two such nodes sit in szd.korrespondenzen.freud-sigmund.xml ("Hôtel" is correct,
"Château" is not) and four in szd.korrespondenzen.unidentified.xml; a scan that only counts the
"Ã"/"Â" marker finds 179 candidate text nodes across 18 files, of which 173 round-trip clean.
The remaining six remain candidates after this script runs and are reported as left alone by
design, which is why --verify checks for nodes that still repair cleanly rather than for the
marker alone.

szd.korrespondenzen.rascher-und-cie.xml is excluded entirely (knowledge/plan.md, section
Konvolute: the file carries the content of another object under the wrong PID, an operator
question of its own).

A text node is every run of characters between a ">" and the next "<". Attribute values sit
inside the tag before that ">and are never matched. The konvolut files carry no comments or
processing instructions (checked once, 2026-09-29), so this boundary is exact for this corpus.

Serialisation follows scripts/checkup_2026_09_konvolute/fix_konvolut_defects.py: the file text
is read and written byte-preserving through scripts/_szd_io.py, the repair is string surgery on
that text, and the result is checked well formed with xml.etree.ElementTree before it is
written.

Usage:

    python scripts/datenkorrektur_2026_09_29/fix_mojibake.py            # dry run
    python scripts/datenkorrektur_2026_09_29/fix_mojibake.py --apply
    python scripts/datenkorrektur_2026_09_29/fix_mojibake.py --verify

Regime: script pipeline, standard library only, run with plain python.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252
    sys.stdout.reconfigure(errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]
KONVOLUTE = REPO_ROOT / "data" / "Correspondence" / "konvolute"
EXCLUDED_FILE = "szd.korrespondenzen.rascher-und-cie.xml"
OUT_CSV = Path(__file__).resolve().parent / "mojibake_log.csv"

_spec = importlib.util.spec_from_file_location("_szd_io", REPO_ROOT / "scripts" / "_szd_io.py")
szd_io = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(szd_io)

LOG_FIELDS = ["datei", "zeile", "alt", "neu"]

TEXT_NODE = re.compile(r">([^<]*)<")
MOJIBAKE_MARKER = re.compile(r"[ÃÂ]")
ENCODINGS = ("cp1252", "latin-1")


def repair(segment: str) -> str | None:
    """The corrected text, or None where the round trip does not clean the whole node."""
    if not MOJIBAKE_MARKER.search(segment):
        return None
    for encoding in ENCODINGS:
        try:
            repaired = segment.encode(encoding).decode("utf-8")
        except (UnicodeDecodeError, UnicodeEncodeError):
            continue
        if repaired != segment and not MOJIBAKE_MARKER.search(repaired):
            return repaired
    return None


def konvolut_files() -> list[Path]:
    return sorted(p for p in KONVOLUTE.glob("*.xml") if p.name != EXCLUDED_FILE)


def process(rows: list[dict], left_alone: list[str]) -> dict[Path, str]:
    changed: dict[Path, str] = {}
    for path in konvolut_files():
        original = szd_io.read_text(path)

        def rewrite(match: re.Match[str], path: Path = path, text: str = original) -> str:
            segment = match.group(1)
            fixed = repair(segment)
            if fixed is None:
                if MOJIBAKE_MARKER.search(segment):
                    line = text.count("\n", 0, match.start()) + 1
                    left_alone.append(
                        f"{path.relative_to(REPO_ROOT).as_posix()}:{line} "
                        f"round trip does not clean the whole node: {segment.strip()[:60]!r}"
                    )
                return match.group(0)
            line = text.count("\n", 0, match.start()) + 1
            rows.append(
                {
                    "datei": path.relative_to(REPO_ROOT).as_posix(),
                    "zeile": line,
                    "alt": segment,
                    "neu": fixed,
                }
            )
            return f">{fixed}<"

        new_text = TEXT_NODE.sub(rewrite, original)
        if new_text != original:
            ET.fromstring(new_text)  # trust boundary: never write what is not well formed
            changed[path] = new_text
    return changed


def verify() -> int:
    failures: list[str] = []
    for path in konvolut_files():
        text = szd_io.read_text(path)
        try:
            ET.fromstring(text)
        except ET.ParseError as error:
            failures.append(f"{path.relative_to(REPO_ROOT).as_posix()}: not well formed, {error}")

    rows: list[dict] = []
    left_alone: list[str] = []
    changed = process(rows, left_alone)
    for row in rows:
        failures.append(
            f"{row['datei']}:{row['zeile']} still repairable, {row['alt']!r} -> {row['neu']!r}"
        )
    if changed:
        failures.append(f"{len(changed)} files would still change")
    for note in left_alone:
        print(f"NOTE  left alone by design: {note}")
    for failure in failures:
        print(f"FAIL  {failure}")
    if failures:
        return 1
    print("OK  no repairable double-encoded text node remains in the konvolut files")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--apply", action="store_true", help="write the changes")
    parser.add_argument("--verify", action="store_true", help="check the repaired state only")
    args = parser.parse_args()

    if not KONVOLUTE.is_dir():
        print(f"FAIL  {KONVOLUTE} missing", file=sys.stderr)
        return 1
    if args.verify:
        return verify()

    rows: list[dict] = []
    left_alone: list[str] = []
    changed = process(rows, left_alone)

    for row in rows:
        print(f"OK  {row['datei']}:{row['zeile']} {row['alt']!r} -> {row['neu']!r}")
    for note in left_alone:
        print(f"SKIP  {note}")
    if not rows:
        print("SKIP  nothing to do, no repairable double-encoded text node found")
        return 0
    if not args.apply:
        print(f"SKIP  dry run, {len(rows)} changes planned in {len(changed)} files")
        return 0

    for path, text in changed.items():
        szd_io.write_atomic(path, text)
    szd_io.append_log(OUT_CSV, LOG_FIELDS, rows)
    print(f"OK  {OUT_CSV.relative_to(REPO_ROOT).as_posix()} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
