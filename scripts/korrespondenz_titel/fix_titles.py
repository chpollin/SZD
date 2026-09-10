#!/usr/bin/env python3
"""Normalise the entry titles of the correspondence konvolut objects
(data/Correspondence/konvolute/*.xml) to the title pattern that the majority of the
entries in the same files already use.

Two title defects are repaired, both of them machine-made leftovers of earlier imports:

1. "machine-date" titles -- German and English title are identical and carry an ISO date
   and/or the archival signature in the title text
   ("Walter Bauer an Stefan Zweig, 1933-01-07 | SZ-SAM/AK.284").
2. "mangled-partner" titles -- the German title carries a raw
   "Nachname, Vorname; Nachname, Vorname" cell instead of the resolved partner names
   ("Brief von Lotte Zweig an Hannah; Altmann, Manfred Altmann [...]").

Both are rebuilt from correspDesc/correspAction and the physical extent, which is the
same source the (already correct) English titles of the majority were generated from.
A --verify run proves that claim against the untouched corpus.

Where a machine-date title carries an ISO year that the sent date's @when contradicts
only in the century (@when 2021-02-20 vs. title 1921-02-20, the two-digit year of the
source having been expanded into the 2000s), @when is corrected from the title before the
date is dropped from the title text, so no information is lost. Every other date
divergence is reported, not changed.

Serialisation is byte-preserving: only the matched title text and the affected @when
attribute values are replaced in the file text, so indentation, attribute order, XML
declaration (several files have none) and line endings stay exactly as they are.

Default behaviour is a dry run. Pass --apply to write.
"""
from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252
    sys.stdout.reconfigure(errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]
KONVOLUTE = REPO_ROOT / "data" / "Correspondence" / "konvolute"

TEI = "{http://www.tei-c.org/ns/1.0}"
XML = "{http://www.w3.org/XML/1998/namespace}"

# Document type of the entry title, keyed by the leading noun of the German extent.
# Derived from the corpus, not invented: every value below is attested in title/extent
# pairs of the already correct entries.
DOC_TYPES = {
    "Brief": ("Brief", "Letter"),
    "Brieffragment": ("Brieffragment", "Letter"),
    "Ansichtspostkarte": ("Ansichtspostkarte", "Picture postcard"),
    "Postkarte": ("Postkarte", "Postcard"),
    "Telegramm": ("Telegramm", "Telegram"),
    "Kuvert": ("Kuvert", "Envelope"),
}
DOC_DEFAULT = ("Brief", "Letter")

MONTHS_DE = ["Januar", "Februar", "März", "April", "Mai", "Juni",
             "Juli", "August", "September", "Oktober", "November", "Dezember"]

# persName/name values that are a bilingual pair rather than a name, resolved per title
# language. Declared explicitly instead of splitting any "/" so nothing is guessed.
BILINGUAL_NAMES = {"Unbekannt/Unidentified": ("Unbekannt", "Unidentified")}

# Titles in the shape the majority uses; used by --verify and by the guard below.
CANONICAL_DE = re.compile(r"^(?:%s) von .+ an .+?(?: \[[^\]]+\])?$" % "|".join(DOC_TYPES))
CANONICAL_EN = re.compile(r"^(?:%s) from .+ to .+?(?:, .+)?$"
                          % "|".join(sorted({en for _, en in DOC_TYPES.values()})))

HAS_ISO = re.compile(r"\d{4}-\d{2}")
HAS_SIGNATURE = re.compile(r"SZ-[A-Z]")
TITLE_ISO = re.compile(r"\b(\d{4}(?:-\d{2}){0,2})\b")
MANGLED_PARTNER = re.compile(r"(?: an |^)(?:[^\[]*;|[^\[]*,\s)")

# Stefan Zweig died in 1942; nothing in this corpus can carry a later date. Used only to
# recognise the century defect, never to invent a date.
LAST_PLAUSIBLE_YEAR = 1942


def local(tag: str) -> str:
    return tag.split("}")[-1]


def text_of(elem: ET.Element) -> str:
    return re.sub(r"\s+", " ", "".join(elem.itertext())).strip()


def escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;")


def partner_names(corresp_desc: ET.Element, action: str) -> list[str]:
    """Names of one correspAction side, rendered as the titles render them.

    persName with forename/surname -> "Vorname Nachname"; persName carrying a bare
    <name> or plain text -> that text; orgName only when the action has no person.
    Several correspAction elements of the same @type are one list of partners.
    """
    names: list[str] = []
    for act in corresp_desc.findall(f"{TEI}correspAction"):
        if act.get("type") != action:
            continue
        side: list[str] = []
        for child in act:
            if child.tag != f"{TEI}persName":
                continue
            forename = child.find(f"{TEI}forename")
            surname = child.find(f"{TEI}surname")
            name = child.find(f"{TEI}name")
            if forename is not None or surname is not None:
                parts = [text_of(e) for e in (forename, surname) if e is not None]
                side.append(" ".join(p for p in parts if p))
            elif name is not None:
                side.append(text_of(name))
            else:
                side.append(text_of(child))
        if not side:
            side = [text_of(c) for c in act if c.tag == f"{TEI}orgName"]
        names.extend(n for n in side if n)
    return names


def sent_date(corresp_desc: ET.Element) -> tuple[str, str, list[ET.Element]]:
    """(@when, displayed text, all date elements) of the sending action.

    The German date element is the single source for both titles; several entries carry a
    less precise or missing @when on the English one.
    """
    for act in corresp_desc.findall(f"{TEI}correspAction"):
        if act.get("type") != "sent":
            continue
        dates = act.findall(f"{TEI}date")
        if not dates:
            return "", "", []
        german = [d for d in dates if d.get(XML + "lang") == "de"] or dates
        return german[0].get("when") or "", text_of(german[0]), dates
    return "", "", []


def extent_noun(bibl_full: ET.Element) -> str:
    for span in bibl_full.iter(f"{TEI}span"):
        if span.get(XML + "lang") == "de":
            return re.sub(r"^\d+\s+", "", text_of(span).split(",")[0].strip())
    return ""


def german_date(when: str) -> str:
    parts = when.split("-")
    if len(parts) == 3:
        return f"{int(parts[2])}. {MONTHS_DE[int(parts[1]) - 1]} {parts[0]}"
    if len(parts) == 2:
        return f"{MONTHS_DE[int(parts[1]) - 1]} {parts[0]}"
    return parts[0]


def build_titles(bibl_full: ET.Element) -> tuple[str, str, str, list[str], list[str]]:
    """Canonical (de, en) title plus the @when and both partner lists of one entry."""
    corresp_desc = bibl_full.find(f".//{TEI}correspDesc")
    if corresp_desc is None:
        return "", "", "", [], []
    senders = partner_names(corresp_desc, "sent")
    recipients = partner_names(corresp_desc, "received")
    when, when_text, _ = sent_date(corresp_desc)
    doc_de, doc_en = DOC_TYPES.get(extent_noun(bibl_full), DOC_DEFAULT)

    def render(names: list[str], index: int) -> list[str]:
        return [BILINGUAL_NAMES.get(n, (n, n))[index] for n in names]

    title_de = (f"{doc_de} von {' und '.join(render(senders, 0))}"
                f" an {' und '.join(render(recipients, 0))}")
    title_en = (f"{doc_en} from {' and '.join(render(senders, 1))}"
                f" to {' and '.join(render(recipients, 1))}")
    # The German title takes the date only from @when, rendered long; the English title
    # takes the ISO value, or the displayed wording when the entry has no @when at all
    # ("Letter from Friderike Zweig to Stefan Zweig, Freitag"). Both as attested.
    if when:
        title_de += f" [{german_date(when)}]"
        title_en += f", {when}"
    elif when_text:
        title_en += f", {when_text}"
    return title_de, title_en, when, senders, recipients


def century_fix(title_iso: str, when: str) -> str:
    """Corrected @when when the title's ISO date proves a wrong century, else ''."""
    if not title_iso or not when:
        return ""
    try:
        when_year = int(when[:4])
    except ValueError:
        return ""
    if when_year <= LAST_PLAUSIBLE_YEAR:
        return ""
    if title_iso[2:4] != when[2:4]:
        return ""
    if len(title_iso) > 4 and title_iso[4:] != when[4:len(title_iso)]:
        return ""
    return title_iso[:4] + when[4:]


class Case:
    """One entry that a rule applies to, plus the reason it may be skipped."""

    def __init__(self, path: Path, xml_id: str, rule: str):
        self.path = path
        self.xml_id = xml_id
        self.rule = rule
        self.old_de = ""
        self.old_en = ""
        self.new_de = ""
        self.new_en = ""
        self.when_old = ""
        self.when_new = ""
        self.skip = ""


def collect(paths: list[Path]) -> list[Case]:
    cases: list[Case] = []
    for path in paths:
        root = ET.parse(path).getroot()
        for bibl_full in root.iter(f"{TEI}biblFull"):
            xml_id = bibl_full.get(XML + "id") or ""
            titles = {t.get(XML + "lang"): text_of(t)
                      for t in bibl_full.iter(f"{TEI}title")}
            old_de, old_en = titles.get("de", ""), titles.get("en", "")
            machine_date = (old_de == old_en
                            and bool(HAS_ISO.search(old_de) or HAS_SIGNATURE.search(old_de)))
            mangled = (bool(CANONICAL_DE.match(re.sub(r";", "", old_de)) or old_de.startswith(
                tuple(f"{d} von " for d in DOC_TYPES)))
                and bool(MANGLED_PARTNER.search(old_de.split(" an ", 1)[-1])
                         or ";" in old_de.split(" an ", 1)[-1]))
            if not machine_date and not mangled:
                continue
            case = Case(path, xml_id, "machine-date" if machine_date else "mangled-partner")
            case.old_de, case.old_en = old_de, old_en
            new_de, new_en, when, senders, recipients = build_titles(bibl_full)
            case.new_de, case.new_en, case.when_old = new_de, new_en, when

            if not senders or not recipients:
                case.skip = "correspAction ohne Namen (Sender oder Empfänger leer)"
            elif machine_date:
                match = TITLE_ISO.search(old_de)
                title_iso = match.group(1) if match else ""
                if not title_iso and when:
                    case.skip = ("Titel ohne Datum, date/@when aber gesetzt und "
                                 "unplausibel; Jahrhundert nicht aus dem Eintrag ableitbar"
                                 if int(when[:4]) > LAST_PLAUSIBLE_YEAR else "")
                elif title_iso and when and title_iso != when[:len(title_iso)]:
                    fixed = century_fix(title_iso, when)
                    if fixed:
                        case.when_new = fixed
                        case.new_de = case.new_de.replace(german_date(when), german_date(fixed))
                        case.new_en = case.new_en.replace(when, fixed)
                    else:
                        case.skip = (f"Titeldatum {title_iso} und date/@when {when} "
                                     f"widersprechen sich nicht nur im Jahrhundert")
            if not case.skip and case.new_de == old_de and case.new_en == old_en:
                continue
            # Guard: never overwrite an already canonical German title whose partner names
            # differ from correspDesc -- that is the editorial maiden-name variant
            # ("Lotte Altmann" for letters before the 1939 marriage), not a defect.
            if not case.skip and CANONICAL_DE.match(old_de) and ";" not in old_de \
                    and ", " not in old_de.split(" an ", 1)[-1]:
                case.skip = "Titel bereits in Zielform, abweichende Namensform ist redaktionell"
            cases.append(case)
    return cases


BIBL_FULL = re.compile(r'<biblFull xml:id="([^"]+)"')


def block_span(text: str, xml_id: str) -> tuple[int, int]:
    match = re.search(r'<biblFull xml:id="%s"' % re.escape(xml_id), text)
    if not match:
        raise KeyError(xml_id)
    end = text.index("</biblFull>", match.start())
    return match.start(), end


def rewrite(text: str, case: Case) -> str:
    start, end = block_span(text, case.xml_id)
    block = text[start:end]
    for lang, new in (("de", case.new_de), ("en", case.new_en)):
        pattern = re.compile(r'(<title xml:lang="%s">)(.*?)(</title>)' % lang, re.S)
        block, count = pattern.subn(lambda m: m.group(1) + escape(new) + m.group(3),
                                    block, count=1)
        if count != 1:
            raise ValueError(f"{case.xml_id}: title[@xml:lang={lang}] nicht eindeutig gefunden")
    if case.when_new:
        sent = re.search(r'<correspAction type="sent">.*?</correspAction>', block, re.S)
        if not sent:
            raise ValueError(f"{case.xml_id}: correspAction[@type=sent] nicht gefunden")
        patched = re.sub(r'(<date[^>]*?)when="%s"' % re.escape(case.when_old),
                         lambda m: m.group(1) + 'when="%s"' % case.when_new, sent.group(0))
        block = block[:sent.start()] + patched + block[sent.end():]
    return text[:start] + block + text[end:]


def report(cases: list[Case]) -> None:
    changed = [c for c in cases if not c.skip]
    skipped = [c for c in cases if c.skip]
    for rule in ("machine-date", "mangled-partner"):
        group = [c for c in changed if c.rule == rule]
        print(f"\n=== {rule}: {len(group)} Einträge")
        for case in group:
            print(f"  {case.xml_id}")
            print(f"    de  alt: {case.old_de}")
            print(f"    de  neu: {case.new_de}")
            if case.old_en != case.new_en:
                print(f"    en  alt: {case.old_en}")
                print(f"    en  neu: {case.new_en}")
            if case.when_new:
                print(f"    @when  : {case.when_old} -> {case.when_new}")
    print(f"\n=== Restliste (nicht geändert): {len(skipped)} Einträge")
    for case in skipped:
        print(f"  {case.xml_id} | {case.old_de}")
        print(f"    Grund: {case.skip}")
    print(f"\nGeändert: {len(changed)}  Restliste: {len(skipped)}")


# Entries the rules deliberately leave alone; the README says why. A leftover outside
# this set makes --verify fail.
KNOWN_UNRESOLVED = {
    "SZDKOR.altmann-hannah.102", "SZDKOR.altmann-manfred.64",
    "SZDKOR.unidentified.039", "SZDKOR.unidentified.040", "SZDKOR.unidentified.041",
}

# Only these may differ between HEAD and the working tree.
ALLOWED_TEXT_CHANGE = f"{TEI}title"
ALLOWED_ATTR_CHANGE = (f"{TEI}date", "when")


def flatten(elem: ET.Element, path: str = "") -> list[tuple[str, str, str, dict]]:
    """(path, tag, own text, attributes) of every element, in document order.

    Own text only, so a change deep inside a subtree is reported at the element that
    actually carries it and not again at each of its ancestors.
    """
    here = f"{path}/{local(elem.tag)}"
    own = (elem.text or "") + "".join(child.tail or "" for child in elem)
    out = [(here, elem.tag, re.sub(r"\s+", " ", own).strip(), dict(elem.attrib))]
    counts: dict[str, int] = {}
    for child in elem:
        counts[child.tag] = counts.get(child.tag, 0) + 1
        out.extend(flatten(child, f"{here}[{counts[child.tag]}]"))
    return out


def structural_diff(before: str, after: str) -> list[str]:
    """Differences between two revisions of one file, beyond the permitted ones."""
    old, new = flatten(ET.fromstring(before)), flatten(ET.fromstring(after))
    if len(old) != len(new):
        return [f"Elementanzahl {len(old)} -> {len(new)}"]
    problems: list[str] = []
    for (path_o, tag_o, text_o, attr_o), (path_n, tag_n, text_n, attr_n) in zip(old, new):
        if (path_o, tag_o) != (path_n, tag_n):
            problems.append(f"Struktur verschoben: {path_o} -> {path_n}")
            continue
        if text_o != text_n and tag_o != ALLOWED_TEXT_CHANGE:
            problems.append(f"Text geändert in {path_o}: {text_o!r} -> {text_n!r}")
        for key in set(attr_o) | set(attr_n):
            if attr_o.get(key) == attr_n.get(key):
                continue
            if (tag_o, key) != ALLOWED_ATTR_CHANGE:
                problems.append(f"Attribut geändert: {path_o}/@{key} "
                                f"{attr_o.get(key)!r} -> {attr_n.get(key)!r}")
    return problems


def head_revision(path: Path) -> str | None:
    import subprocess
    rel = path.resolve().relative_to(REPO_ROOT).as_posix()
    result = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=REPO_ROOT,
                            capture_output=True)
    return result.stdout.decode("utf-8") if result.returncode == 0 else None


def verify(paths: list[Path]) -> int:
    """Re-derive every canonical title in the corpus and check the invariants."""
    problems = 0
    reproduced = total = 0
    leftovers: list[tuple[str, str]] = []
    entries_before = entries_after = 0
    for path in paths:
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as exc:
            print(f"NICHT WOHLGEFORMT: {path.name}: {exc}")
            problems += 1
            continue
        entries_after += len(list(root.iter(f"{TEI}biblFull")))
        before = head_revision(path)
        if before is None:
            print(f"HINWEIS: {path.name} ist in HEAD nicht vorhanden, kein Strukturvergleich")
        else:
            entries_before += len(list(ET.fromstring(before).iter(f"{TEI}biblFull")))
            for line in structural_diff(before, path.read_text(encoding="utf-8")):
                print(f"UNZULÄSSIGE ÄNDERUNG in {path.name}: {line}")
                problems += 1
        for bibl_full in root.iter(f"{TEI}biblFull"):
            xml_id = bibl_full.get(XML + "id") or ""
            titles = {t.get(XML + "lang"): text_of(t)
                      for t in bibl_full.iter(f"{TEI}title")}
            old_de, old_en = titles.get("de", ""), titles.get("en", "")
            if old_de == old_en and (HAS_ISO.search(old_de) or HAS_SIGNATURE.search(old_de)):
                leftovers.append((xml_id, f"machine-date: {xml_id} | {old_de}"))
            if ";" in old_de.split(" an ", 1)[-1] and CANONICAL_DE.match(old_de.replace(";", "")):
                leftovers.append((xml_id, f"mangled-partner: {xml_id} | {old_de}"))
            if CANONICAL_DE.match(old_de) and CANONICAL_EN.match(old_en):
                total += 1
                new_de, new_en, _, _, _ = build_titles(bibl_full)
                if (new_de, new_en) == (old_de, old_en):
                    reproduced += 1
    print(f"Einträge (biblFull): HEAD {entries_before}, Arbeitsstand {entries_after}")
    if entries_before != entries_after:
        problems += 1
        print("FEHLER: Eintragszahl hat sich geändert")
    print(f"Alle Dateien wohlgeformt: {'ja' if problems == 0 else 'siehe oben'}")
    print(f"Titelregel reproduziert {reproduced} von {total} Titeln in Zielform "
          f"(Abweichungen sind redaktionelle Namensvarianten, siehe README).")
    unexpected = [line for xml_id, line in leftovers if xml_id not in KNOWN_UNRESOLVED]
    print(f"Verbliebene Altmuster: {len(leftovers)} "
          f"(davon dokumentierte Restliste: {len(leftovers) - len(unexpected)})")
    for _, line in leftovers:
        print("  " + line)
    problems += len(unexpected)
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--konvolute", type=Path, default=KONVOLUTE,
                        help="Ordner mit den Konvolut-Dateien")
    parser.add_argument("--apply", action="store_true", help="Änderungen schreiben")
    parser.add_argument("--verify", action="store_true",
                        help="nur prüfen: Altmuster weg, Regel reproduziert den Bestand")
    args = parser.parse_args()

    paths = sorted(args.konvolute.glob("*.xml"))
    if not paths:
        print(f"Keine Dateien in {args.konvolute}", file=sys.stderr)
        return 2

    if args.verify:
        return 1 if verify(paths) else 0

    cases = collect(paths)
    report(cases)
    if not args.apply:
        print("\nTrockenlauf -- nichts geschrieben. Mit --apply anwenden.")
        return 0

    by_file: dict[Path, list[Case]] = {}
    for case in cases:
        if not case.skip:
            by_file.setdefault(case.path, []).append(case)
    for path, file_cases in by_file.items():
        text = path.read_text(encoding="utf-8")
        for case in file_cases:
            text = rewrite(text, case)
        path.write_text(text, encoding="utf-8", newline="")
        try:
            ET.fromstring(text)
        except ET.ParseError as exc:
            print(f"FEHLER: {path.name} ist nach dem Schreiben nicht wohlgeformt: {exc}",
                  file=sys.stderr)
            return 1
        print(f"geschrieben: {path.name} ({len(file_cases)} Einträge)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
