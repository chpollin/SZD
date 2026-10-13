#!/usr/bin/env python3
"""Read-only consistency checks over the TEI files under data/, with an exit code.

Checks, each finding keyed by (check, file, context, detail) so that it can be frozen:

    wellformed       the file parses as XML                                     fatal
    mojibake         double-encoded UTF-8 in text or attribute values ("Ã¼")   enforced
    duplicate-id     an xml:id occurs twice in one file                          enforced
    dangling-ref     a #SZDxxx.n fragment in @ref or @target names no xml:id     enforced
    ref-bare-id      an SZDxxx.n token in @ref or @target without "#"          enforced
    ref-separator    @ref separates several values by ";" "," or " / "          enforced
    gnd-form         a d-nb.info/gnd/ value is no valid GND number               enforced
    date-invalid     @when, @from, @to, @notBefore, @notAfter empty or no date   enforced
    konvolut-pid     a Konvolut file does not name o:<file name> as its PID      enforced
    konvolut-link    an SZDKOR konvolut pointer has no file in konvolute/        enforced
    nfc              text not in Unicode NFC                                     warn
    ref-whitespace   @ref starts or ends with whitespace                         warn
    after-1950       a correspondence date after 1950 (century error or late)    warn

Fatal and enforced findings fail the run unless KNOWN_EXCEPTIONS lists them. Warn checks are
the ones the operator has not decided (NFC normalisation, the century corrections, the ref
whitespace); they are counted and never fail. A known exception that no longer occurs is
reported, so that the list can shrink with the data.

GND_ID accepts the identifier forms of the GND, a record number of eight to ten characters
ending in a check digit or X, and the older form of up to eight digits, a hyphen and a check
character. The pattern is checked against the corpus only, where every number but the
placeholders and one eleven-digit value fits; it is not verified against the DNB syntax rules.

Usage:

    python scripts/check_data.py            # working tree
    python scripts/check_data.py --head     # the committed state, as the staging package reads it
    python scripts/check_data.py -v         # also list known and warn findings

build_staging_package.py calls check() on the HEAD files before it writes a package.

Regime: script pipeline, standard library only, run with plain python.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import importlib.util
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Shared file helpers, loaded by path because the scripts run as plain files.
_spec = importlib.util.spec_from_file_location("_szd_io", REPO_ROOT / "scripts" / "_szd_io.py")
szd_io = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(szd_io)

TEI, XML_ID = szd_io.TEI, szd_io.XML_ID
KONVOLUT_DIR = "data/Correspondence/konvolute/"
SZDKOR = "data/Correspondence/SZDKOR.xml"

FATAL = frozenset({"wellformed"})
ENFORCED = frozenset({
    "mojibake", "duplicate-id", "dangling-ref", "ref-bare-id", "ref-separator", "gnd-form", "date-invalid",
    "konvolut-pid", "konvolut-link",
})
WARN = frozenset({"nfc", "ref-whitespace", "after-1950"})

GND_ID = re.compile(r"(?:1[0123]?\d{7}[0-9X]|[47]\d{6}-\d|[1-9]\d{0,7}-[0-9X]|3\d{7}[0-9X])")
DATE = re.compile(r"(-?)(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?(?:Z|[+-]\d{2}:\d{2})?")
DATE_ATTRS = ("when", "from", "to", "notBefore", "notAfter")
SZD_FRAGMENT = re.compile(r"#(SZD[A-Z]{3}\.[0-9A-Za-z_.\-]+)")
# The RDF mapping reads only the fragment form and drops a bare id.
BARE_ID = re.compile(r"SZD[A-Z]{3}\.\S+")
REF_SEPARATOR = re.compile(r"[;,]|\s/\s")
LAST_PLAUSIBLE_YEAR = 1950


def _mojibake_pattern() -> re.Pattern[str]:
    """A UTF-8 lead byte and its continuation bytes, each read back as cp1252 or latin-1."""
    continuation = set()
    for byte in range(0x80, 0xC0):
        continuation.add(bytes([byte]).decode("latin-1"))
        with contextlib.suppress(UnicodeDecodeError):  # five bytes are undefined in cp1252
            continuation.add(bytes([byte]).decode("cp1252"))
    cont = "[" + re.escape("".join(sorted(continuation))) + "]"
    return re.compile(f"[Â-ß]{cont}|[à-ï]{cont}{{2}}|[ð-ô]{cont}{{3}}")


MOJIBAKE = _mojibake_pattern()


def _raw_byte(char: str) -> bytes:
    try:
        return char.encode("cp1252")
    except UnicodeEncodeError:
        return char.encode("latin-1")


def mojibake(text: str) -> list[str]:
    """The characters a text carries double-encoded, each decoded back from its sequence."""
    found = []
    for match in MOJIBAKE.finditer(text):
        try:
            found.append(b"".join(_raw_byte(c) for c in match.group()).decode("utf-8"))
        except (UnicodeDecodeError, UnicodeEncodeError):
            continue
    return found


def valid_date(value: str) -> bool:
    match = DATE.fullmatch(value)
    if not match:
        return False
    negative, year, month, day = match.groups()
    if month is None:
        return True
    if not 1 <= int(month) <= 12:
        return False
    if day is None:
        return True
    try:
        # proleptic calendar; year 0 and negative years only carry a month in this corpus
        dt.date(int(year) if not negative and int(year) > 0 else 2000, int(month), int(day))
    except ValueError:
        return False
    return True


@dataclass(frozen=True)
class Finding:
    check: str
    file: str
    context: str
    detail: str

    @property
    def key(self) -> tuple[str, str, str, str]:
        return (self.check, self.file, self.context, self.detail)


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)

    def add(self, check: str, file: str, context: str, detail: str) -> None:
        self.findings.append(Finding(check, file, context, detail))

    def unexpected(self) -> list[Finding]:
        return [f for f in self.findings if f.check not in WARN and f.key not in KNOWN_EXCEPTIONS]

    def stale(self) -> list[tuple[str, str, str, str]]:
        found = {f.key for f in self.findings}
        return sorted(k for k in KNOWN_EXCEPTIONS if k not in found)


def walk(root: ET.Element) -> Iterator[tuple[ET.Element, str]]:
    """Every element with the xml:id of its nearest identified ancestor-or-self."""
    stack = [(root, root.get(XML_ID, ""))]
    while stack:
        elem, context = stack.pop()
        yield elem, context
        for child in reversed(list(elem)):
            stack.append((child, child.get(XML_ID) or context))


def _check_text(report: Report, name: str, text: str) -> None:
    if not unicodedata.is_normalized("NFC", text):
        lines = [i for i, line in enumerate(text.splitlines(), 1) if not unicodedata.is_normalized("NFC", line)]
        report.add("nfc", name, "", f"{len(lines)} lines, first at line {lines[0]}")


def _check_tree(report: Report, name: str, root: ET.Element) -> list[tuple[str, str]]:
    """Checks within one parsed file; returns its (context, fragment target) references."""
    seen: Counter[str] = Counter()
    references: list[tuple[str, str]] = []
    for elem, context in walk(root):
        if XML_ID in elem.attrib:
            seen[elem.get(XML_ID)] += 1
        values = [elem.text or "", elem.tail or "", *elem.attrib.values()]
        for char in sorted({c for v in values for c in mojibake(v)}):
            report.add("mojibake", name, context, char)
        ref = elem.get("ref")
        if ref is not None:
            if REF_SEPARATOR.search(ref):
                report.add("ref-separator", name, context, ref)
            if ref != ref.strip():
                report.add("ref-whitespace", name, context, ref)
            for number in szd_io.gnd_ids(ref):
                if not GND_ID.fullmatch(number):
                    report.add("gnd-form", name, context, number)
        for attr in ("ref", "target"):
            value = elem.get(attr) or ""
            references.extend((context, target) for target in SZD_FRAGMENT.findall(value))
            for token in value.split():
                if BARE_ID.fullmatch(token):
                    report.add("ref-bare-id", name, context, token)
        for attr in DATE_ATTRS:
            value = elem.get(attr)
            if value is None:
                continue
            if not valid_date(value):
                report.add("date-invalid", name, context, f"@{attr}={value!r}")
            elif name.startswith("data/Correspondence/") and value.lstrip("-")[:4] > str(LAST_PLAUSIBLE_YEAR):
                report.add("after-1950", name, context, f"@{attr}={value}")
    for xml_id, count in seen.items():
        if count > 1:
            report.add("duplicate-id", name, xml_id, f"{count} times")
    return references


def _check_konvolute(report: Report, files: dict[str, bytes], roots: dict[str, ET.Element]) -> None:
    konvolute = {p for p in files if p.startswith(KONVOLUT_DIR) and "/" not in p[len(KONVOLUT_DIR):]}
    for path in sorted(konvolute):
        root = roots.get(path)
        if root is None:
            continue
        stem = Path(path).stem
        pids = [szd_io.text_of(i) for i in root.iter(f"{TEI}idno") if i.get("type") == "PID"]
        if f"o:{stem}" not in pids:
            report.add("konvolut-pid", path, "", ", ".join(pids[:1]) or "no PID")
    index = roots.get(SZDKOR)
    if index is None:
        return
    for entry in index.iter(f"{TEI}biblFull"):
        for idno in entry.iter(f"{TEI}idno"):
            if idno.get("type") != "konvolut":
                continue
            pid = szd_io.text_of(idno)
            if f"{KONVOLUT_DIR}{pid.removeprefix('o:')}.xml" not in konvolute:
                report.add("konvolut-link", SZDKOR, entry.get(XML_ID, ""), pid)


def check(files: dict[str, bytes]) -> Report:
    """All checks over {repository path: file bytes}."""
    report = Report()
    roots: dict[str, ET.Element] = {}
    defined: set[str] = set()
    references: list[tuple[str, str, str]] = []
    for name in sorted(files):
        try:
            text = files[name].decode("utf-8")
            root = ET.fromstring(files[name])
        except (UnicodeDecodeError, ET.ParseError) as error:
            report.add("wellformed", name, "", str(error))
            continue
        roots[name] = root
        _check_text(report, name, text)
        references.extend((name, *ref) for ref in _check_tree(report, name, root))
        defined.update(e.get(XML_ID) for e in root.iter() if XML_ID in e.attrib)
    for name, context, target in references:
        if target not in defined:
            report.add("dangling-ref", name, context, target)
    _check_konvolute(report, files, roots)
    return report


def working_tree_files(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted((root / "data").rglob("*.xml"))}


def summarise(report: Report, verbose: bool = False, out=sys.stdout) -> int:
    """Print the report; the exit code is 1 when a fatal or enforced finding is not known."""
    by_check = Counter(f.check for f in report.findings)
    unexpected = report.unexpected()
    new_by_check = Counter(f.check for f in unexpected)
    for check_name in sorted(FATAL | ENFORCED | WARN):
        level = "warn" if check_name in WARN else "fatal" if check_name in FATAL else "enforced"
        total = by_check.get(check_name, 0)
        new = new_by_check.get(check_name, 0)
        status = "OK" if not new else "FEHLER"
        if level == "warn":
            status = "WARNUNG" if total else "OK"
        print(f"{status:8s} {check_name:15s} {level:8s} {total} findings, {new if level != 'warn' else '-'} unexpected", file=out)
    for f in unexpected:
        print(f"  NEU {f.check}: {f.file} [{f.context}] {f.detail}", file=out)
    if verbose:
        for f in report.findings:
            if f not in unexpected:
                print(f"  {'bekannt' if f.check not in WARN else 'warn'} {f.check}: {f.file} [{f.context}] {f.detail}", file=out)
    for key in report.stale():
        print(f"  HINWEIS bekannte Ausnahme tritt nicht mehr auf: {key}", file=out)
    return 1 if unexpected else 0


def main() -> int:
    szd_io.console_utf8()
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--head", action="store_true", help="check HEAD instead of the working tree")
    parser.add_argument("-v", "--verbose", action="store_true", help="list known and warn findings too")
    args = parser.parse_args()
    files = szd_io.head_files(REPO_ROOT, "data/") if args.head else working_tree_files(REPO_ROOT)
    return summarise(check(files), args.verbose)


# Findings that stand in the data as open work, frozen as (check, file, context, detail) from the
# run over HEAD on 2026-09-29. Each group names where the open question is recorded. An entry
# leaves this list when the data no longer shows it, a new one comes in only with its question.
KNOWN_EXCEPTIONS: frozenset[tuple[str, str, str, str]] = frozenset({
    # dangling-ref. SZDPER.1026 is a name variant of SZDPER.818 since a108c6f3, SZDPER.1304 never
    # existed (plan, Person index).
    ("dangling-ref", "data/Library/SZDBIB.xml", "SZDBIB.397", "SZDPER.1304"),
    ("dangling-ref", "data/Library/SZDBIB.xml", "SZDBIB.802", "SZDPER.1304"),
    ("dangling-ref", "data/Library/SZDBIB.xml", "SZDBIB.884", "SZDPER.1026"),
    # date-invalid. 29 February 1934 does not exist, the source decides (plan, Konvolute).
    ("date-invalid", "data/Correspondence/konvolute/szd.korrespondenzen.reitter-eugenie.xml", "SZDKOR.reitter-eugenie.65", "@when='1934-02-29'"),
    # gnd-form. gnd/placeholder in SZDKOR.xml (plan, Person index) and the eleven-digit number of
    # SZDKOR.371 and SZDPER.1858 (plan, Reconciliation).
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.371", "11055719711"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.684", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.687", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.688", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.689", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.690", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.696", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.705", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.706", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.724", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.734", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.761", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.764", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.792", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.793", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.794", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.800", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.803", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.850", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.864", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.871", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.891", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.892", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.902", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.904", "placeholder"),
    ("gnd-form", "data/Correspondence/SZDKOR.xml", "SZDKOR.908", "placeholder"),
    ("gnd-form", "data/Index/Person/SZDPER.xml", "SZDPER.1858", "11055719711"),
    # konvolut-pid. The three defective production objects (plan, Konvolute).
    ("konvolut-pid", "data/Correspondence/konvolute/szd.korrespondenzen.judischer-jugendverein-dusseldorf.xml", "", "o:szd.korrespondenzen.judischer-jugendverein-(dusseldorf)"),
    ("konvolut-pid", "data/Correspondence/konvolute/szd.korrespondenzen.judischer-jugendverein.xml", "", "o:szd.korrespondenzen.judischer-jugendverein-(dusseldorf)"),
    ("konvolut-pid", "data/Correspondence/konvolute/szd.korrespondenzen.rascher-und-cie.xml", "", "o:szd.rascher-und-cie"),
    # ref-separator. Two GND numbers on one index person and a name written into @ref (plan, Person
    # index).
    ("ref-separator", "data/Correspondence/konvolute/szd.korrespondenzen.zweig-friderike.xml", "SZDKOR.zweig-friderike.89", "Zweig, Friderike"),
    ("ref-separator", "data/Index/Person/SZDPER.xml", "SZDPER.1680", "http://d-nb.info/gnd/1037465881 / http://d-nb.info/gnd/1037465261"),
})


if __name__ == "__main__":
    raise SystemExit(main())
