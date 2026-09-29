#!/usr/bin/env python3
"""Remove the empty date/@when attribute from the muller-einigen-hans konvolut.

Two date elements at the sent action of one letter carry an empty when="" beside their
human-readable, uncertain text ("14. 8. (?)"), one in the German and one in the English
date element. An empty machine-readable date is worse than none, it claims a value that is
not there, so the attribute is dropped and the display text stays untouched.

Serialisation follows scripts/checkup_2026_09_konvolute/fix_konvolut_defects.py: the file text
is read and written byte-preserving through scripts/_szd_io.py, the removal is string surgery
on that text, and the result is checked well formed with xml.etree.ElementTree before it is
written.

Usage:

    python scripts/datenkorrektur_2026_09_29/fix_empty_when.py            # dry run
    python scripts/datenkorrektur_2026_09_29/fix_empty_when.py --apply
    python scripts/datenkorrektur_2026_09_29/fix_empty_when.py --verify

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
TARGET = (
    REPO_ROOT
    / "data"
    / "Correspondence"
    / "konvolute"
    / "szd.korrespondenzen.muller-einigen-hans.xml"
)
OUT_CSV = Path(__file__).resolve().parent / "empty_when_log.csv"

_spec = importlib.util.spec_from_file_location("_szd_io", REPO_ROOT / "scripts" / "_szd_io.py")
szd_io = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(szd_io)

LOG_FIELDS = ["datei", "zeile", "alt", "neu"]

EMPTY_WHEN = re.compile(r'\s*when=""')


def process(rows: list[dict]) -> str | None:
    original = szd_io.read_text(TARGET)

    def rewrite(match: re.Match[str]) -> str:
        line = original.count("\n", 0, match.start()) + 1
        rows.append(
            {
                "datei": TARGET.relative_to(REPO_ROOT).as_posix(),
                "zeile": line,
                "alt": match.group(0),
                "neu": "",
            }
        )
        return ""

    new_text = EMPTY_WHEN.sub(rewrite, original)
    if new_text == original:
        return None
    ET.fromstring(new_text)  # trust boundary: never write what is not well formed
    return new_text


def verify() -> int:
    failures: list[str] = []
    text = szd_io.read_text(TARGET)
    try:
        ET.fromstring(text)
    except ET.ParseError as error:
        failures.append(f"{TARGET.relative_to(REPO_ROOT).as_posix()}: not well formed, {error}")
    remaining = len(EMPTY_WHEN.findall(text))
    if remaining:
        failures.append(f"{remaining} empty date/@when attribute(s) remain in {TARGET.name}")
    for failure in failures:
        print(f"FAIL  {failure}")
    if failures:
        return 1
    print("OK  no empty date attribute remains in the muller-einigen-hans konvolut")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--apply", action="store_true", help="write the change")
    parser.add_argument("--verify", action="store_true", help="check the repaired state only")
    args = parser.parse_args()

    if not TARGET.exists():
        print(f"FAIL  {TARGET} missing", file=sys.stderr)
        return 1
    if args.verify:
        return verify()

    rows: list[dict] = []
    new_text = process(rows)

    for row in rows:
        print(f"OK  {row['datei']}:{row['zeile']} {row['alt']!r} removed")
    if not rows:
        print("SKIP  nothing to do, no empty date/@when attribute found")
        return 0
    if not args.apply:
        print(f"SKIP  dry run, {len(rows)} changes planned")
        return 0

    szd_io.write_atomic(TARGET, new_text)
    szd_io.append_log(OUT_CSV, LOG_FIELDS, rows)
    print(f"OK  {OUT_CSV.relative_to(REPO_ROOT).as_posix()} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
