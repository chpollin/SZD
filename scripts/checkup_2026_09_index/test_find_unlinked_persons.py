"""NFC handling of the name search in find_unlinked_persons.py, against the real corpus.

SZDPER.21 is written decomposed in the person index (e + combining grave accent), while
the autograph holding writes the same surname composed. The search has to meet both.
"""
from __future__ import annotations

import unicodedata

import find_unlinked_persons as fup
import pytest

DECOMPOSED = "Ampère"
COMPOSED = unicodedata.normalize("NFC", DECOMPOSED)
AUTOGRAPHS = fup.DATA / "Autograph" / "SZDAUT.xml"


@pytest.fixture(scope="module")
def ampere() -> fup.Person:
    if DECOMPOSED not in fup.SZDPER_FILE.read_text(encoding="utf-8"):
        pytest.fail("SZDPER.xml no longer carries the decomposed form this test is built on")
    return next(p for p in fup.load_persons() if p.pid == "SZDPER.21")


def test_index_names_are_read_as_nfc(ampere):
    assert ampere.surname == COMPOSED
    assert all(unicodedata.is_normalized("NFC", v) for v in ampere.variants)


def test_decomposed_index_name_finds_the_composed_text(ampere):
    assert COMPOSED in AUTOGRAPHS.read_text(encoding="utf-8")
    index = fup.TextIndex([fup.load_doc(AUTOGRAPHS, "data/Autograph/SZDAUT.xml", False)])
    hits, _ = fup.search_person(ampere, index)
    assert hits
    assert index.candidates(DECOMPOSED) == index.candidates(COMPOSED)
