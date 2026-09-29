#!/usr/bin/env python3
"""Build a staging ingest package from the repository, with the Cirilo references still to set.

The package is a folder outside the repository (the operator's ingest workspace). It holds a
copy of every TEI file to ingest, grouped in the order the ingest needs, a SHA256SUMS file and a
README. The README lists, per object, the STYLESHEET and TORDF reference it must carry, read
live from the datastream redirects of gams-staging.uni-graz.at, so that only the references
that are missing, dead or end in an illegal character appear as work.

The files come from HEAD, not from the working tree, so the package is exactly the data state
of the commit its README names. Uncommitted changes under data/ are reported and left out,
because parallel sessions edit the working tree while a package is built.

Order matters: szd-TORDF.xsl resolves persons, repositories and corporate bodies against the
index objects on the instance at ingest time, so the indexes go in before everything else.

A konvolut whose TEI does not name its own PID is left out, because Cirilo takes the PID of a
new object from the file and would create a wrong object.

Before anything is written, scripts/check_data.py runs over the same HEAD files. A file that
is not well formed or a finding of a decided check outside its known exceptions stops the
build, the checks the operator has not decided (NFC, century, ref whitespace) only warn.

A staging answer other than a redirect, 400 or 404 (a server error, a timeout, no network) is
collected as an error instead of being read as "new object" or "reference to set". The package
is still written, its README lists the errors, and the exit code is 1.

Usage:

    python scripts/staging_package/build_staging_package.py --out <folder>
    python scripts/staging_package/build_staging_package.py --out <folder> --no-staging  # skip reading references

Standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import re
import shutil
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Shared file helpers, loaded by path because the scripts run as plain files.
_spec = importlib.util.spec_from_file_location("_szd_io", ROOT / "scripts" / "_szd_io.py")
szd_io = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(szd_io)
# Registered before it runs, because its dataclasses look their module up by name.
_spec = importlib.util.spec_from_file_location("check_data", ROOT / "scripts" / "check_data.py")
check_data = importlib.util.module_from_spec(_spec)
sys.modules["check_data"] = check_data
_spec.loader.exec_module(check_data)

STAGING = "https://gams-staging.uni-graz.at"
MIRROR = STAGING + "/gamsdev/pollin/szd/gams-www/"
PAUSE = 0.2
KONVOLUT_DIR = "data/Correspondence/konvolute/"

# (PID, file below data/, page stylesheet); every object also gets szd-TORDF.xsl.
# The three include wrappers render through szd-Index.xsl and are what Cirilo references today.
INDEXES = [
    ("o:szd.organisation", "Index/Organisation/SZDORG.xml", "szd-Organisationen.xsl"),
    ("o:szd.personen", "Index/Person/SZDPER.xml", "szd-Personenliste.xsl"),
    ("o:szd.standorte", "Index/Location/SZDSTA.xml", "szd-Standortliste.xsl"),
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

Group = tuple[str, str, list[tuple[str, str, str]]]  # (title, folder, [(PID, repo path, stylesheet)])


class StagingError(Exception):
    """Staging gave no answer this script can read as a state of the object."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def reference(pid: str, datastream: str) -> str:
    """The target of a datastream reference, or a short description of why there is none."""
    time.sleep(PAUSE)
    url = f"{STAGING}/archive/objects/{pid}/datastreams/{datastream}/content"
    try:
        OPENER.open(url, timeout=30).close()
        return "no redirect"
    except urllib.error.HTTPError as error:
        if error.code in (301, 302, 303, 307, 308):
            return error.headers.get("Location", "")
        if error.code == 400:
            return "illegal character at the end"
        if error.code == 404:
            return "missing"
        raise StagingError(f"{datastream}: HTTP {error.code}") from error
    except (urllib.error.URLError, TimeoutError) as error:
        raise StagingError(f"{datastream}: {error}") from error


def exists(pid: str) -> bool:
    """Whether staging holds the object; only a 404 means it does not."""
    time.sleep(PAUSE)
    try:
        urllib.request.urlopen(f"{STAGING}/{pid}/TEI_SOURCE", timeout=60).close()
        return True
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return False
        raise StagingError(f"TEI_SOURCE: HTTP {error.code}") from error
    except (urllib.error.URLError, TimeoutError) as error:
        raise StagingError(f"TEI_SOURCE: {error}") from error


def own_pid(stem: str, text: str) -> bool:
    """Whether the file names o:<file stem> as its PID, whitespace around tags ignored."""
    compact = re.sub(r">\s+|\s+<", lambda m: m.group(0).strip(), text)
    return f'<idno type="PID">o:{stem}</idno>' in compact


def package_groups(files: dict[str, bytes]) -> tuple[list[Group], list[str]]:
    """The ingest groups in ingest order, and the Konvolut files left out.

    A fixed index or holding file missing from HEAD aborts, because a package without it
    would ingest the holdings against a stale index.
    """
    for _, rel, _ in INDEXES + HOLDINGS:
        if f"data/{rel}" not in files:
            raise SystemExit(f"data/{rel} is not in HEAD, no package built")
    konvolute, skipped = [], []
    for path in sorted(p for p in files if p.startswith(KONVOLUT_DIR) and "/" not in p[len(KONVOLUT_DIR) :]):
        stem = Path(path).stem
        (konvolute if own_pid(stem, files[path].decode("utf-8")) else skipped).append(path)
    groups = [
        ("1 Indexes", "1-index", [(p, f"data/{f}", s) for p, f, s in INDEXES]),
        ("2 Holdings", "2-bestaende", [(p, f"data/{f}", s) for p, f, s in HOLDINGS]),
        ("3 Konvolute", "3-konvolute", [("o:" + Path(f).stem, f, "szd-Konvolut.xsl") for f in konvolute]),
    ]
    return groups, skipped


def inside_repository(path: Path) -> bool:
    return path.resolve().is_relative_to(ROOT)


def staging_state(pid: str, stylesheet: str) -> tuple[str, list[str]]:
    """(status, references to set) of one object on staging."""
    if not exists(pid):
        # a new object inherits TORDF from cirilo:TEI.szd, which points to the mirror,
        # but the generic TEI stylesheet, so only STYLESHEET is left to set after the ingest
        return "new", ["STYLESHEET"]
    todo = []
    for datastream, want in (("STYLESHEET", MIRROR + stylesheet), ("TORDF", MIRROR + "szd-TORDF.xsl")):
        if reference(pid, datastream) != want:
            todo.append(datastream)
    return "update", todo


def main() -> int:
    szd_io.console_utf8()
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--no-staging", action="store_true")
    args = parser.parse_args()

    if inside_repository(args.out):
        print(f"ERROR: --out {args.out} lies inside the repository, the package belongs outside it", file=sys.stderr)
        return 2
    pending = szd_io.uncommitted(ROOT, "data/")
    if pending:
        print(f"WARNING: {len(pending)} uncommitted paths under data/ stay out, the package holds HEAD:", file=sys.stderr)
        for path in pending:
            print(f"  {path}", file=sys.stderr)
    files = szd_io.head_files(ROOT, "data/")
    # A file that does not parse would break the ingest, and a new finding of a decided check
    # is a regression; both stop the package. Undecided checks only warn.
    print("data checks over HEAD (scripts/check_data.py):")
    if check_data.summarise(check_data.check(files)):
        print("ERROR: data checks failed, no package built", file=sys.stderr)
        return 1
    groups, skipped = package_groups(files)

    if args.out.exists():
        # only a folder this script wrote before is refreshed, and only its own parts: Cirilo writes
        # ingest.log into the folder it ingests from, and a rebuild during an ingest must not touch that
        if not (args.out / "SHA256SUMS").exists():
            print(f"ERROR: {args.out} exists and is not a package built by this script", file=sys.stderr)
            return 2
        for _, folder, _ in groups:
            if (args.out / folder).exists():
                shutil.rmtree(args.out / folder)
    sums, table, errors = [], [], []
    for title, folder, items in groups:
        target = args.out / folder
        target.mkdir(parents=True, exist_ok=True)
        for pid, source, stylesheet in items:
            name = Path(source).name
            content = files[source]
            (target / name).write_bytes(content)
            sums.append(f"{hashlib.sha256(content).hexdigest()}  {folder}/{name}")
            row = {"group": title, "pid": pid, "file": f"{folder}/{name}", "stylesheet": stylesheet, "status": "", "todo": []}
            if not args.no_staging:
                try:
                    row["status"], row["todo"] = staging_state(pid, stylesheet)
                except StagingError as error:
                    row["status"] = "error"
                    errors.append((pid, str(error)))
            table.append(row)
            print(pid, row["status"], ",".join(row["todo"]))

    revision = szd_io.head_commit(ROOT)
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
        "An existing object needs both references below before the ingest, a new one needs its STYLESHEET set after the ingest. Type or paste them so that nothing follows `.xsl`; a trailing character makes the reference unusable.",
        "",
        "- STYLESHEET: `" + MIRROR + "<stylesheet>`",
        "- TORDF: `" + MIRROR + "szd-TORDF.xsl`",
        "",
    ]
    if errors:
        lines += [f"## Staging not readable ({len(errors)} objects)", "", "Their status is unknown. Read them again before the ingest.", ""]
        lines += [f"- `{pid}`: {message}" for pid, message in errors]
        lines.append("")
    if not args.no_staging:
        todo = [r for r in table if r["todo"]]
        lines += [f"## References to set ({len(todo)} objects)", "", "| Object | Status | STYLESHEET | TORDF |", "|---|---|---|---|"]
        for r in todo:
            lines.append(f"| `{r['pid']}` | {r['status']} | {r['stylesheet'] if 'STYLESHEET' in r['todo'] else 'ok'} | {'szd-TORDF.xsl' if 'TORDF' in r['todo'] else 'ok'} |")
        lines.append("")
    lines += ["## Contents", "", "| Group | Object | File | Stylesheet |", "|---|---|---|---|"]
    lines += [f"| {r['group']} | `{r['pid']}` | `{r['file']}` | {r['stylesheet']} |" for r in table]
    lines += ["", "## Left out", ""]
    lines += [f"- `{Path(p).name}`, the file does not name its own PID (defective production object)" for p in skipped]
    (args.out / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(table)} files, {len(skipped)} left out, {args.out}")
    if errors:
        print(f"ERROR: staging did not answer readably for {len(errors)} objects, see the README", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
