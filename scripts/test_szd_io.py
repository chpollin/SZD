"""Checks for the shared file helpers in _szd_io.py."""
from __future__ import annotations

import csv

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
