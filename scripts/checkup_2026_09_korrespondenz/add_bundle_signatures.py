#!/usr/bin/env python3
"""Give the signature-less aggregate entries of data/Correspondence/SZDKOR.xml the bundle
signature their konvolut object proves.

Fifty-four entries of the correspondence index carry no msIdentifier/idno[@type="signature"]:
the contiguous block SZDKOR.928 to SZDKOR.970 created with the SZ-AAL/B ingest of June 2026
and eleven older ones. The report reports these entries as duplicate correspondent headings,
because the two-level model distinguishes two entries of one person by their archival bundle
and without a signature the second entry looks like a repetition of the first. The signature
is not new information: it is the bundle every piece of the konvolut object is filed under.

The rule this script applies, and its only claim, is arithmetic over the konvolut:

    take the signature of every piece of the konvolut object the entry points to,
    drop the item number, drop the group SZ-SAM/AK,
    and if exactly one group is left, that group is the entry's bundle signature.

SZ-SAM/AK is dropped because that picture-postcard series is a collection-wide series with
an index entry of its own, held by 167 entries of this index, so it is never the bundle a
signature-less second entry describes. Where the arithmetic leaves zero groups or more than
one, the entry is left untouched and listed with its groups, because then the konvolut merges
several bundles and which of them the aggregate counts is an editorial question the data does
not answer. Nothing is derived from a name, a title or a piece count.

Forty-two konvolut objects exist as files under data/Correspondence/konvolute/. The remaining
pointers are resolved by one GET of the object's TEI_SOURCE datastream from GAMS, cached on
disk outside the repository, so a repeated run makes no request. GAMS is read-only here.

Serialisation is byte-preserving: one line carrying the new idno element is inserted before
the first altIdentifier of the entry's msIdentifier, which is where every entry that has a
signature carries it, with the indentation of that line. Nothing else in the file is touched.

Default behaviour is a dry run. Pass --apply to write.

Usage:

    python scripts/checkup_2026_09_korrespondenz/add_bundle_signatures.py            # dry run
    python scripts/checkup_2026_09_korrespondenz/add_bundle_signatures.py --apply
    python scripts/checkup_2026_09_korrespondenz/add_bundle_signatures.py --verify

Regime: script pipeline in the shape the other scripts of this repo use, standard library
only, run with plain python.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252
    sys.stdout.reconfigure(errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]

# Shared file helpers, loaded by path because the scripts run as plain files.
_spec = importlib.util.spec_from_file_location("_szd_io", REPO_ROOT / "scripts" / "_szd_io.py")
szd_io = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(szd_io)
INDEX = REPO_ROOT / "data" / "Correspondence" / "SZDKOR.xml"
KONVOLUTE = REPO_ROOT / "data" / "Correspondence" / "konvolute"
DEFAULT_CACHE = Path(tempfile.gettempdir()) / "szd-konvolut-tei"

TEI = "{http://www.tei-c.org/ns/1.0}"
XML = "{http://www.w3.org/XML/1998/namespace}"

GAMS_TEI_SOURCE = "https://gams.uni-graz.at/archive/objects/{pid}/datastreams/TEI_SOURCE/content"

# An item number is a dot, digits and at most one disambiguating letter ("SZ-AAL/B1.110a").
# The group is the signature without it; a signature that carries none is already a group.
ITEM_NUMBER = re.compile(r"\.\d+[a-z]?$")

# The collection-wide picture-postcard series, never the bundle of an aggregate entry.
IGNORED_GROUPS = frozenset({"SZ-SAM/AK"})


def text_of(elem: ET.Element) -> str:
    return re.sub(r"\s+", " ", "".join(elem.itertext())).strip()


def signature_group(signature: str) -> str:
    return ITEM_NUMBER.sub("", signature)


def cache_name(pid: str) -> str:
    """Filename for a cached TEI_SOURCE; ':' is not a legal path character on Windows."""
    return pid.replace(":", "_") + ".xml"


def konvolut_source(pid: str, cache: Path, offline: bool) -> tuple[Path | None, str]:
    """(path to the konvolut TEI, where it came from) for one konvolut PID."""
    local = KONVOLUTE / (pid[2:] + ".xml") if pid.startswith("o:") else None
    if local is not None and local.exists():
        return local, "local"
    cached = cache / cache_name(pid)
    if cached.exists():
        return cached, "cache"
    if offline:
        return None, "not cached"
    url = GAMS_TEI_SOURCE.format(pid=urllib.parse.quote(pid, safe=""))
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            body = response.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        return None, f"GAMS unreachable ({exc})"
    cache.mkdir(parents=True, exist_ok=True)
    cached.write_bytes(body)
    return cached, "GAMS"


def konvolut_groups(path: Path) -> tuple[list[str], int]:
    """(sorted distinct bundle groups, number of piece signatures) of one konvolut file."""
    root = ET.parse(path).getroot()
    signatures = [text_of(idno) for idno in root.iter(f"{TEI}idno")
                  if idno.get("type") == "signature"]
    groups = {signature_group(s) for s in signatures}
    return sorted(groups - IGNORED_GROUPS), len(signatures)


class Case:
    """One signature-less index entry, its konvolut evidence and the resulting action."""

    def __init__(self, xml_id: str, pid: str):
        self.xml_id = xml_id
        self.pid = pid
        self.origin = ""
        self.pieces = 0
        self.groups: list[str] = []
        self.signature = ""
        self.skip = ""


def collect(cache: Path, offline: bool) -> list[Case]:
    root = ET.parse(INDEX).getroot()
    cases: list[Case] = []
    for bibl_full in root.iter(f"{TEI}biblFull"):
        ms_identifier = bibl_full.find(f".//{TEI}msIdentifier")
        if ms_identifier is None:
            continue
        if any(idno.get("type") == "signature"
               for idno in ms_identifier.findall(f"{TEI}idno")):
            continue
        pointers = [text_of(idno) for idno in ms_identifier.iter(f"{TEI}idno")
                    if idno.get("type") == "konvolut"]
        case = Case(bibl_full.get(XML + "id") or "", pointers[0] if pointers else "")
        cases.append(case)
        if not case.pid:
            case.skip = "entry has no konvolut pointer"
            continue
        path, case.origin = konvolut_source(case.pid, cache, offline)
        if path is None:
            case.skip = f"konvolut not resolvable: {case.origin}"
            continue
        try:
            case.groups, case.pieces = konvolut_groups(path)
        except ET.ParseError as exc:
            case.skip = f"konvolut not well formed: {exc}"
            continue
        if len(case.groups) == 1:
            case.signature = case.groups[0]
        elif not case.groups:
            case.skip = "konvolut has no bundle group beside SZ-SAM/AK"
        else:
            case.skip = f"konvolut merges {len(case.groups)} bundles"
    return cases


def escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;")


def insert_signature(text: str, case: Case) -> str:
    """Insert the signature idno where the entries that have one carry it."""
    start = re.search(r'<biblFull xml:id="%s"' % re.escape(case.xml_id), text).start()
    end = text.index("</biblFull>", start)
    ms_start = text.index("<msIdentifier>", start)
    ms_end = text.index("</msIdentifier>", ms_start)
    if not ms_start < ms_end < end:
        raise ValueError(f"{case.xml_id}: msIdentifier not inside the entry")
    anchor = re.search(r"\n([ \t]*)<altIdentifier>", text[ms_start:ms_end])
    if anchor is None:
        raise ValueError(f"{case.xml_id}: no altIdentifier to insert before")
    indent = anchor.group(1)
    at = ms_start + anchor.start()
    line = f'\n{indent}<idno type="signature">{escape(case.signature)}</idno>'
    return text[:at] + line + text[at:]


def report(cases: list[Case]) -> None:
    written = [c for c in cases if not c.skip]
    skipped = [c for c in cases if c.skip]
    print(f"\n=== signature written: {len(written)} entries")
    for case in written:
        piece = "piece" if case.pieces == 1 else "pieces"
        print(f"  {case.xml_id:14s} {case.signature:12s} <- {case.pid} "
              f"({case.origin}, {case.pieces} {piece})")
    print(f"\n=== left untouched: {len(skipped)} entries")
    for case in skipped:
        print(f"  {case.xml_id:14s} {case.pid}")
        print(f"    groups: {', '.join(case.groups) if case.groups else '-'}")
        print(f"    reason: {case.skip}")


def head_revision(path: Path) -> str | None:
    rel = path.resolve().relative_to(REPO_ROOT).as_posix()
    result = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=REPO_ROOT,
                            capture_output=True)
    return result.stdout.decode("utf-8") if result.returncode == 0 else None


def signatures_of(xml_text: str) -> dict[str, tuple[str, str]]:
    """{entry id: (signature, konvolut pid)} over one revision of the index."""
    out: dict[str, tuple[str, str]] = {}
    for bibl_full in ET.fromstring(xml_text).iter(f"{TEI}biblFull"):
        ms_identifier = bibl_full.find(f".//{TEI}msIdentifier")
        if ms_identifier is None:
            continue
        signature = next((text_of(i) for i in ms_identifier.findall(f"{TEI}idno")
                          if i.get("type") == "signature"), "")
        pointer = next((text_of(i) for i in ms_identifier.iter(f"{TEI}idno")
                        if i.get("type") == "konvolut"), "")
        out[bibl_full.get(XML + "id") or ""] = (signature, pointer)
    return out


def verify(cache: Path, offline: bool) -> int:
    """Check that every written signature is the one its konvolut proves.

    The comparison is against HEAD, so the check covers exactly the entries this script
    can have written and no other edit to the same file.
    """
    problems = 0
    try:
        now_text = INDEX.read_text(encoding="utf-8")
        ET.fromstring(now_text)
    except (ET.ParseError, OSError) as exc:
        print(f"NOT WELL FORMED: {INDEX.name}: {exc}")
        return 1
    print(f"{INDEX.name} well formed: yes")

    before_text = head_revision(INDEX)
    if before_text is None:
        print(f"ERROR: {INDEX.name} is not in HEAD, no comparison possible")
        return 1
    before, now = signatures_of(before_text), signatures_of(now_text)
    if set(before) != set(now):
        print(f"ERROR: entry set changed, HEAD {len(before)} -> working tree {len(now)}")
        return 1
    print(f"entries (biblFull): HEAD {len(before)}, working tree {len(now)}")

    checked = 0
    for xml_id, (signature, pointer) in sorted(now.items()):
        if before[xml_id][0] or not signature:
            continue  # not written by this script
        path, origin = konvolut_source(pointer, cache, offline)
        if path is None:
            print(f"ERROR {xml_id}: konvolut not resolvable: {origin}")
            problems += 1
            continue
        groups, pieces = konvolut_groups(path)
        checked += 1
        if groups != [signature]:
            print(f"ERROR {xml_id}: index says {signature}, konvolut {pointer} "
                  f"yields {groups or '-'}")
            problems += 1
    print(f"signatures written by this script and re-derived from the konvolut: {checked}")

    left = [c for c in collect(cache, offline) if not c.skip]
    if left:
        print(f"ERROR: {len(left)} signature-less entries still resolve to one group")
        for case in left:
            print(f"  {case.xml_id} -> {case.signature}")
        problems += len(left)
    else:
        print("no signature-less entry left that the rule could resolve")
    print(f"problems: {problems}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE,
                        help="directory for the fetched konvolut TEI_SOURCE files")
    parser.add_argument("--offline", action="store_true",
                        help="use only local and already cached konvolute, make no request")
    parser.add_argument("--apply", action="store_true", help="write the changes")
    parser.add_argument("--verify", action="store_true",
                        help="only check: every written signature matches its konvolut")
    args = parser.parse_args()

    if args.verify:
        return 1 if verify(args.cache, args.offline) else 0

    cases = collect(args.cache, args.offline)
    report(cases)
    if not args.apply:
        print("\ndry run -- nothing written. Use --apply to write.")
        return 0

    text = szd_io.read_text(INDEX)
    written = [c for c in cases if not c.skip]
    # Descending by position, so an earlier insertion cannot move a later offset.
    written.sort(key=lambda c: text.index('<biblFull xml:id="%s"' % c.xml_id), reverse=True)
    for case in written:
        text = insert_signature(text, case)
    try:
        ET.fromstring(text)
    except ET.ParseError as exc:
        print(f"ERROR: the result is not well formed, nothing written: {exc}",
              file=sys.stderr)
        return 1
    szd_io.write_atomic(INDEX, text)
    print(f"\nwritten: {INDEX.name} ({len(written)} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
