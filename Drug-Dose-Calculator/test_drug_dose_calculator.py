import math

import pytest
from maindrug import calculate_dose


def test_paracetamol_example_respects_displayed_daily_cap():
    result = calculate_dose("paracetamol", 100)

    assert result["dose"] == 1000
    assert result["max_doses_per_day"] == 4
    assert result["frequency"] == "No clinical schedule supplied"


@pytest.mark.parametrize("weight", [0, -1, math.nan, math.inf, -math.inf])
def test_rejects_non_finite_or_non_positive_weight(weight):
    with pytest.raises(ValueError):
        calculate_dose("ors", weight)


def test_rejects_unknown_drug():
    with pytest.raises(ValueError):
        calculate_dose("unknown", 20)

