"""fix_double_encoding.py on strings taken from the corpus before the repair of 2026-10-13."""
from __future__ import annotations

import fix_double_encoding as fde
import pytest


@pytest.mark.parametrize(
    ("damaged", "repaired", "steps"),
    [
        ("HÃ´tel-Château", "Hôtel-Château", 1),  # freud-sigmund, correct "â" beside a damaged "ô"
        ("dâ\x80\x99Antibes", "d’Antibes", 1),  # freud-sigmund, latin-1 C1 form
        ("dâ€™Antibes", "d’Antibes", 1),  # the cp1252 form of the same damage
        ("L&apos;Ã\x89glise", "L&apos;Église", 1),  # unidentified
        ("Schloss |Â\xa0Kleiner", "Schloss |\xa0Kleiner", 1),  # unidentified
        ("zusammenzufÃ\x83Â¼hren", "zusammenzuführen", 2),  # rascher-und-cie, damaged twice
    ],
)
def test_damage_is_reversed_and_provably_lossless(damaged, repaired, steps):
    result = fde.repair_text(damaged)
    assert result.text == repaired
    assert [r.steps for r in result.repairs] == [steps]
    assert fde.lossless(damaged, result)


@pytest.mark.parametrize(
    "correct",
    [
        "Sterngewölbe",
        "Havre. –\xa0L'Église",
        "LIVRARIA CIVILIZAÇÃO</title>",  # SZDLEB.xml
        "Ollendorff, 1922 (L'Âme",  # SZDESS.xml
        "Château\r\n",
    ],
)
def test_correct_text_is_untouched(correct):
    result = fde.repair_text(correct)
    assert result.text == correct
    assert result.repairs == [] and result.ambiguous == []


def test_cluster_decoding_to_a_control_character_is_left_as_ambiguous():
    result = fde.repair_text("aÂ\x85b")
    assert result.text == "aÂ\x85b"
    assert result.repairs == []
    assert [cluster for _, cluster, _ in result.ambiguous] == ["Â\x85"]
