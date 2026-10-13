#!/usr/bin/env python3
"""Repair the evidenced data findings of the live-site audit of 2026-10-13.

Four findings, each repaired only where the data itself evidences the value:

    misc-number     webpage/MISCELLANEOUS.xml numbers the English news items differently
                    from the German ones, twice n="2", which gives the rendered page the id
                    miscellaneous.2 twice. Each English item takes the n of the German item
                    that shows the same NEWS_IMG datastream.
    empty-prov      data/Autograph/SZDAUT.xml: SZDAUT.218 carries a typed provenance whose
                    only content is a blank German span. Entries without that value omit
                    the element, so the empty one is removed.
    essay-id        data/Aufsatzablage/SZDESS.xml: one entry (SZ-AAP/W-AA212.3, o:szd.2838)
                    has the empty id "SZDESS.", because its row in the source table had no
                    ID. The ids run 1..n without gap and without suffix and existing ids are
                    never renumbered, so the entry takes the next free number.
    empty-wikidata  data/Index/Person/SZDPER.xml: SZDPER.2299 carries an empty wikidata
                    idno. Persons without a Wikidata identifier omit the element, so it is
                    removed.

Text is read and written byte-preserving through scripts/_szd_io.py, every change is string
surgery on that text, and the result is checked well formed before it is written.

Usage:

    python scripts/datenkorrektur_2026_10_13/fix_audit_findings.py            # dry run
    python scripts/datenkorrektur_2026_10_13/fix_audit_findings.py --apply
    python scripts/datenkorrektur_2026_10_13/fix_audit_findings.py --verify

Regime: script pipeline, standard library only, run with plain python.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
import xml.etree.ElementTree as ET
from collections.abc import Callable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_CSV = Path(__file__).resolve().parent / "audit_findings_log.csv"

_spec = importlib.util.spec_from_file_location("_szd_io", REPO_ROOT / "scripts" / "_szd_io.py")
szd_io = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(szd_io)

MISC = REPO_ROOT / "webpage" / "MISCELLANEOUS.xml"
AUT = REPO_ROOT / "data" / "Autograph" / "SZDAUT.xml"
ESS = REPO_ROOT / "data" / "Aufsatzablage" / "SZDESS.xml"
PER = REPO_ROOT / "data" / "Index" / "Person" / "SZDPER.xml"

LOG_FIELDS = ["befund", "datei", "zeile", "alt", "neu"]

NEWS_DIV = re.compile(r'<div n="(\d+)" type="miscellaneous">')
NEWS_IMG = re.compile(r"NEWS_IMG_(\d+)/")
# The patterns of removed elements take the line terminator before them, so no blank line
# remains where the element stood.
EMPTY_PROV = re.compile(
    r'\r?\n[ \t]*<provenance type="provenance">(?:<span xml:lang="[a-z]{2}">\s*</span>)*</provenance>'
)
EMPTY_WIKIDATA = re.compile(r'\r?\n[ \t]*<idno type="wikidata">\s*</idno>')
EMPTY_ESS_ID = 'xml:id="SZDESS."'
ESS_ID = re.compile(r'xml:id="SZDESS\.(\d+)"')


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def fix_misc(text: str, rows: list[dict]) -> str:
    de_at = text.index('<div xml:lang="de">')
    en_at = text.index('<div xml:lang="en">')
    if not de_at < en_at:
        raise ValueError("MISCELLANEOUS.xml: the German part does not precede the English part")

    def items(start: int, end: int) -> list[tuple[re.Match[str], str]]:
        found = []
        for div in NEWS_DIV.finditer(text, start, end):
            img = NEWS_IMG.search(text, div.end())
            found.append((div, img.group(1)))
        return found

    german_items = items(de_at, en_at)
    german = {img: div.group(1) for div, img in german_items}
    if len(german) != len(german_items):
        raise ValueError("MISCELLANEOUS.xml: one NEWS_IMG occurs in two German items")
    english = items(en_at, len(text))
    if sorted(img for _, img in english) != sorted(german):
        raise ValueError("MISCELLANEOUS.xml: the two parts show different news images")

    out, last = [], 0
    for div, img in english:
        if div.group(1) == german[img]:
            continue
        new = f'<div n="{german[img]}" type="miscellaneous">'
        rows.append({"befund": "misc-number", "datei": rel(MISC),
                     "zeile": line_of(text, div.start()), "alt": div.group(0), "neu": new})
        out += [text[last : div.start()], new]
        last = div.end()
    return "".join(out) + text[last:]


def remover(befund: str, path: Path, pattern: re.Pattern[str]) -> Callable[[str, list[dict]], str]:
    def fix(text: str, rows: list[dict]) -> str:
        def drop(match: re.Match[str]) -> str:
            rows.append({"befund": befund, "datei": rel(path),
                         "zeile": line_of(text, match.start()) + 1,
                         "alt": match.group(0).strip(), "neu": ""})
            return ""

        return pattern.sub(drop, text)

    fix.__name__ = befund
    return fix


def fix_essay_id(text: str, rows: list[dict]) -> str:
    count = text.count(EMPTY_ESS_ID)
    if count == 0:
        return text
    if count > 1:
        raise ValueError("SZDESS.xml: more than one empty id, the next free number is ambiguous")
    numbers = sorted(int(n) for n in ESS_ID.findall(text))
    if numbers != list(range(1, len(numbers) + 1)):
        raise ValueError("SZDESS.xml: the ids do not run 1..n without gap, next free number unclear")
    new = f'xml:id="SZDESS.{numbers[-1] + 1}"'
    pos = text.index(EMPTY_ESS_ID)
    rows.append({"befund": "essay-id", "datei": rel(ESS), "zeile": line_of(text, pos),
                 "alt": EMPTY_ESS_ID, "neu": new})
    return text.replace(EMPTY_ESS_ID, new)


FIXES: list[tuple[Path, Callable[[str, list[dict]], str]]] = [
    (MISC, fix_misc),
    (AUT, remover("empty-prov", AUT, EMPTY_PROV)),
    (ESS, fix_essay_id),
    (PER, remover("empty-wikidata", PER, EMPTY_WIKIDATA)),
]


def verify() -> int:
    failures: list[str] = []
    for path, fix in FIXES:
        text = szd_io.read_text(path)
        try:
            ET.fromstring(text)
        except ET.ParseError as error:
            failures.append(f"{rel(path)}: not well formed, {error}")
            continue
        if fix(text, []) != text:
            failures.append(f"{rel(path)}: {fix.__name__} would still change the file")
    for failure in failures:
        print(f"FAIL  {failure}")
    if failures:
        return 1
    print("OK  all four audit findings are repaired and every file is well formed")
    return 0


def main() -> int:
    szd_io.console_utf8()
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--apply", action="store_true", help="write the changes")
    parser.add_argument("--verify", action="store_true", help="check the repaired state only")
    args = parser.parse_args()

    for path, _ in FIXES:
        if not path.exists():
            print(f"FAIL  {path} missing", file=sys.stderr)
            return 1
    if args.verify:
        return verify()

    rows: list[dict] = []
    changed: dict[Path, str] = {}
    for path, fix in FIXES:
        original = szd_io.read_text(path)
        new_text = fix(original, rows)
        if new_text != original:
            ET.fromstring(new_text)  # trust boundary: never write what is not well formed
            changed[path] = new_text

    for row in rows:
        print(f"OK  {row['befund']}  {row['datei']}:{row['zeile']}  {row['alt']!r} -> {row['neu']!r}")
    if not rows:
        print("SKIP  nothing to do")
        return 0
    if not args.apply:
        print(f"SKIP  dry run, {len(rows)} changes planned")
        return 0

    for path, new_text in changed.items():
        szd_io.write_atomic(path, new_text)
    szd_io.append_log(OUT_CSV, LOG_FIELDS, rows)
    print(f"OK  {rel(OUT_CSV)} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
