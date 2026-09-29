"""File helpers shared by the scripts that rewrite TEI under data/ and log what they change.

The data files are mixed, the index files carry LF and the konvolut files CRLF, and on
Windows a plain read_text/write_text pair turns one into the other. Reading and writing
with newline="" hands the text through unchanged, so a script that edits a few attributes
leaves every line terminator as it found it.

The scripts run as plain files (python scripts/<folder>/<script>.py), so this module is not
on the import path. They load it by file location:

    _spec = importlib.util.spec_from_file_location(
        "_szd_io", Path(__file__).resolve().parents[1] / "_szd_io.py"
    )
    szd_io = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(szd_io)

Standard library only.
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

# A person id as the index mints it, SZDPER.<n> with at most one letter suffix
# (SZDPER.2080a is a person of its own beside SZDPER.2080). The lookahead makes it a whole
# id: SZDPER.105 misses SZDPER.1056 and SZDPER.2080 misses SZDPER.2080a.
SZDPER_ID = re.compile(r"SZDPER\.\d+[a-z]?(?![0-9A-Za-z_])")


def person_id_pattern(person_id: str) -> re.Pattern[str]:
    """One given id as a whole id, with the same boundary as SZDPER_ID."""
    return re.compile(rf"{re.escape(person_id)}(?![0-9A-Za-z_])")


def console_utf8() -> None:
    """Write stdout and stderr as UTF-8.

    On Windows a redirected stream defaults to the ANSI code page, and a console that
    decodes the output as UTF-8 then shows "M�rz"; errors="replace" alone only hides the
    characters the code page lacks. Called from main(), never at import, so that tests
    keep their captured streams.
    """
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def read_text(path: Path) -> str:
    """Read without translating line terminators, so that a write reproduces them."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write_atomic(path: Path, text: str) -> None:
    """Replace the file in one step, writing the text's own line terminators unchanged.

    A crash leaves either the old file or the new one, never a half-written file.
    """
    temp = path.with_suffix(path.suffix + ".tmp")
    try:
        with temp.open("w", encoding="utf-8", newline="") as handle:
            handle.write(text)
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)


def append_log(path: Path, fieldnames: Sequence[str], rows: Iterable[Mapping]) -> int:
    """Append rows to a CSV log, writing the header only when the file is new or empty.

    The logs are provenance and committed with the data, so a later run adds to them and
    never replaces what an earlier run recorded. An existing header that differs from
    fieldnames stops the append, because rows under the wrong columns would corrupt the
    record. Returns the number of rows written.
    """
    rows = list(rows)
    fresh = not path.exists() or path.stat().st_size == 0
    if not fresh:
        with path.open("r", encoding="utf-8", newline="") as handle:
            header = next(csv.reader(handle), [])
        if header != list(fieldnames):
            raise ValueError(
                f"{path}: header {header} differs from {list(fieldnames)}, nothing appended"
            )
        with path.open("rb") as handle:
            handle.seek(-1, 2)
            missing_newline = handle.read(1) != b"\n"
    with path.open("a", encoding="utf-8", newline="") as handle:
        if not fresh and missing_newline:
            handle.write("\r\n")  # csv's own row terminator
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        if fresh:
            writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def _git(root: Path, *args: str, stdin: bytes | None = None) -> bytes:
    """Run git in root and return stdout; a failing call is a broken precondition."""
    result = subprocess.run(["git", "-C", str(root), *args], input=stdin, capture_output=True)
    if result.returncode != 0:
        message = result.stderr.decode(errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args)}: {message}")
    return result.stdout


def head_commit(root: Path) -> str:
    """Short hash of HEAD."""
    return _git(root, "rev-parse", "--short", "HEAD").decode().strip()


def head_revision(path: Path, root: Path) -> str | None:
    """The file's text at HEAD, or None where HEAD does not hold it."""
    rel = path.resolve().relative_to(root.resolve()).as_posix()
    result = subprocess.run(["git", "-C", str(root), "show", f"HEAD:{rel}"], capture_output=True)
    return result.stdout.decode("utf-8") if result.returncode == 0 else None


def head_files(root: Path, prefix: str, suffix: str = ".xml") -> dict[str, bytes]:
    """{repository path: bytes at HEAD} of every tracked file under prefix ending in suffix.

    Read in one git cat-file batch rather than one git show per file, because the Konvolut
    folder alone holds several hundred files. The bytes are the committed blobs, so their
    line endings do not depend on the autocrlf setting of the working tree.
    """
    listing = _git(root, "ls-tree", "-r", "-z", "HEAD", "--", prefix)
    entries: list[tuple[str, str]] = []
    for record in filter(None, listing.split(b"\x00")):
        meta, _, name = record.partition(b"\t")
        _, kind, sha = meta.decode().split()
        path = name.decode("utf-8")
        if kind == "blob" and path.endswith(suffix):
            entries.append((sha, path))
    request = "".join(f"{sha}\n" for sha, _ in entries).encode()
    out = _git(root, "cat-file", "--batch", stdin=request)
    files: dict[str, bytes] = {}
    at = 0
    for sha, path in entries:
        header_end = out.index(b"\n", at)
        got_sha, _, size = out[at:header_end].decode().split()
        if got_sha != sha:
            raise RuntimeError(f"git cat-file answered {got_sha} for {sha} ({path})")
        start = header_end + 1
        files[path] = out[start : start + int(size)]
        at = start + int(size) + 1
    return files


def uncommitted(root: Path, prefix: str) -> list[str]:
    """Paths under prefix whose working tree differs from HEAD, untracked files included."""
    status = _git(root, "status", "--porcelain", "-z", "--untracked-files=all", "--", prefix)
    records = iter(status.split(b"\x00"))
    paths: list[str] = []
    for entry in records:
        if len(entry) > 3:
            paths.append(entry[3:].decode("utf-8"))
            if entry[:1] in (b"R", b"C"):
                next(records, None)  # the source path of a rename or copy follows
    return paths
