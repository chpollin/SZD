#!/usr/bin/env python3
"""List the persons of the index that the person search cannot find, with text candidates.

The person search of the website matches ?re ?role <o:szd.personen#SZDPER.n>. A TEI person
reference reaches that URI in two ways in szd-TORDF.xsl. A value containing "#SZDPER.n" is
passed through, and a GND value (containing "d-nb.info/gnd/") is resolved by GetPersonlist
against the person index, where it matches every person whose persName/@ref contains the
value as a substring. The transformation reads a fixed set of element paths. This script
deliberately reads more, every @ref, @key and @corresp token of every scanned file, so a person
it calls unreferenced is unreferenced under any mapping, while a person it counts as
referenced may still be missed by the mapping (see the summary for those gaps).

For every unreferenced person the element text of the scanned files is searched for the name,
so that the operator can decide where a reference is missing. Nothing in the data is changed.

Usage:

    python scripts/checkup_2026_09_index/find_unlinked_persons.py \
        --staging C:/Users/Chrisi/Documents/PROJECTS/szd/ingest_staging_2026-09-23/konvolute_neu \
        --out-dir C:/Users/Chrisi/Documents/PROJECTS/szd/checkup-2026-09

Regime: script pipeline in the shape the other scripts of this repo use, standard library
only, run with plain python.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252
    sys.stdout.reconfigure(errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA = REPO_ROOT / "data"
SZDPER_FILE = DATA / "Index" / "Person" / "SZDPER.xml"
ESSAY_LOG = Path(__file__).resolve().parent / "essay_author_log.csv"

# Object holdings only. data/Index holds no objects, the glossary no persons, data/derived is
# generated from the biography.
SCAN_DIRS = [
    "Aufsatzablage",
    "Autograph",
    "Biography",
    "Correspondence",
    "Issue",
    "Library",
    "PersonalDocument",
    "Work",
]

TEI = "{http://www.tei-c.org/ns/1.0}"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
REF_ATTRS = ("ref", "key", "corresp")

SZDPER_TOKEN = re.compile(r"#(SZDPER\.\d+[a-z]?)\b")
BARE_SZDPER = re.compile(r"^(SZDPER\.\d+[a-z]?)$")
OBJECT_ID = re.compile(r"^SZD[A-Z]+\.")
WORD = re.compile(r"\w+")

# A surname found in more text nodes than this is only reported where the forename stands near.
TOO_COMMON = 150
FORENAME_WINDOW = 60
SNIPPET = 120
MIN_VARIANT = 5
# Name parts and inline markup, through which the context of a hit climbs to the whole name.
INLINE = {"surname", "forename", "name", "persName", "roleName", "addName", "genName", "hi", "emph", "foreign", "q"}
PARTICLES = {"von", "van", "de", "der", "den", "du", "da", "di", "del", "la", "le", "zu", "y"}

CLASS_CANDIDATE = "Kandidat gefunden"
CLASS_SURNAME = "nur Nachname"
CLASS_NONE = "kein Treffer im Text"
CLASS_COMMON = "Nachname zu häufig, nicht durchsucht"
FORMER_ERROR = "früher nur durch Nummerierungsfehler verknüpft"

CSV_FIELDS = ["szdper", "name", "gnd", "klasse", "datei", "objekt", "pfad", "vorhandener_ref", "kontext"]


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def norm(text: str) -> str:
    return " ".join(text.replace("\u2019", "'").split())


@dataclass
class Person:
    pid: str
    surname: str = ""
    forename: str = ""
    name: str = ""
    gnds: list[str] = field(default_factory=list)
    variants: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        if self.name:
            return self.name
        return f"{self.surname}, {self.forename}" if self.forename else self.surname


def load_persons() -> list[Person]:
    persons = []
    for el in ET.parse(SZDPER_FILE).getroot().iter(f"{TEI}person"):
        person = Person(el.get(XML_ID, ""))
        for pn in el.findall(f"{TEI}persName"):
            if pn.get("ref"):
                person.gnds.append(pn.get("ref").strip())
            if pn.get("type"):
                continue
            person.surname = person.surname or norm(pn.findtext(f"{TEI}surname") or "")
            person.forename = person.forename or norm(pn.findtext(f"{TEI}forename") or "")
            person.name = person.name or norm(pn.findtext(f"{TEI}name") or "")
        for note in el.findall(f"{TEI}note[@type='variants']"):
            for variant in norm("".join(note.itertext())).split(";"):
                variant = variant.strip()
                if len(variant) >= MIN_VARIANT:
                    person.variants.append(variant)
        persons.append(person)
    return persons


@dataclass
class Doc:
    label: str
    konvolut: bool
    root: ET.Element
    parent: dict
    pid: str
    texts: list = field(default_factory=list)  # (owner element, normalised text)


def scan_files(staging: Path | None) -> list[tuple[Path, str, bool]]:
    files = []
    for sub in SCAN_DIRS:
        for path in sorted((DATA / sub).rglob("*.xml")):
            label = path.relative_to(REPO_ROOT).as_posix()
            files.append((path, label, "/konvolute/" in label))
    if staging:
        for path in sorted(staging.glob("*.xml")):
            files.append((path, f"staging/{staging.name}/{path.name}", True))
    return files


def load_doc(path: Path, label: str, konvolut: bool) -> Doc | None:
    root = ET.parse(path).getroot()
    if root.tag != f"{TEI}TEI":  # METS files beside the theme pages
        return None
    parent = {child: el for el in root.iter() for child in el}
    pid = next((norm(i.text or "") for i in root.iter(f"{TEI}idno") if i.get("type") == "PID"), "")
    doc = Doc(label, konvolut, root, parent, pid)
    for el in root.iter():
        if el.text and el.text.strip():
            doc.texts.append((el, norm(el.text)))
        for child in el:
            if child.tail and child.tail.strip():
                doc.texts.append((el, norm(child.tail)))
    return doc


class GndResolver:
    """GetPersonlist: index persName/@ref contains the data value (substring, no normalisation)."""

    def __init__(self, persons: list[Person]):
        self.pairs = [(gnd, p.pid) for p in persons for gnd in p.gnds]
        self.cache: dict[str, set[str]] = {}

    def resolve(self, value: str) -> set[str]:
        if value not in self.cache:
            self.cache[value] = {pid for gnd, pid in self.pairs if value in gnd}
        return self.cache[value]


def lenient(value: str) -> str:
    return value.replace("https://", "http://").rstrip("/")


def count_references(docs: list[Doc], persons: list[Person]):
    resolver = GndResolver(persons)
    lenient_resolver = GndResolver(
        [Person(p.pid, gnds=[lenient(g) for g in p.gnds]) for p in persons]
    )
    strict: dict[str, int] = defaultdict(int)
    outside_konvolut: set[str] = set()
    near_miss: dict[str, set[str]] = defaultdict(set)
    bare: list[str] = []
    ambiguous: set[str] = set()
    for doc in docs:
        for el in doc.root.iter():
            for attr in REF_ATTRS:
                for token in (el.get(attr) or "").split():
                    hit = SZDPER_TOKEN.search(token)
                    if hit:
                        ids = {hit.group(1)}
                    elif token.split("d-nb.info/gnd/", 1)[-1] and "d-nb.info/gnd/" in token:
                        ids = resolver.resolve(token)
                        if len(ids) > 1:
                            ambiguous.add(token)
                        if not ids:
                            for pid in lenient_resolver.resolve(lenient(token)):
                                near_miss[pid].add(f"{doc.label}: {token}")
                    else:
                        if BARE_SZDPER.match(token):
                            bare.append(f"{doc.label}: {local(el.tag)}/@{attr}={token}")
                        continue
                    for pid in ids:
                        strict[pid] += 1
                        if not doc.konvolut:
                            outside_konvolut.add(pid)
    return strict, outside_konvolut, near_miss, bare, ambiguous


def phrase_pattern(phrase: str) -> re.Pattern:
    body = r"\s+".join(re.escape(part) for part in norm(phrase).split())
    upper = r"\s+".join(re.escape(part.upper()) for part in norm(phrase).split())
    return re.compile(rf"(?<![\w-])(?:{body}|{upper})(?![\w-])")


def forename_patterns(forename: str) -> tuple[re.Pattern, re.Pattern] | None:
    """Full forename parts, and their initials followed by a full stop."""
    parts = [p for p in re.split(r"[\s\-]+", forename) if len(p) >= 2 and p.lower() not in PARTICLES]
    if not parts:
        return None
    full = "|".join(re.escape(p) for p in parts)
    initials = "|".join(re.escape(p[0]) + r"\." for p in parts)
    return re.compile(rf"(?<!\w)(?:{full})(?!\w)"), re.compile(rf"(?<!\w)(?:{initials})")


class TextIndex:
    def __init__(self, docs: list[Doc]):
        self.nodes = [(doc, el, text) for doc in docs for el, text in doc.texts]
        self.words: dict[str, list[int]] = defaultdict(list)
        for i, (_, _, text) in enumerate(self.nodes):
            for word in set(WORD.findall(text.casefold())):
                self.words[word].append(i)
        self.fulltext: dict[int, str] = {}

    def candidates(self, phrase: str) -> list[int]:
        words = WORD.findall(phrase.casefold())
        if not words:
            return []
        return self.words.get(max(words, key=len), [])

    def full(self, el: ET.Element) -> str:
        key = id(el)
        if key not in self.fulltext:
            self.fulltext[key] = norm(" ".join(el.itertext()))
        return self.fulltext[key]


def object_of(doc: Doc, el: ET.Element) -> ET.Element | None:
    node = el
    while node is not None:
        if OBJECT_ID.match(node.get(XML_ID, "")):
            return node
        node = doc.parent.get(node)
    return None


def describe(doc: Doc, owner: ET.Element, index: TextIndex):
    obj = object_of(doc, owner)
    object_id = obj.get(XML_ID) if obj is not None else doc.pid
    steps, node = [], owner
    while node is not None and node is not obj and len(steps) < 4:
        steps.append(local(node.tag))
        node = doc.parent.get(node)
    path = "/".join(reversed(steps))
    existing, node = "", owner
    for _ in range(3):
        if node is None or node is obj:
            break
        refs = [f"{local(node.tag)}/@{a}={node.get(a)}" for a in REF_ATTRS if node.get(a)]
        if refs:
            existing = " ".join(refs)
            break
        node = doc.parent.get(node)
    context = owner
    while local(context.tag) in INLINE:
        up = doc.parent.get(context)
        if up is None or up is obj:
            break
        context = up
    return object_id, path, existing, context


def snippet(text: str, match: re.Match) -> str:
    half = (SNIPPET - (match.end() - match.start())) // 2
    start, end = max(0, match.start() - half), min(len(text), match.end() + half)
    return ("…" if start else "") + text[start:end] + ("…" if end < len(text) else "")


@dataclass
class Hit:
    doc: Doc
    object_id: str
    path: str
    existing: str
    context: str
    kind: str


def search_person(person: Person, index: TextIndex) -> tuple[list[Hit], bool]:
    """Return the hits and whether the primary name was too common to be listed in full."""
    primary = person.name or person.surname
    searches = []
    if primary:
        searches.append((primary, "primary"))
    # A single-word variant of a person with surname and forename is no better than a surname
    # hit, and a variant with several commas is a GND qualifier chain, not a written form.
    for variant in person.variants:
        if variant.count(",") > 1:
            continue
        forms = [variant]
        if "," in variant:
            last, first = (part.strip() for part in variant.split(",", 1))
            forms.append(f"{first} {last}")
        for form in forms:
            if " " in form or person.name:
                searches.append((form, "Variante"))
    fore = forename_patterns(person.forename) if not person.name else None
    hits: dict[int, Hit] = {}
    too_common = False
    for phrase, source in searches:
        if len(phrase) < 3:
            too_common = too_common or source == "primary"
            continue
        pattern = phrase_pattern(phrase)
        nodes = [i for i in index.candidates(phrase) if pattern.search(index.nodes[i][2])]
        common = len(nodes) > TOO_COMMON
        if common and source == "primary":
            too_common = True
        elif common:
            continue
        for i in nodes:
            doc, owner, _ = index.nodes[i]
            object_id, path, existing, ctx_el = describe(doc, owner, index)
            key = id(ctx_el)
            if key in hits:
                continue
            text = index.full(ctx_el)
            matches = list(pattern.finditer(text))
            if not matches:  # the text node lies in a context that normalised differently
                text, matches = index.nodes[i][2], list(pattern.finditer(index.nodes[i][2]))
            if source == "Variante":
                kind = "Variante"
            elif person.name:
                kind = "Name"
            elif fore is None:
                kind = "nur Nachname, Vorname im Index leer"
            else:
                windows = [text[max(0, m.start() - FORENAME_WINDOW): m.end() + FORENAME_WINDOW] for m in matches]
                if any(fore[0].search(w) for w in windows):
                    kind = "Vorname in Nähe"
                elif any(fore[1].search(w) for w in windows):
                    kind = "Initiale in Nähe"
                else:
                    kind = "nur Nachname"
            if common and kind not in ("Vorname in Nähe", "Variante"):
                continue
            hits[key] = Hit(doc, object_id, path, existing, f"[{kind}] {snippet(text, matches[0])}", kind)
    return list(hits.values()), too_common


def classify(hits: list[Hit], too_common: bool) -> str:
    if any(h.kind in ("Vorname in Nähe", "Initiale in Nähe", "Name", "Variante") for h in hits):
        return CLASS_CANDIDATE
    if hits:
        return CLASS_SURNAME
    return CLASS_COMMON if too_common else CLASS_NONE


def former_error_ids() -> set[str]:
    if not ESSAY_LOG.exists():
        return set()
    with ESSAY_LOG.open(encoding="utf-8", newline="") as handle:
        return {m.group(1) for row in csv.DictReader(handle) for m in SZDPER_TOKEN.finditer(row["alte_referenz"])}


def promise(hits: list[Hit]) -> tuple[int, int]:
    strong = [h for h in hits if h.kind in ("Vorname in Nähe", "Name", "Variante")]
    return (sum(1 for h in strong if not h.existing), len(strong))


def write_summary(path: Path, results, counts, n_persons, n_files, strict, outside, near_miss, bare, ambiguous) -> None:
    zero = len(results)
    near_miss = {pid: v for pid, v in near_miss.items() if pid in {r["pid"] for r in results}}
    konvolut_only = sorted(set(strict) - outside)
    ranked = sorted(
        (r for r in results if r["klasse"].startswith(CLASS_CANDIDATE)),
        key=lambda r: (r["pid"] in near_miss, *promise(r["hits"])),
        reverse=True,
    )[:10]
    lines = [
        "# Unverknüpfte Personen, Kandidatenliste",
        "",
        "Erzeugt von `scripts/checkup_2026_09_index/find_unlinked_persons.py` im Repository SZD. "
        "Die Kandidatenliste steht in `unverknuepfte_personen_kandidaten.csv`, eine Zeile je Fundstelle.",
        "",
        "## Methode",
        "",
        "Die Personensuche findet eine Person, wenn ein Tripel auf `o:szd.personen#SZDPER.n` zeigt. "
        "In `szd-TORDF.xsl` entsteht ein solches Tripel aus einem Wert mit `#SZDPER.n` oder aus einer GND, "
        "die `GetPersonlist` im Personenindex nachschlägt. Dieser Abgleich prüft, ob `persName/@ref` des "
        "Index den Wert als Teilzeichenkette enthält, ohne http und https anzugleichen. Gezählt wurde "
        "bewusst weiter als die Transformation liest, nämlich jedes Token in `@ref`, `@key` und `@corresp` "
        f"aller {n_files} durchsuchten TEI-Dateien (Bestände, Korrespondenz mit Konvoluten, Biographie, "
        "Themenseiten, Aufsatzablage und die neuen Konvolute aus dem Staging-Paket, ohne `data/Index/`). "
        "Eine hier als unverknüpft geführte Person ist deshalb unter jeder Abbildung unverknüpft.",
        "",
        "Für jede unverknüpfte Person wurde der Elementtext (nicht die Attribute) nach dem Nachnamen "
        "beziehungsweise dem Einzelnamen als ganzem Wort durchsucht, in Schreibung des Index oder in "
        f"Versalien, dazu nach Namensvarianten ab {MIN_VARIANT} Zeichen, auch in umgestellter Form "
        f"Vorname Nachname. Ein Vorname oder seine Initiale im Abstand bis {FORENAME_WINDOW} Zeichen "
        "innerhalb desselben Elements (samt umschließendem Namenselement) zählt als Vornamenstreffer. "
        f"Nachnamen in mehr als {TOO_COMMON} Textknoten werden nur mit ausgeschriebenem Vornamen "
        "gelistet. Die Rangfolge der Kandidaten zählt Fundstellen mit ausgeschriebenem Vornamen, "
        "Einzelnamen oder Variante ohne vorhandenen Verweis.",
        "",
        "## Ergebnis",
        "",
        f"- Personen im Index: {n_persons}",
        f"- ohne Referenz, also ohne Treffer in der Personensuche: {zero}",
    ]
    for klasse in (CLASS_CANDIDATE, CLASS_SURNAME, CLASS_NONE, CLASS_COMMON):
        lines.append(f"  - {klasse}: {counts.get(klasse, 0)}")
    lines.append(f"- davon {FORMER_ERROR}: {counts.get(FORMER_ERROR, 0)}")
    lines += ["", "## Die zehn aussichtsreichsten Kandidaten", ""]
    for r in ranked:
        free, strong = promise(r["hits"])
        extra = ", GND im Bestand nur mit abweichender Schreibung" if r["pid"] in near_miss else ""
        strong_hits = [h for h in r["hits"] if h.kind in ("Vorname in Nähe", "Name", "Variante")]
        first = next((h for h in strong_hits if not h.existing), (strong_hits or r["hits"])[0])
        lines.append(
            f"1. {r['pid']} {r['label']}: {strong} Fundstellen mit ausgeschriebenem Vor- oder Einzelnamen oder Variante, "
            f"{free} davon ohne vorhandenen Verweis{extra}, etwa {first.doc.label} {first.object_id}"
        )
    lines += ["", "## Grenzen", ""]
    lines.append(
        "- Namen in abweichender Schreibung, Flexion oder Transliteration und mehrteilige Nachnamen, "
        "die im Text verkürzt stehen, bleiben ohne Treffer. Die Klasse kein Treffer im Text heißt "
        "deshalb nicht, dass die Person im Bestand fehlt."
    )
    lines.append(
        "- Ein Nachnamenstreffer kann eine andere Person gleichen Namens meinen, die Spalte "
        "`vorhandener_ref` zeigt, ob die Fundstelle schon auf jemanden verweist."
    )
    lines.append(
        "- Weil jedes Referenztoken zählt, gelten auch Personen als verknüpft, deren Verweis die "
        "Transformation nicht liest, etwa ein zweites Token einer Liste in `GetPersonlist`, das nur "
        "das erste Token auswertet, oder ein Verweis außerhalb der dort gelesenen Pfade."
    )
    if konvolut_only:
        lines.append(
            f"- {len(konvolut_only)} Personen sind nur in Konvolutdateien verknüpft. Die Stücke eines "
            "Konvoluts landen im Graphen `o:szd.korrespondenzen.<name>`, die Personensuche liest aber nur "
            "`FROM <o:szd.korrespondenzen>`. Ob diese Personen online gefunden werden, ist ungeprüft."
        )
    if near_miss:
        pids = ", ".join(sorted(near_miss, key=lambda p: int(p.split(".")[1])))
        lines.append(
            "- Bei folgenden unverknüpften Personen steht ihre GND im Bestand, aber in einer Schreibung, "
            f"die der Teilzeichenkettenabgleich verfehlt (https oder Schrägstrich am Ende): {pids}"
        )
    if ambiguous:
        lines.append(
            f"- {len(ambiguous)} GND-Werte im Bestand treffen mehrere Indexeinträge, weil der Index dieselbe "
            "GND mehrfach vergibt oder der Teilzeichenkettenabgleich greift. Jeder dieser Einträge gilt "
            "dann als verknüpft."
        )
    if bare:
        lines.append(
            f"- {len(bare)} Verweise tragen `SZDPER.n` ohne `#` und wurden nicht gezählt, "
            "weil `GetPersonlist` sie verwirft."
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--staging", type=Path, help="folder with not yet ingested bundle TEI files")
    parser.add_argument("--out-dir", type=Path, required=True, help="archive-internal output folder")
    args = parser.parse_args()

    persons = load_persons()
    docs = [d for d in (load_doc(*f) for f in scan_files(args.staging)) if d is not None]
    strict, outside, near_miss, bare, ambiguous = count_references(docs, persons)
    index = TextIndex(docs)
    former = former_error_ids()

    results, counts = [], defaultdict(int)
    for person in persons:
        if person.pid in strict:
            continue
        hits, too_common = search_person(person, index)
        klasse = classify(hits, too_common)
        counts[klasse] += 1
        if person.pid in former:
            klasse = f"{klasse}; {FORMER_ERROR}"
            counts[FORMER_ERROR] += 1
        results.append({"pid": person.pid, "label": person.label, "gnd": " ".join(person.gnds),
                        "klasse": klasse, "hits": hits})

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = args.out_dir / "unverknuepfte_personen_kandidaten.csv"
    with out_csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(CSV_FIELDS)
        for r in results:
            base = [r["pid"], r["label"], r["gnd"], r["klasse"]]
            if not r["hits"]:
                writer.writerow(base + ["", "", "", "", ""])
            for h in r["hits"]:
                writer.writerow(base + [h.doc.label, h.object_id, h.path, h.existing, h.context])
    write_summary(args.out_dir / "unverknuepfte_personen_zusammenfassung.md", results, counts,
                  len(persons), len(docs), strict, outside, near_miss, bare, ambiguous)

    print(f"{len(docs)} TEI files, {len(persons)} persons, {len(results)} without reference")
    for klasse, n in sorted(counts.items()):
        print(f"  {klasse}: {n}")
    print(f"wrote {out_csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
