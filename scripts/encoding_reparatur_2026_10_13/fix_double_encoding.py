#!/usr/bin/env python3
"""Reverse double- and triple-encoded UTF-8 in the TEI files under data/, one run at a time.

A text that went through "read UTF-8 bytes as latin-1 or cp1252, write as UTF-8" once turns
"ü" into "Ã¼"; a second pass turns it into "Ã\\x83Â¼". datenkorrektur_2026_09_29/fix_mojibake.py
reversed this per whole text node and therefore left every node alone that mixes a correct
character with a damaged one (freud-sigmund "HÃ´tel-Château", unidentified "L'Ã\\x89glise"), and
it excluded szd.korrespondenzen.rascher-und-cie.xml, whose header carries the triple form.

This script works on the smallest unit instead. A cluster is a maximal run of at least two
characters that each stand for one byte of 0x80-0xFF under cp1252 or latin-1. The cluster's
bytes are decoded as UTF-8, and the step is repeated while it succeeds, so the triple form takes
two steps. A cluster whose bytes are no valid UTF-8 is left as written. This keeps correct
non-ASCII text untouched ("Château", "Sterngewölbe", "–\\xa0", "CIVILIZAÇÃO"), because a lone
correct character never forms a cluster and a run of correct Latin characters is no valid UTF-8
as bytes. ASCII, markup and line terminators lie outside every cluster and are copied unchanged.

Two guards stop a repair that would not be the plain reversal.
- Every decoded character must be printable or a no-break space. A cluster that decodes to a
  control character is left alone and reported as ambiguous.
- The repaired file must give back the original when every repaired span is encoded again the
  way it was damaged; this is checked over the whole file before it is written.

Files under data/Library/ are out of scope (operator ingest in progress). data/Issue/ and
data/Correspondence/SZDKOR.xml are scanned and reported but never written.

Usage:

    python scripts/encoding_reparatur_2026_10_13/fix_double_encoding.py            # dry run
    python scripts/encoding_reparatur_2026_10_13/fix_double_encoding.py --apply
    python scripts/encoding_reparatur_2026_10_13/fix_double_encoding.py --verify

Regime: script pipeline, standard library only, run with plain python.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import importlib.util
import re
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA = REPO_ROOT / "data"
OUT_CSV = Path(__file__).resolve().parent / "encoding_log.csv"
OUT_OF_SCOPE = ("data/Library/",)
READ_ONLY = ("data/Issue/", "data/Correspondence/SZDKOR.xml")

_spec = importlib.util.spec_from_file_location("_szd_io", REPO_ROOT / "scripts" / "_szd_io.py")
szd_io = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(szd_io)

LOG_FIELDS = ["datum", "datei", "zeile", "alt", "neu", "schritte"]


def _byte_of() -> dict[str, int]:
    """Each character that stands for one byte 0x80-0xFF under cp1252 or latin-1, with that byte.

    The two code pages agree on 0xA0-0xFF. In 0x80-0x9F cp1252 has letters and punctuation
    (U+2019, U+0152, ...) and latin-1 the C1 controls, and the data shows both forms (freud-sigmund
    has "â\\x80\\x99", the earlier log "Ã\\x96"), so both characters map to the same byte.
    """
    table: dict[str, int] = {}
    for byte in range(0x80, 0x100):
        table[bytes([byte]).decode("latin-1")] = byte
        with contextlib.suppress(UnicodeDecodeError):  # five bytes are undefined in cp1252
            table[bytes([byte]).decode("cp1252")] = byte
    return table


BYTE_OF = _byte_of()
CLUSTER = re.compile("[" + re.escape("".join(sorted(BYTE_OF))) + "]{2,}")


def plausible(char: str) -> bool:
    return char == "\xa0" or not unicodedata.category(char).startswith("C")


def decode_cluster(cluster: str) -> tuple[str, int] | None:
    """(repaired text, number of decoding steps), or None where the cluster is no mojibake."""
    current, steps = cluster, 0
    while len(current) > 1 and all(c in BYTE_OF for c in current):
        try:
            decoded = bytes(BYTE_OF[c] for c in current).decode("utf-8")
        except UnicodeDecodeError:
            break
        current, steps = decoded, steps + 1
    return (current, steps) if steps else None


@dataclass(frozen=True)
class Repair:
    start: int
    end: int
    old: str
    new: str
    steps: int


@dataclass
class Result:
    text: str
    repairs: list[Repair]
    ambiguous: list[tuple[int, str, str]]  # (offset, cluster, reason)


def repair_text(text: str) -> Result:
    repairs: list[Repair] = []
    ambiguous: list[tuple[int, str, str]] = []
    parts: list[str] = []
    at = 0
    for match in CLUSTER.finditer(text):
        decoded = decode_cluster(match.group())
        if decoded is None:
            continue
        new, steps = decoded
        if not all(plausible(c) for c in new):
            ambiguous.append((match.start(), match.group(), f"decodes to {new!r}"))
            continue
        parts += [text[at : match.start()], new]
        at = match.end()
        repairs.append(Repair(match.start(), match.end(), match.group(), new, steps))
    parts.append(text[at:])
    return Result("".join(parts), repairs, ambiguous)


def damaged_bytes(text: str, steps: int) -> bytes:
    """The bytes the text had after `steps` rounds of the damage: UTF-8 read back byte by byte."""
    data = text.encode("utf-8")
    for _ in range(steps - 1):
        data = "".join(bytes([b]).decode("latin-1") for b in data).encode("utf-8")
    return data


def lossless(original: str, result: Result) -> bool:
    """Putting every repaired span back as written gives the original, and each span is the damage.

    Comparing bytes rather than characters is deliberate: the written form decides whether a byte
    in 0x80-0x9F appears as its cp1252 or latin-1 character, the bytes are the same either way.
    """
    parts, at, cursor = [], 0, 0
    for r in result.repairs:
        parts.append(result.text[at : at + r.start - cursor])
        at += r.start - cursor
        if result.text[at : at + len(r.new)] != r.new:
            return False
        at += len(r.new)
        cursor = r.end
        if damaged_bytes(r.new, r.steps) != bytes(BYTE_OF[c] for c in r.old):
            return False
        parts.append(r.old)
    parts.append(result.text[at:])
    return "".join(parts) == original


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def files_in_scope() -> list[Path]:
    return sorted(p for p in DATA.rglob("*.xml") if not rel(p).startswith(OUT_OF_SCOPE))


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def process() -> tuple[dict[Path, str], list[dict], list[str], list[str]]:
    """(files to write, log rows, ambiguous notes, hits in read-only files)."""
    changed: dict[Path, str] = {}
    rows: list[dict] = []
    notes: list[str] = []
    read_only_hits: list[str] = []
    today = dt.date.today().isoformat()
    for path in files_in_scope():
        original = szd_io.read_text(path)
        result = repair_text(original)
        name = rel(path)
        notes += [f"{name}:{line_of(original, o)} {c!r} {why}" for o, c, why in result.ambiguous]
        if not result.repairs:
            continue
        if name.startswith(READ_ONLY):
            read_only_hits += [f"{name}:{line_of(original, r.start)} {r.old!r} -> {r.new!r}" for r in result.repairs]
            continue
        if not lossless(original, result):
            raise RuntimeError(f"{name}: repair is not reversible, nothing written")
        ET.fromstring(result.text)  # trust boundary: never write what is not well formed
        changed[path] = result.text
        rows += [
            {
                "datum": today,
                "datei": name,
                "zeile": line_of(original, r.start),
                "alt": r.old,
                "neu": r.new,
                "schritte": r.steps,
            }
            for r in result.repairs
        ]
    return changed, rows, notes, read_only_hits


def verify() -> int:
    failures: list[str] = []
    files = files_in_scope()
    for path in files:
        try:
            ET.fromstring(szd_io.read_text(path))
        except ET.ParseError as error:
            failures.append(f"{rel(path)}: not well formed, {error}")
    _, rows, notes, read_only_hits = process()
    failures += [f"{r['datei']}:{r['zeile']} still repairable, {r['alt']!r} -> {r['neu']!r}" for r in rows]
    failures += [f"read-only file carries mojibake: {hit}" for hit in read_only_hits]
    for note in notes:
        print(f"NOTE  ambiguous, left as written: {note}")
    for failure in failures:
        print(f"FAIL  {failure}")
    if failures:
        return 1
    print(f"OK  {len(files)} files outside data/Library/ well formed, no repairable cluster left")
    return 0


def main() -> int:
    szd_io.console_utf8()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="write the changes")
    parser.add_argument("--verify", action="store_true", help="check the repaired state only")
    args = parser.parse_args()
    if args.verify:
        return verify()

    changed, rows, notes, read_only_hits = process()
    for row in rows:
        print(f"OK  {row['datei']}:{row['zeile']} {row['alt']!r} -> {row['neu']!r} ({row['schritte']} steps)")
    for hit in read_only_hits:
        print(f"SKIP  read-only, not written: {hit}")
    for note in notes:
        print(f"SKIP  ambiguous: {note}")
    if not rows:
        print("SKIP  nothing to do, no repairable cluster found")
        return 0
    if not args.apply:
        print(f"SKIP  dry run, {len(rows)} repairs planned in {len(changed)} files")
        return 0
    for path, text in changed.items():
        szd_io.write_atomic(path, text)
    szd_io.append_log(OUT_CSV, LOG_FIELDS, rows)
    print(f"OK  {rel(OUT_CSV)} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
