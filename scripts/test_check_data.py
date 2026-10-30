"""check_data.py over the real corpus, and its detectors on values taken from that corpus.

The synthetic TEI snippets below cover what the corpus cannot show (a broken file, a new
dangling reference), because a test must not wait for the data to break.
"""
from __future__ import annotations

import io

import check_data as cd
import pytest


@pytest.fixture(scope="module")
def corpus_report() -> cd.Report:
    return cd.check(cd.working_tree_files(cd.REPO_ROOT))


def test_corpus_has_no_unexpected_finding(corpus_report):
    assert corpus_report.unexpected() == []
    assert cd.summarise(corpus_report, out=io.StringIO()) == 0


def test_every_finding_belongs_to_a_declared_check(corpus_report):
    assert {f.check for f in corpus_report.findings} <= cd.FATAL | cd.ENFORCED | cd.WARN


@pytest.mark.parametrize(
    ("text", "chars"),
    [
        ("Ã\u0096sterreich", ["Ö"]),  # the example of datenkorrektur_2026_09_29/fix_mojibake.py
        ("H\u00c3\u00b4tel", ["\u00f4"]),
        ("â\u0080\u0099", ["\u2019"]),
        ("Österreich, Hôtel, Ã la", []),  # correct text; "Ã " is no UTF-8 sequence
        # SZDKLA src-wiki-1973 and src-wiki-313: "ß" before a closing quote reads as an NKo letter
        ("mit dem “Anschluß” Österreichs", []),
        ("zum Lesebuch ‘Kompaß’]", []),
        ("×©×œ×•×", ["ש", "ל", "ו"]),  # a double-encoded Hebrew word stays a run of sequences
    ],
)
def test_mojibake(text, chars):
    assert cd.mojibake(text) == chars


@pytest.mark.parametrize(
    ("value", "valid"),
    [
        ("1911-07-10", True), ("2025", True), ("1927-09", True), ("-0525", True),
        ("2019-03-21+01:00", True), ("1934-02-29", False), ("", False), ("1925-13", False),
        ("19.3.1925", False),
    ],
)
def test_valid_date(value, valid):
    assert cd.valid_date(value) is valid


@pytest.mark.parametrize(
    ("number", "valid"),
    [("118637479", True), ("11850357X", True), ("1217682775", True), ("7846367-1", True),
     ("2131189-4", True), ("38379-X", True), ("11055719711", False), ("placeholder", False)],
)
def test_gnd_form(number, valid):
    assert bool(cd.GND_ID.fullmatch(number)) is valid


TEI_HEAD = '<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body>'
TEI_TAIL = "</body></text></TEI>"


def test_fatal_and_new_findings_fail():
    files = {
        "data/a.xml": b"<TEI><unclosed></TEI>",
        "data/b.xml": (TEI_HEAD + '<p xml:id="X.1"><persName ref="#SZDPER.999999 ; #X.1"/></p>'
                       '<p xml:id="X.1"/>' + TEI_TAIL).encode(),
    }
    report = cd.check(files)
    assert {f.check for f in report.unexpected()} == {
        "wellformed", "dangling-ref", "ref-separator", "duplicate-id",
    }
    assert cd.summarise(report, out=io.StringIO()) == 1


def test_warn_findings_do_not_fail():
    files = {"data/c.xml": (TEI_HEAD + '<p><persName ref=" http://d-nb.info/gnd/118637479">Ampère</persName></p>'
                            + TEI_TAIL).encode()}
    report = cd.check(files)
    assert {f.check for f in report.findings} == {"nfc", "ref-whitespace"}
    assert cd.summarise(report, out=io.StringIO()) == 0
