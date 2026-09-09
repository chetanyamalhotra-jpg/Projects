import math

import pytest
from main import calculate_bmi, classify_bmi


@pytest.mark.parametrize(
    ("bmi", "expected"),
    [
        (18.49, "Underweight"),
        (18.5, "Healthy weight"),
        (25, "Overweight"),
        (30, "Obese"),
    ],
)
def test_bmi_category_boundaries(bmi, expected):
    assert classify_bmi(bmi) == expected


def test_calculates_bmi():
    assert calculate_bmi(72, 1.8) == pytest.approx(22.2222, rel=1e-4)


@pytest.mark.parametrize("height", [0, -1, math.nan, math.inf])
def test_rejects_invalid_height(height):
    with pytest.raises(ValueError):
        calculate_bmi(70, height)

