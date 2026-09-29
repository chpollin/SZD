"""Checks for build_staging_package.py against the committed data and a stubbed staging."""
from __future__ import annotations

import io
import urllib.error

import build_staging_package as bsp
import pytest

KONVOLUTE = bsp.ROOT / "data" / "Correspondence" / "konvolute"
# Production objects whose files name no PID of their own (knowledge/plan.md, Konvolute).
DEFECTIVE = {
    "szd.korrespondenzen.judischer-jugendverein",
    "szd.korrespondenzen.judischer-jugendverein-dusseldorf",
    "szd.korrespondenzen.rascher-und-cie",
}


@pytest.fixture(scope="module")
def head() -> dict[str, bytes]:
    return bsp.szd_io.head_files(bsp.ROOT, "data/")


@pytest.mark.parametrize("stem", sorted(DEFECTIVE))
def test_defective_konvolute_do_not_name_their_own_pid(stem):
    assert not bsp.own_pid(stem, (KONVOLUTE / f"{stem}.xml").read_text(encoding="utf-8"))


def test_own_pid_of_a_sound_konvolut_and_across_line_breaks():
    stem = "szd.korrespondenzen.freud-sigmund"
    assert bsp.own_pid(stem, (KONVOLUTE / f"{stem}.xml").read_text(encoding="utf-8"))
    assert bsp.own_pid("szd.x", '<idno type="PID">\r\n   o:szd.x\r\n</idno>')
    assert not bsp.own_pid("szd.x", '<idno type="PID">o:szd.x.y</idno>')


def test_groups_follow_the_ingest_order(head):
    groups, skipped = bsp.package_groups(head)
    assert [folder for _, folder, _ in groups] == ["1-index", "2-bestaende", "3-konvolute"]
    indexes, holdings, konvolute = (items for _, _, items in groups)
    assert {pid for pid, _, _ in indexes} == {
        "o:szd.organisation", "o:szd.personen", "o:szd.standorte", "o:szd.werkindex",
    }
    assert holdings[0][0] == "o:szd.korrespondenzen"
    assert all(stylesheet == "szd-Konvolut.xsl" for _, _, stylesheet in konvolute)
    assert all(pid == "o:" + path.rsplit("/", 1)[1][:-4] for pid, path, _ in konvolute)
    assert {path.rsplit("/", 1)[1][:-4] for path in skipped} == DEFECTIVE
    assert len(konvolute) + len(skipped) == sum(1 for p in head if p.startswith(bsp.KONVOLUT_DIR))


def test_out_inside_the_repository_is_refused(tmp_path):
    assert bsp.inside_repository(bsp.ROOT / "tmp-package")
    assert not bsp.inside_repository(tmp_path)


def _raise(code: int):
    def opener(*args, **kwargs):
        raise urllib.error.HTTPError("url", code, "stub", {}, io.BytesIO())
    return opener


def test_only_404_means_new_and_other_errors_are_collected(monkeypatch):
    monkeypatch.setattr(bsp, "PAUSE", 0)
    monkeypatch.setattr(bsp.urllib.request, "urlopen", _raise(404))
    assert bsp.staging_state("o:szd.x", "szd-Konvolut.xsl") == ("new", ["STYLESHEET"])
    monkeypatch.setattr(bsp.urllib.request, "urlopen", _raise(500))
    with pytest.raises(bsp.StagingError):
        bsp.staging_state("o:szd.x", "szd-Konvolut.xsl")
    monkeypatch.setattr(bsp.urllib.request, "urlopen", lambda *a, **k: io.BytesIO())
    monkeypatch.setattr(bsp.OPENER, "open", _raise(503))
    with pytest.raises(bsp.StagingError):
        bsp.staging_state("o:szd.x", "szd-Konvolut.xsl")


def test_redirects_decide_which_references_to_set(monkeypatch):
    monkeypatch.setattr(bsp, "PAUSE", 0)
    monkeypatch.setattr(bsp.urllib.request, "urlopen", lambda *a, **k: io.BytesIO())
    targets = {"STYLESHEET": bsp.MIRROR + "szd-Konvolut.xsl", "TORDF": bsp.MIRROR + "szd-TORDF.xsl "}

    def redirect(url, **kwargs):
        location = targets[url.split("/datastreams/")[1].split("/")[0]]
        raise urllib.error.HTTPError(url, 302, "Found", {"Location": location}, io.BytesIO())

    monkeypatch.setattr(bsp.OPENER, "open", redirect)
    assert bsp.staging_state("o:szd.x", "szd-Konvolut.xsl") == ("update", ["TORDF"])
