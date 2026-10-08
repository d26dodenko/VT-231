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