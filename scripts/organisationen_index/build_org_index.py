#!/usr/bin/env python3
"""Build the corporate body index data/Index/Organisation/SZDORG.xml from the material that
already exists in the repository, and write the decision table that explains every entry.

Two sources feed the index.

    1. data/Index/Person/SZDPER.xml -- corporate bodies that the person authority file
       carries as <person>. They are not marked as such anywhere, so they are found by
       heuristic (a persName without surname/forename, or a name matching the corporate
       name pattern) and then decided one by one in DECISIONS below.
    2. Every orgName/@ref under data/ -- corporate bodies the holdings already point at by
       authority number. They must all resolve in the new index, whether or not SZDPER
       knows them.

The location index data/Index/Location/SZDSTA.xml is read as well, and not as an optional
extra: the holdings point at most of the repositories by the same orgName/@ref, so they
have to resolve here too. Reading SZDSTA means they arrive under their curated name with
country, settlement and institutional link instead of the surface form of a shelfmark
line, each carrying a cross-reference to its SZDSTA id.

The presentation layer expects the result at o:szd.organisation: szd-TORDF.xsl loads that
object into $OrganisationList and resolves orgName/@ref against t:org/t:orgName[@ref] to
get the internal SZDORG id. The @ref spelling therefore has to match the holdings byte for
byte, which is http://d-nb.info/gnd/<number> throughout.

The script reads only. Removing the corporate bodies from SZDPER.xml and rewriting the
references of the holdings is the job of migrate_org_references.py, which runs after this
one and uses the ids minted here.

Two editorial decisions of 2026-09-11 are carried as rules, not as hand corrections:
NON_CORPORATE_SZDSTA keeps the SZDSTA entries that name no corporate body out of the
index, and MERGE_INTO folds a SZDPER entry into another one where both describe the same
body under different names.

Usage:

    python scripts/organisationen_index/build_org_index.py
    python scripts/organisationen_index/build_org_index.py --dry-run

Regime: script pipeline in the shape the other scripts of this repo use, standard library
only, no dependency manifest, run with plain python.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252
    sys.stdout.reconfigure(errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA = REPO_ROOT / "data"
SZDPER_FILE = DATA / "Index" / "Person" / "SZDPER.xml"
SZDSTA_FILE = DATA / "Index" / "Location" / "SZDSTA.xml"
OUT_XML = DATA / "Index" / "Organisation" / "SZDORG.xml"
OUT_CSV = Path(__file__).resolve().parent / "organisation_decisions.csv"

TEI = "{http://www.tei-c.org/ns/1.0}"
XML = "{http://www.w3.org/XML/1998/namespace}"

GND_BASE = "http://d-nb.info/gnd/"
GND_IN_REF = re.compile(r"gnd/([0-9Xx\-]+)\s*$")

# A GND number containing a hyphen comes from the corporate body and subject files, never
# from the individual person file. Used only as a hint, never as the decision itself.
GND_CORPORATE = re.compile(r"-")

ORG_NAME_PATTERN = re.compile(
    r"(?i)\b("
    r"verlag|verlagsanstalt|verlagsbuchhandlung|buchhandlung|antiquariat|auktionshaus|"
    r"&\s*co|co\.|ltd|inc|gmbh|ag|aktiengesellschaft|kg|ohg|e\.\s*v\.|s\.\s*a\.|n\.\s*v\.|"
    r"ministry|ministerium|amt|behörde|office|konsulat|botschaft|legation|"
    r"bank|gesellschaft|company|corporation|union|verband|bund|"
    r"universit|hochschule|schule|college|akademie|academy|institut|"
    r"zeitung|zeitschrift|magazin|magazine|journal|revue|redaktion|presse|press|"
    r"theater|museum|archiv|bibliothek|library|galerie|"
    r"verein|society|association|club|committee|komitee|kommission|guild|"
    r"stiftung|foundation|fonds|anstalt|agentur|agency|"
    r"rundfunk|broadcasting|radio|film|studio|pictures|"
    r"pen[- ]club|publishing|publishers|editions|éditions|edizioni|editorial|wydawnictwo"
    r")\b"
)

# SZDSTA entries that hold material but name no corporate body. They stay in the location
# index, which is a view of where things are kept, and stay out of the organisation index,
# which lists bodies. Holdings references to them keep pointing at o:szd.standorte.
NON_CORPORATE_SZDSTA: dict[str, str] = {
    "SZDSTA.12": "Privatbesitz, keine Körperschaft",
    "SZDSTA.13": "Privatbesitz, keine Körperschaft",
    "SZDSTA.14": "Privatbesitz, keine Körperschaft",
    "SZDSTA.15": "Privatbesitz, keine Körperschaft",
    "SZDSTA.16": "Privatbesitz, keine Körperschaft",
    "SZDSTA.24": "Privatbesitz, keine Körperschaft",
    "SZDSTA.18": "Erbengemeinschaft, keine Körperschaft",
}

# Two SZDPER entries describing one body under names too different for the name match to
# join them. The value is the entry whose name and authority number lead the merged
# record, the key becomes a name variant with its own idno back-reference.
MERGE_INTO: dict[str, str] = {
    "SZDPER.1735": "SZDPER.2326",
}

# Editorial decision per candidate, taken by reading the entry against the holdings.
# Candidates not listed here fall to the rule in _fallback_decision.
DECISIONS: dict[str, tuple[str, str]] = {
    "SZDPER.1056": ("org", "Körperschaft mit Körperschafts-GND"),
    "SZDPER.1461": ("org", "Verlegergruppe, Körperschaft mit GND"),
    "SZDPER.1626": ("org", "Museum, Körperschafts-GND, im Bestand als persName referenziert"),
    "SZDPER.1628": ("org", "Hilfsorganisation, keine Normdatennummer im Bestand"),
    "SZDPER.1659": ("org", "Rundfunkgremium, als Nachname/Vorname erfasst"),
    "SZDPER.1673": ("org", "Berufsverband"),
    "SZDPER.1688": ("org", "zwischenstaatliches Gremium"),
    "SZDPER.1735": (
        "org",
        "Behörde, als Nachname/Vorname erfasst, mit SZDPER.2326 zusammengeführt",
    ),
    "SZDPER.1791": ("org", "Verlag, Dublette zu SZDPER.1996"),
    "SZDPER.1975": ("org", "Zeitung"),
    "SZDPER.1996": ("org", "Verlag, Dublette zu SZDPER.1791"),
    "SZDPER.2324": ("org", "Verlag, Körperschafts-GND, 2026-06 als Person eingetragen"),
    "SZDPER.2325": ("org", "Bank, Körperschafts-GND, 2026-06 als Person eingetragen"),
    "SZDPER.2326": ("org", "Behörde, Körperschafts-GND, führt den Eintrag mit SZDPER.1735"),
    "SZDPER.2327": ("org", "Wirtschaftsprüfung, Körperschafts-GND, 2026-06 als Person eingetragen"),
    "SZDPER.2328": ("org", "Versicherung, Körperschafts-GND, 2026-06 als Person eingetragen"),
    "SZDPER.1578": ("unclear", "Dynastie, keine Körperschaft, GND im Personenformat"),
    "SZDPER.1657": ("unclear", "Ordnungsplatzhalter der Verzeichnung, kein Akteur"),
    "SZDPER.1804": ("unclear", "Ordnungsplatzhalter der Verzeichnung, kein Akteur"),
    "SZDPER.1805": ("unclear", "Ordnungsplatzhalter der Verzeichnung, kein Akteur"),
    "SZDPER.1868": ("unclear", "Familie, keine Körperschaft"),
    "SZDPER.1899": ("unclear", "Buchreihe oder Verlagsprogramm, Trägerschaft ungeklärt"),
    "SZDPER.2065": ("unclear", "Rechtssache, kein Akteur"),
    "SZDPER.2142": ("unclear", "Familienname ohne Vornamen, Zuordnung ungeklärt"),
    "SZDPER.644": ("person", "Personenname, Treffer des Namensmusters auf House"),
    "SZDPER.2029": ("person", "Personenname, Treffer des Namensmusters auf House"),
}


def _text(elem: ET.Element | None) -> str:
    if elem is None:
        return ""
    return re.sub(r"\s+", " ", "".join(elem.itertext())).strip()


def _gnd(ref: str | None) -> str:
    """The bare GND number of a @ref, uppercased so that the check digit X compares."""
    match = GND_IN_REF.search((ref or "").strip())
    return match.group(1).upper() if match else ""


def _sort_key(name: str) -> str:
    """Locale-free sort key so that two runs on the same input produce the same ids."""
    folded = unicodedata.normalize("NFKD", name.casefold())
    return re.sub(r"[^a-z0-9 ]", "", folded).strip()


def _match_key(name: str) -> str:
    """Name form for matching a SZDPER entry against a holdings orgName.

    Leading article, punctuation and case carry no distinguishing weight here: the
    holdings write 'The Authors' Guild' where the person index writes 'Authors Guild'.
    """
    folded = unicodedata.normalize("NFKD", name.casefold())
    folded = re.sub(r"[^a-z0-9 ]", " ", folded)
    folded = re.sub(r"^(the|le|la|les|der|die|das)\s+", "", folded.strip())
    return re.sub(r"\s+", " ", folded).strip()


def _person_name(person: ET.Element) -> str:
    pers_name = person.find(f"{TEI}persName")
    if pers_name is None:
        return ""
    name = pers_name.find(f"{TEI}name")
    if name is not None:
        return _text(name)
    parts = [
        _text(pers_name.find(f"{TEI}{tag}"))
        for tag in ("surname", "forename")
        if _text(pers_name.find(f"{TEI}{tag}"))
    ]
    return ", ".join(parts)


def _is_candidate(person: ET.Element) -> bool:
    pers_name = person.find(f"{TEI}persName")
    if pers_name is None:
        return False
    if pers_name.find(f"{TEI}name") is not None:
        return True
    return bool(ORG_NAME_PATTERN.search(_person_name(person)))


def _fallback_decision(gnd: str) -> tuple[str, str]:
    """Decision for a candidate nobody has reviewed yet.

    A GND number without a hyphen is an individual person number, which for an entry the
    heuristic flagged means a one-name person such as Homer or Novalis. Everything else
    stays unclear, so that a new corporate body added to SZDPER surfaces in the report
    instead of slipping into the index unseen.
    """
    if gnd and not GND_CORPORATE.search(gnd):
        return "person", "einnamige Personenansetzung mit Personen-GND"
    return "unclear", "nicht geprüft, Heuristik schlägt an"


def _read_person_index() -> tuple[list[dict[str, str]], set[str]]:
    """Candidates with their decision, plus every GND that SZDPER uses for a person."""
    root = ET.parse(SZDPER_FILE).getroot()
    candidates: list[dict[str, str]] = []
    person_gnds: set[str] = set()
    for person in root.iter(f"{TEI}person"):
        pers_name = person.find(f"{TEI}persName")
        gnd = _gnd(pers_name.get("ref") if pers_name is not None else "")
        person_id = person.get(f"{XML}id", "")
        if not _is_candidate(person):
            if gnd:
                person_gnds.add(gnd)
            continue
        decision, reason = DECISIONS.get(person_id, _fallback_decision(gnd))
        if decision != "org" and gnd:
            person_gnds.add(gnd)
        candidates.append(
            {
                "id": person_id,
                "name": _person_name(person),
                "gnd": gnd,
                "decision": decision,
                "reason": reason,
                "corresp": person.get("corresp", ""),
            }
        )
    return candidates, person_gnds


def _missing_decided_bodies(candidates: list[dict[str, str]]) -> list[str]:
    """Decided corporate bodies that SZDPER no longer carries.

    Once migrate_org_references.py has removed them, a rerun of this script would rebuild
    the index without them and renumber everything that follows. That has to stop the run
    rather than silently shrink the index.
    """
    found = {candidate["id"] for candidate in candidates}
    return sorted(
        person_id
        for person_id, (decision, _reason) in DECISIONS.items()
        if decision == "org" and person_id not in found
    )


def _read_holdings() -> tuple[dict[str, Counter[str]], dict[str, set[str]]]:
    """Every orgName/@ref in a text body under data/, by GND: name forms and files."""
    forms: dict[str, Counter[str]] = {}
    files: dict[str, set[str]] = {}
    for path in sorted(DATA.rglob("*.xml")):
        if path == OUT_XML:  # a previous run of this script is not a source
            continue
        root = ET.parse(path).getroot()
        text = root.find(f"{TEI}text")
        if text is None:
            continue
        for org_name in text.iter(f"{TEI}orgName"):
            gnd = _gnd(org_name.get("ref"))
            if not gnd:
                continue
            forms.setdefault(gnd, Counter())[_text(org_name)] += 1
            files.setdefault(gnd, set()).add(path.relative_to(REPO_ROOT).as_posix())
    return forms, files


def _read_repositories() -> tuple[dict[str, dict[str, str]], list[dict[str, str]]]:
    """The location index by GND, plus the entries NON_CORPORATE_SZDSTA rules out."""
    root = ET.parse(SZDSTA_FILE).getroot()
    repositories: dict[str, dict[str, str]] = {}
    excluded: list[dict[str, str]] = []
    for org in root.iter(f"{TEI}org"):
        org_name = org.find(f"{TEI}orgName")
        if org_name is None:
            continue
        org_id = org.get(f"{XML}id", "")
        if org_id in NON_CORPORATE_SZDSTA:
            excluded.append(
                {"id": org_id, "name": _text(org_name), "reason": NON_CORPORATE_SZDSTA[org_id]}
            )
            continue
        gnd = _gnd(org_name.get("ref"))
        key = gnd or f"noref:{org.get(f'{XML}id', '')}"
        repositories[key] = {
            "id": org.get(f"{XML}id", ""),
            "name": _text(org_name),
            "gnd": gnd,
            "corresp": org.get("corresp", ""),
            "country": _text(org.find(f"{TEI}country")),
            "settlement": _text(org.find(f"{TEI}settlement")),
        }
    return repositories, excluded


def _new_record(name: str, gnd: str) -> dict:
    return {
        "name": name,
        "gnd": gnd,
        "corresp": "",
        "country": "",
        "settlement": "",
        "variants": [],
        "szdper": [],
        "szdsta": "",
    }


def _add_variant(record: dict, form: str) -> None:
    if not form or form == record["name"] or form in record["variants"]:
        return
    record["variants"].append(form)


def _is_same_body(first: str, second: str) -> bool:
    """Whether two name forms plausibly name the same body.

    The holdings write the fuller form of a name the indices write short, usually by
    appending the place ('Theatermuseum' against 'Theatermuseum, Wien'), so containment
    one way or the other is the test. Two forms that share nothing mean one authority
    number carries two different bodies, which is a defect in the source, not a variant.
    """
    left, right = _match_key(first), _match_key(second)
    return bool(left) and bool(right) and (left in right or right in left)


def collect_organisations() -> tuple[list[dict], list[dict], list[dict], list[dict[str, str]]]:
    """Index records, the SZDPER decision rows, the conflicts, and the ruled-out entries."""
    candidates, person_gnds = _read_person_index()
    forms, files = _read_holdings()
    repositories, excluded = _read_repositories()

    records: dict[str, dict] = {}
    by_match_key: dict[str, str] = {}
    conflicts: list[dict] = []

    def key_of(name: str, gnd: str) -> str:
        return gnd or f"name:{_match_key(name)}"

    # The location index first, so that its curated name, country and settlement win.
    for entry in repositories.values():
        key = key_of(entry["name"], entry["gnd"])
        record = records.setdefault(key, _new_record(entry["name"], entry["gnd"]))
        record["corresp"] = entry["corresp"]
        record["country"] = entry["country"]
        record["settlement"] = entry["settlement"]
        record["szdsta"] = entry["id"]
        by_match_key[_match_key(entry["name"])] = key

    key_by_person: dict[str, str] = {}
    # A merged candidate needs the key of the entry it folds into, so it goes last.
    for candidate in sorted(candidates, key=lambda c: c["id"] in MERGE_INTO):
        if candidate["decision"] != "org":
            continue
        merge_target = MERGE_INTO.get(candidate["id"])
        if merge_target:
            if merge_target not in key_by_person:
                raise RuntimeError(
                    f"MERGE_INTO: {merge_target} ist kein als Körperschaft entschiedener Eintrag"
                )
            key = key_by_person[merge_target]
            record = records[key]
            record["szdper"].append(candidate["id"])
            _add_variant(record, candidate["name"])
            candidate["_key"] = key
            continue
        gnd = candidate["gnd"]
        if not gnd:
            # The holdings may carry the authority number the person index lacks; only an
            # orgName of the same name settles it, never a guess.
            matched = [
                g
                for g, counter in forms.items()
                if _match_key(candidate["name"]) in {_match_key(f) for f in counter}
            ]
            if len(matched) == 1:
                gnd = matched[0]
                candidate["gnd"] = gnd
                candidate["reason"] += ", GND aus dem Bestand über Namensgleichheit"
        key = (
            key_of(candidate["name"], gnd)
            if gnd
            else by_match_key.get(_match_key(candidate["name"]), key_of(candidate["name"], gnd))
        )
        record = records.setdefault(key, _new_record(candidate["name"], gnd))
        record["szdper"].append(candidate["id"])
        if candidate["corresp"]:
            record["corresp"] = record["corresp"] or candidate["corresp"]
        by_match_key.setdefault(_match_key(candidate["name"]), key)
        candidate["_key"] = key
        key_by_person[candidate["id"]] = key

    for gnd, counter in sorted(forms.items()):
        if gnd in person_gnds:
            conflicts.append(
                {
                    "gnd": gnd,
                    "kind": "Personeneintrag",
                    "forms": "; ".join(sorted(counter)),
                    "files": "; ".join(sorted(files.get(gnd, ()))),
                }
            )
            continue
        attested = [form for form, _count in counter.most_common() if form]
        record = records.setdefault(gnd, _new_record(attested[0] if attested else "", gnd))
        divergent = [form for form in attested if not _is_same_body(record["name"], form)]
        if divergent:
            conflicts.append(
                {
                    "gnd": gnd,
                    "kind": "zwei Körperschaften an einer Nummer",
                    "forms": "; ".join([record["name"], *divergent]),
                    "files": "; ".join(sorted(files.get(gnd, ()))),
                }
            )
        for form in attested:
            _add_variant(record, form)

    ordered = sorted(records.values(), key=lambda r: (_sort_key(r["name"]), r["gnd"]))
    for number, record in enumerate(ordered, start=1):
        record["id"] = f"SZDORG.{number}"
    for candidate in candidates:
        if candidate["decision"] == "org":
            candidate["szdorg"] = records[candidate["_key"]]["id"]
        else:
            candidate["szdorg"] = ""
    return ordered, candidates, conflicts, excluded


def _escape(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _attr(value: str) -> str:
    return _escape(value).replace('"', "&quot;")


def _header(date_iso: str, date_display: str) -> str:
    """The header of the other indices, with title, PID and source description changed."""
    return f"""  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title xml:lang="de">Organisationen</title>
        <title xml:lang="en">Organisations</title>
      </titleStmt>
      <publicationStmt>
        <publisher>
          <orgName corresp="https://www.uni-salzburg.at/index.php?id=72"
            ref="d-nb.info/gnd/1047605287">Literaturarchiv Salzburg</orgName>
        </publisher>
        <authority>
          <orgName corresp="https://informationsmodellierung.uni-graz.at"
            ref="d-nb.info/gnd/1137284463">Zentrum für Informationsmodellierung - Austrian Centre
            for Digital Humanities, Karl-Franzens-Universität Graz</orgName>
        </authority>
        <distributor>
          <orgName ref="https://gams.uni-graz.at">GAMS - Geisteswissenschaftliches Asset Management
            System</orgName>
        </distributor>
        <availability>
          <licence target="https://creativecommons.org/licenses/by/4.0">Creative Commons BY 4.0</licence>
        </availability>
        <publisher>Literaturarchiv Salzburg</publisher>
        <idno type="PID">o:szd.organisation</idno>
        <date when="{date_iso}">{date_display}</date>
      </publicationStmt>
      <seriesStmt>
        <title ref="https://gams.uni-graz.at/szd">Stefan Zweig digital</title>
        <respStmt>
          <resp>Datenerfassung</resp>
          <persName>
            <forename>Stefan</forename>
            <surname>Matthias</surname>
          </persName>
          <persName>
            <forename>Oliver</forename>
            <surname>Matuschek</surname>
          </persName>
          <persName>
            <forename>Julia</forename>
            <surname>Glunk</surname>
          </persName>
          <persName>
            <forename>Lina</forename>
            <surname>Zangerl</surname>
          </persName>
          <persName>
            <forename>Verena</forename>
            <surname>Höller</surname>
          </persName>
        </respStmt>
        <respStmt>
          <resp>Datenmodellierung</resp>
          <persName>
            <forename>Christopher</forename>
            <surname>Pollin</surname>
          </persName>
        </respStmt>
      </seriesStmt>
      <sourceDesc>
        <p>Körperschaften des Nachlasses von Stefan Zweig, zusammengeführt aus den
          Körperschaftseinträgen des Personenindex und den Körperschaftsverweisen der
          Bestandsdateien.</p>
      </sourceDesc>
    </fileDesc>
    <encodingDesc>
      <projectDesc>
        <ab>
          <ref target="https://gams.uni-graz.at/o:szd.organisation" type="object"/>
        </ab>
        <p>Das Projekt verfolgt das Ziel, den weltweit verstreuten Nachlass von Stefan Zweig im
          digitalen Raum zusammenzuführen und ihn einem literaturwissenschaftlich bzw.
          wissenschaftlich interessierten Publikum zu erschließen. In Zusammenarbeit mit dem
          Literaturarchiv der Universität Salzburg wird dabei, basierend auf dem dort vorhandenen
          Quellenmaterial, eine digitale Nachlassrekonstruktion des Bestandes generiert. So entsteht
          ein strukturierter Bestand an digitalen Objekten, der im Sinne der digitalen
          Langzeitarchivierung repräsentiert wird, und NutzerInnen orts- und zeitunabhängig
          zugänglich ist. Das Projekt ist so konzipiert, dass zu einem späteren Zeitpunkt
          Erschließung und Anreicherung des Quellenmaterials (z.B. digitalen Editionen) möglich
          werden.</p>
      </projectDesc>
    </encodingDesc>
  </teiHeader>"""


def render_tei(records: list[dict], date_iso: str, date_display: str) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<TEI xmlns="http://www.tei-c.org/ns/1.0">']
    lines.append(_header(date_iso, date_display))
    lines.append("  <text>")
    lines.append("    <body>")
    lines.append("      <listOrg>")
    for record in records:
        attrs = ""
        if record["corresp"]:
            attrs += f' corresp="{_attr(record["corresp"])}"'
        attrs += f' xml:id="{_attr(record["id"])}"'
        lines.append(f"        <org{attrs}>")
        ref = f' ref="{_attr(GND_BASE + record["gnd"])}"' if record["gnd"] else ""
        lines.append(f"          <orgName{ref}>{_escape(record['name'])}</orgName>")
        for variant in record["variants"]:
            lines.append(f'          <orgName type="variant">{_escape(variant)}</orgName>')
        if record["country"]:
            lines.append(f"          <country>{_escape(record['country'])}</country>")
        if record["settlement"]:
            lines.append(f"          <settlement>{_escape(record['settlement'])}</settlement>")
        for person_id in record["szdper"]:
            lines.append(f'          <idno type="SZDPER" subtype="superseded">{_escape(person_id)}</idno>')
        if record["szdsta"]:
            lines.append(f'          <idno type="SZDSTA">{_escape(record["szdsta"])}</idno>')
        lines.append("        </org>")
    lines.append("      </listOrg>")
    lines.append("    </body>")
    lines.append("  </text>")
    lines.append("</TEI>")
    return "\n".join(lines) + "\n"


def write_decisions(
    candidates: list[dict], records: list[dict], excluded: list[dict[str, str]]
) -> None:
    rows = []
    for candidate in sorted(candidates, key=lambda c: int(re.sub(r"\D", "", c["id"]) or 0)):
        rows.append(
            {
                "szdper_id": candidate["id"],
                "name": candidate["name"],
                "gnd": candidate["gnd"],
                "entscheidung": candidate["decision"],
                "grund": candidate["reason"],
                "szdorg_id": candidate["szdorg"],
                "quelle": "SZDPER",
            }
        )
    for record in records:
        if record["szdper"]:
            continue
        rows.append(
            {
                "szdper_id": "",
                "name": record["name"],
                "gnd": record["gnd"],
                "entscheidung": "org",
                "grund": (
                    "Standortindex SZDSTA" + (f", {record['szdsta']}" if record["szdsta"] else "")
                    if record["szdsta"]
                    else "im Bestand als orgName mit GND geführt"
                ),
                "szdorg_id": record["id"],
                "quelle": "SZDSTA" if record["szdsta"] else "Bestand",
            }
        )
    for entry in excluded:
        rows.append(
            {
                "szdper_id": "",
                "name": entry["name"],
                "gnd": "",
                "entscheidung": "keine-koerperschaft",
                "grund": f"{entry['reason']}, {entry['id']} bleibt im Standortindex",
                "szdorg_id": "",
                "quelle": "SZDSTA",
            }
        )
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["szdper_id", "name", "gnd", "entscheidung", "grund", "szdorg_id", "quelle"],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--dry-run", action="store_true", help="nur berichten, nichts schreiben")
    parser.add_argument("--date", default="2026-09-11", help="Datum des publicationStmt, ISO")
    args = parser.parse_args()

    for required in (SZDPER_FILE, SZDSTA_FILE):
        if not required.exists():
            print(f"FEHLER: {required} fehlt", file=sys.stderr)
            return 1

    records, candidates, conflicts, excluded = collect_organisations()
    missing = _missing_decided_bodies(candidates)
    if missing:
        print(
            "FEHLER: SZDPER führt diese als Körperschaft entschiedenen Einträge nicht mehr: "
            f"{', '.join(missing)}. Der Index ist nach dem Lauf von migrate_org_references.py "
            "nicht mehr aus den Quellen erzeugbar und wird von Hand gepflegt.",
            file=sys.stderr,
        )
        return 1

    year, month, day = args.date.split("-")
    xml_text = render_tei(records, args.date, f"{day}.{month}.{year}")
    ET.fromstring(xml_text)  # trust boundary: never write something that is not well-formed

    decisions = Counter(c["decision"] for c in candidates)
    print(f"OK  Kandidaten in SZDPER: {sum(decisions.values())} ({dict(decisions)})")
    print(f"OK  Einträge im Index: {len(records)}")
    for entry in excluded:
        print(f"SKIP  {entry['id']} {entry['name']}: {entry['reason']}")
    for conflict in conflicts:
        print(
            f"WARNUNG  GND {conflict['gnd']}, {conflict['kind']}: {conflict['forms']} "
            f"[{conflict['files']}]",
            file=sys.stderr,
        )
    if args.dry_run:
        print("SKIP  dry-run, nichts geschrieben")
        return 0

    OUT_XML.parent.mkdir(parents=True, exist_ok=True)
    temp = OUT_XML.with_suffix(".xml.tmp")
    temp.write_text(xml_text, encoding="utf-8")
    temp.replace(OUT_XML)
    write_decisions(candidates, records, excluded)
    print(f"OK  {OUT_XML.relative_to(REPO_ROOT).as_posix()}")
    print(f"OK  {OUT_CSV.relative_to(REPO_ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
