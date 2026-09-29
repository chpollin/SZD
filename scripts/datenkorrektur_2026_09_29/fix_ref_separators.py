#!/usr/bin/env python3
"""Turn a ";" or "," separated @ref into single-space-separated tokens.

GetPersonlist and the other RDF mappings split @ref on whitespace. A value written
'http://d-nb.info/gnd/A; http://d-nb.info/gnd/B' keeps the first URI as one token and
'; http://d-nb.info/gnd/B' malformed as the rest, so the second identifier is silently lost.
Splitting on ";", "," and whitespace alike and rejoining with a single space each, dropping any
empty token a double separator would otherwise leave, turns it into two clean tokens.

In scope by an explicit count from the September 2026 archive checkup: data/Aufsatzablage/
SZDESS.xml and the masereel-frans konvolut. SZDPER.xml (SZDPER.1680) uses " / " as a
separator, which is not this defect and stays an operator decision; this script never opens
that file.

Serialisation follows scripts/checkup_2026_09_konvolute/fix_konvolut_defects.py: the file text
is read and written byte-preserving through scripts/_szd_io.py, the rewrite is string surgery
on that text, and the result is checked well formed with xml.etree.ElementTree before it is
written.

Usage:

    python scripts/datenkorrektur_2026_09_29/fix_ref_separators.py            # dry run
    python scripts/datenkorrektur_2026_09_29/fix_ref_separators.py --apply
    python scripts/datenkorrektur_2026_09_29/fix_ref_separators.py --verify

Regime: script pipeline, standard library only, run with plain python.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252
    sys.stdout.reconfigure(errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]
TARGETS = [
    REPO_ROOT / "data" / "Aufsatzablage" / "SZDESS.xml",
    REPO_ROOT
    / "data"
    / "Correspondence"
    / "konvolute"
    / "szd.korrespondenzen.masereel-frans.xml",
]
OUT_CSV = Path(__file__).resolve().parent / "ref_separators_log.csv"

_spec = importlib.util.spec_from_file_location("_szd_io", REPO_ROOT / "scripts" / "_szd_io.py")
szd_io = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(szd_io)

LOG_FIELDS = ["datei", "zeile", "alt", "neu"]

REF_ATTR = re.compile(r'ref="([^"]*)"')
SEPARATOR = re.compile(r"[;,\s]+")
# internal fragment references such as "#SZDPER.1560" are valid tokens beside absolute URIs
URI = re.compile(r"^(https?://|#SZD[A-Z]+\.)")


def rejoin(value: str) -> str | None:
    """value with ';'/',' separators turned into single spaces, or None where the value
    carries none of them."""
    if ";" not in value and "," not in value:
        return None
    tokens = [token for token in SEPARATOR.split(value) if token]
    return " ".join(tokens)


def process(rows: list[dict]) -> dict[Path, str]:
    changed: dict[Path, str] = {}
    for path in TARGETS:
        original = szd_io.read_text(path)

        def rewrite(match: re.Match[str], path: Path = path, text: str = original) -> str:
            value = match.group(1)
            new_value = rejoin(value)
            if new_value is None or new_value == value:
                return match.group(0)
            line = text.count("\n", 0, match.start()) + 1
            rows.append(
                {
                    "datei": path.relative_to(REPO_ROOT).as_posix(),
                    "zeile": line,
                    "alt": f'ref="{value}"',
                    "neu": f'ref="{new_value}"',
                }
            )
            return f'ref="{new_value}"'

        new_text = REF_ATTR.sub(rewrite, original)
        if new_text != original:
            ET.fromstring(new_text)  # trust boundary: never write what is not well formed
            changed[path] = new_text
    return changed


def verify() -> int:
    failures: list[str] = []
    with OUT_CSV.open(encoding="utf-8", newline="") as handle:
        changed_values = {row["neu"] for row in csv.DictReader(handle)}
    for path in TARGETS:
        text = szd_io.read_text(path)
        try:
            ET.fromstring(text)
        except ET.ParseError as error:
            failures.append(f"{path.relative_to(REPO_ROOT).as_posix()}: not well formed, {error}")
            continue
        for match in REF_ATTR.finditer(text):
            value = match.group(1)
            if ";" in value or "," in value:
                line = text.count("\n", 0, match.start()) + 1
                failures.append(
                    f"{path.relative_to(REPO_ROOT).as_posix()}:{line} still separated: {value!r}"
                )
                continue
            # only the rewritten values are checked, other schemeless refs are a separate open question
            if f'ref="{value}"' not in changed_values:
                continue
            for token in value.split():
                if not URI.match(token):
                    line = text.count("\n", 0, match.start()) + 1
                    failures.append(
                        f"{path.relative_to(REPO_ROOT).as_posix()}:{line} "
                        f"token is not a URI: {token!r}"
                    )
    for failure in failures:
        print(f"FAIL  {failure}")
    if failures:
        return 1
    print("OK  every changed @ref token is a URI, no ';' or ',' separator remains")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--apply", action="store_true", help="write the changes")
    parser.add_argument("--verify", action="store_true", help="check the repaired state only")
    args = parser.parse_args()

    for path in TARGETS:
        if not path.exists():
            print(f"FAIL  {path} missing", file=sys.stderr)
            return 1
    if args.verify:
        return verify()

    rows: list[dict] = []
    changed = process(rows)

    for row in rows:
        print(f"OK  {row['datei']}:{row['zeile']} {row['alt']} -> {row['neu']}")
    if not rows:
        print("SKIP  nothing to do, no ';' or ',' separated @ref found")
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
