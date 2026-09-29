"""The century rule of fix_titles.py on real Konvolut entries.

The files are read at a fixed data commit rather than from the working tree, because an
applied run corrects exactly the dates these tests look at.
"""
from __future__ import annotations

import csv
import subprocess
import sys

import fix_titles as ft
import pytest

DATA_COMMIT = "2198922e"


def konvolut_at_commit(tmp_path, slug: str):
    rel = f"data/Correspondence/konvolute/szd.korrespondenzen.{slug}.xml"
    result = subprocess.run(["git", "-C", str(ft.REPO_ROOT), "show", f"{DATA_COMMIT}:{rel}"], capture_output=True)
    if result.returncode != 0:
        pytest.fail(f"{rel} not readable at {DATA_COMMIT}: {result.stderr.decode(errors='replace')}")
    path = tmp_path / f"szd.korrespondenzen.{slug}.xml"
    path.write_bytes(result.stdout)
    return path


def case_of(cases, xml_id):
    return next(c for c in cases if c.xml_id == xml_id)


@pytest.mark.parametrize(
    ("title_iso", "when", "fixed"),
    [
        ("1925-04-15", "2025-04-15", "1925-04-15"),  # SZDKOR.freud-sigmund.5
        ("1925", "2025-04-15", "1925-04-15"),
        ("1925-04-15", "1925-04-15", ""),  # nothing to correct
        ("1925-04-16", "2025-04-15", ""),  # differs beyond the century
        ("1935-04-15", "2025-04-15", ""),
    ],
)
def test_century_fix(title_iso, when, fixed):
    assert ft.century_fix(title_iso, when) == fixed


def test_title_proves_the_century(tmp_path):
    case = case_of(ft.collect([konvolut_at_commit(tmp_path, "freud-sigmund")]), "SZDKOR.freud-sigmund.5")
    assert not case.skip
    assert (case.when_old, case.when_new) == ("2025-04-15", "1925-04-15")
    assert case.new_de.endswith("[15. April 1925]")
    assert case.new_en.endswith(", 1925-04-15")


def test_title_without_date_stays_in_the_residual_list(tmp_path):
    case = case_of(ft.collect([konvolut_at_commit(tmp_path, "heidelbach-paul")]), "SZDKOR.heidelbach-paul.B.1")
    assert case.skip.startswith("Titel ohne Datum")
    assert case.when_new == ""


def test_apply_writes_the_date_and_logs_every_change(tmp_path, monkeypatch):
    path = konvolut_at_commit(tmp_path, "freud-sigmund")
    log = tmp_path / "titles_log.csv"
    monkeypatch.setattr(ft, "LOG", log)
    monkeypatch.setattr(sys, "argv", ["fix_titles.py", "--konvolute", str(tmp_path), "--apply"])
    assert ft.main() == 0
    assert 'when="1925-04-15"' in path.read_text(encoding="utf-8")
    with log.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    century = [r for r in rows if r["entry"] == "SZDKOR.freud-sigmund.5" and r["rule"] == "century"]
    assert [(r["old"], r["new"]) for r in century] == [("2025-04-15", "1925-04-15")]
    assert {r["file"] for r in rows} == {path.name}
    assert ft.collect([path]) == [] or all(c.skip for c in ft.collect([path]))
