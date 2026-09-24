#!/usr/bin/env python3
"""Repair the grouping key term[@type="classification"] in
data/Aufsatzablage/SZDESS.xml and survey the grouped lists for entries that the
renderer drops.

szd-Werke.xsl (gams-www) groups the outer navbar level by
term[@type="classification"][@xml:lang=$locale]. An entry whose classification is missing
in one language disappears from that language's output; a classification that differs from
the established one only in spelling opens a second, near-identical navbar category.

Two rules, both derived from the file itself:

* missing-language -- the entry has a classification in one language only. The pair is
  taken from the entries that carry the same object type (extent/span/term[@type=
  "objecttyp"], de and en) and a complete classification, but only if all of them agree on
  exactly one pair. Otherwise the entry is reported, not changed.
* case-variant -- a classification value differs from a value used by the majority of the
  entries in the same language only by letter case, and is normalised to that spelling.

The survey part is read-only and covers SZDESS, SZDMSK and SZDLEB: entries without a
complete classification, without an Einheitssachtitel and without a PID in
msIdentifier/altIdentifier.

Serialisation is byte-preserving: only the affected term elements are replaced in the file
text, so indentation, attribute order and the CRLF line endings of this file stay as they
are. Default behaviour is a dry run; pass --apply to write.
"""
from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252
    sys.stdout.reconfigure(errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]
SZDESS = REPO_ROOT / "data" / "Aufsatzablage" / "SZDESS.xml"
GROUPED_LISTS = [
    SZDESS,
    REPO_ROOT / "data" / "Work" / "SZDMSK.xml",
    REPO_ROOT / "data" / "PersonalDocument" / "SZDLEB.xml",
]

TEI = "{http://www.tei-c.org/ns/1.0}"
XML = "{http://www.w3.org/XML/1998/namespace}"


def text_of(elem: ET.Element) -> str:
    return re.sub(r"\s+", " ", "".join(elem.itertext())).strip()


def classification(bibl_full: ET.Element) -> dict[str, str]:
    return {t.get(XML + "lang"): text_of(t)
            for t in bibl_full.iter(f"{TEI}term") if t.get("type") == "classification"}


def object_type(bibl_full: ET.Element) -> tuple[str, str]:
    found: dict[str, str] = {}
    for span in bibl_full.iter(f"{TEI}span"):
        for term in span.iter(f"{TEI}term"):
            if term.get("type") == "objecttyp":
                found.setdefault(span.get(XML + "lang") or "", text_of(term))
    return found.get("de", ""), found.get("en", "")


def entries(path: Path) -> list[ET.Element]:
    return list(ET.parse(path).getroot().iter(f"{TEI}biblFull"))


class Change:
    def __init__(self, xml_id: str, rule: str, old: dict[str, str], new: dict[str, str],
                 reason: str):
        self.xml_id = xml_id
        self.rule = rule
        self.old = old
        self.new = new
        self.reason = reason


def plan(path: Path) -> tuple[list[Change], list[str]]:
    all_entries = entries(path)
    complete = Counter()
    by_object_type: dict[tuple[str, str], set[tuple[str, str]]] = defaultdict(set)
    for bibl_full in all_entries:
        cls = classification(bibl_full)
        if cls.get("de") and cls.get("en"):
            pair = (cls["de"], cls["en"])
            complete[pair] += 1
            by_object_type[object_type(bibl_full)].add(pair)

    majority: dict[str, dict[str, str]] = {"de": {}, "en": {}}
    for lang, index in (("de", 0), ("en", 1)):
        counts: dict[str, Counter] = defaultdict(Counter)
        for pair, number in complete.items():
            counts[pair[index].casefold()][pair[index]] += number
        for folded, spellings in counts.items():
            majority[lang][folded] = spellings.most_common(1)[0][0]

    changes: list[Change] = []
    unresolved: list[str] = []
    for bibl_full in all_entries:
        xml_id = bibl_full.get(XML + "id") or ""
        cls = classification(bibl_full)
        if not cls:
            unresolved.append(f"{xml_id}: keine Klassifikation, kein Objekttyp zum Ableiten")
            continue
        if not cls.get("de") or not cls.get("en"):
            candidates = by_object_type.get(object_type(bibl_full), set())
            if len(candidates) == 1:
                pair = next(iter(candidates))
                changes.append(Change(
                    xml_id, "missing-language", dict(cls),
                    {"de": pair[0], "en": pair[1]},
                    f"Objekttyp {object_type(bibl_full)[0]!r}/{object_type(bibl_full)[1]!r} "
                    f"trägt im Bestand genau eine vollständige Klassifikation"))
            else:
                unresolved.append(
                    f"{xml_id}: Klassifikation {cls} unvollständig, Objekttyp "
                    f"{object_type(bibl_full)} erlaubt {len(candidates)} Paare")
            continue
        wanted = {lang: majority[lang].get(value.casefold(), value)
                  for lang, value in cls.items() if lang}
        if wanted != cls:
            changes.append(Change(xml_id, "case-variant", dict(cls), wanted,
                                  "Schreibvariante einer im Bestand etablierten Kategorie"))
    return changes, unresolved


TERM_PATTERN = '<term type="classification" xml:lang="%s">'


def rewrite(text: str, change: Change) -> str:
    start = text.index('<biblFull xml:id="%s"' % change.xml_id)
    end = text.index("</biblFull>", start)
    block = text[start:end]
    for lang in ("de", "en"):
        new = change.new[lang]
        pattern = re.compile(r'(<term type="classification" xml:lang="%s">)(.*?)(</term>)'
                             % lang, re.S)
        block, count = pattern.subn(lambda m: m.group(1) + new + m.group(3), block, count=1)
        if count:
            continue
        # Language missing: insert next to the sibling that is present, same indentation.
        other = "en" if lang == "de" else "de"
        sibling = re.search(r'([ \t]*)<term type="classification" xml:lang="%s">.*?</term>'
                            % other, block, re.S)
        if not sibling:
            raise ValueError(f"{change.xml_id}: kein classification-Term zum Anlehnen")
        indent = sibling.group(1)
        newline = "\r\n" if "\r\n" in block else "\n"
        inserted = (f'{newline}{indent}<term type="classification" xml:lang="{lang}">'
                    f"{new}</term>")
        block = block[:sibling.end()] + inserted + block[sibling.end():]
    return text[:start] + block + text[end:]


def survey() -> None:
    print("\n=== Render-Vertrag: Gruppierungsschlüssel in den gruppierten Listen")
    for path in GROUPED_LISTS:
        no_class, no_title, no_pid = [], [], []
        all_entries = entries(path)
        for bibl_full in all_entries:
            xml_id = bibl_full.get(XML + "id") or ""
            cls = classification(bibl_full)
            if not cls.get("de") or not cls.get("en"):
                no_class.append(xml_id)
            if not any(t.get("type") == "Einheitssachtitel"
                       for t in bibl_full.iter(f"{TEI}title")):
                no_title.append(xml_id)
            if not any(idno.get("type") == "PID"
                       for alt in bibl_full.iter(f"{TEI}altIdentifier")
                       for idno in alt.iter(f"{TEI}idno")):
                no_pid.append(xml_id)
        print(f"  {path.name}: {len(all_entries)} Einträge")
        print(f"    ohne vollständige Klassifikation (de+en): {len(no_class)}"
              + (f" -> {', '.join(no_class[:10])}" if no_class else ""))
        print(f"    ohne Einheitssachtitel: {len(no_title)}"
              + (f" -> {', '.join(no_title[:10])}" if no_title else ""))
        print(f"    ohne PID in altIdentifier: {len(no_pid)}"
              + (f" -> {', '.join(no_pid[:10])}{' …' if len(no_pid) > 10 else ''}"
                 if no_pid else ""))


def verify(path: Path) -> int:
    problems = 0
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        print(f"NICHT WOHLGEFORMT: {path.name}: {exc}")
        return 1
    all_entries = list(root.iter(f"{TEI}biblFull"))
    print(f"Einträge (biblFull): {len(all_entries)}")

    import subprocess
    rel = path.resolve().relative_to(REPO_ROOT).as_posix()
    result = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=REPO_ROOT,
                            capture_output=True)
    if result.returncode == 0:
        before = ET.fromstring(result.stdout.decode("utf-8"))
        before_entries = list(before.iter(f"{TEI}biblFull"))
        print(f"Einträge in HEAD: {len(before_entries)}")
        if len(before_entries) != len(all_entries):
            print("FEHLER: Eintragszahl hat sich geändert")
            problems += 1
        touched = 0
        for old, new in zip(before_entries, all_entries):
            if old.get(XML + "id") != new.get(XML + "id"):
                print(f"FEHLER: Reihenfolge verschoben bei {old.get(XML + 'id')}")
                problems += 1
                break
            old_flat = [(e.tag, e.get("type"), e.get(XML + "lang"), text_of(e))
                        for e in old.iter()]
            new_flat = [(e.tag, e.get("type"), e.get(XML + "lang"), text_of(e))
                        for e in new.iter()]
            if old_flat == new_flat:
                continue
            touched += 1
            others = [a for a in old_flat if a not in new_flat
                      and not (a[0] == f"{TEI}term" and a[1] == "classification")]
            others += [a for a in new_flat if a not in old_flat
                       and not (a[0] == f"{TEI}term" and a[1] == "classification")]
            # keywords and its ancestors change their concatenated text with the term,
            # that is the same change seen from above.
            others = [a for a in others
                      if a[0] not in (f"{TEI}keywords", f"{TEI}textClass",
                                      f"{TEI}profileDesc", f"{TEI}biblFull")]
            for entry in others:
                print(f"UNZULÄSSIGE ÄNDERUNG in {new.get(XML + 'id')}: {entry}")
                problems += 1
        print(f"Geänderte Einträge gegenüber HEAD: {touched}")
    else:
        print(f"HINWEIS: {path.name} ist in HEAD nicht vorhanden, kein Vergleich")

    incomplete = [b.get(XML + "id") for b in all_entries
                  if not classification(b).get("de") or not classification(b).get("en")]
    print(f"Einträge ohne vollständige Klassifikation: {len(incomplete)} {incomplete}")
    problems += len(incomplete)

    per_language: dict[str, Counter] = {"de": Counter(), "en": Counter()}
    for bibl_full in all_entries:
        for lang, value in classification(bibl_full).items():
            if lang:
                per_language[lang][value] += 1
    variants = []
    for lang, counts in per_language.items():
        folded: dict[str, list[str]] = defaultdict(list)
        for value in counts:
            folded[value.casefold()].append(value)
        variants += [f"{lang}: {sorted(v)}" for v in folded.values() if len(v) > 1]
    print(f"Kategorien mit Schreibvarianten: {len(variants)} {variants}")
    problems += len(variants)
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--szdess", type=Path, default=SZDESS)
    parser.add_argument("--apply", action="store_true", help="Änderungen schreiben")
    parser.add_argument("--verify", action="store_true", help="nur prüfen")
    args = parser.parse_args()

    if args.verify:
        return 1 if verify(args.szdess) else 0

    changes, unresolved = plan(args.szdess)
    for change in changes:
        print(f"{change.rule}: {change.xml_id}")
        print(f"  alt: {change.old}")
        print(f"  neu: {change.new}")
        print(f"  Regel: {change.reason}")
    print(f"\nRestliste (nicht ableitbar): {len(unresolved)}")
    for line in unresolved:
        print("  " + line)
    survey()

    if not args.apply:
        print(f"\nTrockenlauf -- {len(changes)} Änderungen geplant, nichts geschrieben. "
              f"Mit --apply anwenden.")
        return 0

    with open(args.szdess, encoding="utf-8", newline="") as handle:
        text = handle.read()
    for change in changes:
        text = rewrite(text, change)
    with open(args.szdess, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    try:
        ET.fromstring(text)
    except ET.ParseError as exc:
        print(f"FEHLER: {args.szdess.name} ist nicht wohlgeformt: {exc}", file=sys.stderr)
        return 1
    print(f"\ngeschrieben: {args.szdess.name} ({len(changes)} Einträge)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
