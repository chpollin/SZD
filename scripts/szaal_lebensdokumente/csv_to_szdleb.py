#!/usr/bin/env python3
"""Generate TEI <biblFull> entries for the SZ-AAL Lebensdokumente from a CSV export
and insert them into data/PersonalDocument/SZDLEB.xml.

The script is parametric: all paths, the Gesamttitel and the starting xml:id can be
overridden on the command line. GND -> SZDPER resolution is read live from the person
authority file, so no person ids are hard-coded.

Default behaviour is a dry run (prints the generated XML block and a report). Pass
--apply to actually write the entries into the SZDLEB file (before </listBibl>).
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# --- column indices (0-based) of the CSV export ---------------------------------
C_SIG, C_KAT = 0, 1
C_AUTHOR, C_AUTHOR_GND = 2, 3
C_HAND = 4
C_CONTRIB, C_CONTRIB_GND = 5, 6
C_AFFECTED, C_AFFECTED_GND = 7, 8
C_TIT_ORIG, C_TIT_DE, C_TIT_EN = 9, 10, 11      # "Titel (fingiert)"=assigned de, "Titel (assigned)"=assigned en
C_INSCRIPTION = 12
C_EXTENT_DE, C_EXTENT_EN = 13, 14
C_FOLIATION = 15
C_ENCL_DE, C_ENCL_EN = 16, 17
C_ADD_DE, C_ADD_EN = 18, 19
C_DATE_ORIG, C_DATE_INFERRED, C_DATE_NORM = 20, 21, 22
C_PLACE = 23
C_LANG = 24
C_INCIPIT = 25
C_MAT_DE, C_MAT_EN = 26, 27                      # Beschreibstoff / Writing Material
C_INSTR_DE, C_INSTR_EN = 28, 29                  # Schreibstoff / Writing Instrument
C_FORMAT = 30                                    # Maße
C_REPO_GND = 31
C_PROVENANCE = 32
C_ACQ_DE, C_ACQ_EN = 33, 34
C_NOTE_DE, C_NOTE_EN = 35, 36
C_REMARK = 37

# --- controlled lookups ---------------------------------------------------------
CLASS_EN = {
    "Rechtsdokumente": "Legal Papers",
    "Finanzen": "Finances",
    "Adressbücher": "Address books",
}
PROV_EN = {"Erben Stefan Zweigs": "Heirs of Stefan Zweig"}
REPO = {"1047605287": ("Österreich", "Salzburg", "Literaturarchiv Salzburg")}
LANG_MAP = {"GER": ("ger", "Deutsch"), "ENG": ("eng", "Englisch"), "FRE": ("fre", "Französisch")}
INSCR_LANG = {"ger": "de", "eng": "en", "fre": "fr"}
# Heuristic to tell corporate bodies apart from persons (persons with a SZDPER entry
# are always treated as persons regardless of these keywords).
ORG_KEYWORDS = ["Bank", "Press", "Botschaft", "Standesamt", "Home Office", "Notare",
                "Stiftung", "Gesellschaft", "Verlag", "& Co", "Reich", "Office",
                "Passtelle", "Telegraph"]

NS = "http://www.tei-c.org/ns/1.0"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def collapse_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def gnd_id(raw: str) -> str:
    m = re.search(r"gnd/([\w-]+)", raw or "")
    return m.group(1) if m else ""


def load_gnd2szdper(path: Path) -> dict[str, str]:
    """Map every GND id occurring inside a <person> to that person's xml:id."""
    text = path.read_text(encoding="utf-8")
    mapping: dict[str, str] = {}
    for m in re.finditer(r'<person\b[^>]*\bxml:id="(SZDPER\.\d+)"[^>]*>(.*?)</person>',
                          text, re.DOTALL):
        pid, body = m.group(1), m.group(2)
        for g in re.findall(r"gnd/([\w-]+)", body):
            mapping.setdefault(g, pid)
    return mapping


def split_name(name: str):
    parts = [p.strip() for p in name.split(",")]
    if len(parts) == 2 and all(parts):
        return parts[0], parts[1]
    return None, None


def is_org(name: str, gid: str, gnd2szdper: dict) -> bool:
    if gid and gid in gnd2szdper:
        return False
    low = name.lower()
    return any(kw.lower() in low for kw in ORG_KEYWORDS)


def parse_actors(names: str, gnds: str):
    name_list = [n.strip() for n in names.split(";")] if names.strip() else []
    gnd_list = [gnd_id(g) for g in gnds.split(";")] if gnds.strip() else []
    out = []
    for i, name in enumerate(name_list):
        if not name:
            continue
        gid = gnd_list[i] if i < len(gnd_list) else ""
        out.append((name, gid))
    return out


def actor_xml(tag: str, open_attrs: str, name: str, gid: str, gnd2szdper: dict, report: dict):
    gnd_url = f"http://d-nb.info/gnd/{gid}" if gid else None
    if is_org(name, gid, gnd2szdper):
        report["orgs"].add(name)
        inner = "<orgName" + (f' ref="{gnd_url}"' if gnd_url else "") + f">{esc(name)}</orgName>"
        ref_attr = ""
    else:
        szdper = gnd2szdper.get(gid) if gid else None
        if not szdper:
            report["persons_without_ref"].add(name)
        sn, fn = split_name(name)
        if sn is not None:
            pn_inner = f"<surname>{esc(sn)}</surname><forename>{esc(fn)}</forename>"
        else:
            pn_inner = esc(name)
            report["persons_unstructured"].add(name)
        inner = "<persName" + (f' ref="{gnd_url}"' if gnd_url else "") + f">{pn_inner}</persName>"
        ref_attr = f' ref="#{szdper}"' if szdper else ""
    return f"<{tag}{open_attrs}{ref_attr}>{inner}</{tag}>"


def split_extent(s: str):
    s = collapse_ws(s)
    m = re.match(r"^\s*\d+\s+(.+?)(?:,\s*(.*))?$", s)
    if m:
        return m.group(1).strip(), (m.group(2) or "").strip()
    return "", s


def date_text(orig: str, inferred: str, norm: str) -> str:
    orig, inferred, norm = collapse_ws(orig), collapse_ws(inferred), collapse_ws(norm)
    if orig:
        return orig
    if inferred:
        return f"[{inferred}]"
    return norm


def iso_when(norm: str):
    norm = collapse_ws(norm)
    return norm if re.match(r"^\d{4}(-\d{2}(-\d{2})?)?$", norm) else ""


def build_entry(row, xmlid: str, gnd2szdper: dict, gesamttitel: str, report: dict) -> str:
    def g(i):
        return row[i].strip() if i < len(row) and row[i] else ""

    L: list[str] = []
    def add(lvl, s):
        L.append("  " * lvl + s)

    add(4, f'<biblFull xml:id="{xmlid}">')
    add(5, "<fileDesc>")
    # --- titleStmt ---
    add(6, "<titleStmt>")
    if g(C_TIT_ORIG):
        add(7, f'<title ana="original">{esc(collapse_ws(g(C_TIT_ORIG)))}</title>')
    if g(C_TIT_DE):
        add(7, f'<title ana="assigned" xml:lang="de">{esc(collapse_ws(g(C_TIT_DE)))}</title>')
    if g(C_TIT_EN):
        add(7, f'<title ana="assigned" xml:lang="en">{esc(collapse_ws(g(C_TIT_EN)))}</title>')
    add(7, f'<title type="Gesamttitel">{esc(gesamttitel)}</title>')
    for name, gid in parse_actors(g(C_AUTHOR), g(C_AUTHOR_GND)):
        add(7, actor_xml("author", "", name, gid, gnd2szdper, report))
    for name, gid in parse_actors(g(C_CONTRIB), g(C_CONTRIB_GND)):
        add(7, actor_xml("editor", ' role="contributor"', name, gid, gnd2szdper, report))
    add(6, "</titleStmt>")
    add(6, "<publicationStmt>")
    add(7, "<ab>Archivmaterial</ab>")
    add(6, "</publicationStmt>")
    # --- notesStmt ---
    if g(C_NOTE_DE) or g(C_NOTE_EN):
        add(6, "<notesStmt>")
        if g(C_NOTE_DE):
            add(7, f'<note xml:lang="de">{esc(collapse_ws(g(C_NOTE_DE)))}</note>')
        if g(C_NOTE_EN):
            add(7, f'<note xml:lang="en">{esc(collapse_ws(g(C_NOTE_EN)))}</note>')
        add(6, "</notesStmt>")
    # --- sourceDesc / msDesc ---
    add(6, "<sourceDesc>")
    add(7, "<msDesc>")
    add(8, "<msIdentifier>")
    country, settlement, repo_name = REPO.get(gnd_id(g(C_REPO_GND)), ("", "", ""))
    if country:
        add(9, f"<country>{esc(country)}</country>")
    if settlement:
        add(9, f"<settlement>{esc(settlement)}</settlement>")
    if g(C_REPO_GND):
        add(9, f'<repository ref="http://d-nb.info/gnd/{gnd_id(g(C_REPO_GND))}">{esc(repo_name)}</repository>')
    add(9, f'<idno type="signature">{esc(g(C_SIG))}</idno>')
    add(9, "<!-- PID (o:szd.*) wird beim GAMS-Ingest vergeben -->")
    add(8, "</msIdentifier>")
    # msContents
    langs = []
    for code in re.split(r"[;,]", g(C_LANG)):
        code = code.strip().upper()
        if code in LANG_MAP:
            langs.append(LANG_MAP[code])
    has_msitem = bool(g(C_INSCRIPTION) or g(C_INCIPIT))
    if langs or has_msitem:
        add(8, "<msContents>")
        if langs:
            add(9, "<textLang>")
            for xl, label in langs:
                add(10, f'<lang xml:lang="{xl}">{esc(label)}</lang>')
            add(9, "</textLang>")
        if has_msitem:
            add(9, "<msItem>")
            if g(C_INSCRIPTION):
                il = INSCR_LANG.get(langs[0][0], "de") if langs else "de"
                add(10, f'<docEdition ana="szdg:IdentifyingInscription" xml:lang="{il}">'
                        f"{esc(collapse_ws(g(C_INSCRIPTION)))}</docEdition>")
            if g(C_INCIPIT):
                add(10, f"<incipit>{esc(collapse_ws(g(C_INCIPIT)))}</incipit>")
            add(9, "</msItem>")
        add(8, "</msContents>")
    # physDesc
    add(8, "<physDesc>")
    add(9, "<objectDesc>")
    add(10, "<supportDesc>")
    has_material = any(g(c) for c in (C_MAT_DE, C_MAT_EN, C_INSTR_DE, C_INSTR_EN))
    if has_material:
        add(11, "<support>")
        for col, lang in ((C_MAT_DE, "de"), (C_MAT_EN, "en")):
            if g(col):
                add(12, f'<material ana="szdg:WritingMaterial" xml:lang="{lang}">{esc(collapse_ws(g(col)))}</material>')
        for col, lang in ((C_INSTR_DE, "de"), (C_INSTR_EN, "en")):
            if g(col):
                add(12, f'<material ana="szdg:WritingInstrument" xml:lang="{lang}">{esc(collapse_ws(g(col)))}</material>')
        add(11, "</support>")
    add(11, "<extent>")
    for col, lang in ((C_EXTENT_DE, "de"), (C_EXTENT_EN, "en")):
        if not g(col):
            continue
        objtyp, measure = split_extent(g(col))
        parts = []
        if objtyp:
            parts.append(f'<term type="objecttyp">{esc(objtyp)}</term>')
        if measure:
            sep = ", " if objtyp else ""
            parts.append(f'{sep}<measure type="leaf">{esc(measure)}</measure>')
        add(12, f'<span xml:lang="{lang}">{"".join(parts)}</span>')
    if g(C_FORMAT):
        add(12, f'<measure type="format">{esc(collapse_ws(g(C_FORMAT)))}</measure>')
    add(11, "</extent>")
    if g(C_FOLIATION):
        add(11, "<foliation>")
        add(12, f"<ab>{esc(collapse_ws(g(C_FOLIATION)))}</ab>")
        add(11, "</foliation>")
    add(10, "</supportDesc>")
    add(9, "</objectDesc>")
    if g(C_HAND):
        add(9, "<handDesc>")
        add(10, f"<ab>{esc(collapse_ws(g(C_HAND)))}</ab>")
        add(9, "</handDesc>")
    encl = [(C_ENCL_DE, C_ENCL_EN, "szdg:Enclosures"), (C_ADD_DE, C_ADD_EN, "szdg:AdditionalMaterial")]
    if any(g(de) or g(en) for de, en, _ in encl):
        add(9, "<accMat>")
        add(10, "<list>")
        for de, en, ana in encl:
            if not (g(de) or g(en)):
                continue
            add(11, f'<item ana="{ana}">')
            if g(de):
                add(12, f'<desc xml:lang="de">{esc(collapse_ws(g(de)))}</desc>')
            if g(en):
                add(12, f'<desc xml:lang="en">{esc(collapse_ws(g(en)))}</desc>')
            add(11, "</item>")
        add(10, "</list>")
        add(9, "</accMat>")
    add(8, "</physDesc>")
    # history
    add(8, "<history>")
    add(9, "<origin>")
    if g(C_PLACE):
        add(10, f"<origPlace>{esc(collapse_ws(g(C_PLACE)))}</origPlace>")
    dt = date_text(g(C_DATE_ORIG), g(C_DATE_INFERRED), g(C_DATE_NORM))
    when = iso_when(g(C_DATE_NORM))
    if dt or when:
        attr = f' when="{when}"' if when else ""
        add(10, f"<origDate{attr}>{esc(dt)}</origDate>")
    add(9, "</origin>")
    if g(C_PROVENANCE):
        prov_de = collapse_ws(g(C_PROVENANCE))
        add(9, "<provenance>")
        add(10, f'<ab xml:lang="de">{esc(prov_de)}</ab>')
        add(10, f'<ab xml:lang="en">{esc(PROV_EN.get(prov_de, prov_de))}</ab>')
        add(9, "</provenance>")
    if g(C_ACQ_DE) or g(C_ACQ_EN):
        add(9, "<acquisition>")
        if g(C_ACQ_DE):
            add(10, f'<ab xml:lang="de">{esc(collapse_ws(g(C_ACQ_DE)))}</ab>')
        if g(C_ACQ_EN):
            add(10, f'<ab xml:lang="en">{esc(collapse_ws(g(C_ACQ_EN)))}</ab>')
        add(9, "</acquisition>")
    add(8, "</history>")
    add(7, "</msDesc>")
    add(6, "</sourceDesc>")
    add(5, "</fileDesc>")
    # profileDesc
    add(5, "<profileDesc>")
    add(6, "<textClass>")
    add(7, "<keywords>")
    if g(C_KAT):
        kat = collapse_ws(g(C_KAT))
        add(8, f'<term type="classification" xml:lang="de">{esc(kat)}</term>')
        en = CLASS_EN.get(kat)
        if en:
            add(8, f'<term type="classification" xml:lang="en">{esc(en)}</term>')
        else:
            report["unknown_classification"].add(kat)
    for name, gid in parse_actors(g(C_AFFECTED), g(C_AFFECTED_GND)):
        add(8, actor_xml("term", ' type="person_affected"', name, gid, gnd2szdper, report))
    add(7, "</keywords>")
    add(6, "</textClass>")
    add(5, "</profileDesc>")
    add(4, "</biblFull>")
    return "\n".join(L)


def next_start_id(szdleb_text: str) -> int:
    ids = [int(n) for n in re.findall(r'xml:id="SZDLEB\.(\d+)"', szdleb_text)]
    return max(ids) + 1 if ids else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", required=True, help="CSV export of the SZ-AAL Lebensdokumente")
    ap.add_argument("--szdleb", default=str(REPO_ROOT / "data/PersonalDocument/SZDLEB.xml"))
    ap.add_argument("--szdper", default=str(REPO_ROOT / "data/Index/Person/SZDPER.xml"))
    ap.add_argument("--gesamttitel", default="Stefan Zweig - SZ-AAL",
                    help="Collection title shared by all entries (verify the human-readable name)")
    ap.add_argument("--start-id", type=int, default=0, help="First SZDLEB.N (0 = auto from file)")
    ap.add_argument("--apply", action="store_true", help="Write into the SZDLEB file (default: dry run)")
    args = ap.parse_args()

    szdleb_path = Path(args.szdleb)
    szdleb_text = szdleb_path.read_text(encoding="utf-8")
    gnd2szdper = load_gnd2szdper(Path(args.szdper))

    with open(args.csv, encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.reader(f)]
    header, data = rows[0], [r for r in rows[1:] if any(c.strip() for c in r)]

    first_sig = data[0][C_SIG].strip() if data else ""
    if first_sig and first_sig in szdleb_text:
        print(f"ABBRUCH: '{first_sig}' steht bereits in {szdleb_path.name} "
              f"(doppelter Import?). Nichts geaendert.", file=sys.stderr)
        return 1

    start = args.start_id or next_start_id(szdleb_text)
    report = {"orgs": set(), "persons_without_ref": set(), "persons_unstructured": set(),
              "unknown_classification": set(), "entries": []}

    blocks = []
    for i, row in enumerate(data):
        xmlid = f"SZDLEB.{start + i}"
        blocks.append(build_entry(row, xmlid, gnd2szdper, args.gesamttitel, report))
        report["entries"].append((xmlid, row[C_SIG].strip()))

    new_xml = "\n".join(blocks)

    # validate the generated block in isolation (wrapped with the TEI namespace)
    try:
        ET.fromstring(f'<listBibl xmlns="{NS}" xmlns:szdg="x">{new_xml}</listBibl>')
    except ET.ParseError as e:
        print(f"FEHLER: generiertes XML nicht wohlgeformt: {e}", file=sys.stderr)
        return 2

    if args.apply:
        if "</listBibl>" not in szdleb_text:
            print("FEHLER: </listBibl> nicht gefunden.", file=sys.stderr)
            return 3
        head, tail = szdleb_text.rsplit("</listBibl>", 1)
        merged = head.rstrip() + "\n" + new_xml + "\n      </listBibl>" + tail
        szdleb_path.write_text(merged, encoding="utf-8")
        try:
            ET.parse(str(szdleb_path))
        except ET.ParseError as e:
            print(f"FEHLER: SZDLEB.xml nach Einfuegen nicht wohlgeformt: {e}", file=sys.stderr)
            return 4

    # --- report ---
    out = sys.stderr
    print(f"\n{'APPLIED' if args.apply else 'DRY RUN'} - {len(blocks)} Eintraege "
          f"{report['entries'][0][0]}..{report['entries'][-1][0]}", file=out)
    print(f"Gesamttitel: {args.gesamttitel!r}  (bitte Klartext verifizieren)", file=out)
    for xmlid, sig in report["entries"]:
        print(f"  {xmlid}  <- {sig}", file=out)
    if report["orgs"]:
        print("\nAls Koerperschaft (orgName) modelliert - im Bestand neu:", file=out)
        for n in sorted(report["orgs"]):
            print(f"  - {n}", file=out)
    if report["persons_without_ref"]:
        print("\nPersonen OHNE SZDPER-Verknuepfung (in SZDPER nachzupflegen):", file=out)
        for n in sorted(report["persons_without_ref"]):
            print(f"  - {n}", file=out)
    if report["persons_unstructured"]:
        print("\nPersonen ohne 'Nachname, Vorname'-Form (persName als Volltext, pruefen):", file=out)
        for n in sorted(report["persons_unstructured"]):
            print(f"  - {n}", file=out)
    if report["unknown_classification"]:
        print("\nUnbekannte Klassifikation (kein EN-Pendant):", file=out)
        for n in sorted(report["unknown_classification"]):
            print(f"  - {n}", file=out)

    if not args.apply:
        print("\n" + "=" * 80 + "\n" + new_xml)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
