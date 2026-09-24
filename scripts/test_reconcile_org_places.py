"""Checks for the GND-derived country/settlement mapping in reconcile_org_places.py.

Covers the logic that is not obvious from reading the code once: the area-code-to-country
table including subdivision and historical codes, the ambiguity rules that make the script
add nothing rather than guess, the England/Großbritannien split for XA-GB, and the anchor
that places new <country>/<settlement> elements after the last <orgName> while preserving
indentation and the existing element order.
"""
from __future__ import annotations

import reconcile_org_places as rop


def _place(area_codes=(), top_level_labels=(), place_labels=()) -> rop.GndPlace:
    return rop.GndPlace(area_codes=area_codes, top_level_labels=top_level_labels, place_labels=place_labels)


def test_subdivision_and_historical_codes_resolve_to_the_country():
    assert rop._area_code_to_country("XA-DE-NW") == "Deutschland"
    assert rop._area_code_to_country("XA-AT-9") == "Österreich"
    assert rop._area_code_to_country("XA-DXDE") == "Deutschland"
    assert rop._area_code_to_country("XA-DDDE") == "Deutschland"
    assert rop._area_code_to_country("ZZ") is None
    assert rop._area_code_to_country("XP") is None
    assert rop._area_code_to_country("XA-IT") is None  # not in the table, never guessed


def test_settlement_needs_exactly_one_distinct_place():
    single = _place(place_labels=("Berlin",))
    assert rop._resolve_settlement(single) == ("Berlin", "")

    several = _place(place_labels=("Zürich", "Leipzig", "Wien"))
    settlement, note = rop._resolve_settlement(several)
    assert settlement is None and "uneindeutig" in note

    none_at_all = _place()
    assert rop._resolve_settlement(none_at_all) == (None, "")


def test_settlement_that_is_only_the_country_name_is_not_a_place():
    # SZDORG.38: geo "XA-AT" (top-level, label "Österreich"), placeOfBusiness "Österreich".
    austria_only = _place(area_codes=("XA-AT",), top_level_labels=("Österreich",), place_labels=("Österreich",))
    settlement, note = rop._resolve_settlement(austria_only)
    assert settlement is None
    assert "nennt nur den Staat" in note

    # A subdivision code's own label ("Berlin" for XA-DE-BE) must NOT suppress a real
    # placeOfBusiness "Berlin" reached through a different, non-subdivision code.
    berlin = _place(area_codes=("XA-DXDE", "XA-DE-BE"), top_level_labels=("Deutschland, Deutsches Reich",), place_labels=("Berlin",))
    assert rop._resolve_settlement(berlin) == ("Berlin", "")


def test_country_needs_exactly_one_distinct_country():
    single = _place(area_codes=("XA-DE-NW",))
    assert rop._resolve_country(single, settlement="Bonn") == ("Deutschland", "")

    several = _place(area_codes=("XA-AT-9", "XA-CH-ZH", "XA-DXDE"))
    country, note = rop._resolve_country(several, settlement=None)
    assert country is None and "uneindeutig" in note

    unmapped = _place(area_codes=("XA-IT",))
    country, note = rop._resolve_country(unmapped, settlement=None)
    assert country is None and "nicht in der Ländertabelle" in note

    only_ignored = _place(area_codes=("ZZ",))
    assert rop._resolve_country(only_ignored, settlement=None) == (None, "")


def test_gb_uses_england_with_a_known_city_and_grossbritannien_without():
    with_city = _place(area_codes=("XA-GB",), place_labels=("London",))
    assert rop._resolve_country(with_city, settlement="London") == ("England", "")

    without_city = _place(area_codes=("XA-GB",))
    assert rop._resolve_country(without_city, settlement=None) == ("Großbritannien", "")


def test_bare_gnd_ids_from_http_https_and_several_whitespace_separated():
    assert rop._bare_gnd_ids("http://d-nb.info/gnd/2140517-7") == ["2140517-7"]
    assert rop._bare_gnd_ids("https://d-nb.info/gnd/35565-3") == ["35565-3"]
    assert rop._bare_gnd_ids("http://d-nb.info/gnd/1-X http://d-nb.info/gnd/2-Y") == ["1-X", "2-Y"]


def _sole_org_and_text(org_text: str) -> tuple["rop.OrgEntry", str]:
    """Parse a single <org>...</org> snippet (no leading indentation, as ORG_RE itself
    captures it) embedded in a one-line file, and return the entry plus the exact
    substring run() would pass to _insert_country_settlement (text[block_start:block_end]).
    """
    text = org_text + "\n"
    entry = rop._parse_orgs(text)[0]
    return entry, text[entry.block_start : entry.block_end]


def test_insert_adds_country_then_settlement_after_the_last_orgname():
    org_text = (
        '<org xml:id="SZDORG.2">\n'
        '          <orgName ref="http://d-nb.info/gnd/2131189-4">American Guild</orgName>\n'
        "        </org>"
    )
    entry, sliced = _sole_org_and_text(org_text)
    new_block = rop._insert_country_settlement(
        sliced, entry, {"country": "USA", "settlement": "New York, NY"}, newline="\n"
    )
    assert new_block == (
        '<org xml:id="SZDORG.2">\n'
        '          <orgName ref="http://d-nb.info/gnd/2131189-4">American Guild</orgName>\n'
        "          <country>USA</country>\n"
        "          <settlement>New York, NY</settlement>\n"
        "        </org>"
    )


def test_insert_uses_the_files_own_line_ending():
    # SZDORG.xml is CRLF throughout; a hard-coded "\n" would leave the two new lines as the
    # only bare-LF lines in the file.
    org_text = '<org xml:id="SZDORG.2">\r\n          <orgName>American Guild</orgName>\r\n        </org>'
    entry, sliced = _sole_org_and_text(org_text)
    new_block = rop._insert_country_settlement(sliced, entry, {"country": "USA"}, newline="\r\n")
    assert "\r\n          <country>USA</country>\r\n" in new_block
    assert "\n" not in new_block.replace("\r\n", "")


def test_insert_settlement_only_goes_after_an_existing_country():
    org_text = (
        '<org xml:id="SZDORG.9">\n'
        "          <orgName>Biblioteca Central</orgName>\n"
        "          <country>Brasilien</country>\n"
        "        </org>"
    )
    entry, sliced = _sole_org_and_text(org_text)
    assert entry.has_country and not entry.has_settlement
    new_block = rop._insert_country_settlement(sliced, entry, {"settlement": "Petrópolis"}, newline="\n")
    assert new_block == (
        '<org xml:id="SZDORG.9">\n'
        "          <orgName>Biblioteca Central</orgName>\n"
        "          <country>Brasilien</country>\n"
        "          <settlement>Petrópolis</settlement>\n"
        "        </org>"
    )
