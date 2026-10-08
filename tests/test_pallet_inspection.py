import pytest
from pallet_inspection import inspect_board


def test_01_ok_nominal():
    assert inspect_board(0.0, 145.0, "edge") == "ok"


def test_02_shifted():
    assert inspect_board(7.0, 145.0, "center") == "shifted"


def test_03_rejected():
    assert inspect_board(15.0, 100.0, "inner") == "rejected"


def test_04_negative_offset_uses_abs():
    assert inspect_board(-7.0, 145.0, "edge") == "shifted"


@pytest.mark.parametrize("offset, expected", [
    (5.0, "ok"),
    (5.01, "shifted"),
    (10.0, "shifted"),
    (10.01, "rejected"),
])
def test_05_offset_boundaries(offset, expected):
    assert inspect_board(offset, 145.0, "edge") == expected


@pytest.mark.parametrize("width, expected", [
    (148.0, "ok"),
    (148.01, "damaged"),
    (141.99, "damaged"),
])
def test_06_width_boundaries(width, expected):
    assert inspect_board(0.0, width, "edge") == expected


def test_07_damaged_has_priority_over_shift():
    assert inspect_board(15.0, 120.0, "edge") == "damaged"


@pytest.mark.parametrize("offset, width", [(None, 145.0), (0.0, None), (None, None)])
def test_08_missing_board(offset, width):
    assert inspect_board(offset, width, "edge") == "missing"


def test_09_strict_mode_tightens_position_tolerance():
    assert inspect_board(3.0, 145.0, "edge", strict=False) == "ok"
    assert inspect_board(3.0, 145.0, "edge", strict=True) == "shifted"


@pytest.mark.parametrize("offset, expected", [(2.5, "ok"), (5.0, "shifted"), (5.01, "rejected")])
def test_10_strict_mode_boundaries(offset, expected):
    assert inspect_board(offset, 145.0, "edge", strict=True) == expected

def test_11_strict_mode_tightens_width_tolerance():
    assert inspect_board(0.0, 147.0, "edge", strict=False) == "ok"
    assert inspect_board(0.0, 147.0, "edge", strict=True) == "damaged"

def test_12_unknown_board_type():
    with pytest.raises(ValueError):
        inspect_board(0.0, 145.0, "diagonal")


def test_13_non_positive_width():
    with pytest.raises(ValueError):
        inspect_board(0.0, -145.0, "edge")

@pytest.mark.parametrize("offset, width", [(float("nan"), 145.0), (0.0, float("nan"))])
def test_14_nan_measurements(offset, width):
    with pytest.raises(ValueError):
        inspect_board(offset, width, "edge")