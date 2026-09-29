"""Checks for the shared file helpers in _szd_io.py."""
from __future__ import annotations

import csv
import os
import subprocess
import sys
from pathlib import Path

import _szd_io as szd_io
import pytest

FIELDS = ["datei", "kontext", "aktion"]


def test_append_log_keeps_one_header_and_every_row(tmp_path):
    log = tmp_path / "log.csv"
    first = [{"datei": "a.xml", "kontext": "X.1", "aktion": "eins"}]
    second = [
        {"datei": "b.xml", "kontext": "X.2", "aktion": "zwei"},
        {"datei": "c.xml", "kontext": "X.3", "aktion": "drei"},
    ]
    szd_io.append_log(log, FIELDS, first)
    szd_io.append_log(log, FIELDS, second)
    with log.open(encoding="utf-8", newline="") as handle:
        lines = list(csv.reader(handle))
    assert lines == [FIELDS] + [list(row.values()) for row in first + second]


def test_append_log_refuses_a_foreign_header(tmp_path):
    log = tmp_path / "log.csv"
    log.write_text("andere,spalten\r\n", encoding="utf-8", newline="")
    with pytest.raises(ValueError):
        szd_io.append_log(log, FIELDS, [{"datei": "a", "kontext": "b", "aktion": "c"}])


def test_append_log_after_a_last_row_without_newline(tmp_path):
    log = tmp_path / "log.csv"
    log.write_text("datei,kontext,aktion\r\na.xml,X.1,eins", encoding="utf-8", newline="")
    szd_io.append_log(log, FIELDS, [{"datei": "b.xml", "kontext": "X.2", "aktion": "zwei"}])
    with log.open(encoding="utf-8", newline="") as handle:
        assert list(csv.reader(handle))[1:] == [["a.xml", "X.1", "eins"], ["b.xml", "X.2", "zwei"]]


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_read_and_write_keep_line_endings(tmp_path, newline):
    path = tmp_path / "file.xml"
    original = f"<a>{newline}  <b/>{newline}</a>{newline}".encode()
    path.write_bytes(original)
    szd_io.write_atomic(path, szd_io.read_text(path))
    assert path.read_bytes() == original
    assert not path.with_suffix(".xml.tmp").exists()


def test_whole_person_id():
    assert szd_io.SZDPER_ID.findall('ref="#SZDPER.2080a #SZDPER.105"') == [
        "SZDPER.2080a",
        "SZDPER.105",
    ]
    assert not szd_io.SZDPER_ID.search("SZDPER.12ab")
    pattern = szd_io.person_id_pattern("SZDPER.2080")
    assert not pattern.search("#SZDPER.2080a")
    assert not pattern.search("#SZDPER.20801")
    assert pattern.search('ref="#SZDPER.2080"')


def test_console_utf8_writes_umlauts_as_utf8_into_a_pipe():
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONIOENCODING", "PYTHONUTF8")}
    code = (
        "import importlib.util, sys; "
        f"s = importlib.util.spec_from_file_location('_szd_io', {str(Path(szd_io.__file__))!r}); "
        "m = importlib.util.module_from_spec(s); s.loader.exec_module(m); "
        "m.console_utf8(); print('M\u00e4rz'); print('M\u00e4rz', file=sys.stderr)"
    )
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, env=env, check=True)
    assert result.stdout.strip() == "März".encode()
    assert result.stderr.strip() == "März".encode()


# Reference values as they stand in the data (SZDPER.xml, SZDESS.xml, SZDKOR.xml).
@pytest.mark.parametrize(
    ("value", "ids"),
    [
        ("http://d-nb.info/gnd/1037465881 / http://d-nb.info/gnd/1037465261", ["1037465881", "1037465261"]),
        ("http://d-nb.info/gnd/118543628, http://d-nb.info/gnd/118563076", ["118543628", "118563076"]),
        ("https://d-nb.info/gnd/118527053; http://d-nb.info/gnd/118732641", ["118527053", "118732641"]),
        ("http://d-nb.info/gnd/1038039797 http://d-nb.info/gnd/116060891", ["1038039797", "116060891"]),
        (" http://d-nb.info/gnd/1217682775", ["1217682775"]),
        ("http://d-nb.info/gnd/7846367-1 ", ["7846367-1"]),
        ("http://d-nb.info/gnd/placeholder", ["placeholder"]),
        ("#SZDPER.42", []),
    ],
)
def test_gnd_ids_split_every_separator_of_the_data(value, ids):
    assert szd_io.gnd_ids(value) == ids
