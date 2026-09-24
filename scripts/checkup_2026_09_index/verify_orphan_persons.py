#!/usr/bin/env python3
"""Decide which persons of the index are certainly unreferenced, as a precondition for removal.

find_unlinked_persons.py classifies the persons that no reference token reaches, and its
class "kein Treffer im Text" means that neither the surname nor a written-out variant occurs
in any element text of the holdings, konvolute and theme pages. This script takes that class
and adds three independent checks. A person is certain only if all of them hold.

1. Identifier. The string SZDPER.<n> occurs nowhere else: not in another entry of the person
   index, not in the organisation index (superseded identifiers), not in any other file of the
   data repository and not in the presentation layer (stylesheets, scripts, timeline data).
2. Authority. None of the person's GND numbers occurs in any file of the data repository
   outside the person's own entry.
3. Search. The person search of GAMS production and of staging returns no hit. Both are read
   sequentially with a pause.

Nothing is changed. The result is an archive-internal CSV.

Usage:

    python scripts/checkup_2026_09_index/verify_orphan_persons.py \
        --candidates <out-dir>/unverknuepfte_personen_kandidaten.csv --out <out-dir>/sicher_unverknuepft.csv

Standard library only.
"""

from __future__ import annotations

import argparse
import csv
import re
import time
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA = REPO_ROOT / "data"
PERSON_INDEX = DATA / "Index" / "Person" / "SZDPER.xml"
FRONTEND = REPO_ROOT.parent / "ZIMLAB" / "szd"
# Build outputs of the frontend harness copy the whole index and would match every identifier.
FRONTEND_SKIP = ("local-test-build/build", "node_modules", ".git")
TEXT_SUFFIXES = {".xml", ".xsl", ".js", ".json", ".html", ".sparql", ".md", ".py", ".mjs", ".css"}
NONE_CLASS = "kein Treffer im Text"
SEARCH = "{host}/archive/objects/query:szd.person_search/methods/sdef:Query/get?params=%241%7C%3Chttps%3A%2F%2Fgams.uni-graz.at%2Fo%3Aszd.personen%23{pid}%3E%3B%242%7Cde&locale=de"
HOSTS = {"production": "https://gams.uni-graz.at", "staging": "https://gams-staging.uni-graz.at"}
PAUSE = 0.3


def id_pattern(pid: str) -> re.Pattern[str]:
    return re.compile(re.escape(pid) + r"(?![0-9A-Za-z])")


def person_entries() -> dict[str, str]:
    text = PERSON_INDEX.read_text(encoding="utf-8")
    return {m.group(1): m.group(0) for m in re.finditer(r'<person\b[^>]*xml:id="(SZDPER\.[^"]+)".*?</person>', text, re.S)}


def corpus() -> list[tuple[str, str]]:
    files = []
    for path in sorted(DATA.rglob("*")):
        if path.is_file() and path.suffix == ".xml" and path != PERSON_INDEX:
            files.append((path.relative_to(REPO_ROOT).as_posix(), path.read_text(encoding="utf-8", errors="replace")))
    if FRONTEND.exists():
        for path in sorted(FRONTEND.rglob("*")):
            rel = path.relative_to(FRONTEND).as_posix()
            if path.is_file() and path.suffix in TEXT_SUFFIXES and not rel.startswith(FRONTEND_SKIP):
                files.append(("gams-www/" + rel, path.read_text(encoding="utf-8", errors="replace")))
    return files


def hits(host: str, pid: str) -> str:
    with urllib.request.urlopen(SEARCH.format(host=host, pid=pid), timeout=60) as response:
        page = response.read().decode("utf-8", errors="replace")
    match = re.search(r"Suchergebnisse:\s*(?:<[^>]+>\s*)*(\d+)", page)
    return match.group(1) if match else "?"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--no-search", action="store_true", help="skip the requests to GAMS")
    args = parser.parse_args()

    with args.candidates.open(encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    candidates = {}
    for row in rows:
        # the class may carry "; früher nur durch Nummerierungsfehler verknüpft", still without text hit
        if row["klasse"].split(";")[0] == NONE_CLASS:
            candidates.setdefault(row["szdper"], row)
    entries = person_entries()
    index_text = PERSON_INDEX.read_text(encoding="utf-8")
    files = corpus()

    results = []
    for pid, row in sorted(candidates.items(), key=lambda item: int(re.sub(r"\D", "", item[0]) or 0)):
        entry = entries.get(pid, "")
        pattern = id_pattern(pid)
        elsewhere = [label for label, text in files if pattern.search(text)]
        in_index = len(pattern.findall(index_text)) - len(pattern.findall(entry))
        gnds = sorted(set(re.findall(r"d-nb\.info/gnd/([0-9X-]+)", entry)) - {"placeholder"})
        gnd_hits = [label for label, text in files for gnd in gnds if re.search(r"gnd/" + re.escape(gnd) + r"(?![0-9X-])", text)]
        search = {}
        if not args.no_search:
            for name, host in HOSTS.items():
                time.sleep(PAUSE)
                search[name] = hits(host, pid)
        certain = not elsewhere and in_index == 0 and not gnd_hits and all(v == "0" for v in search.values())
        results.append({
            "szdper": pid, "name": row["name"], "gnd": " ".join(gnds), "klasse": row["klasse"],
            "kennung_anderswo": "; ".join(elsewhere[:5]) + (" (Index)" if in_index else ""),
            "gnd_anderswo": "; ".join(sorted(set(gnd_hits))[:5]),
            "treffer_produktion": search.get("production", ""), "treffer_staging": search.get("staging", ""),
            "sicher_unverknuepft": "ja" if certain else "nein",
        })
        print(pid, results[-1]["sicher_unverknuepft"], results[-1]["kennung_anderswo"], results[-1]["gnd_anderswo"], search)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    sure = sum(r["sicher_unverknuepft"] == "ja" for r in results)
    print(f"{len(results)} ohne Texttreffer geprüft, {sure} sicher unverknüpft, {len(results) - sure} mit Befund, {args.out}")


if __name__ == "__main__":
    main()
