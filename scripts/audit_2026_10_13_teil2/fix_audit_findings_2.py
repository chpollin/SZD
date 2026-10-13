#!/usr/bin/env python3
"""Correct the second batch of findings of the live-site audit of 2026-10-13.

Every change is a literal replacement whose evidence lies in the repository, applied only
where the old text occurs exactly as often as expected and, where a scope is given, inside the
expected entry (enclosing biblFull) or language column (nearest enclosing div xml:lang). The
README lists each change with its evidence and the findings left unchanged.

Usage:

    python scripts/audit_2026_10_13_teil2/fix_audit_findings_2.py            # dry run
    python scripts/audit_2026_10_13_teil2/fix_audit_findings_2.py --apply
    python scripts/audit_2026_10_13_teil2/fix_audit_findings_2.py --verify

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
OUT_CSV = Path(__file__).resolve().parent / "audit_findings_2_log.csv"

_spec = importlib.util.spec_from_file_location("_szd_io", REPO_ROOT / "scripts" / "_szd_io.py")
szd_io = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(szd_io)

LOG_FIELDS = ["befund", "datei", "zeile", "eintrag", "alt", "neu", "beleg"]

THEMA1 = "data/Issue/MarieAntoinette/szd-thema1.xml"
THEMA4 = "data/Issue/Autographen/szd-thema4.xml"
THEMA6 = "data/Issue/Freud/szd-thema6.xml"
THEMA7 = "data/Issue/Masereel-Aufsatz/szd-thema7-masareel.xml"
SZDLEB = "data/PersonalDocument/SZDLEB.xml"
SZDMSK = "data/Work/SZDMSK.xml"
ABOUT = "webpage/ABOUT.xml"
KONVOLUT = "data/Correspondence/konvolute/szd.korrespondenzen.{}.xml"

BIBLFULL_ID = re.compile(r'<biblFull\b[^>]*\bxml:id="([^"]+)"')
DIV_LANG = re.compile(r'<div\b[^>]*\bxml:lang="([^"]+)"')


@dataclass(frozen=True)
class Change:
    finding: str
    file: str
    old: str
    new: str
    count: int
    evidence: str
    entry: str = ""  # xml:id of the enclosing biblFull, empty where no entry applies
    lang: str = ""  # xml:lang of the enclosing language column, empty where any applies


GALLERY_EVIDENCE = (
    "anchor SigmundFreud does not exist; SZDKOR.xml context anchor of SZ-LAS/B7 is "
    "context:szd.facsimiles.korrespondenzen#freud-sigmund (fn:konvolut-slug of 'Freud, Sigmund')"
)
SPACE_EVIDENCE = "missing space at an element boundary, English column"

THEME_CHANGES = (
    Change(
        "thema6-reply", THEMA6,
        '<ref target="https://gams.uni-graz.at/o:szd.122/sdef:IIIF/getMirador">reply</ref>',
        '<ref target="https://gams.uni-graz.at/o:szd.996/sdef:IIIF/getMirador">reply</ref>',
        1,
        "o:szd.122 is SZDLEB.38 (publishing contract); German column links the same reply as "
        "o:szd.996 = SZ-LAS/B7.9, letter to Freud of 6 Dec 1929 (late 1929, Maylan incident)",
        lang="en",
    ),
    Change(
        "thema6-last-letter", THEMA6,
        '<ref target="https://gams.uni-graz.at/o:szd.162/sdef:IIIF/getMirador">last letter</ref>',
        '<ref target="https://gams.uni-graz.at/o:szd.990/sdef:IIIF/getMirador">last letter</ref>',
        1,
        "o:szd.162 404; German column links the same letter of 14 Sep 1939 as "
        "o:szd.990 = SZ-LAS/B7.47, letter to Freud of 14 September 1939",
        lang="en",
    ),
    Change(
        "thema6-scheme", THEMA6,
        'target="stefanzweig.digital/o:szd.lebenskalender#SZDBIO.87"',
        'target="https://stefanzweig.digital/o:szd.lebenskalender#SZDBIO.87"',
        1,
        "relative target without scheme; every other stefanzweig.digital link in the file, "
        "the German eulogy link included, uses https://",
        lang="en",
    ),
    Change(
        "thema6-gallery", THEMA6,
        'context:szd.facsimiles.korrespondenzen#SigmundFreud"',
        'context:szd.facsimiles.korrespondenzen#freud-sigmund"',
        4,
        GALLERY_EVIDENCE,
    ),
    Change("thema6-space", THEMA6, "<name>Freud’s</name>scientific",
           "<name>Freud’s</name> scientific", 1, SPACE_EVIDENCE, lang="en"),
    Change("thema6-space", THEMA6, "<name>Zweig</name>for his volume",
           "<name>Zweig</name> for his volume", 1, SPACE_EVIDENCE, lang="en"),
    Change("thema6-space", THEMA6, "<name>Freud</name>for the Nobel Prize",
           "<name>Freud</name> for the Nobel Prize", 1, SPACE_EVIDENCE, lang="en"),
    Change("thema6-space", THEMA6, "<name>Freud</name>and his methods",
           "<name>Freud</name> and his methods", 1, SPACE_EVIDENCE, lang="en"),
    Change("thema6-space", THEMA6, "<name>Maylan</name>incident",
           "<name>Maylan</name> incident", 1, SPACE_EVIDENCE, lang="en"),
    Change("thema6-space", THEMA6, "eulogy</ref>at London",
           "eulogy</ref> at London", 1, SPACE_EVIDENCE, lang="en"),
    Change(
        "thema6-typo", THEMA6,
        "<name>Maylan</name> sa “malicious fool” and an “Aryan fanatic”",
        "<name>Maylan</name> a “malicious fool” and an “Aryan fanatic”",
        1,
        "stray s; 'called X a ... and an ...' (German: Maylan sei ein bösartiger Narr)",
        lang="en",
    ),
    Change(
        "thema4-markup", THEMA4,
        '>">An autograph of Honoré de Balzac</ref>',
        ">An autograph of Honoré de Balzac</ref>",
        1,
        'leftover ">" after the start tag of the SZDAUT.28 link, rendered as visible text',
        lang="en",
    ),
    Change(
        "thema1-nli", THEMA1,
        "<ref>http://merhav.nli.org.il/primo-explore/fulldisplay?vid=NLI&amp;docid="
        "NNL_ARCHIVE_AL003432560&amp;context=L&amp;lang=en&quot;</ref>",
        "<ref>https://www.nli.org.il/en/archives/NNL_ARCHIVE_AL003432560/NLI</ref>",
        1,
        "old catalogue URL with a literal quote; German column gives the same record "
        "NNL_ARCHIVE_AL003432560 (ARC. Ms. Var. 305 3) under the current URL",
        lang="en",
    ),
    Change(
        "thema1-heading", THEMA1,
        '<title facs="o:szd.143" ref="#SZDLEB.3">Hauptbuch</title>',
        '<title facs="o:szd.143" ref="#SZDLEB.3">Principal Ledger</title>',
        1,
        "SZDLEB.3 English Einheitssachtitel is 'Principal Ledger'",
        lang="en",
    ),
    Change(
        "thema7-locale", THEMA7,
        "/sdef:TEI/get?locale=de#",
        "/sdef:TEI/get?locale=en#",
        14,
        "catalogue links in the English column hard-code the German locale",
        lang="en",
    ),
)

RECORD_CHANGES = (
    Change(
        "szdleb-classification", SZDLEB,
        '<term type="classification" xml:lang="en">Contracts</term>',
        '<term type="classification" xml:lang="en">Publishing Contracts</term>',
        1,
        "every other entry with German classification Verlagsverträge carries "
        "English Publishing Contracts",
        entry="SZDLEB.40",
    ),
    Change(
        "szdmsk-title", SZDMSK,
        "„Drei Dicher ihres Lebens“",
        "„Drei Dichter ihres Lebens“",
        3,
        "the entry's own work reference reads 'Drei Dichter ihres Lebens' (#SZDWRK.164)",
        entry="SZDMSK.289",
    ),
    Change("about-typo", ABOUT, "TECHNISCHE INFRASTRUKTUR UND MEADATEN",
           "TECHNISCHE INFRASTRUKTUR UND METADATEN", 1, "typo in German heading"),
    Change("about-typo", ABOUT, "TRÄGER*INNENT, KOOPERATIONSPARTNER*INNEN",
           "TRÄGER*INNEN, KOOPERATIONSPARTNER*INNEN", 1, "typo in German heading"),
    Change("about-typo", ABOUT, "using the the Integrated Authority File",
           "using the Integrated Authority File", 1, "doubled article, English text"),
)

# (Konvolut slug, entry, @when in the data, display text of the date). The display text
# gives the two-digit year, the entry title the four-digit 19xx year (except
# unidentified.039, whose title has no date), and the 20xx value lies in the future.
CENTURY_ERRORS = (
    ("freud-sigmund", "SZDKOR.freud-sigmund.8", "2027-03-18", "18. 3. 27"),
    ("freud-sigmund", "SZDKOR.freud-sigmund.9", "2029-12-06", "6. 12. 29"),
    ("freud-sigmund", "SZDKOR.freud-sigmund.10", "2029-12-08", "8. 12. 29"),
    ("freud-sigmund", "SZDKOR.freud-sigmund.11", "2029-12-31", "31. 12. 29"),
    ("freud-sigmund", "SZDKOR.freud-sigmund.12", "2030-08-12", "12. 8. 30"),
    ("kaemmerer-maria", "SZDKOR.kaemmerer-maria.B.2", "2027-02-24", "24. 2. 27"),
    ("kaemmerer-maria", "SZDKOR.kaemmerer-maria.B.3", "2027-08-02", "2. 8. 27"),
    ("mees-friedrich-siegbert", "SZDKOR.mees-friedrich-siegbert.B.2", "2027-04-19", "19. 4. 27"),
    ("mees-friedrich-siegbert", "SZDKOR.mees-friedrich-siegbert.B.3", "2027-05-16", "16. 5. 27"),
    ("mees-friedrich-siegbert", "SZDKOR.mees-friedrich-siegbert.B.4", "2030-08-26", "26. 8. 30"),
    ("unidentified", "SZDKOR.unidentified.039", "2030-09-23", "23. 9. 30"),
)


def century_changes() -> tuple[Change, ...]:
    changes = []
    for slug, entry, when, display in CENTURY_ERRORS:
        fixed = "19" + when[2:]
        for lang in ("de", "en"):
            changes.append(
                Change(
                    "konvolut-century", KONVOLUT.format(slug),
                    f'<date when="{when}" xml:lang="{lang}">{display}</date>',
                    f'<date when="{fixed}" xml:lang="{lang}">{display}</date>',
                    1,
                    f"display text '{display}' gives the two-digit year; {when[:4]} is in the "
                    f"future, {fixed[:4]} lies within Zweig's lifetime",
                    entry=entry,
                )
            )
    return tuple(changes)


CHANGES = THEME_CHANGES + RECORD_CHANGES + century_changes()


def last_match(pattern: re.Pattern[str], text: str, position: int) -> str:
    found = pattern.findall(text, 0, position)
    return found[-1] if found else ""


def in_scope(change: Change, text: str, position: int) -> bool:
    if change.entry and last_match(BIBLFULL_ID, text, position) != change.entry:
        return False
    return not change.lang or last_match(DIV_LANG, text, position) == change.lang


def positions(change: Change, value: str, text: str) -> list[int]:
    return [m.start() for m in re.finditer(re.escape(value), text) if in_scope(change, text, m.start())]


def plan(rows: list[dict]) -> tuple[dict[str, str], list[str]]:
    """Return the rewritten texts per file and the problems that block writing."""
    texts: dict[str, str] = {}
    problems: list[str] = []
    for change in CHANGES:
        text = texts.get(change.file)
        if text is None:
            text = szd_io.read_text(REPO_ROOT / change.file)
        found = positions(change, change.old, text)
        if not found:
            texts[change.file] = text
            continue  # already applied
        if len(found) != change.count:
            problems.append(f"{change.file}: {change.old!r} found {len(found)}x in scope, expected {change.count}")
            continue
        for pos in found:
            rows.append(
                {
                    "befund": change.finding,
                    "datei": change.file,
                    "zeile": text.count("\n", 0, pos) + 1,
                    "eintrag": change.entry,
                    "alt": change.old,
                    "neu": change.new,
                    "beleg": change.evidence,
                }
            )
        for pos in reversed(found):
            text = text[:pos] + change.new + text[pos + len(change.old):]
        texts[change.file] = text
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
        if positions(change, change.old, text):
            failures.append(f"{change.file}: {change.old!r} still present")
        hits = positions(change, change.new, text)
        if len(hits) < change.count:
            failures.append(f"{change.file}: {change.new!r} found {len(hits)}x, expected {change.count}")
    for file in sorted({change.file for change in CHANGES}):
        try:
            ET.fromstring(szd_io.read_text(REPO_ROOT / file))
        except ET.ParseError as error:
            failures.append(f"{file}: not well formed, {error}")
    for failure in failures:
        print(f"FAIL  {failure}")
    if failures:
        return 1
    print("OK  every finding of the second batch is corrected")
    return 0


def main() -> int:
    szd_io.console_utf8()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="write the changes")
    parser.add_argument("--verify", action="store_true", help="check the corrected state only")
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
        print("SKIP  nothing to do, every finding is already corrected")
        return 0
    if not args.apply:
        print(f"SKIP  dry run, {len(rows)} changes planned")
        return 0
    changed = {row["datei"] for row in rows}
    for file in sorted(changed):
        szd_io.write_atomic(REPO_ROOT / file, texts[file])
    szd_io.append_log(OUT_CSV, LOG_FIELDS, rows)
    print(f"OK  {OUT_CSV.relative_to(REPO_ROOT).as_posix()} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
