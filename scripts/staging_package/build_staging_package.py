#!/usr/bin/env python3
"""Build a staging ingest package from the repository, with the Cirilo references still to set.

The package is a folder outside the repository (the operator's ingest workspace). It holds a
copy of every TEI file to ingest, grouped in the order the ingest needs, a SHA256SUMS file and a
README. The README lists, per object, the STYLESHEET and TORDF reference it must carry, read
live from the datastream redirects of gams-staging.uni-graz.at, so that only the references
that are missing, dead or end in an illegal character appear as work.

Order matters: szd-TORDF.xsl resolves persons, repositories and corporate bodies against the
index objects on the instance at ingest time, so the indexes go in before everything else.

A konvolut whose TEI does not name its own PID is left out, because Cirilo takes the PID of a
new object from the file and would create a wrong object.

Usage:

    python scripts/staging_package/build_staging_package.py --out <folder>
    python scripts/staging_package/build_staging_package.py --out <folder> --no-staging  # skip reading references

Standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
STAGING = "https://gams-staging.uni-graz.at"
MIRROR = STAGING + "/gamsdev/pollin/szd/gams-www/"
PAUSE = 0.2

# (group, PID, repository file, page stylesheet); every object gets szd-TORDF.xsl
INDEXES = [
    ("o:szd.organisation", "Index/Organisation/SZDORG.xml", "szd-Index.xsl"),
    ("o:szd.personen", "Index/Person/SZDPER.xml", "szd-Index.xsl"),
    ("o:szd.standorte", "Index/Location/SZDSTA.xml", "szd-Index.xsl"),
    ("o:szd.werkindex", "Index/Werke/SZDWRK.xml", "szd-Index.xsl"),
]
HOLDINGS = [
    ("o:szd.korrespondenzen", "Correspondence/SZDKOR.xml", "szd-Korrespondenzen.xsl"),
    ("o:szd.bibliothek", "Library/SZDBIB.xml", "szd-Bibliothek.xsl"),
    ("o:szd.lebensdokumente", "PersonalDocument/SZDLEB.xml", "szd-Werke.xsl"),
    ("o:szd.werke", "Work/SZDMSK.xml", "szd-Werke.xsl"),
    ("o:szd.aufsatzablage", "Aufsatzablage/SZDESS.xml", "szd-Essays.xsl"),
    ("o:szd.autographen", "Autograph/SZDAUT.xml", "szd-Autographen.xsl"),
    ("o:szd.lebenskalender", "Biography/SZDBIO.xml", "szd-Lebenskalender.xsl"),
]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def reference(pid: str, datastream: str) -> str:
    """The target of a datastream reference, or a short description of why there is none."""
    time.sleep(PAUSE)
    try:
        OPENER.open(f"{STAGING}/archive/objects/{pid}/datastreams/{datastream}/content", timeout=30)
        return "no redirect"
    except urllib.error.HTTPError as error:
        if error.code in (301, 302, 303, 307, 308):
            return error.headers.get("Location", "")
        if error.code == 400:
            return "illegal character at the end"
        if error.code == 404:
            return "missing"
        return f"HTTP {error.code}"


def exists(pid: str) -> bool:
    time.sleep(PAUSE)
    try:
        urllib.request.urlopen(f"{STAGING}/{pid}/TEI_SOURCE", timeout=60).close()
        return True
    except urllib.error.HTTPError:
        return False


def own_pid(path: Path) -> bool:
    return f'<idno type="PID">o:{path.stem}</idno>' in re.sub(r">\s+|\s+<", lambda m: m.group(0).strip(), path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--no-staging", action="store_true")
    args = parser.parse_args()

    konvolute, skipped = [], []
    for path in sorted((DATA / "Correspondence" / "konvolute").glob("*.xml")):
        (konvolute if own_pid(path) else skipped).append(path)
    groups = [
        ("1 Indexes", "1-index", [(p, DATA / f, s) for p, f, s in INDEXES]),
        ("2 Holdings", "2-bestaende", [(p, DATA / f, s) for p, f, s in HOLDINGS]),
        ("3 Konvolute", "3-konvolute", [("o:" + f.stem, f, "szd-Konvolut.xsl") for f in konvolute]),
    ]

    if args.out.exists():
        # only a folder this script wrote before is replaced, never an arbitrary directory
        if not (args.out / "SHA256SUMS").exists():
            raise SystemExit(f"{args.out} exists and is not a package built by this script")
        shutil.rmtree(args.out)
    sums, table = [], []
    for title, folder, items in groups:
        target = args.out / folder
        target.mkdir(parents=True)
        for pid, source, stylesheet in items:
            shutil.copy2(source, target / source.name)
            sums.append(f"{hashlib.sha256(source.read_bytes()).hexdigest()}  {folder}/{source.name}")
            row = {"group": title, "pid": pid, "file": f"{folder}/{source.name}", "stylesheet": stylesheet, "status": "", "todo": []}
            if not args.no_staging:
                if not exists(pid):
                    row["status"] = "new"
                    row["todo"] = ["STYLESHEET", "TORDF"]
                else:
                    row["status"] = "update"
                    for datastream, want in (("STYLESHEET", MIRROR + stylesheet), ("TORDF", MIRROR + "szd-TORDF.xsl")):
                        if reference(pid, datastream) != want:
                            row["todo"].append(datastream)
            table.append(row)
            print(pid, row["status"], ",".join(row["todo"]))

    revision = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    # sha256sum -c reads LF only, and Windows would otherwise write CRLF
    (args.out / "SHA256SUMS").write_text("\n".join(sums) + "\n", encoding="utf-8", newline="\n")
    lines = [
        f"# Staging ingest package, data repository `{revision}`",
        "",
        "Generated by `scripts/staging_package/build_staging_package.py`. Regenerate it instead of editing it by hand.",
        "",
        "## Order",
        "",
        "1. Folder `1-index`, because the RDF transformation looks persons, repositories and corporate bodies up in the index objects at ingest time.",
        "2. Folder `2-bestaende`.",
        "3. Folder `3-konvolute`. Cirilo creates a missing object from the PID in the file.",
        "",
        "Each folder goes through the Cirilo dialog Ingest objects with the content model `TEI Object | cirilo:TEI.szd`, PID box unticked, button From filesystem. Cirilo takes the PID from `<idno type=\"PID\">` in each file. A new object inherits the references of `cirilo:TEI.szd`, see `knowledge/ARCHITECTURE.md` in the data repository.",
        "",
        "Before the ingest every object needs both references below. Type or paste them so that nothing follows `.xsl`; a trailing character makes the reference unusable.",
        "",
        "- STYLESHEET: `" + MIRROR + "<stylesheet>`",
        "- TORDF: `" + MIRROR + "szd-TORDF.xsl`",
        "",
    ]
    if not args.no_staging:
        todo = [r for r in table if r["todo"]]
        lines += [f"## References to set ({len(todo)} objects)", "", "| Object | Status | STYLESHEET | TORDF |", "|---|---|---|---|"]
        for r in todo:
            lines.append(f"| `{r['pid']}` | {r['status']} | {r['stylesheet'] if 'STYLESHEET' in r['todo'] else 'ok'} | {'szd-TORDF.xsl' if 'TORDF' in r['todo'] else 'ok'} |")
        lines.append("")
    lines += ["## Contents", "", "| Group | Object | File | Stylesheet |", "|---|---|---|---|"]
    lines += [f"| {r['group']} | `{r['pid']}` | `{r['file']}` | {r['stylesheet']} |" for r in table]
    lines += ["", "## Left out", ""]
    lines += [f"- `{p.name}`, the file does not name its own PID (defective production object)" for p in skipped]
    (args.out / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(table)} files, {len(skipped)} left out, {args.out}")


if __name__ == "__main__":
    main()
