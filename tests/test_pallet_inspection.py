import pytest
from pallet_inspection import inspect_board

def test_01_ok_nominal():
    assert inspect_board(0.0, 145.0, "edge") == "ok"