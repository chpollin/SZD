#!/usr/bin/env python3
"""Fill missing <country>/<settlement> in the organisation index from the GND.

data/Index/Organisation/SZDORG.xml carries one <org> per corporate body, each with an
<orgName ref="http://d-nb.info/gnd/..."> and, for most entries, a <country> and a
<settlement> taken from the repository index SZDSTA at build time (see
the README beside this script). 32 entries never received a place because they
came from the person index or a holding reference instead of SZDSTA. This script looks
their GND record up at lobid.org and adds what the record actually states, never a guess.

Two GND fields are used, both restricted to what the record spells out:

    * geographicAreaCode maps to the country, by the DNB's own code table. A code has two
      or three segments ("XA-AT", "XA-DE-NW"); the last segment before a possible third one
      names the country, so a subdivision code ("XA-DE-NW" = Nordrhein-Westfalen) still
      resolves to "Deutschland" the way the existing entries already do (SZDORG.7, Beethoven-
      Haus Bonn, has only "XA-DE-NW" and country "Deutschland"). "XP" (international/unclear)
      and "ZZ" (not assigned) never resolve to a country.
    * placeOfBusiness maps to the settlement, taken as its label verbatim. An entry whose
      label equals a *country-level* geographicAreaCode's own label in the same record names
      the country, not a city (SZDORG.38, Österreichischer Frauen-Not-Dienst: geo "XA-AT" =
      "Österreich", placeOfBusiness "Österreich") and is not written as a settlement.

Several distinct countries or several distinct cities in one record mean the record does not
determine a single value; per the operator's instruction such a case is logged and nothing is
written for that field, never a guess between the candidates (SZDORG.24, Herbert Reichner
Verlag, moved between Wien, Zürich and Leipzig and stays without country or settlement).

XA-GB maps to "Großbritannien" like every other code. Until 2026-09-24 the indexes split
Great Britain into "England" (with a city) and "Großbritannien" (without), and the country
switch of the index pages showed two groups for one country; the operator unified both indexes
to "Großbritannien" on 2026-09-24.

For an entry that already carries country and settlement, the script only compares them
against the GND record and logs a contradiction; it never overwrites an existing value.

Regime: script pipeline, standard library only, run as a plain file
(python scripts/organisationen_index/reconcile_org_places.py). File I/O and the append-only CSV log reuse
scripts/_szd_io.py, loaded by file location because the scripts are not on the import path.

Usage:

    python scripts/organisationen_index/reconcile_org_places.py --dry-run
    python scripts/organisationen_index/reconcile_org_places.py

Options:

    --cache-dir PATH   directory for the cached lobid.org JSON responses (default: a
                        reconcile_org_places subdirectory of the OS temp directory, so
                        nothing is committed; reused between runs to avoid refetching)
    --delay SECONDS     pause between HTTP requests (default 0.3)
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252
    sys.stdout.reconfigure(errors="replace")

REPO_ROOT = Path(__file__).resolve().parents[2]

# Shared file helpers, loaded by path because the scripts run as plain files.
_spec = importlib.util.spec_from_file_location("_szd_io", REPO_ROOT / "scripts" / "_szd_io.py")
szd_io = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(szd_io)

SZDORG_FILE = REPO_ROOT / "data" / "Index" / "Organisation" / "SZDORG.xml"
LOG_FILE = Path(__file__).resolve().parent / "reconcile_places_log.csv"
LOG_FIELDS = ["szdorg_id", "name", "gnd", "aktion", "feld", "neuer_wert", "geo_codes", "orte", "bemerkung"]

TEI = "{http://www.tei-c.org/ns/1.0}"
LOBID_URL = "https://lobid.org/gnd/{}.json"
USER_AGENT = "SZD-reconcile-org-places/1.0 (https://github.com/chpollin/SZD)"

# geographicAreaCode -> German country name, in the spelling SZDORG.xml and SZDSTA.xml
# already use (Deutschland, Österreich, Schweiz, USA, Brasilien, Israel, Frankreich).
# Niederlande and Kanada are new to this index but follow the same German-exonym pattern.
COUNTRY_BY_AREA_CODE = {
    "XA-AT": "Österreich",
    "XA-DE": "Deutschland",
    "XA-CH": "Schweiz",
    "XA-FR": "Frankreich",
    "XA-NL": "Niederlande",
    "XA-GB": "Großbritannien",
    "XD-US": "USA",
    "XD-CA": "Kanada",
    "XD-BR": "Brasilien",
    "XB-IL": "Israel",
}
# Historical whole-Germany codes that do not reduce to "XA-DE" by prefix but are attested in
# the holdings as Germany (SZDORG.59, Rostock, carries "XA-DDDE" and "XA-DXDE" alongside
# "XA-DE-MV" for the same, already-filled entry).
GERMANY_HISTORICAL_CODES = {"XA-DXDE", "XA-DDDE"}
IGNORED_AREA_CODES = {"XP", "ZZ"}


@dataclass(frozen=True)
class GndPlace:
    """The geography lobid.org's GND record gives for one authority number."""

    area_codes: tuple[str, ...] = ()
    top_level_labels: tuple[str, ...] = ()  # labels of two-segment (country-level) area codes
    place_labels: tuple[str, ...] = ()
    fetch_error: str = ""


@dataclass
class OrgEntry:
    """One <org> block, parsed just enough to decide what, if anything, to add."""

    xml_id: str
    name: str
    gnd_ids: list[str]
    has_country: bool
    has_settlement: bool
    existing_country: str | None
    existing_settlement: str | None
    block_start: int
    block_end: int
    orgname_end: int  # offset of the last </orgName>, relative to block_start
    orgname_indent: str


ORG_RE = re.compile(
    r'<org\b[^>]*\bxml:id="(SZDORG\.\d+[a-z]?)"[^>]*>.*?</org>', re.DOTALL
)
ORGNAME_RE = re.compile(r'(?P<indent>[ \t]*)<orgName\b(?P<attrs>[^>]*)>(?P<text>.*?)</orgName>', re.DOTALL)
COUNTRY_RE = re.compile(r"<country>(.*?)</country>", re.DOTALL)
SETTLEMENT_RE = re.compile(r"<settlement>(.*?)</settlement>", re.DOTALL)
GND_ID_RE = re.compile(r"gnd/([0-9Xx][0-9A-Za-z-]*)")


def _bare_gnd_ids(ref: str) -> list[str]:
    """Every bare GND identifier in a @ref, http or https, possibly several separated by whitespace."""
    return [m.group(1) for m in GND_ID_RE.finditer(ref)]


def _parse_orgs(text: str) -> list[OrgEntry]:
    entries = []
    for m in ORG_RE.finditer(text):
        block = m.group(0)
        xml_id = re.search(r'xml:id="(SZDORG\.\d+[a-z]?)"', block).group(1)
        orgnames = list(ORGNAME_RE.finditer(block))
        if not orgnames:
            continue  # no orgName at all, nothing this script can reconcile
        gnd_ids: list[str] = []
        for on in orgnames:
            ref_m = re.search(r'ref="([^"]*)"', on.group("attrs"))
            if ref_m:
                gnd_ids.extend(_bare_gnd_ids(ref_m.group(1)))
        seen = set()
        gnd_ids = [g for g in gnd_ids if not (g in seen or seen.add(g))]
        name = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", orgnames[0].group("text"))).strip()
        country_m = COUNTRY_RE.search(block)
        settlement_m = SETTLEMENT_RE.search(block)
        last = orgnames[-1]
        entries.append(
            OrgEntry(
                xml_id=xml_id,
                name=name,
                gnd_ids=gnd_ids,
                has_country=country_m is not None,
                has_settlement=settlement_m is not None,
                existing_country=country_m.group(1).strip() if country_m else None,
                existing_settlement=settlement_m.group(1).strip() if settlement_m else None,
                block_start=m.start(),
                block_end=m.end(),
                orgname_end=last.end(),
                orgname_indent=last.group("indent"),
            )
        )
    return entries


def _fetch_gnd(gnd_id: str, cache_dir: Path, delay: float) -> dict | None:
    cache_file = cache_dir / f"{gnd_id}.json"
    if cache_file.exists():
        return json.loads(cache_file.read_text(encoding="utf-8"))
    url = LOBID_URL.format(gnd_id)
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read()
    except (urllib.error.HTTPError, urllib.error.URLError) as exc:
        return {"_fetch_error": str(exc)}
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file.write_bytes(raw)
    time.sleep(delay)
    return json.loads(raw)


def _gnd_place(gnd_ids: list[str], cache_dir: Path, delay: float) -> GndPlace:
    """The merged geography of every GND id an <org> carries (normally exactly one)."""
    area_codes: list[str] = []
    top_level_labels: list[str] = []
    place_labels: list[str] = []
    errors: list[str] = []
    for gnd_id in gnd_ids:
        data = _fetch_gnd(gnd_id, cache_dir, delay)
        if data is None:
            errors.append(f"{gnd_id}: keine Daten")
            continue
        if "_fetch_error" in data:
            errors.append(f"{gnd_id}: {data['_fetch_error']}")
            continue
        for entry in data.get("geographicAreaCode", []):
            code = entry.get("id", "").rsplit("#", 1)[-1]
            label = entry.get("label", "")
            if code:
                area_codes.append(code)
            if code and len(code.split("-")) == 2 and label:
                top_level_labels.append(label)
        for entry in data.get("placeOfBusiness", []):
            label = entry.get("label", "")
            if label:
                place_labels.append(label)
    return GndPlace(
        area_codes=tuple(dict.fromkeys(area_codes)),
        top_level_labels=tuple(dict.fromkeys(top_level_labels)),
        place_labels=tuple(dict.fromkeys(place_labels)),
        fetch_error="; ".join(errors),
    )


def _area_code_to_country(code: str) -> str | None:
    if code in IGNORED_AREA_CODES:
        return None
    if code in GERMANY_HISTORICAL_CODES:
        return "Deutschland"
    if code in COUNTRY_BY_AREA_CODE:
        return COUNTRY_BY_AREA_CODE[code]
    parts = code.split("-")
    if len(parts) >= 2:
        base = f"{parts[0]}-{parts[1][:2]}"
        if base in COUNTRY_BY_AREA_CODE:
            return COUNTRY_BY_AREA_CODE[base]
    return None


def _resolve_settlement(place: GndPlace) -> tuple[str | None, str]:
    top_level = {label.strip().lower() for label in place.top_level_labels}
    distinct = [p for p in dict.fromkeys(place.place_labels) if p.strip().lower() not in top_level]
    if not distinct:
        if place.place_labels:
            return None, f"placeOfBusiness nennt nur den Staat: {', '.join(place.place_labels)}"
        return None, ""
    if len(distinct) > 1:
        return None, f"placeOfBusiness uneindeutig: {'; '.join(distinct)}"
    return distinct[0], ""


def _resolve_country(place: GndPlace, settlement: str | None) -> tuple[str | None, str]:
    known_codes = list(place.area_codes)
    countries = {_area_code_to_country(c) for c in known_codes}
    countries.discard(None)
    unmapped = [c for c in known_codes if c not in IGNORED_AREA_CODES and _area_code_to_country(c) is None]
    if not countries:
        if unmapped:
            return None, f"geographicAreaCode nicht in der Ländertabelle: {', '.join(unmapped)}"
        if not place.area_codes:
            return None, ""
        return None, ""  # only IGNORED_AREA_CODES present
    if len(countries) > 1:
        return None, f"geographicAreaCode uneindeutig: {', '.join(sorted(countries))}"
    return next(iter(countries)), ""


SETTLEMENT_COMPARE_STOPWORDS = {"city"}


def _settlement_tokens(s: str) -> set[str]:
    """Core place-name tokens, dropping state/country codes and "City" so that
    "New York City" and "New York, NY" are recognised as the same place.
    """
    words = re.findall(r"[a-zäöüß]+", s.lower())
    return {w for w in words if len(w) > 2 and w not in SETTLEMENT_COMPARE_STOPWORDS}


def _country_matches(existing: str, place: GndPlace, settlement_hint: str | None) -> bool:
    countries = {_area_code_to_country(c) for c in place.area_codes}
    countries.discard(None)
    if not countries:
        return True  # nothing to compare against
    return existing.strip().lower() in {c.lower() for c in countries}


def _settlement_matches(existing: str, place: GndPlace) -> bool:
    if not place.place_labels:
        return True  # nothing to compare against
    existing_tokens = _settlement_tokens(existing)
    for label in place.place_labels:
        if existing_tokens & _settlement_tokens(label):
            return True
    return False


def _insert_country_settlement(block: str, entry: OrgEntry, additions: dict[str, str], newline: str) -> str:
    # entry.orgname_end already comes from a regex run on this same block string
    # (see _parse_orgs), so it is block-relative, not a position in the full file text.
    # newline must match the file's own line ending (SZDORG.xml carries CRLF throughout),
    # or the new lines would be the only bare-LF lines in an otherwise CRLF file.
    pos = entry.orgname_end
    indent = entry.orgname_indent
    if "country" in additions:
        insertion = f"{newline}{indent}<country>{additions['country']}</country>"
        block = block[:pos] + insertion + block[pos:]
        pos += len(insertion)
    else:
        m = re.match(r"\s*<country>.*?</country>", block[pos:], re.DOTALL)
        if m:
            pos += m.end()
    if "settlement" in additions:
        insertion = f"{newline}{indent}<settlement>{additions['settlement']}</settlement>"
        block = block[:pos] + insertion + block[pos:]
    return block


def run(cache_dir: Path, delay: float, dry_run: bool) -> int:
    text = szd_io.read_text(SZDORG_FILE)
    newline = "\r\n" if "\r\n" in text else "\n"
    entries = _parse_orgs(text)
    print(f"{len(entries)} <org> entries")

    log_rows: list[dict[str, str]] = []
    replacements: dict[tuple[int, int], str] = {}
    n_added = 0
    n_ambiguous = 0
    n_no_place_data = 0
    n_contradictions = 0
    n_no_gnd = 0

    for entry in entries:
        if not entry.gnd_ids:
            n_no_gnd += 1
            log_rows.append(
                {
                    "szdorg_id": entry.xml_id,
                    "name": entry.name,
                    "gnd": "",
                    "aktion": "ohne_gnd",
                    "feld": "",
                    "neuer_wert": "",
                    "geo_codes": "",
                    "orte": "",
                    "bemerkung": "kein GND-Verweis in orgName/@ref",
                }
            )
            continue

        place = _gnd_place(entry.gnd_ids, cache_dir, delay)
        geo_codes_s = ", ".join(place.area_codes)
        orte_s = ", ".join(place.place_labels)

        if place.fetch_error and not place.area_codes and not place.place_labels:
            n_no_place_data += 1
            log_rows.append(
                {
                    "szdorg_id": entry.xml_id,
                    "name": entry.name,
                    "gnd": ", ".join(entry.gnd_ids),
                    "aktion": "abruffehler",
                    "feld": "",
                    "neuer_wert": "",
                    "geo_codes": "",
                    "orte": "",
                    "bemerkung": place.fetch_error,
                }
            )
            continue

        if entry.has_country and entry.has_settlement:
            # Existing entry: compare only, never overwrite.
            if entry.existing_country and not _country_matches(entry.existing_country, place, entry.existing_settlement):
                n_contradictions += 1
                log_rows.append(
                    {
                        "szdorg_id": entry.xml_id,
                        "name": entry.name,
                        "gnd": ", ".join(entry.gnd_ids),
                        "aktion": "widerspruch",
                        "feld": "country",
                        "neuer_wert": entry.existing_country,
                        "geo_codes": geo_codes_s,
                        "orte": orte_s,
                        "bemerkung": "vorhandenes country stimmt mit keinem GND-Länder-Code überein",
                    }
                )
            if entry.existing_settlement and not _settlement_matches(entry.existing_settlement, place):
                n_contradictions += 1
                log_rows.append(
                    {
                        "szdorg_id": entry.xml_id,
                        "name": entry.name,
                        "gnd": ", ".join(entry.gnd_ids),
                        "aktion": "widerspruch",
                        "feld": "settlement",
                        "neuer_wert": entry.existing_settlement,
                        "geo_codes": geo_codes_s,
                        "orte": orte_s,
                        "bemerkung": "vorhandenes settlement stimmt mit keinem placeOfBusiness überein",
                    }
                )
            continue

        settlement, settlement_note = _resolve_settlement(place)
        country, country_note = _resolve_country(place, settlement)

        additions: dict[str, str] = {}
        if not entry.has_country:
            if country:
                additions["country"] = country
                n_added += 1
                log_rows.append(
                    {
                        "szdorg_id": entry.xml_id,
                        "name": entry.name,
                        "gnd": ", ".join(entry.gnd_ids),
                        "aktion": "ergänzt",
                        "feld": "country",
                        "neuer_wert": country,
                        "geo_codes": geo_codes_s,
                        "orte": orte_s,
                        "bemerkung": "",
                    }
                )
            else:
                if country_note:
                    n_ambiguous += 1
                    aktion = "uneindeutig"
                else:
                    n_no_place_data += 1
                    aktion = "keine_geodaten"
                log_rows.append(
                    {
                        "szdorg_id": entry.xml_id,
                        "name": entry.name,
                        "gnd": ", ".join(entry.gnd_ids),
                        "aktion": aktion,
                        "feld": "country",
                        "neuer_wert": "",
                        "geo_codes": geo_codes_s,
                        "orte": orte_s,
                        "bemerkung": country_note,
                    }
                )
        if not entry.has_settlement:
            if settlement:
                additions["settlement"] = settlement
                n_added += 1
                log_rows.append(
                    {
                        "szdorg_id": entry.xml_id,
                        "name": entry.name,
                        "gnd": ", ".join(entry.gnd_ids),
                        "aktion": "ergänzt",
                        "feld": "settlement",
                        "neuer_wert": settlement,
                        "geo_codes": geo_codes_s,
                        "orte": orte_s,
                        "bemerkung": "",
                    }
                )
            else:
                if settlement_note:
                    n_ambiguous += 1
                    aktion = "uneindeutig"
                else:
                    n_no_place_data += 1
                    aktion = "keine_geodaten"
                log_rows.append(
                    {
                        "szdorg_id": entry.xml_id,
                        "name": entry.name,
                        "gnd": ", ".join(entry.gnd_ids),
                        "aktion": aktion,
                        "feld": "settlement",
                        "neuer_wert": "",
                        "geo_codes": geo_codes_s,
                        "orte": orte_s,
                        "bemerkung": settlement_note,
                    }
                )

        if additions:
            block = text[entry.block_start:entry.block_end]
            new_block = _insert_country_settlement(block, entry, additions, newline)
            replacements[(entry.block_start, entry.block_end)] = new_block

    # Apply replacements back to front so earlier offsets stay valid.
    new_text = text
    for (start, end), new_block in sorted(replacements.items(), reverse=True):
        new_text = new_text[:start] + new_block + new_text[end:]

    if replacements:
        try:
            ET.fromstring(new_text.encode("utf-8"))
        except ET.ParseError as exc:
            print(f"REFUSING TO WRITE: result is not well-formed XML: {exc}", file=sys.stderr)
            return 1

    print(f"added: {n_added} value(s) across {len(replacements)} <org> entries")
    print(f"ambiguous (not written): {n_ambiguous}")
    print(f"no usable GND place data: {n_no_place_data}")
    print(f"contradictions with existing data (not changed): {n_contradictions}")
    print(f"without a GND: {n_no_gnd}")

    if dry_run:
        print("--dry-run: no file written, log not appended")
        return 0

    if replacements:
        szd_io.write_atomic(SZDORG_FILE, new_text)
        print(f"wrote {SZDORG_FILE}")
    else:
        print("nothing to write")

    # The append-only log is provenance of what the script wrote, like migration_log.csv in
    # the same folder; it does not re-record a diagnostic (ambiguous, no GND data, without a
    # GND, contradiction) on every rerun, or an unchanged tree would grow the log forever.
    # Those diagnostics stay in the run's stdout and the operator report instead.
    written_rows = [r for r in log_rows if r["aktion"] == "ergänzt"]
    if written_rows:
        n_logged = szd_io.append_log(LOG_FILE, LOG_FIELDS, written_rows)
        print(f"logged {n_logged} row(s) to {LOG_FILE}")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="report without writing the index or the log")
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path(tempfile.gettempdir()) / "reconcile_org_places",
        help="directory for cached lobid.org responses",
    )
    parser.add_argument("--delay", type=float, default=0.3, help="seconds between HTTP requests")
    args = parser.parse_args()
    return run(args.cache_dir, args.delay, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
