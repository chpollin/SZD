#!/usr/bin/env python3
"""Derive the timeline lanes of the Lebenskalender from the TEI sources.

The website gets a timeline view in which lanes are switched on and off. This script
produces one JSON file per lane, all of them in the same event schema, plus an index.json
that lists the lanes and carries the generation timestamp.

Lanes and their sources:

* biography            -- docs/lebenskalender/SZDBIO.xml (o:szd.lebenskalender)
* correspondence       -- data/Correspondence/SZDKOR.xml plus the konvolut objects in
                          data/Correspondence/konvolute/
* personal-documents   -- data/PersonalDocument/SZDLEB.xml
* autographs           -- data/Autograph/SZDAUT.xml

Usage:

    python scripts/lebenskalender_lanes/build_lanes.py

Design decisions, with their reasons:

* The event date of an autograph is the acquisition date from history/acquisition, not the
  creation date in msContents/summary. The Lebenskalender is a calendar of Stefan Zweig's
  life; the acquisition dates run 1903-1941, the creation dates reach back to the 16th
  century and would break the scale.
* Person identifiers are resolved against data/Index/Person/SZDPER.xml at run time, by GND
  URI for the correspondence (which carries persName/@ref to the GND) and by SZDPER key for
  the other holdings. Nothing is cached in this file, so the script keeps working after
  edits to the person index.
* Dates that a source states only as display text are parsed by a narrow parser that
  recognises the forms actually present. Anything it cannot resolve stays undated and keeps
  its source text as the display label; no century is inferred for two-digit years.
* Duplicates inside the correspondence are merged on the PID of the facsimile, which is the
  only identifier the two levels share for one physical letter. A letter addressed to
  several recipients appears in several konvolut objects with the same PID.
* Output is deterministic. The only varying value, the generation timestamp, sits in a
  single field of index.json so that a comparison can exclude it.
* Stdlib only, following the other scripts in this repository; no dependency management is
  introduced for this one script, which departs from the house default of a pyproject.toml
  per pipeline.

See knowledge/Lebenskalender-Lanes.md for the schema and the delivery path.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]

SZDBIO = REPO_ROOT / "docs" / "lebenskalender" / "SZDBIO.xml"
SZDKOR = REPO_ROOT / "data" / "Correspondence" / "SZDKOR.xml"
KONVOLUTE = REPO_ROOT / "data" / "Correspondence" / "konvolute"
SZDLEB = REPO_ROOT / "data" / "PersonalDocument" / "SZDLEB.xml"
SZDAUT = REPO_ROOT / "data" / "Autograph" / "SZDAUT.xml"
SZDPER = REPO_ROOT / "data" / "Index" / "Person" / "SZDPER.xml"

DEFAULT_OUT_DIR = REPO_ROOT / "data" / "derived" / "lebenskalender"
DEFAULT_DOCS_DIR = REPO_ROOT / "docs" / "lebenskalender" / "lanes"

TEI = "{http://www.tei-c.org/ns/1.0}"
XML = "{http://www.w3.org/XML/1998/namespace}"

# The estate's home archive. Only a bundle held elsewhere states its repository, because
# the view presents the holdings of Salzburg by default. The name is matched besides the GND,
# because some Konvolut files carry a wrong GND on this repository.
HOME_REPOSITORY_GND = "1047605287"
HOME_REPOSITORY_NAME = "Literaturarchiv Salzburg"

# Titles that organise the grouped lists instead of naming the single item.
STRUCTURAL_TITLE_TYPES = frozenset({"Einheitssachtitel", "Gesamttitel"})
LANES = ("biography", "correspondence", "personal-documents", "autographs")

MONTHS_DE = (
    "Januar", "Februar", "März", "April", "Mai", "Juni",
    "Juli", "August", "September", "Oktober", "November", "Dezember",
)
MONTHS_EN = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)
MONTH_NUMBER = {name.lower(): i + 1 for i, name in enumerate(MONTHS_DE)}
MONTH_NUMBER.update({name.lower(): i + 1 for i, name in enumerate(MONTHS_EN)})
MONTH_ALTERNATION = "|".join(sorted(MONTH_NUMBER, key=len, reverse=True))

# Ordered longest-match-first; every pattern yields (iso, granularity).
TEXT_DATE_PATTERNS = (
    (re.compile(rf"(\d{{1,2}})\.\s*({MONTH_ALTERNATION})\s+(\d{{4}})", re.I), "dmy"),
    (re.compile(rf"(\d{{1,2}})\s+({MONTH_ALTERNATION})\s+(\d{{4}})", re.I), "dmy"),
    (re.compile(r"(\d{1,2})\.(\d{1,2})\.(\d{4})"), "d.m.y"),
    (re.compile(r"(\d{4})-(\d{2})-(\d{2})"), "iso"),
    (re.compile(rf"({MONTH_ALTERNATION})\s+(\d{{4}})", re.I), "my"),
    (re.compile(r"(?<!\d)(1[5-9]\d\d|20\d\d)(?!\d)"), "y"),
)

# Roman month with a two- or four-digit year, the form "16. III. 38".
ROMAN_MONTHS = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6,
    "VII": 7, "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12,
}
ROMAN_DATE = re.compile(
    r"(?<!\d)(\d{1,2})\.\s*(XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)\.?\s*(\d{2,4})(?!\d)"
)

WHITESPACE = re.compile(r"\s+")
# A trailing German date expression in a head line that carries no date element.
TRAILING_DE_DATE = re.compile(
    rf",?\s*(?:\d{{1,2}}\.\s*)?(?:{'|'.join(MONTHS_DE)})?\s*\d{{4}}\s*$", re.I
)


@dataclass(frozen=True)
class DateValue:
    """A resolved date: ISO start, optional ISO end, and the precision label.

    label_from_source keeps the wording of the source as the display label where the ISO
    value carries more than the source states, which happens when a two-digit year is read
    as a 20th-century one.
    """

    iso: str
    precision: str
    end: str | None = None
    label_from_source: bool = False


@dataclass
class Report:
    """Collected findings of one run, printed as the closing summary."""

    problems: list[str] = field(default_factory=list)
    merges: list[dict[str, object]] = field(default_factory=list)
    unresolved_dates: Counter[str] = field(default_factory=Counter)
    places: Counter[str] = field(default_factory=Counter)
    precision: dict[str, Counter[str]] = field(
        default_factory=lambda: defaultdict(Counter)
    )

    def note(self, message: str) -> None:
        self.problems.append(message)


def text_of(elem: ET.Element | None) -> str:
    if elem is None:
        return ""
    return WHITESPACE.sub(" ", "".join(elem.itertext())).strip()


def parse(path: Path) -> ET.ElementTree:
    if not path.exists():
        raise FileNotFoundError(f"source missing: {path}")
    return ET.parse(path)


def object_pid(tree: ET.ElementTree) -> str:
    """PID of the GAMS object, taken from the teiHeader rather than from a hard-coded map."""
    idno = tree.getroot().find(f"{TEI}teiHeader//{TEI}publicationStmt/{TEI}idno[@type='PID']")
    if idno is None or not (idno.text or "").strip():
        raise ValueError("teiHeader carries no publicationStmt/idno[@type='PID']")
    return idno.text.strip()


# --- person index -----------------------------------------------------------------


def person_name(person: ET.Element) -> str:
    pers_name = person.find(f"{TEI}persName")
    if pers_name is None:
        return ""
    surname = text_of(pers_name.find(f"{TEI}surname"))
    forename = text_of(pers_name.find(f"{TEI}forename"))
    if surname and forename:
        return f"{surname}, {forename}"
    return surname or forename or text_of(pers_name)


def load_person_index() -> tuple[dict[str, str], dict[str, str]]:
    """Return (GND URI -> SZDPER key, SZDPER key -> display name).

    The GND map is keyed on the bare number so that the http/https spellings both resolve.
    """
    by_gnd: dict[str, str] = {}
    names: dict[str, str] = {}
    for person in parse(SZDPER).getroot().iter(f"{TEI}person"):
        key = person.get(XML + "id")
        if not key:
            continue
        names[key] = person_name(person)
        pers_name = person.find(f"{TEI}persName")
        gnd = gnd_number(pers_name.get("ref") if pers_name is not None else None)
        if gnd:
            by_gnd.setdefault(gnd, key)
    return by_gnd, names


def gnd_number(ref: str | None) -> str | None:
    if not ref:
        return None
    match = re.search(r"gnd/([\w-]+)", ref)
    return match.group(1) if match else None


def person_entry(
    key: str | None, fallback_name: str, names: dict[str, str]
) -> dict[str, str | None]:
    return {"id": key, "name": names.get(key or "", "") or fallback_name}


def pers_name_text(pers_name: ET.Element) -> str:
    """Index order, the form the person index uses and the form persons[].name carries."""
    surname = text_of(pers_name.find(f"{TEI}surname"))
    forename = text_of(pers_name.find(f"{TEI}forename"))
    if surname and forename:
        return f"{surname}, {forename}"
    return surname or forename or text_of(pers_name)


def pers_name_display(pers_name: ET.Element) -> str:
    """Reading order, for the generated correspondence title."""
    surname = text_of(pers_name.find(f"{TEI}surname"))
    forename = text_of(pers_name.find(f"{TEI}forename"))
    if surname and forename:
        return f"{forename} {surname}"
    return surname or forename or text_of(pers_name)


# --- dates ------------------------------------------------------------------------


def precision_of(iso: str) -> str:
    return {4: "year", 7: "month", 10: "day"}.get(len(iso), "year")


def attribute_date(date_elem: ET.Element) -> DateValue | None:
    """Resolve @when, @from/@to and @notBefore/@notAfter.

    A span wins over a point, because one biography head carries @when for its beginning and
    @to for its end. @type="undated" is not honoured on an element that also carries a
    value: in SZDKOR it marks a bundle holding undated pieces besides the dated ones
    ("1930-1932, n. d.").
    """
    when = date_elem.get("when")
    start = date_elem.get("from") or when
    end = date_elem.get("to")
    if start and end and end != start:
        return DateValue(start, "range", end)
    if when:
        return DateValue(when, precision_of(when))
    if start:
        return DateValue(start, "range")
    not_before, not_after = date_elem.get("notBefore"), date_elem.get("notAfter")
    if not_before or not_after:
        begin = not_before or not_after
        assert begin is not None
        closing = not_after if not_after and not_after != begin else None
        return DateValue(begin, "inferred", closing)
    return None


def text_date_tokens(text: str) -> tuple[list[str], str]:
    """Find the date tokens in free text and return them with the unmatched remainder."""
    remainder = list(text)
    tokens: list[str] = []
    for pattern, kind in TEXT_DATE_PATTERNS:
        for match in pattern.finditer("".join(remainder)):
            if any(remainder[i] == "\0" for i in range(match.start(), match.end())):
                continue
            iso = iso_from_match(match, kind)
            if iso is None:
                continue
            tokens.append(iso)
            for i in range(match.start(), match.end()):
                remainder[i] = "\0"
    return tokens, "".join(c for c in remainder if c != "\0")


def iso_from_match(match: re.Match[str], kind: str) -> str | None:
    if kind == "dmy":
        month = MONTH_NUMBER.get(match.group(2).lower())
        if month is None:
            return None
        return f"{int(match.group(3)):04d}-{month:02d}-{int(match.group(1)):02d}"
    if kind == "d.m.y":
        return f"{int(match.group(3)):04d}-{int(match.group(2)):02d}-{int(match.group(1)):02d}"
    if kind == "iso":
        return match.group(0)
    if kind == "my":
        month = MONTH_NUMBER.get(match.group(1).lower())
        if month is None:
            return None
        return f"{int(match.group(2)):04d}-{month:02d}"
    return match.group(1)


def text_date(raw: str) -> DateValue | None:
    """Resolve a date stated only as display text.

    Brackets, qualifiers and any leftover wording downgrade the precision to inferred; two
    or more tokens make a range. A text that yields no token stays unresolved, so that no
    century is invented for a two-digit year and no weekday becomes a date.
    """
    text = WHITESPACE.sub(" ", raw).strip()
    if not text:
        return None
    roman = roman_numeral_date(text)
    if roman is not None:
        return roman
    bracketed = "[" in text or "]" in text
    tokens, remainder = text_date_tokens(text.strip("[]"))
    if not tokens:
        return None
    tokens = sorted(tokens)
    if len(tokens) > 1:
        return DateValue(tokens[0], "range", tokens[-1])
    leftover = re.sub(r"[\s.,;:()\[\]–—-]+", "", remainder)  # noqa: RUF001 (range dashes)
    if bracketed or leftover:
        return DateValue(tokens[0], "inferred")
    return DateValue(tokens[0], precision_of(tokens[0]))


def roman_numeral_date(text: str) -> DateValue | None:
    """Resolve a date written with a Roman month.

    A two-digit year is read as a 20th-century one, which the holding does not state; such a
    date therefore carries inferred precision and keeps the source wording as its label.
    """
    match = ROMAN_DATE.search(text)
    if match is None:
        return None
    day, month = int(match.group(1)), ROMAN_MONTHS[match.group(2)]
    if not 1 <= day <= 31:
        return None
    digits = match.group(3)
    year = 1900 + int(digits) if len(digits) == 2 else int(digits)
    iso = f"{year:04d}-{month:02d}-{day:02d}"
    if len(digits) == 2:
        return DateValue(iso, "inferred", label_from_source=True)
    return DateValue(iso, "day")


def resolve_date(date_elem: ET.Element | None) -> tuple[DateValue | None, str]:
    """Return the resolved date and the verbatim display text of the element."""
    if date_elem is None:
        return None, ""
    raw = text_of(date_elem)
    value = attribute_date(date_elem) or text_date(raw)
    return value, raw


def date_label(value: DateValue | None, source_text: str) -> dict[str, str]:
    """Display text per language, generated from the ISO value.

    An unresolved date keeps the wording of the source, which is the only information the
    holding offers about it.
    """
    if value is None or (value.label_from_source and source_text):
        if source_text:
            return {"de": source_text, "en": source_text}
        return {"de": "ohne Datum", "en": "undated"}
    start = {"de": iso_label(value.iso, "de"), "en": iso_label(value.iso, "en")}
    if not value.end:
        return start
    # The en dash is the intended separator of a date range.
    return {lang: f"{start[lang]}–{iso_label(value.end, lang)}" for lang in ("de", "en")}  # noqa: RUF001


def iso_label(iso: str, lang: str) -> str:
    parts = iso.split("-")
    year = parts[0]
    if len(parts) == 1:
        return year
    months = MONTHS_DE if lang == "de" else MONTHS_EN
    month = months[int(parts[1]) - 1]
    if len(parts) == 2:
        return f"{month} {year}"
    day = int(parts[2])
    return f"{day}. {month} {year}" if lang == "de" else f"{day} {month} {year}"


# --- event assembly ---------------------------------------------------------------


def make_event(
    event_id: str,
    lane: str,
    value: DateValue | None,
    source_text: str,
    title: dict[str, str],
    persons: list[dict[str, str | None]],
    place: str | None,
    signature: str | None,
    href: str | None,
    facsimile: str | None,
    origin: DateValue | None = None,
    origin_text: str = "",
) -> dict[str, object]:
    """Assemble one event in the schema all lanes share.

    The dateOrigin block mirrors the date block and states when the item itself came into
    being. Only the autographs distinguish the two, so it stays null elsewhere; it also
    stays null where a holding states no origin date, because an absent statement is not an
    editorial statement that the item is undated.
    """
    event: dict[str, object] = {
        "id": event_id,
        "lane": lane,
        "date": value.iso if value else None,
        "datePrecision": value.precision if value else "undated",
    }
    if value and value.end:
        event["dateEnd"] = value.end
    event["dateLabel"] = date_label(value, source_text)
    event["dateOrigin"] = origin.iso if origin else None
    event["dateOriginPrecision"] = origin.precision if origin else None
    if origin and origin.end:
        event["dateOriginEnd"] = origin.end
    event["dateOriginLabel"] = date_label(origin, origin_text) if origin else None
    event["title"] = title
    event["place"] = place or None
    event["persons"] = persons
    event["signature"] = signature or None
    event["href"] = href
    event["facsimile"] = facsimile
    return event


def sort_key(event: dict[str, object]) -> tuple[int, str, str]:
    date = event["date"]
    return (1, "", str(event["id"])) if date is None else (0, str(date), str(event["id"]))


def signature_of(bibl_full: ET.Element) -> str | None:
    idno = bibl_full.find(f".//{TEI}idno[@type='signature']")
    return text_of(idno) or None


def facsimile_of(bibl_full: ET.Element) -> str | None:
    idno = bibl_full.find(f".//{TEI}altIdentifier/{TEI}idno[@type='PID']")
    return text_of(idno) or None


def entry_href(pid: str, entry_id: str) -> str:
    # relative, so the view resolves it on the host it runs on (staging or production)
    return f"/{pid}/sdef:TEI/get#{entry_id}"


# --- lanes ------------------------------------------------------------------------


def build_biography(names: dict[str, str], report: Report) -> list[dict[str, object]]:
    tree = parse(SZDBIO)
    pid = object_pid(tree)
    events: list[dict[str, object]] = []
    for event_elem in tree.getroot().iter(f"{TEI}event"):
        event_id = event_elem.get(XML + "id")
        if not event_id:
            report.note("biography: event without xml:id skipped")
            continue
        head = event_elem.find(f"{TEI}head")
        spans = {
            span.get(XML + "lang"): span
            for span in (head.findall(f"{TEI}span") if head is not None else [])
        }
        date_elem = None
        for lang in ("de", "en"):
            span = spans.get(lang)
            if span is not None and span.find(f"{TEI}date") is not None:
                date_elem = span.find(f"{TEI}date")
                break
        value, raw = resolve_date(date_elem)
        if value is None:
            report.note(f"biography: {event_id} has no resolvable date in its head")
        place = head_place(spans.get("de"), spans.get("en"), event_id, report)
        title = {
            lang: text_of(event_elem.find(f"{TEI}ab[@{XML}lang='{lang}']"))
            for lang in ("de", "en")
        }
        persons = biography_persons(event_elem, names)
        events.append(
            make_event(
                event_id, "biography", value, raw, title, persons, place,
                None, entry_href(pid, event_id), None,
            )
        )
    return events


def head_place(
    span_de: ET.Element | None, span_en: ET.Element | None, event_id: str, report: Report
) -> str | None:
    """The place stands before the date element in the German head line.

    One entry states its head as plain text without a date element; there the trailing date
    expression is stripped instead.
    """
    if span_de is None:
        return None
    prefix = WHITESPACE.sub(" ", span_de.text or "").strip().rstrip(",").strip()
    if not prefix:
        return None
    if span_de.find(f"{TEI}date") is None:
        stripped = TRAILING_DE_DATE.sub("", prefix).rstrip(",").strip()
        if stripped != prefix:
            report.note(
                f"biography: {event_id} has a German head line without a date element "
                f"({prefix!r}); place taken as {stripped!r}"
            )
        return stripped or None
    return prefix


def biography_persons(
    event_elem: ET.Element, names: dict[str, str]
) -> list[dict[str, str | None]]:
    seen: dict[str, str] = {}
    for ab in event_elem.findall(f"{TEI}ab"):
        for name in ab.iter(f"{TEI}name"):
            ref = name.get("ref") or ""
            if not ref.startswith("#SZDPER."):
                continue
            seen.setdefault(ref[1:], text_of(name))
    return [person_entry(key, text, names) for key, text in sorted(seen.items())]


def build_correspondence(
    by_gnd: dict[str, str], names: dict[str, str], report: Report
) -> list[dict[str, object]]:
    """Keep both catalogue levels; shared archival signatures do not prove coverage."""
    index_events, konvolut_events = correspondence_sources(by_gnd, names, report)
    return merge_on_facsimile(index_events + konvolut_events, report)


def correspondence_sources(
    by_gnd: dict[str, str], names: dict[str, str], report: Report
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Events of the index and of all Konvolut files, with ids unique across the files."""
    paths = sorted(KONVOLUTE.glob("szd.korrespondenzen.*.xml"))
    per_file = {SZDKOR: correspondence_from(SZDKOR, by_gnd, names, report, konvolut_pids(paths))}
    for path in paths:
        per_file[path] = correspondence_from(path, by_gnd, names, report)
    disambiguate_ids(per_file, report)
    index_events = per_file.pop(SZDKOR)
    return index_events, [event for events in per_file.values() for event in events]


def disambiguate_ids(per_file: dict[Path, list[dict[str, object]]], report: Report) -> None:
    """Give an xml:id that occurs in several files a suffix naming the file.

    The view uses the id as DOM id and URL fragment, so it must be unique. Every occurrence
    is suffixed, including the first, so that the result does not depend on file order, and
    an id that is unique keeps its plain form and with it its existing permalink. `~` cannot
    occur in an xml:id, which is an NCName, and is safe in a URL fragment.
    """
    files_of: dict[str, set[Path]] = defaultdict(set)
    for path, events in per_file.items():
        for event in events:
            files_of[str(event["id"])].add(path)
    shared = {event_id for event_id, paths in files_of.items() if len(paths) > 1}
    for path, events in per_file.items():
        slug = path.stem.removeprefix("szd.korrespondenzen.")
        for event in events:
            if event["id"] in shared:
                event["id"] = f"{event['id']}~{slug}"
    groups = Counter(
        tuple(sorted(path.name for path in files_of[event_id])) for event_id in shared
    )
    for files, count in sorted(groups.items()):
        report.note(f"{' and '.join(files)} share {count} xml:id value(s); ids suffixed with ~<file>")


def konvolut_pids(paths: list[Path]) -> frozenset[str]:
    """PIDs of the Konvolut files present, taken from the file names.

    The import names each file after its production PID, while the teiHeader of a few
    defective production objects names another one, so the header is no guide here.
    """
    return frozenset(f"o:{path.stem}" for path in paths)


def correspondence_from(
    path: Path,
    by_gnd: dict[str, str],
    names: dict[str, str],
    report: Report,
    known_konvolute: frozenset[str] | None = None,
) -> list[dict[str, object]]:
    """Events of one correspondence file.

    known_konvolute is passed for the index only, whose bundle entries carry the link to
    their Konvolut, the holding repository and the number of pieces.
    """
    tree = parse(path)
    pid = object_pid(tree)
    events: list[dict[str, object]] = []
    for bibl_full in tree.getroot().iter(f"{TEI}biblFull"):
        entry_id = bibl_full.get(XML + "id")
        if not entry_id:
            report.note(f"{path.name}: biblFull without xml:id skipped")
            continue
        sent = bibl_full.find(f".//{TEI}correspAction[@type='sent']")
        received = bibl_full.find(f".//{TEI}correspAction[@type='received']")
        sender = action_person(sent, by_gnd, names)
        recipient = action_person(received, by_gnd, names)
        # Element is falsy when it has no children, so no "or" chaining here.
        date_elem = action_date(sent)
        if date_elem is None:
            date_elem = action_date(received)
        value, raw = resolve_date(date_elem)
        if value is None and raw:
            report.unresolved_dates[raw] += 1
        persons = [p for p in (sender, recipient) if p is not None]
        # An entry that aggregates several pieces keeps the title its source states.
        title = correspondence_title(sent, received)
        if piece_count(bibl_full) > 1:
            stated = holding_title(bibl_full)
            if stated["de"] or stated["en"]:
                title = stated
        event = make_event(
            entry_id, "correspondence", value, raw,
            title,
            persons, action_place(sent),
            signature_of(bibl_full), entry_href(pid, entry_id),
            facsimile_of(bibl_full),
        )
        if known_konvolute is not None:
            event["konvolut"] = konvolut_href(bibl_full, known_konvolute, entry_id, report)
            event["repository"] = foreign_repository(bibl_full)
            event["extent"] = extent_of(bibl_full)
        events.append(event)
    return events


def konvolut_href(
    bibl_full: ET.Element, known: frozenset[str], entry_id: str, report: Report
) -> str | None:
    """Detail page of the Konvolut an index entry names, if that object is in the repository.

    A link to a Konvolut the repository lacks would lead to an object nobody can check here,
    so it is reported instead of emitted.
    """
    for idno in bibl_full.iter(f"{TEI}idno"):
        if idno.get("type") != "konvolut":
            continue
        pid = text_of(idno)
        if pid in known:
            return f"/{pid}/sdef:TEI/get"
        report.note(f"SZDKOR.xml: {entry_id} names Konvolut {pid}, which is not in the repository")
    return None


def foreign_repository(bibl_full: ET.Element) -> dict[str, str] | None:
    identifier = bibl_full.find(f".//{TEI}msIdentifier")
    if identifier is None:
        return None
    repository = identifier.find(f"{TEI}repository")
    name = text_of(repository)
    if not name:
        return None
    assert repository is not None
    if name == HOME_REPOSITORY_NAME or gnd_number(repository.get("ref")) == HOME_REPOSITORY_GND:
        return None
    return {"name": name, "settlement": text_of(identifier.find(f"{TEI}settlement"))}


def extent_of(bibl_full: ET.Element) -> list[dict[str, object]] | None:
    """Pieces per direction, a list because a bundle can hold letters sent and received."""
    extent = [
        {"count": int(text_of(measure)), "subtype": measure.get("subtype")}
        for measure in bibl_full.iter(f"{TEI}measure")
        if measure.get("type") == "correspondence" and text_of(measure).isdigit()
    ]
    return extent or None


def piece_count(bibl_full: ET.Element) -> int:
    """Number of correspondence pieces the entry stands for.

    measure[@type="correspondence"] is the structural criterion; the title wording is not,
    because single-piece entries appear under both the singular and the plural noun.
    """
    total = 0
    for measure in bibl_full.iter(f"{TEI}measure"):
        if measure.get("type") != "correspondence":
            continue
        value = text_of(measure)
        if value.isdigit():
            total += int(value)
    return total


def action_person(
    action: ET.Element | None, by_gnd: dict[str, str], names: dict[str, str]
) -> dict[str, str | None] | None:
    """The person of a correspAction, keyed by GND or by a direct SZDPER reference.

    An empty persName carries no person, only the slot; such entries are dropped instead of
    becoming a nameless person.
    """
    pers_name = action_pers_name(action)
    if pers_name is None:
        return None
    ref = pers_name.get("ref") or ""
    key = ref[1:] if ref.startswith("#SZDPER.") else by_gnd.get(gnd_number(ref) or "")
    label = pers_name_text(pers_name)
    if key is None and not label:
        return None
    return person_entry(key, label, names)


def action_pers_name(action: ET.Element | None) -> ET.Element | None:
    if action is None:
        return None
    pers_name = action.find(f"{TEI}persName")
    if pers_name is None or not (text_of(pers_name) or pers_name.get("ref")):
        return None
    return pers_name


def action_date(action: ET.Element | None) -> ET.Element | None:
    if action is None:
        return None
    dates = action.findall(f"{TEI}date")
    for date_elem in dates:
        if date_elem.get(XML + "lang") == "de":
            return date_elem
    return dates[0] if dates else None


def action_place(action: ET.Element | None) -> str | None:
    if action is None:
        return None
    places = action.findall(f"{TEI}placeName")
    for place in places:
        if place.get(XML + "lang") == "de":
            return text_of(place) or None
    return (text_of(places[0]) or None) if places else None


def correspondence_title(
    sent: ET.Element | None, received: ET.Element | None
) -> dict[str, str]:
    """Generate the title from correspAction, in the reading order the konvolut titles use."""
    unknown = {"de": "Unbekannt", "en": "unknown"}
    sender = action_pers_name(sent)
    recipient = action_pers_name(received)
    from_name = pers_name_display(sender) if sender is not None else ""
    to_name = pers_name_display(recipient) if recipient is not None else ""
    return {
        "de": f"Brief von {from_name or unknown['de']} an {to_name or unknown['de']}",
        "en": f"Letter from {from_name or unknown['en']} to {to_name or unknown['en']}",
    }


def merge_on_facsimile(
    events: list[dict[str, object]], report: Report
) -> list[dict[str, object]]:
    """Fold compatible records of the same facsimile and retain all source metadata.

    A letter with several recipients is catalogued in each partner's konvolut object; the
    facsimile PID is the identifier the copies share. The kept event is the first in the
    sorted order, and the persons of the folded copies are added to it. Conflicting
    signatures, dates or places keep their separate events for editorial review.
    """
    by_pid: dict[str, list[dict[str, object]]] = defaultdict(list)
    singles: list[dict[str, object]] = []
    for event in events:
        pid = event["facsimile"]
        if pid:
            by_pid[str(pid)].append(event)
        else:
            singles.append(event)
    merged: list[dict[str, object]] = []
    for pid, group in sorted(by_pid.items()):
        group.sort(key=sort_key)
        keeper = dict(group[0])
        if len(group) > 1:
            if not compatible_facsimile_records(group):
                report.note(f"facsimile {pid}: conflicting records kept separately")
                merged.extend(group)
                continue
            keeper["sources"] = [dict(event) for event in group]
            persons: list[dict[str, str | None]] = list(keeper["persons"])  # type: ignore[arg-type]
            known = {(p["id"], p["name"]) for p in persons}
            for other in group[1:]:
                for person in other["persons"]:  # type: ignore[union-attr]
                    marker = (person["id"], person["name"])
                    if marker not in known:
                        known.add(marker)
                        persons.append(person)
            keeper["persons"] = persons
            report.merges.append(
                {"facsimile": pid, "kept": keeper["id"], "folded": [e["id"] for e in group[1:]]}
            )
        merged.append(keeper)
    return singles + merged


def compatible_facsimile_records(group: list[dict[str, object]]) -> bool:
    """Require an identical signature and no conflicting nonempty date or place values."""
    signatures = {event["signature"] for event in group}
    if len(signatures) != 1 or not next(iter(signatures)):
        return False
    dates = {
        (event["date"], event.get("dateEnd"), event["datePrecision"])
        for event in group if event["date"]
    }
    places = {event["place"] for event in group if event["place"]}
    return len(dates) <= 1 and len(places) <= 1


def build_personal_documents(names: dict[str, str], report: Report) -> list[dict[str, object]]:
    tree = parse(SZDLEB)
    pid = object_pid(tree)
    events: list[dict[str, object]] = []
    for bibl_full in tree.getroot().iter(f"{TEI}biblFull"):
        entry_id = bibl_full.get(XML + "id")
        if not entry_id:
            report.note("SZDLEB.xml: biblFull without xml:id skipped")
            continue
        orig_date = bibl_full.find(f".//{TEI}history/{TEI}origin/{TEI}origDate")
        value, raw = resolve_date(orig_date)
        if value is None and raw:
            report.unresolved_dates[raw] += 1
        events.append(
            make_event(
                entry_id, "personal-documents", value, raw,
                holding_title(bibl_full), holding_persons(bibl_full, names), None,
                signature_of(bibl_full), entry_href(pid, entry_id), facsimile_of(bibl_full),
            )
        )
    return events


def build_autographs(names: dict[str, str], report: Report) -> list[dict[str, object]]:
    tree = parse(SZDAUT)
    pid = object_pid(tree)
    events: list[dict[str, object]] = []
    for bibl_full in tree.getroot().iter(f"{TEI}biblFull"):
        entry_id = bibl_full.get(XML + "id")
        if not entry_id:
            report.note("SZDAUT.xml: biblFull without xml:id skipped")
            continue
        acquisition = bibl_full.find(f".//{TEI}history/{TEI}acquisition")
        value, raw = resolve_date(
            acquisition.find(f".//{TEI}date") if acquisition is not None else None
        )
        if value is None and raw:
            report.unresolved_dates[raw] += 1
        summary = bibl_full.find(f".//{TEI}msContents/{TEI}summary")
        origin, origin_raw = resolve_date(
            summary.find(f".//{TEI}date") if summary is not None else None
        )
        events.append(
            make_event(
                entry_id, "autographs", value, raw,
                holding_title(bibl_full), holding_persons(bibl_full, names),
                acquisition_place(acquisition), signature_of(bibl_full),
                entry_href(pid, entry_id), facsimile_of(bibl_full),
                origin, origin_raw,
            )
        )
    return events


def holding_title(bibl_full: ET.Element) -> dict[str, str]:
    """Title of the biblFull per language.

    Structural titles are skipped; among the rest an assigned title wins over an object
    title and that over an original one. A language-neutral title serves both languages,
    and a language without its own title borrows the other one.
    """
    title_stmt = bibl_full.find(f"{TEI}fileDesc/{TEI}titleStmt")
    if title_stmt is None:
        return {"de": "", "en": ""}
    all_titles = title_stmt.findall(f"{TEI}title")
    candidates = sorted(
        (t for t in all_titles if t.get("type") not in STRUCTURAL_TITLE_TYPES),
        key=lambda t: {"assigned": 0, "object": 1, "original": 2}.get(t.get("ana") or "", 3),
    )
    result: dict[str, str] = {}
    for lang in ("de", "en"):
        for title in candidates:
            if title.get(XML + "lang") == lang and text_of(title):
                result[lang] = text_of(title)
                break
    neutral = next(
        (text_of(t) for t in candidates if t.get(XML + "lang") is None and text_of(t)), ""
    )
    uniform = next(
        (
            text_of(t)
            for t in all_titles
            if t.get("type") == "Einheitssachtitel" and t.get(XML + "lang") == "de"
        ),
        "",
    )
    for lang in ("de", "en"):
        if not result.get(lang):
            other = result.get("en" if lang == "de" else "de", "")
            result[lang] = neutral or other or uniform
    return {"de": result["de"], "en": result["en"]}


def holding_persons(
    bibl_full: ET.Element, names: dict[str, str]
) -> list[dict[str, str | None]]:
    persons: list[dict[str, str | None]] = []
    seen: set[tuple[str | None, str]] = set()
    for author in bibl_full.findall(f"{TEI}fileDesc/{TEI}titleStmt/{TEI}author"):
        ref = author.get("ref") or ""
        key = ref[1:] if ref.startswith("#SZDPER.") else None
        pers_name = author.find(f"{TEI}persName")
        fallback = pers_name_text(pers_name) if pers_name is not None else text_of(author)
        entry = person_entry(key, fallback, names)
        marker = (entry["id"], str(entry["name"]))
        if marker not in seen:
            seen.add(marker)
            persons.append(entry)
    return persons


def acquisition_place(acquisition: ET.Element | None) -> str | None:
    if acquisition is None:
        return None
    for span in acquisition.findall(f"{TEI}span"):
        if span.get(XML + "lang") == "de":
            place = span.find(f".//{TEI}placeName")
            if place is not None:
                return text_of(place) or None
    place = acquisition.find(f".//{TEI}placeName")
    return text_of(place) or None if place is not None else None


# --- output -----------------------------------------------------------------------


def slim(event: dict[str, object]) -> dict[str, object]:
    """Drop empty fields for delivery; date stays, because the view reads null as undated."""
    kept = {key: value for key, value in event.items() if value is not None or key == "date"}
    if "sources" in kept:
        kept["sources"] = [slim(source) for source in kept["sources"]]
    return kept


def write_json(path: Path, payload: object) -> None:
    """Write compact UTF-8 JSON with LF endings through a temporary file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))
        handle.write("\n")
    if path.exists():  # Windows rename fails on an existing target
        path.unlink()
    tmp.rename(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR,
                        help="target directory of the lane files")
    parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR,
                        help="copy target below docs/ for the GitHub Pages delivery")
    parser.add_argument("--no-docs", action="store_true",
                        help="skip the copy below docs/")
    args = parser.parse_args()

    report = Report()
    by_gnd, names = load_person_index()
    lanes = {
        "biography": build_biography(names, report),
        "correspondence": build_correspondence(by_gnd, names, report),
        "personal-documents": build_personal_documents(names, report),
        "autographs": build_autographs(names, report),
    }

    index_lanes = []
    for lane in LANES:
        events = sorted(lanes[lane], key=sort_key)
        for event in events:
            report.precision[lane][str(event["datePrecision"])] += 1
            if event["place"]:
                report.places[str(event["place"])] += 1
        write_json(args.out_dir / f"{lane}.json", [slim(event) for event in events])
        index_lanes.append(
            {
                "lane": lane,
                "file": f"{lane}.json",
                "events": len(events),
                "datePrecision": dict(sorted(report.precision[lane].items())),
            }
        )

    index = {
        "lanes": index_lanes,
        "mergedDuplicates": len(report.merges),
        "mergedRecords": sum(len(merge["folded"]) for merge in report.merges),
        "suppressedIndexEntries": 0,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    write_json(args.out_dir / "index.json", index)

    if not args.no_docs:
        for name in [f"{lane}.json" for lane in LANES] + ["index.json"]:
            source = (args.out_dir / name).read_bytes()
            target = args.docs_dir / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source)

    print_summary(args, index_lanes, report)
    return 0


def print_summary(args: argparse.Namespace, index_lanes: list[dict[str, object]], report: Report) -> None:
    print("=" * 72)
    print(f"OK lanes written to {args.out_dir}")
    if not args.no_docs:
        print(f"OK copy written to {args.docs_dir}")
    for entry in index_lanes:
        print(f"   {entry['lane']}: {entry['events']} events {entry['datePrecision']}")
    print(f"   merged duplicates: {len(report.merges)}")
    print(f"   merged source records: {sum(len(merge['folded']) for merge in report.merges)}")
    print("   suppressed index entries: 0")
    print("-" * 72)
    print("top places:")
    for place, count in report.places.most_common(10):
        print(f"   {count:5d}  {place}")
    if report.unresolved_dates:
        print("-" * 72)
        print("date texts left unresolved:", file=sys.stderr)
        for text, count in sorted(report.unresolved_dates.items()):
            print(f"   {count:5d}  {text!r}", file=sys.stderr)
    if report.problems:
        print("-" * 72)
        print("WARNUNG findings:", file=sys.stderr)
        for problem in report.problems:
            print(f"   {problem}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
