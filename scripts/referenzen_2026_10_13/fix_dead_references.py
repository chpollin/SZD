#!/usr/bin/env python3
"""Repoint dead object references in the correspondence index and two theme pages.

The live-site audit of 2026-10-13 found references to GAMS objects that production does not
serve (404 on the object or its TEI_SOURCE). Each replacement below names the object that the
evidence identifies, read from production one request at a time, and is applied only where the
old value occurs exactly as often as expected and, for the index, inside the expected entry.

- SZDKOR.857 names o:szd.korrespondenzen.podbielski-gert-rene, production serves only
  o:szd.korrespondenzen.podbieliki-gert-rene, whose single letter carries the same signature
  SZ-SAM/B16. The data follow the misspelt live PID, because renaming a GAMS object is the
  operator's.
- SZDKOR.696 (SZ-SAM/AK, sender "Unbekannt", 1903-1939) names o:szd.korrespondenzen.unbekannt,
  which production does not serve. The only Konvolut holding SZ-SAM/AK pieces from an unknown
  sender is o:szd.korrespondenzen.unidentified, whose senders read "Unbekannt/Unidentified".
- Theme page 1 (English column) gives the Hauptbuch SZDLEB.3 the pre-2022 PID o:szd.8360, the
  German column and SZDLEB.xml give o:szd.143 (commit e71a0edb mapped 8360 to 143 for the German
  line only).
- Theme page 2 links the pre-2022 PIDs o:szd.8249, o:szd.8231 and o:szd.8232. The image files
  behind each link name the scanned holding: SZ_AAP_W45 notebook pages for 8249 (Werknotizen 7,
  SZDMSK.64, o:szd.233), SZ_AAP_W7 typescript pages for 8232 (SZDMSK.13, o:szd.278), and the
  loose sheets H2 for 8231, whose page "Dieses Jahr 1837, Menschheit ..." is IMG.1 of
  o:szd.234 (Das erste Wort über den Ozean [Beilage], SZ-AAP/W45, SZDMSK.287).

The context anchors of the two index entries stay as they are, they are gallery anchors and
not object PIDs.

Usage:

    python scripts/referenzen_2026_10_13/fix_dead_references.py            # dry run
    python scripts/referenzen_2026_10_13/fix_dead_references.py --apply
    python scripts/referenzen_2026_10_13/fix_dead_references.py --verify

Regime: script pipeline, standard library only, run with plain python.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_CSV = Path(__file__).resolve().parent / "dead_references_log.csv"

_spec = importlib.util.spec_from_file_location("_szd_io", REPO_ROOT / "scripts" / "_szd_io.py")
szd_io = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(szd_io)

LOG_FIELDS = ["datei", "zeile", "eintrag", "alt", "neu", "beleg"]

SZDKOR = "data/Correspondence/SZDKOR.xml"
THEMA1 = "data/Issue/MarieAntoinette/szd-thema1.xml"
THEMA2 = "data/Issue/Textgenese/szd-thema2.xml"
MISCELLANEOUS = "webpage/MISCELLANEOUS.xml"

BIBLFULL_ID = re.compile(r'<biblFull\b[^>]*\bxml:id="([^"]+)"')


@dataclass(frozen=True)
class Change:
    file: str
    old: str
    new: str
    count: int
    entry: str  # xml:id of the enclosing biblFull, empty where no entry applies
    evidence: str


CHANGES = (
    Change(
        SZDKOR,
        '<idno type="konvolut">o:szd.korrespondenzen.podbielski-gert-rene</idno>',
        '<idno type="konvolut">o:szd.korrespondenzen.podbieliki-gert-rene</idno>',
        1,
        "SZDKOR.857",
        "production: podbielski 404, podbieliki 200; podbieliki letter has signature SZ-SAM/B16",
    ),
    Change(
        SZDKOR,
        '<idno type="konvolut">o:szd.korrespondenzen.unbekannt</idno>',
        '<idno type="konvolut">o:szd.korrespondenzen.unidentified</idno>',
        1,
        "SZDKOR.696",
        "production: unbekannt 404; unidentified holds the SZ-SAM/AK pieces of sender Unbekannt",
    ),
    Change(
        THEMA1,
        '<title facs="o:szd.8360" ref="#SZDLEB.3">',
        '<title facs="o:szd.143" ref="#SZDLEB.3">',
        1,
        "",
        "o:szd.8360 404; SZDLEB.3 and the German column give o:szd.143 (Hauptbuch, SZ-SAM/L1)",
    ),
    Change(
        THEMA2,
        'target="o:szd.8249"',
        'target="o:szd.233"',
        12,
        "",
        "o:szd.8249 404; linked images are SZ_AAP_W45 notebook pages, o:szd.233 Werknotizen 7",
    ),
    Change(
        THEMA2,
        'target="o:szd.8232"',
        'target="o:szd.278"',
        6,
        "",
        "o:szd.8232 404; linked images are SZ_AAP_W7 typescript pages, o:szd.278 SZ-AAP/W7",
    ),
    Change(
        THEMA2,
        'target="o:szd.8231"',
        'target="o:szd.234"',
        8,
        "",
        "o:szd.8231 404; H2 page matches o:szd.234 IMG.1 (Beilage SZ-AAP/W45)",
    ),
    Change(
        MISCELLANEOUS,
        "/objects/o:szd.8250/methods/",
        "/objects/o:szd.306/methods/",
        2,
        "",
        "o:szd.8250 404; news item 4 links SZDMSK.351, whose facsimile is o:szd.306 (Über Dostojewsky, SZ-LAS/W3)",
    ),
)


def enclosing_entry(text: str, position: int) -> str:
    ids = BIBLFULL_ID.findall(text, 0, position)
    return ids[-1] if ids else ""


def plan(rows: list[dict]) -> tuple[dict[str, str], list[str]]:
    """Return the rewritten texts per file and the problems that block writing."""
    texts: dict[str, str] = {}
    problems: list[str] = []
    for change in CHANGES:
        text = texts.get(change.file)
        if text is None:
            text = szd_io.read_text(REPO_ROOT / change.file)
        found = [m.start() for m in re.finditer(re.escape(change.old), text)]
        if not found:
            continue  # already applied
        if len(found) != change.count:
            problems.append(
                f"{change.file}: {change.old!r} found {len(found)}x, expected {change.count}"
            )
            continue
        if change.entry and any(enclosing_entry(text, pos) != change.entry for pos in found):
            problems.append(f"{change.file}: {change.old!r} outside {change.entry}")
            continue
        for pos in found:
            rows.append(
                {
                    "datei": change.file,
                    "zeile": text.count("\n", 0, pos) + 1,
                    "eintrag": change.entry,
                    "alt": change.old,
                    "neu": change.new,
                    "beleg": change.evidence,
                }
            )
        texts[change.file] = text.replace(change.old, change.new)
    for file, text in texts.items():
        try:
            ET.fromstring(text)  # trust boundary: never write what is not well formed
        except ET.ParseError as error:
            problems.append(f"{file}: result not well formed, {error}")
    return texts, problems


def verify() -> int:
    failures: list[str] = []
    for change in CHANGES:
        text = szd_io.read_text(REPO_ROOT / change.file)
        if change.old in text:
            failures.append(f"{change.file}: {change.old!r} still present")
        hits = [m.start() for m in re.finditer(re.escape(change.new), text)]
        if len(hits) < change.count:
            failures.append(
                f"{change.file}: {change.new!r} found {len(hits)}x, expected {change.count}"
            )
        if change.entry and change.entry not in {enclosing_entry(text, pos) for pos in hits}:
            failures.append(f"{change.file}: {change.new!r} missing in {change.entry}")
    for file in sorted({change.file for change in CHANGES}):
        try:
            ET.fromstring(szd_io.read_text(REPO_ROOT / file))
        except ET.ParseError as error:
            failures.append(f"{file}: not well formed, {error}")
    for failure in failures:
        print(f"FAIL  {failure}")
    if failures:
        return 1
    print("OK  all dead references point to the evidenced objects")
    return 0


def main() -> int:
    szd_io.console_utf8()
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--apply", action="store_true", help="write the changes")
    parser.add_argument("--verify", action="store_true", help="check the repaired state only")
    args = parser.parse_args()
    if args.verify:
        return verify()

    rows: list[dict] = []
    texts, problems = plan(rows)
    for row in rows:
        print(f"OK  {row['datei']}:{row['zeile']} {row['alt']} -> {row['neu']}")
    for problem in problems:
        print(f"FAIL  {problem}")
    if problems:
        return 1
    if not rows:
        print("SKIP  nothing to do, every reference is already repointed")
        return 0
    if not args.apply:
        print(f"SKIP  dry run, {len(rows)} changes planned")
        return 0
    for file, text in texts.items():
        szd_io.write_atomic(REPO_ROOT / file, text)
    szd_io.append_log(OUT_CSV, LOG_FIELDS, rows)
    print(f"OK  {OUT_CSV.relative_to(REPO_ROOT).as_posix()} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
