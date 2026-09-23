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
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

# A person id as the index mints it, SZDPER.<n> with at most one letter suffix
# (SZDPER.2080a is a person of its own beside SZDPER.2080). The lookahead makes it a whole
# id: SZDPER.105 misses SZDPER.1056 and SZDPER.2080 misses SZDPER.2080a.
SZDPER_ID = re.compile(r"SZDPER\.\d+[a-z]?(?![0-9A-Za-z_])")


def person_id_pattern(person_id: str) -> re.Pattern[str]:
    """One given id as a whole id, with the same boundary as SZDPER_ID."""
    return re.compile(rf"{re.escape(person_id)}(?![0-9A-Za-z_])")


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
