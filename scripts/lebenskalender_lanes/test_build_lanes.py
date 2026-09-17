"""Coverage checks against the repository's complete correspondence corpus."""
from __future__ import annotations

import copy
import json
from collections import Counter
from pathlib import Path

import build_lanes as lanes
import pytest


@pytest.fixture(scope="module")
def corpus() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    by_gnd, names = lanes.load_person_index()
    report = lanes.Report()
    index = lanes.correspondence_from(lanes.SZDKOR, by_gnd, names, report)
    pieces = []
    for path in sorted(lanes.KONVOLUTE.glob("szd.korrespondenzen.*.xml")):
        pieces.extend(lanes.correspondence_from(path, by_gnd, names, report))
    return index, pieces


def test_every_source_record_and_its_metadata_survive(corpus) -> None:
    index, pieces = corpus
    before = copy.deepcopy(index + pieces)
    report = lanes.Report()
    by_gnd, names = lanes.load_person_index()
    events = lanes.build_correspondence(by_gnd, names, report)
    represented = [source for event in events for source in event.get("sources", [event])]
    expected = {event["href"]: event for event in before}
    assert len(index) == 765
    assert len(pieces) == 904
    assert len(represented) == len(expected) == 1669
    assert {event["href"]: event for event in represented} == expected
    assert len(events) == 1406
    assert len(report.merges) == 188
    assert sum(len(merge["folded"]) for merge in report.merges) == 263
    assert not report.problems


def test_partial_and_unrelated_bundle_records_remain(corpus) -> None:
    index, pieces = corpus
    events = lanes.merge_on_facsimile(index + pieces, lanes.Report())
    surviving = {event["id"]: event for event in events}
    assert {event["id"] for event in index} <= surviving.keys()
    for entry_id in ("SZDKOR.680", "SZDKOR.719", "SZDKOR.800", "SZDKOR.894"):
        assert surviving[entry_id] == next(event for event in index if event["id"] == entry_id)
    alberts = surviving["SZDKOR.681"]
    assert alberts["signature"] == "SZ-SAM/AK"
    assert "Margot Alberts" in alberts["title"]["de"]
    assert not any("alberts-margot" in event["href"] for event in pieces)


def test_facsimile_merge_keeps_different_source_dates_and_links(corpus) -> None:
    index, pieces = corpus
    before = copy.deepcopy(index + pieces)
    events = lanes.merge_on_facsimile(index + pieces, lanes.Report())
    merged = next(event for event in events if event["facsimile"] == "o:szd.1666")
    assert merged["date"] == "1934-08-31"
    assert merged["place"] == "Salzburg"
    assert {event["date"] for event in merged["sources"]} == {None, "1934-08-31"}
    assert len({event["href"] for event in merged["sources"]}) == 2
    assert index + pieces == before


@pytest.mark.parametrize(
    ("field", "value"),
    [("signature", "different"), ("signature", None), ("date", "1933-01-01"),
     ("dateEnd", "1935"), ("place", "London")],
)
def test_conflicting_facsimile_records_remain_separate(corpus, field: str, value: str | None) -> None:
    _, pieces = corpus
    original = next(event for event in pieces if event["facsimile"] == "o:szd.1666" and event["date"])
    changed = copy.deepcopy(original)
    changed["id"] = "conflicting-source"
    changed["href"] += "-conflicting-source"
    changed[field] = value
    report = lanes.Report()
    assert len(lanes.merge_on_facsimile([original, changed], report)) == 2
    assert not report.merges
    assert len(report.problems) == 1


def test_post_1950_dates_are_preserved_from_tei(corpus) -> None:
    _, pieces = corpus
    expected = {
        "SZDKOR.unidentified.041": "2012-05-26",
        "SZDKOR.unidentified.040": "2018-10-02",
        "SZDKOR.unidentified.039": "2030-09-23",
    }
    actual = {event["id"]: event["date"] for event in pieces if event["date"] and event["date"][:4] > "1950"}
    assert actual == expected


def test_generated_payload_matches_corpus_and_docs_copy(corpus) -> None:
    index, pieces = corpus
    report = lanes.Report()
    expected = sorted(lanes.merge_on_facsimile(index + pieces, report), key=lanes.sort_key)
    output = lanes.DEFAULT_OUT_DIR
    actual = json.loads((output / "correspondence.json").read_text(encoding="utf-8"))
    assert actual == expected
    manifest = json.loads((output / "index.json").read_text(encoding="utf-8"))
    assert manifest["suppressedIndexEntries"] == 0
    assert manifest["mergedDuplicates"] == 188
    assert manifest["mergedRecords"] == 263
    lane = next(lane for lane in manifest["lanes"] if lane["lane"] == "correspondence")
    assert lane["events"] == len(actual)
    assert lane["datePrecision"] == dict(Counter(event["datePrecision"] for event in actual))
    for name in [f"{lane}.json" for lane in lanes.LANES] + ["index.json"]:
        assert (output / name).read_bytes() == (lanes.DEFAULT_DOCS_DIR / name).read_bytes()


def test_lane_output_is_deterministic(corpus, tmp_path: Path) -> None:
    index, pieces = corpus
    for name in ("first", "second"):
        events = lanes.merge_on_facsimile(index + pieces, lanes.Report())
        lanes.write_json(tmp_path / name, sorted(events, key=lanes.sort_key))
    assert (tmp_path / "first").read_bytes() == (tmp_path / "second").read_bytes()
