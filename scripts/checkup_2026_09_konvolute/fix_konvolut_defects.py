#!/usr/bin/env python3
"""Apply the archive-checkup corrections to the correspondence konvolut files that are
proven by evidence, from an explicit table.

Until September 2026 the 306 correspondence konvolut objects existed only on GAMS; commit
e1b156fa brought all of them into data/Correspondence/konvolute/ unchanged from production.
That download let this script work on the objects directly instead of only on the 42 that
existed before.

The table below covers the items of the archive's defect list (05-korrespondenz.md, section 2
wrong or missing facsimile links, and the metadata and structure findings of sections 3 and 4)
for which the archive-internal verification notes (verify-korrespondenz-daten.md,
verify-verknuepfung.md, verify-personenindex.md, classification README.md) establish a single
correct value beyond doubt, re-checked against GAMS production where the note's own snapshot
predates this run. Two categories of finding from the same defect list are deliberately absent
from the table and are listed instead in this script's README: items where the correct value is
not established (needs-archive, needs-operator) and items that were found, during this run, to
already carry the corrected value in the current production download, evidently fixed upstream
between the verification snapshot (17 September 2026) and this download (24 September 2026).

Each fix is anchored to one biblFull entry by its xml:id and applied as an exact, scoped text
substitution, insertion or deletion, never a blind file-wide replace except where a single
attribute value is uniformly wrong across an entire object (the Freud correspDesc/@type). A
fix that finds its target value already in place is treated as already applied and skipped,
which is what makes a second run idempotent. A fix that finds neither the old nor the new value
is an error and stops the run before anything is written.

Serialisation follows scripts/checkup_2026_09_korrespondenz/add_bundle_signatures.py: the file
text is read and written byte-preserving through scripts/_szd_io.py, edits are string surgery
on that text, not a round trip through an XML serialiser, and the result is checked well formed
with xml.etree.ElementTree before it is written.

Default behaviour is a dry run. Pass --apply to write, --verify to check the working tree
against this table without writing.

Usage:

    python scripts/checkup_2026_09_konvolute/fix_konvolut_defects.py            # dry run
    python scripts/checkup_2026_09_konvolute/fix_konvolut_defects.py --apply
    python scripts/checkup_2026_09_konvolute/fix_konvolut_defects.py --verify

Regime: script pipeline, standard library only, run with plain python.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252
    sys.stdout.reconfigure(errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]
KONVOLUTE = REPO_ROOT / "data" / "Correspondence" / "konvolute"
LOG = Path(__file__).resolve().parent / "corrections_log.csv"

_spec = importlib.util.spec_from_file_location("_szd_io", REPO_ROOT / "scripts" / "_szd_io.py")
szd_io = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(szd_io)

LOG_FIELDS = ["date", "file", "shelfmark", "field", "old", "new", "evidence"]


@dataclass
class Fix:
    file: str
    shelfmark: str
    field: str
    evidence: str
    kind: str  # "replace" | "replace_global" | "insert_pid" | "delete_entry" | "replace_entry"
    xml_id: str = ""
    old: str = ""
    new: str = ""
    count: int | None = None  # expected occurrences of `old` within the entry; None means 1


def entry_span(text: str, xml_id: str) -> tuple[int, int]:
    marker = f'<biblFull xml:id="{xml_id}">'
    start = text.index(marker)
    end = text.index("</biblFull>", start) + len("</biblFull>")
    return start, end


def line_span(text: str, start: int, end: int) -> tuple[int, int]:
    """Expand (start, end) to the full lines they sit on, including the line terminators."""
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    line_end = line_end + 1 if line_end != -1 else len(text)
    return line_start, line_end


def apply_replace(text: str, fix: Fix) -> tuple[str, str]:
    expected = fix.count if fix.count is not None else 1
    start, end = entry_span(text, fix.xml_id)
    segment = text[start:end]
    found = segment.count(fix.old)
    if found == 0:
        if fix.new in segment:
            return text, "already applied"
        raise ValueError(f"{fix.xml_id}: neither old nor new value found")
    if found != expected:
        raise ValueError(
            f"{fix.xml_id}: old value occurs {found} times in the entry, expected {expected}")
    segment = segment.replace(fix.old, fix.new, expected)
    return text[:start] + segment + text[end:], "applied"


def apply_replace_global(text: str, fix: Fix) -> tuple[str, str]:
    old_count = text.count(fix.old)
    new_count = text.count(fix.new)
    if old_count == 0:
        if new_count > 0:
            return text, "already applied"
        raise ValueError(f"{fix.file}: neither old nor new value found")
    return text.replace(fix.old, fix.new), "applied"


def apply_insert_pid(text: str, fix: Fix) -> tuple[str, str]:
    start, end = entry_span(text, fix.xml_id)
    segment = text[start:end]
    pid_marker = f'<idno type="PID">{fix.new}</idno>'
    if pid_marker in segment:
        return text, "already applied"
    if "<altIdentifier>" in segment:
        raise ValueError(f"{fix.xml_id}: entry already has an altIdentifier with a different PID")
    anchor = f'<idno type="signature">{fix.shelfmark}</idno>'
    if anchor not in segment:
        raise ValueError(f"{fix.xml_id}: signature idno not found")
    line_start = segment.rindex("\n", 0, segment.index(anchor)) + 1
    indent = segment[line_start:segment.index(anchor)]
    insertion = (
        f"\n{indent}<altIdentifier>"
        f"\n{indent}  <idno type=\"PID\">{fix.new}</idno>"
        f"\n{indent}</altIdentifier>"
    )
    at = start + segment.index(anchor) + len(anchor)
    return text[:at] + insertion + text[at:], "applied"


def apply_insert_before(text: str, fix: Fix) -> tuple[str, str]:
    """Insert fix.new as its own line right before the line holding fix.old, once.

    Unlike apply_replace, fix.old is never consumed, so a marker that is a substring of
    fix.new (an anchor line such as a closing tag that follows the inserted content) cannot
    make the insertion look like its own anchor on a second run. Idempotency instead checks
    whether the exact inserted line is already present.
    """
    start, end = entry_span(text, fix.xml_id)
    segment = text[start:end]
    if fix.new in segment:
        return text, "already applied"
    if segment.count(fix.old) != 1:
        raise ValueError(f"{fix.xml_id}: anchor is not unique (or missing) in the entry")
    at = segment.index(fix.old)
    line_start = segment.rindex("\n", 0, at) + 1
    indent = segment[line_start:at]
    insertion = f"{indent}{fix.new}\n"
    segment = segment[:line_start] + insertion + segment[line_start:]
    return text[:start] + segment + text[end:], "applied"


def apply_delete_entry(text: str, fix: Fix) -> tuple[str, str]:
    marker = f'<biblFull xml:id="{fix.xml_id}">'
    if marker not in text:
        return text, "already applied"
    start, end = entry_span(text, fix.xml_id)
    line_start, line_end = line_span(text, start, end)
    return text[:line_start] + text[line_end:], "applied"


def apply_replace_entry(text: str, fix: Fix) -> tuple[str, str]:
    start, end = entry_span(text, fix.xml_id)
    segment = text[start:end]
    if segment == fix.new:
        return text, "already applied"
    if segment != fix.old:
        raise ValueError(f"{fix.xml_id}: current entry text does not match the expected old block")
    return text[:start] + fix.new + text[end:], "applied"


APPLIERS = {
    "replace": apply_replace,
    "replace_global": apply_replace_global,
    "insert_pid": apply_insert_pid,
    "insert_before": apply_insert_before,
    "delete_entry": apply_delete_entry,
    "replace_entry": apply_replace_entry,
}

# ---------------------------------------------------------------------------
# The correction table
# ---------------------------------------------------------------------------

FIXES: list[Fix] = []


def add(f: Fix) -> None:
    FIXES.append(f)


EVIDENCE_LINK = (
    "verify-verknuepfung.md, confirmed-link: object exists in GAMS, DC title and dc:source "
    "carry the shelfmark, member of context:szd.facsimiles.korrespondenzen, re-checked live"
)

# --- Category A: wrong facsimile PID replaced (05-korrespondenz.md section 2) -------------

for fname, xml_id, shelfmark, old_pid, new_pid in [
    ("szd.korrespondenzen.clauser-suzanne.xml", "SZDKOR.clauser-suzanne.227", "SZ-SAM/AK.39", "o:szd.3326", "o:szd.683"),
    ("szd.korrespondenzen.despres-fernand.xml", "SZDKOR.despres-fernand.232", "SZ-SAM/AK.43", "o:szd.3331", "o:szd.612"),
    ("szd.korrespondenzen.despres-fernand.xml", "SZDKOR.despres-fernand.233", "SZ-SAM/AK.44", "o:szd.3332", "o:szd.613"),
    ("szd.korrespondenzen.diettrich-fritz.xml", "SZDKOR.diettrich-fritz.235", "SZ-SAM/AK.46", "o:szd.3334", "o:szd.684"),
    ("szd.korrespondenzen.lovric-bozo.xml", "SZDKOR.lovric-bozo.16", "SZ-SAM/AK.112", "o:szd.3115", "o:szd.392"),
]:
    add(Fix(fname, shelfmark, "msIdentifier/altIdentifier/idno[@type='PID']", EVIDENCE_LINK,
            "replace", xml_id, f'<idno type="PID">{old_pid}</idno>', f'<idno type="PID">{new_pid}</idno>'))

# --- Category B: missing facsimile PID added (05-korrespondenz.md section 2) --------------

for fname, xml_id, shelfmark, new_pid in [
    ("szd.korrespondenzen.fleischer-victor.xml", "SZDKOR.fleischer-victor.B.28", "SZ-LAS/B3.73", "o:szd.1257"),
    ("szd.korrespondenzen.fleischer-victor.xml", "SZDKOR.fleischer-victor.B.29", "SZ-LAS/B3.74", "o:szd.1258"),
    ("szd.korrespondenzen.fleischer-victor.xml", "SZDKOR.fleischer-victor.B.30", "SZ-LAS/B3.76", "o:szd.1260"),
    ("szd.korrespondenzen.fleischer-max.xml", "SZDKOR.fleischer-max.B.45", "SZ-LAS/B3.75", "o:szd.1259"),
    ("szd.korrespondenzen.freud-anna.xml", "SZDKOR.freud-anna.1", "SZ-LAS/B7.48", "o:szd.991"),
    ("szd.korrespondenzen.friedenthal-richard.xml", "SZDKOR.reichner-herbert.B.38", "SZ-AAP/B2.38", "o:szd.1573"),
    ("szd.korrespondenzen.friedenthal-richard.xml", "SZDKOR.reichner-herbert.B.40", "SZ-AAP/B2.40", "o:szd.1628"),
    ("szd.korrespondenzen.friedenthal-richard.xml", "SZDKOR.reichner-herbert.B.41", "SZ-AAP/B2.41", "o:szd.1532"),
    ("szd.korrespondenzen.kippenberg-katharina.xml", "SZDKOR.kippenberg-katharina.1", "SZ-SAM/AK.295", "o:szd.1662"),
    ("szd.korrespondenzen.hertzka-yella.xml", "SZDKOR.hertzka-yella.1", "SZ-SAM/AK.297", "o:szd.1664"),
    ("szd.korrespondenzen.rolland-romain.xml", "SZDKOR.rolland-romain.2", "SZ-SAM/B5.1", "o:szd.1268"),
    ("szd.korrespondenzen.rolland-romain.xml", "SZDKOR.rolland-romain.1", "SZ-SAM/B5.2", "o:szd.1269"),
    ("szd.korrespondenzen.rolland-romain.xml", "SZDKOR.rolland-romain.3", "SZ-SAM/B5.3", "o:szd.1270"),
]:
    add(Fix(fname, shelfmark, "msIdentifier/altIdentifier/idno[@type='PID'] (added)", EVIDENCE_LINK,
            "insert_pid", xml_id, new=new_pid))

# Specht Richard SZ-SEF/B9.1: only the dead PID is replaced. The recipient (Richard Specht
# against Lotte Altmann, the title still names the latter) is an unresolved contradiction
# between the entry's own title and its correspAction, listed open below, not corrected here.
add(Fix("szd.korrespondenzen.specht-richard.xml", "SZDKOR.specht-richard.1",
        "msIdentifier/altIdentifier/idno[@type='PID']",
        "verify-verknuepfung.md, confirmed-link: o:szd.1378 answers 404, o:szd.1372 carries "
        "the matching DC title/source and context membership, re-checked live",
        "replace", "SZDKOR.specht-richard.1",
        '<idno type="PID">o:szd.1378</idno>', '<idno type="PID">o:szd.1372</idno>'))

# --- Category C: Freud correspDesc/@type, one wrong value repeated across the whole object -

add(Fix("szd.korrespondenzen.freud-sigmund.xml", "SZ-LAS/B7.1-47",
        "correspDesc/@type (47 entries)",
        "verify-korrespondenz-daten.md, confirmed-data: correspDesc type='byZweig' occurs "
        "nowhere else in the corpus and the presentation layer does not resolve it, which is "
        "why every one of these 47 entries renders its sender as unbekannt although the "
        "persName already correctly holds Stefan Zweig with GND 118637479",
        "replace_global", old='<correspDesc type="byZweig">', new='<correspDesc type="fromZweig">'))

# --- Category D: metadata, title/date corrections ------------------------------------------

add(Fix("szd.korrespondenzen.friedenthal-richard.xml", "SZ-AAP/B2.50", "title (de)",
        "verify-korrespondenz-daten.md, confirmed-data: the entry's own manuscript date text "
        "'2. III. 25' (2 March) is encoded as when='1925-03-25' (25 March), a day/month mix-up; "
        "the archive's stated correction (02.03.1925) matches the transcribed text",
        "replace", "SZDKOR.reichner-herbert.B.50",
        "Richard Friedenthal an Stefan Zweig,\n                                25.03.1925",
        "Richard Friedenthal an Stefan Zweig,\n                                02.03.1925"))
add(Fix("szd.korrespondenzen.friedenthal-richard.xml", "SZ-AAP/B2.50", "title (en)",
        "see title (de) above",
        "replace", "SZDKOR.reichner-herbert.B.50",
        "Richard Friedenthal to Stefan Zweig,\n                                25.03.1925",
        "Richard Friedenthal to Stefan Zweig,\n                                02.03.1925"))
add(Fix("szd.korrespondenzen.friedenthal-richard.xml", "SZ-AAP/B2.50", "correspAction/date/@when",
        "see title (de) above",
        "replace", "SZDKOR.reichner-herbert.B.50",
        '<date when="1925-03-25">2. III. 25</date>', '<date when="1925-03-02">2. III. 25</date>'))

for xml_id, shelfmark in [("SZDKOR.fleischer-max.B.21", "SZ-LAS/B3.21"),
                           ("SZDKOR.fleischer-max.B.22", "SZ-LAS/B3.22")]:
    add(Fix("szd.korrespondenzen.fleischer-max.xml", shelfmark, "title (de/en)",
            "verify-korrespondenz-daten.md, confirmed-data: neither entry carries a date "
            "element, the title is the sole date carrier, and the archive states the "
            "corrected date (13/7 against the current 2/7)",
            "replace", xml_id, "02.07.1902", "13.07.1902", count=2))
    add(Fix("szd.korrespondenzen.fleischer-max.xml", shelfmark, "correspAction/date (added)",
            "see title above; no correspAction/date existed before this fix",
            "insert_before", xml_id,
            '<placeName>Berlin</placeName>',
            '<date when="1902-07-13">13.07.1902</date>'))

for xml_id, shelfmark, old_title_de, old_title_en in [
    ("SZDKOR.reichner-herbert.B.271", "SZ-AAP/B1.266",
     "Stefan Zweig an Manfred Altmann, 09.09.1947", "Stefan Zweig to Manfred Altmann, 09.09.1947"),
    ("SZDKOR.reichner-herbert.B.272", "SZ-AAP/B1.267",
     "Stefan Zweig an Manfred Altmann, 09.09.1947", "Stefan Zweig to Manfred Altmann, 09.09.1947"),
    ("SZDKOR.reichner-herbert.B.273", "SZ-AAP/B1.268",
     "Klara Modern an Stefan Zweig, 09.09.1947", "Klara Modern to Stefan Zweig, 09.09.1947"),
]:
    evidence = (
        "verify-korrespondenz-daten.md, confirmed-data: the entry's own correspAction/date "
        "reads 'o. D.'/'n. d.' with no @when, the title's 09.09.1947 is the date of the "
        "neighbouring entry SZ-AAP/B1AN.5 filled down three rows, five years after Zweig's death"
    )
    add(Fix("szd.korrespondenzen.reichner-herbert.xml", shelfmark, "title (de)", evidence,
            "replace", xml_id, old_title_de, old_title_de.split(",")[0]))
    add(Fix("szd.korrespondenzen.reichner-herbert.xml", shelfmark, "title (en)", evidence,
            "replace", xml_id, old_title_en, old_title_en.split(",")[0]))

# --- Category E: structure, persName phrase split into sender/recipient --------------------

add(Fix("szd.korrespondenzen.fleischer-victor.xml", "SZ-SHB/B3", "biblFull entry (deleted)",
        "verify-korrespondenz-daten.md and verify-verknuepfung.md, confirmed-data: no object "
        "carries the bare signature SZ-SHB/B3, its pieces are SZ-SHB/B3.1-5 and belong to the "
        "Kaemmerer correspondence; SZ-SEF/B3 already carries the facsimile in this same konvolut",
        "delete_entry", "SZDKOR.fleischer-victor.B.31"))

add(Fix("szd.korrespondenzen.fleischer-victor.xml", "SZ-SEF/B3", "correspAction (sender/recipient split)",
        "verify-korrespondenz-daten.md, confirmed-data: correspDesc type='fromZweig' with a "
        "single correspAction[@type='sent'] whose persName held the whole title phrase 'Brief "
        "an Victor Fleischer ohne Datum' instead of a name; the title's own wording establishes "
        "sender Stefan Zweig, recipient Victor Fleischer (GND already used elsewhere in this file)",
        "replace", "SZDKOR.fleischer-victor.B.201",
        '<correspDesc type="fromZweig">\n'
        '              <correspAction type="sent">\n'
        '                <persName>\n'
        '                  <surname>Datum</surname>\n'
        '                  <forename>Brief an Victor Fleischer ohne</forename>\n'
        '                </persName>\n'
        '              </correspAction>\n'
        '            </correspDesc>',
        '<correspDesc type="fromZweig">\n'
        '              <correspAction type="sent">\n'
        '                <persName ref="http://d-nb.info/gnd/118637479">\n'
        '                  <surname>Zweig</surname>\n'
        '                  <forename>Stefan</forename>\n'
        '                </persName>\n'
        '              </correspAction>\n'
        '              <correspAction type="received">\n'
        '                <persName ref="https://d-nb.info/gnd/116601485">\n'
        '                  <surname>Fleischer</surname>\n'
        '                  <forename>Victor</forename>\n'
        '                </persName>\n'
        '              </correspAction>\n'
        '            </correspDesc>'))

add(Fix("szd.korrespondenzen.fleischer-victor.xml", "SZ-SAH/B1.1", "correspAction (sender/recipient split)",
        "verify-korrespondenz-daten.md, confirmed-data: correspDesc type='fromZweig' with a "
        "single correspAction[@type='sent'] whose persName held the whole title phrase 'Victor "
        "Fleischer an Paul Heidelbach'; the title's own wording establishes sender Victor "
        "Fleischer (GND already used elsewhere in this file), recipient Paul Heidelbach",
        "replace", "SZDKOR.fleischer-victor.B.202",
        '<correspDesc type="fromZweig">\n'
        '              <correspAction type="sent">\n'
        '                <persName>\n'
        '                  <surname>Heidelbach</surname>\n'
        '                  <forename>Victor Fleischer an Paul</forename>\n'
        '                </persName>\n'
        '              </correspAction>\n'
        '            </correspDesc>',
        '<correspDesc type="fromZweig">\n'
        '              <correspAction type="sent">\n'
        '                <persName ref="https://d-nb.info/gnd/116601485">\n'
        '                  <surname>Fleischer</surname>\n'
        '                  <forename>Victor</forename>\n'
        '                </persName>\n'
        '              </correspAction>\n'
        '              <correspAction type="received">\n'
        '                <persName>\n'
        '                  <surname>Heidelbach</surname>\n'
        '                  <forename>Paul</forename>\n'
        '                </persName>\n'
        '              </correspAction>\n'
        '            </correspDesc>'))

add(Fix("szd.korrespondenzen.moller-rudolf.xml", "SZ-SHB/B6.2", "correspAction (sender/recipient/date split)",
        "verify-korrespondenz-daten.md, confirmed-data: correspDesc type='fromZweig' with a "
        "single correspAction[@type='sent'] whose persName held the whole title phrase "
        "'Ansichtspostkarte an Rudolf Möller vom 28. November 1930'; the title's own wording "
        "establishes sender Stefan Zweig, recipient Rudolf Möller and the date 28 November 1930",
        "replace", "SZDKOR.moller-rudolf.2",
        '<correspDesc type="fromZweig">\n'
        '              <correspAction type="sent">\n'
        '                <persName>\n'
        '                  <surname>1930</surname>\n'
        '                  <forename>Ansichtspostkarte an Rudolf Möller vom 28. November</forename>\n'
        '                </persName>\n'
        '              </correspAction>\n'
        '            </correspDesc>',
        '<correspDesc type="fromZweig">\n'
        '              <correspAction type="sent">\n'
        '                <persName ref="http://d-nb.info/gnd/118637479">\n'
        '                  <surname>Zweig</surname>\n'
        '                  <forename>Stefan</forename>\n'
        '                </persName>\n'
        '                <date when="1930-11-28">28. November 1930</date>\n'
        '              </correspAction>\n'
        '              <correspAction type="received">\n'
        '                <persName>\n'
        '                  <surname>Möller</surname>\n'
        '                  <forename>Rudolf</forename>\n'
        '                </persName>\n'
        '              </correspAction>\n'
        '            </correspDesc>'))

# The sibling entry SZ-SHB/B6.1 carries the same defect class's remedy note: repair its
# doubly encoded umlauts (UTF-8 bytes read as Latin-1 and re-encoded), confined to its own
# entry so the rest of the file, including the teiHeader boilerplate that carries the same
# mojibake outside any defect this checkup reports, is left untouched.
add(Fix("szd.korrespondenzen.moller-rudolf.xml", "SZ-SHB/B6.1", "title/country (encoding)",
        "verify-korrespondenz-daten.md, part of the SZ-SHB/B6.2 remedy: 'repair the encoding "
        "of the sibling entry'; MÃ¶ller and Ãsterreich are UTF-8 mistakenly decoded as Latin-1",
        "replace", "SZDKOR.moller-rudolf.1", "MÃ¶ller ohne Datum,\n                SZ-SHB/B6.1</title>\n              <title xml:lang=\"en\">Ansichtspostkarte an Rudolf MÃ¶ller ohne Datum,\n                SZ-SHB/B6.1</title>",
        "Möller ohne Datum,\n                SZ-SHB/B6.1</title>\n              <title xml:lang=\"en\">Ansichtspostkarte an Rudolf Möller ohne Datum,\n                SZ-SHB/B6.1</title>"))
# The double-encoding turns "Ö" (correct UTF-8 bytes C3 96) into the four bytes C3 83 C2 96,
# which one correct UTF-8 decode renders as the two characters U+00C3 U+0096, not a typeable
# literal, so it is built from the bytes rather than pasted as text.
_MOJIBAKE_OE = bytes([0xC3, 0x83, 0xC2, 0x96]).decode("utf-8")
add(Fix("szd.korrespondenzen.moller-rudolf.xml", "SZ-SHB/B6.1", "country (encoding)",
        "see title/country (encoding) above",
        "replace", "SZDKOR.moller-rudolf.1",
        f"<country>{_MOJIBAKE_OE}sterreich</country>", "<country>Österreich</country>"))

# --- Category F: Hirschfeld, move data from the malformed duplicate, then delete it --------

_HIRSCHFELD_B1 = (
    '<biblFull xml:id="SZDKOR.hirschfeld-eugenie.B.1">\n'
    '          <fileDesc>\n'
    '            <titleStmt>\n'
    '              <title xml:lang="de">Stefan Zweig an Eugenie Hirschfeld,\n'
    '                                15.06.1906</title>\n'
    '              <title xml:lang="en">Stefan Zweig to Eugenie Hirschfeld,\n'
    '                                15.06.1906</title>\n'
    '            </titleStmt>\n'
    '            <publicationStmt>\n'
    '              <ab>Einzelbrief</ab>\n'
    '            </publicationStmt>\n'
    '            <sourceDesc>\n'
    '              <msDesc>\n'
    '                <msIdentifier>\n'
    '                  <country>Österreich</country>\n'
    '                  <settlement>Salzburg</settlement>\n'
    '                  <repository ref="http://d-nb.info/gnd/1047605287">Literaturarchiv Salzburg</repository>\n'
    '                  <idno type="signature">SZ_SEF_B5.1</idno>\n'
    '                </msIdentifier>\n'
    '                <msContents>\n'
    '                  <textLang>\n'
    '                    <lang xml:lang="ger">Deutsch</lang>\n'
    '                    <lang xml:lang="ger">German</lang>\n'
    '                  </textLang>\n'
    '                </msContents>\n'
    '                <physDesc>\n'
    '                  <objectDesc>                    \n'
    '<supportDesc>\n'
    '                      <support>\n'
    '                        <material ana="szdg:WritingMaterial" xml:lang="de">Ansichtspostkarte: &quot;LONDON. THE TOWER FROM THE\n'
    '                                                  RIVER.&quot;</material>\n'
    '                        <material ana="szdg:WritingMaterial" xml:lang="en">Picture postcard: &quot;LONDON. THE TOWER FROM THE\n'
    '                                                  RIVER.&quot;</material>\n'
    '                        <material ana="szdg:WritingInstrument" xml:lang="de">schwarze Tinte</material>\n'
    '                        <material ana="szdg:WritingInstrument" xml:lang="en">black ink</material>\n'
    '                      </support>\n'
    '                      <extent>\n'
    '                        <span xml:lang="de">1 Ansichtspostkarte, Manuskript,\n'
    '                                                  1 Blatt</span>\n'
    '                        <span xml:lang="en">1 picture postcard, manuscript,\n'
    '                                                  1 leaf</span>\n'
    '                      </extent>\n'
    '                    </supportDesc>\n'
    '                  </objectDesc>\n'
    '                  <handDesc>\n'
    '                    <ab>Stefan Zweig</ab>\n'
    '                  </handDesc>\n'
    '                </physDesc>\n'
    '                <history>\n'
    '                  <provenance>\n'
    '                    <ab>Inge und Erich Fitzbauer</ab>\n'
    '                  </provenance>\n'
    '                  <acquisition>\n'
    '                    <ab xml:lang="de">Ankauf 2023</ab>\n'
    '                    <ab xml:lang="en">Acquisition 2023</ab>\n'
    '                  </acquisition>\n'
    '                </history>\n'
    '              </msDesc>\n'
    '            </sourceDesc>\n'
    '          </fileDesc>\n'
    '          <profileDesc>\n'
    '            <correspDesc type="toZweig">\n'
    '              <correspAction type="sent">\n'
    '                <persName ref="http://d-nb.info/gnd/118637479">\n'
    '                  <surname>Zweig</surname>\n'
    '                  <forename>Stefan</forename>\n'
    '                </persName>\n'
    '                <placeName>London</placeName>\n'
    '              </correspAction>\n'
    '              <correspAction type="received">\n'
    '                <persName ref="#SZDPER.2137">\n'
    '                  <surname>Hirschfeld</surname>\n'
    '                  <forename>Eugenie</forename>\n'
    '                </persName>\n'
    '              </correspAction>\n'
    '            </correspDesc>\n'
    '          </profileDesc>\n'
    '        </biblFull>'
)
add(Fix("szd.korrespondenzen.hirschfeld-eugenie.xml", "SZ_SEF_B5.1", "biblFull entry (deleted, data moved to SZ-SEF/B5.1)",
        "verify-verknuepfung.md, confirmed-data: both entries describe the same picture "
        "postcard of 15 June 1906 (both titles agree); the underscore entry carries the "
        "physical description, hand and provenance that the canonical entry lacks",
        "delete_entry", "SZDKOR.hirschfeld-eugenie.B.1"))

_HIRSCHFELD_B19_OLD = (
    '<biblFull xml:id="SZDKOR.hirschfeld-eugenie.B.19">\n'
    '          <fileDesc>\n'
    '            <titleStmt>\n'
    '              <title xml:lang="de">Ansichtspostkarte an Eugenie Hirschfeld vom 15. Juni 1906</title>\n'
    '              <title xml:lang="en">Ansichtspostkarte an Eugenie Hirschfeld vom 15. Juni 1906</title>\n'
    '            </titleStmt>\n'
    '            <publicationStmt>\n'
    '              <ab>Einzelbrief</ab>\n'
    '            </publicationStmt>\n'
    '            <sourceDesc>\n'
    '              <msDesc>\n'
    '                <msIdentifier>\n'
    '                  <country>Österreich</country>\n'
    '                  <settlement>Salzburg</settlement>\n'
    '                  <repository ref="http://d-nb.info/gnd/1047605287">Literaturarchiv Salzburg</repository>\n'
    '                  <idno type="signature">SZ-SEF/B5.1</idno>\n'
    '                  <altIdentifier>\n'
    '                    <idno type="PID">o:szd.1389</idno>\n'
    '                  </altIdentifier>\n'
    '                </msIdentifier>\n'
    '              </msDesc>\n'
    '            </sourceDesc>\n'
    '          </fileDesc>\n'
    '          <profileDesc>\n'
    '            <correspDesc type="fromZweig">\n'
    '              <correspAction type="sent">\n'
    '                <persName ref="#SZDPER.2137">\n'
    '                  <name>Eugenie Hirschfeld</name>\n'
    '                </persName>\n'
    '              </correspAction>\n'
    '            </correspDesc>\n'
    '          </profileDesc>\n'
    '        </biblFull>'
)
_HIRSCHFELD_B19_NEW = (
    '<biblFull xml:id="SZDKOR.hirschfeld-eugenie.B.19">\n'
    '          <fileDesc>\n'
    '            <titleStmt>\n'
    '              <title xml:lang="de">Ansichtspostkarte an Eugenie Hirschfeld vom 15. Juni 1906</title>\n'
    '              <title xml:lang="en">Ansichtspostkarte an Eugenie Hirschfeld vom 15. Juni 1906</title>\n'
    '            </titleStmt>\n'
    '            <publicationStmt>\n'
    '              <ab>Einzelbrief</ab>\n'
    '            </publicationStmt>\n'
    '            <sourceDesc>\n'
    '              <msDesc>\n'
    '                <msIdentifier>\n'
    '                  <country>Österreich</country>\n'
    '                  <settlement>Salzburg</settlement>\n'
    '                  <repository ref="http://d-nb.info/gnd/1047605287">Literaturarchiv Salzburg</repository>\n'
    '                  <idno type="signature">SZ-SEF/B5.1</idno>\n'
    '                  <altIdentifier>\n'
    '                    <idno type="PID">o:szd.1389</idno>\n'
    '                  </altIdentifier>\n'
    '                </msIdentifier>\n'
    '                <msContents>\n'
    '                  <textLang>\n'
    '                    <lang xml:lang="ger">Deutsch</lang>\n'
    '                    <lang xml:lang="ger">German</lang>\n'
    '                  </textLang>\n'
    '                </msContents>\n'
    '                <physDesc>\n'
    '                  <objectDesc>                    \n'
    '<supportDesc>\n'
    '                      <support>\n'
    '                        <material ana="szdg:WritingMaterial" xml:lang="de">Ansichtspostkarte: &quot;LONDON. THE TOWER FROM THE\n'
    '                                                  RIVER.&quot;</material>\n'
    '                        <material ana="szdg:WritingMaterial" xml:lang="en">Picture postcard: &quot;LONDON. THE TOWER FROM THE\n'
    '                                                  RIVER.&quot;</material>\n'
    '                        <material ana="szdg:WritingInstrument" xml:lang="de">schwarze Tinte</material>\n'
    '                        <material ana="szdg:WritingInstrument" xml:lang="en">black ink</material>\n'
    '                      </support>\n'
    '                      <extent>\n'
    '                        <span xml:lang="de">1 Ansichtspostkarte, Manuskript,\n'
    '                                                  1 Blatt</span>\n'
    '                        <span xml:lang="en">1 picture postcard, manuscript,\n'
    '                                                  1 leaf</span>\n'
    '                      </extent>\n'
    '                    </supportDesc>\n'
    '                  </objectDesc>\n'
    '                  <handDesc>\n'
    '                    <ab>Stefan Zweig</ab>\n'
    '                  </handDesc>\n'
    '                </physDesc>\n'
    '                <history>\n'
    '                  <provenance>\n'
    '                    <ab>Inge und Erich Fitzbauer</ab>\n'
    '                  </provenance>\n'
    '                  <acquisition>\n'
    '                    <ab xml:lang="de">Ankauf 2023</ab>\n'
    '                    <ab xml:lang="en">Acquisition 2023</ab>\n'
    '                  </acquisition>\n'
    '                </history>\n'
    '              </msDesc>\n'
    '            </sourceDesc>\n'
    '          </fileDesc>\n'
    '          <profileDesc>\n'
    '            <correspDesc type="fromZweig">\n'
    '              <correspAction type="sent">\n'
    '                <persName ref="http://d-nb.info/gnd/118637479">\n'
    '                  <surname>Zweig</surname>\n'
    '                  <forename>Stefan</forename>\n'
    '                </persName>\n'
    '                <date when="1906-06-15">15. Juni 1906</date>\n'
    '                <placeName>London</placeName>\n'
    '              </correspAction>\n'
    '              <correspAction type="received">\n'
    '                <persName ref="#SZDPER.2137">\n'
    '                  <surname>Hirschfeld</surname>\n'
    '                  <forename>Eugenie</forename>\n'
    '                </persName>\n'
    '              </correspAction>\n'
    '            </correspDesc>\n'
    '          </profileDesc>\n'
    '        </biblFull>'
)
add(Fix("szd.korrespondenzen.hirschfeld-eugenie.xml", "SZ-SEF/B5.1",
        "physDesc/handDesc/history (moved in), correspAction (sender/recipient/date completed)",
        "verify-verknuepfung.md, confirmed-data: the canonical entry carried the facsimile "
        "PID but neither the physical description nor a complete correspAction; both are "
        "established from the SZ_SEF_B5.1 duplicate describing the same postcard",
        "replace_entry", "SZDKOR.hirschfeld-eugenie.B.19", _HIRSCHFELD_B19_OLD, _HIRSCHFELD_B19_NEW))


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def group_by_file(fixes: list[Fix]) -> dict[str, list[Fix]]:
    out: dict[str, list[Fix]] = {}
    for fx in fixes:
        out.setdefault(fx.file, []).append(fx)
    return out


def run(apply: bool) -> int:
    problems = 0
    applied = 0
    already = 0
    log_rows = []
    for fname, fixes in group_by_file(FIXES).items():
        path = KONVOLUTE / fname
        if not path.exists():
            print(f"ERROR {fname}: file not found")
            problems += 1
            continue
        text = szd_io.read_text(path)
        original = text
        for fx in fixes:
            try:
                text, status = APPLIERS[fx.kind](text, fx)
            except ValueError as exc:
                print(f"ERROR {fname} [{fx.shelfmark} / {fx.field}]: {exc}")
                problems += 1
                continue
            label = "applied" if status == "applied" else "already in place"
            print(f"{'  fixing' if apply else '  dry-run'}: {fname} [{fx.shelfmark}] "
                  f"{fx.field}: {label}")
            if status == "applied":
                applied += 1
                log_rows.append({
                    "date": date.today().isoformat(), "file": fname,
                    "shelfmark": fx.shelfmark, "field": fx.field,
                    "old": fx.old or "(added)", "new": fx.new, "evidence": fx.evidence,
                })
            else:
                already += 1
        if text != original:
            try:
                ET.fromstring(text)
            except ET.ParseError as exc:
                print(f"ERROR {fname}: result not well formed, this file is not written: {exc}")
                problems += 1
                continue
            if apply:
                szd_io.write_atomic(path, text)
                print(f"  written: {fname}")

    print(f"\napplied: {applied}, already in place: {already}, problems: {problems}")
    if apply and applied and not problems:
        n = szd_io.append_log(LOG, LOG_FIELDS, log_rows)
        print(f"logged {n} rows to {LOG.name}")
    if not apply:
        print("dry run -- nothing written. Use --apply to write.")
    return 1 if problems else 0


def verify() -> int:
    """Re-run in dry-run mode and fail if anything would still be applied."""
    problems = 0
    for fname, fixes in group_by_file(FIXES).items():
        path = KONVOLUTE / fname
        if not path.exists():
            print(f"ERROR {fname}: file not found")
            problems += 1
            continue
        try:
            ET.fromstring(szd_io.read_text(path))
        except ET.ParseError as exc:
            print(f"NOT WELL FORMED: {fname}: {exc}")
            problems += 1
            continue
        text = szd_io.read_text(path)
        for fx in fixes:
            try:
                _, status = APPLIERS[fx.kind](text, fx)
            except ValueError as exc:
                print(f"ERROR {fname} [{fx.shelfmark} / {fx.field}]: {exc}")
                problems += 1
                continue
            if status == "applied":
                print(f"NOT YET APPLIED: {fname} [{fx.shelfmark}] {fx.field}")
                problems += 1
    print(f"\nfiles well formed and every fix already applied: {'yes' if not problems else 'no'}")
    print(f"problems: {problems}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="write the changes")
    parser.add_argument("--verify", action="store_true",
                         help="check that every fix is applied and every file well formed")
    args = parser.parse_args()
    if args.verify:
        return 1 if verify() else 0
    return run(args.apply)


if __name__ == "__main__":
    raise SystemExit(main())
