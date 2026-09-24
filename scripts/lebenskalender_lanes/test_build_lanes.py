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
    paths = sorted(lanes.KONVOLUTE.glob("szd.korrespondenzen.*.xml"))
    index = lanes.correspondence_from(
        lanes.SZDKOR, by_gnd, names, report, lanes.konvolut_pids(paths)
    )
    pieces = []
    for path in paths:
        pieces.extend(lanes.correspondence_from(path, by_gnd, names, report))
    return index, pieces


# Facsimile groups of the complete holdings whose records disagree on signature, date or
# place. Read from the run of 2026-09-24; each needs an editorial look, not a merge.
CONFLICTING_FACSIMILES = frozenset({
    "o:szd.1233", "o:szd.1235", "o:szd.1236", "o:szd.1237", "o:szd.1239", "o:szd.1240",
    "o:szd.1241", "o:szd.1242", "o:szd.1243", "o:szd.1244", "o:szd.1245", "o:szd.1246",
    "o:szd.1250", "o:szd.1257", "o:szd.1259", "o:szd.1262", "o:szd.1387", "o:szd.1388",
    "o:szd.1611", "o:szd.1614", "o:szd.1672", "o:szd.1733", "o:szd.3204", "o:szd.3317",
    "o:szd.769", "o:szd.798", "o:szd.821", "o:szd.858", "o:szd.909",
})
# Index entries naming a Konvolut PID for which the import found no production object.
MISSING_KONVOLUTE = {
    "SZDKOR.696": "o:szd.korrespondenzen.unbekannt",
    "SZDKOR.857": "o:szd.korrespondenzen.podbielski-gert-rene",
}


def canonical(events: list[dict[str, object]]) -> list[str]:
    """Multiset form, because two defective Konvolut files share one PID and so one href."""
    return sorted(json.dumps(event, sort_keys=True, ensure_ascii=False) for event in events)


def test_every_source_record_and_its_metadata_survive(corpus) -> None:
    index, pieces = corpus
    before = copy.deepcopy(index + pieces)
    report = lanes.Report()
    by_gnd, names = lanes.load_person_index()
    events = lanes.build_correspondence(by_gnd, names, report)
    represented = [source for event in events for source in event.get("sources", [event])]
    assert len(index) == 765
    assert len(pieces) == 2150
    assert len(represented) == len(before) == 2915
    assert canonical(represented) == canonical(before)
    assert len(events) == 2491
    assert len(report.merges) == 330
    assert sum(len(merge["folded"]) for merge in report.merges) == 424
    conflicts = {p.split()[1].rstrip(":") for p in report.problems if p.startswith("facsimile ")}
    assert conflicts == CONFLICTING_FACSIMILES
    assert len(report.problems) == len(CONFLICTING_FACSIMILES) + len(MISSING_KONVOLUTE)


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
    assert alberts["konvolut"] == "/o:szd.korrespondenzen.alberts-margot/sdef:TEI/get"
    assert any("/o:szd.korrespondenzen.alberts-margot/" in event["href"] for event in pieces)


def test_index_entries_link_their_konvolut_where_it_exists(corpus) -> None:
    index, pieces = corpus
    linked = [event for event in index if event["konvolut"]]
    assert len(linked) == 271
    for event in linked:
        pid = str(event["konvolut"]).split("/")[1]
        assert (lanes.KONVOLUTE / f"{pid[2:]}.xml").is_file()
    unlinked = {event["id"] for event in index if not event["konvolut"]}
    assert MISSING_KONVOLUTE.keys() <= unlinked
    assert all("konvolut" not in event for event in pieces)


def test_index_entries_carry_foreign_repository_and_extent(corpus) -> None:
    index, pieces = corpus
    by_id = {event["id"]: event for event in index}
    # The en dash is part of the repository name in SZDKOR.xml.
    reed = {"name": "Reed Library – Stefan Zweig Collection", "settlement": "Fredonia"}  # noqa: RUF001
    israel = {"name": "The National Library of Israel", "settlement": "Jerusalem"}
    bojer = by_id["SZDKOR.45"]
    assert bojer["repository"] == reed
    assert bojer["extent"] == [{"count": 55, "subtype": "received"}]
    assert bojer["konvolut"] is None
    assert by_id["SZDKOR.35"]["extent"] == [
        {"count": 2, "subtype": "sent"}, {"count": 1, "subtype": "received"}
    ]
    repositories = Counter(json.dumps(event["repository"]) for event in index)
    assert repositories == {"null": 273, json.dumps(reed): 489, json.dumps(israel): 3}
    assert all(event["repository"] is None for event in index if event["konvolut"])
    assert sum(1 for event in index if event["extent"]) == 765
    assert all("repository" not in event and "extent" not in event for event in pieces)


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
    # Each source text states a two-digit year that @when places in the 21st century; the
    # lanes keep the TEI value until the data is corrected.
    expected = {
        "SZDKOR.bahr-hermann.B.1": "2023-09-21",
        "SZDKOR.feld-leo.B.1": "2009-02-05",
        "SZDKOR.freud-sigmund.1": "2020-11-03",
        "SZDKOR.freud-sigmund.2": "2024-05-01",
        "SZDKOR.freud-sigmund.3": "2024-05-01",
        "SZDKOR.freud-sigmund.4": "2024-05-22",
        "SZDKOR.freud-sigmund.5": "2025-04-15",
        "SZDKOR.freud-sigmund.6": "2025-06-15",
        "SZDKOR.freud-sigmund.7": "2026-09-08",
        "SZDKOR.freud-sigmund.8": "2027-03-18",
        "SZDKOR.freud-sigmund.9": "2029-12-06",
        "SZDKOR.freud-sigmund.10": "2029-12-08",
        "SZDKOR.freud-sigmund.11": "2029-12-31",
        "SZDKOR.freud-sigmund.12": "2030-08-12",
        "SZDKOR.heidelbach-paul.B.1": "2008-11-22",
        "SZDKOR.heidelbach-paul.B.2": "2008-11-23",
        "SZDKOR.jeanrenaud.B.1": "2012-12-13",
        "SZDKOR.kaemmerer-ami.B.1": "2012-08-18",
        "SZDKOR.kaemmerer-ami.B.2": "2017-06-28",
        "SZDKOR.kaemmerer-ami.B.3": "2017-05-05",
        "SZDKOR.kaemmerer-ami.B.4": "2017-10-10",
        "SZDKOR.kaemmerer-ami.B.5": "2017-12-09",
        "SZDKOR.kaemmerer-ami.B.6": "2022-10-16",
        "SZDKOR.kaemmerer-maria.B.1": "2026-09-28",
        "SZDKOR.kaemmerer-maria.B.2": "2027-02-24",
        "SZDKOR.kaemmerer-maria.B.3": "2027-08-02",
        "SZDKOR.kubin-alfred.B.1": "2024-03-01",
        "SZDKOR.mees-friedrich-siegbert.B.1": "2024-05-09",
        "SZDKOR.mees-friedrich-siegbert.B.2": "2027-04-19",
        "SZDKOR.mees-friedrich-siegbert.B.3": "2027-05-16",
        "SZDKOR.mees-friedrich-siegbert.B.4": "2030-08-26",
        "SZDKOR.unidentified.039": "2030-09-23",
        "SZDKOR.unidentified.040": "2018-10-02",
        "SZDKOR.unidentified.041": "2012-05-26",
        "SZDKOR.winternitz-friderike-von.1": "2019-02-20",
    }
    actual = {event["id"]: event["date"] for event in pieces if event["date"] and event["date"][:4] > "1950"}
    assert actual == expected


def test_generated_payload_matches_corpus_and_docs_copy(corpus) -> None:
    index, pieces = corpus
    report = lanes.Report()
    expected = sorted(lanes.merge_on_facsimile(index + pieces, report), key=lanes.sort_key)
    output = lanes.DEFAULT_OUT_DIR
    actual = json.loads((output / "correspondence.json").read_text(encoding="utf-8"))
    assert actual == [lanes.slim(event) for event in expected]
    manifest = json.loads((output / "index.json").read_text(encoding="utf-8"))
    assert manifest["suppressedIndexEntries"] == 0
    assert manifest["mergedDuplicates"] == 330
    assert manifest["mergedRecords"] == 424
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
