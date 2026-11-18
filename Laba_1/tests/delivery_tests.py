
import pytest

from Laba_1.delivery import calculate_delivery_cost


# Позитивные / граничные

def test_tc01_free_delivery_from_5000():
    assert calculate_delivery_cost(5000, 10, False) == 0.0


def test_tc02_paid_delivery_below_5000():
    assert calculate_delivery_cost(4999.99, 10, False) == 500.0


def test_tc03_short_distance_boundary_5():
    assert calculate_delivery_cost(1000, 5, False) == 200.0


def test_tc04_middle_distance_boundary_20():
    assert calculate_delivery_cost(1000, 20, False) == 500.0


def test_tc05_long_distance():
    assert calculate_delivery_cost(1000, 30, False) == 800.0


def test_tc10_zero_order_amount():
    assert calculate_delivery_cost(0, 0, False) == 200.0


def test_tc11_zero_distance():
    assert calculate_delivery_cost(1000, 0, False) == 200.0


#  Premium

def test_tc06_premium_discount():
    assert calculate_delivery_cost(1000, 10, True) == 250.0


def test_tc07_premium_with_free_delivery():
    assert calculate_delivery_cost(5000, 10, True) == 0.0


def test_tc12_premium_long_distance():
    assert calculate_delivery_cost(1000, 30, True) == 400.0


#  Негативные

def test_tc08_negative_order_amount():
    with pytest.raises(ValueError):
        calculate_delivery_cost(-1, 10, False)


def test_tc09_negative_distance():
    with pytest.raises(ValueError):
        calculate_delivery_cost(1000, -1, False)