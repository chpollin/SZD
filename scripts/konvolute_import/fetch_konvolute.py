#!/usr/bin/env python3
"""Bring every correspondence konvolut that GAMS production publishes into the repository.

Until 2026-09-24 only the konvolute that had been edited here lived under
data/Correspondence/konvolute/; the others existed only as objects on gams.uni-graz.at.
This script lists the objects o:szd.korrespondenzen.* through the Fedora search of the
production instance and downloads the datastream TEI_SOURCE of each one that has no file
here yet.

A file that already exists is never overwritten, because the repository copy is the
edited one and may be ahead of production. The downloaded bytes are written unchanged, so
a file is exactly what production serves (leading newline, no XML declaration, LF), the
same shape as the konvolute already in the repository. A download that is not well-formed
XML or has no TEI root is logged and skipped, and so is one that does not name its own PID,
unless KNOWN_DEFECTS records that production object as defective.

Production is read sequentially with a pause between requests.

Usage:

    python scripts/konvolute_import/fetch_konvolute.py          # dry run, lists what is missing
    python scripts/konvolute_import/fetch_konvolute.py --apply  # download and write

Standard library only.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "_szd_io", Path(__file__).resolve().parents[1] / "_szd_io.py"
)
szd_io = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(szd_io)

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "data" / "Correspondence" / "konvolute"
LOG = Path(__file__).resolve().parent / "fetch_log.csv"
HOST = "https://gams.uni-graz.at"
PAUSE = 0.5
TEI = "{http://www.tei-c.org/ns/1.0}"
FEDORA = "{http://www.fedora.info/definitions/1/0/types/}"

# Production objects whose content does not name their own PID, read on 2026-09-24. They are
# taken over unchanged so that the repository mirrors production, and the defect is logged;
# correcting them is editorial work on the repository copy.
KNOWN_DEFECTS = {
    "o:szd.korrespondenzen.judischer-jugendverein": "names o:szd.korrespondenzen.judischer-jugendverein-(dusseldorf), second object for the same body",
    "o:szd.korrespondenzen.judischer-jugendverein-dusseldorf": "names o:szd.korrespondenzen.judischer-jugendverein-(dusseldorf)",
    "o:szd.korrespondenzen.rascher-und-cie": "carries the konvolut of Margot Alberts and no PID of its own",
}


def get(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read()


def production_pids() -> list[str]:
    """All PIDs o:szd.korrespondenzen.<slug> through the paged Fedora findObjects search."""
    base = f"{HOST}/archive/objects?" + urllib.parse.urlencode(
        {"pid": "true", "terms": "o:szd.korrespondenzen.*", "resultFormat": "xml", "maxResults": "100"}
    )
    pids, url = [], base
    while True:
        tree = ET.fromstring(get(url))
        pids += [e.text for e in tree.iter(f"{FEDORA}pid") if e.text]
        token = tree.find(f"{FEDORA}listSession/{FEDORA}token")
        if token is None or not token.text:
            break
        url = base + "&sessionToken=" + token.text
        time.sleep(PAUSE)
    return sorted(set(pids))


def file_for(pid: str) -> Path:
    # o:szd.korrespondenzen.birman-c. -> szd.korrespondenzen.birman-c..xml, as in the repository
    return TARGET / (pid.removeprefix("o:") + ".xml")


def check(pid: str, data: bytes) -> tuple[str, int]:
    """Problem description (empty if fine) and number of letter entries."""
    try:
        root = ET.fromstring(data)
    except ET.ParseError as error:
        return f"not well-formed: {error}", 0
    if root.tag != f"{TEI}TEI":
        return f"root is {root.tag}", 0
    if pid not in KNOWN_DEFECTS and not re.search(rb">\s*" + re.escape(pid.encode()) + rb"\s*<", data):
        return "PID not named in the file", 0
    return "", sum(1 for _ in root.iter(f"{TEI}biblFull"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--apply", action="store_true", help="download and write the missing konvolute")
    args = parser.parse_args()

    pids = production_pids()
    missing = [pid for pid in pids if not file_for(pid).exists()]
    print(f"production: {len(pids)} konvolute, already in the repository: {len(pids) - len(missing)}, missing: {len(missing)}")
    if not args.apply:
        for pid in missing:
            print("  missing", pid)
        return

    run = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows = []
    for pid in missing:
        time.sleep(PAUSE)
        try:
            data = get(f"{HOST}/{pid}/TEI_SOURCE")
        except OSError as error:
            rows.append({"run": run, "pid": pid, "status": f"download failed: {error}", "letters": 0, "bytes": 0})
            continue
        problem, letters = check(pid, data)
        if not problem:
            path = file_for(pid)
            path.write_bytes(data)
        status = problem or ("written, known defect: " + KNOWN_DEFECTS[pid] if pid in KNOWN_DEFECTS else "written")
        rows.append({"run": run, "pid": pid, "status": status, "letters": letters, "bytes": len(data)})
        print(pid, status, f"{letters} letters")
    szd_io.append_log(LOG, ["run", "pid", "status", "letters", "bytes"], rows)
    written = sum(1 for row in rows if row["status"].startswith("written"))
    print(f"written {written}, skipped {len(rows) - written}, log {LOG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
