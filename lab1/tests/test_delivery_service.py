import pytest

from delivery_service import (
    apply_discount,
    calculate_delivery_cost,
    calculate_final_cost,
)


@pytest.mark.parametrize(
    "distance, weight, express, expected",
    [
        (3, 2, False, 150),
        (5, 10, False, 150),
        (5.1, 2, False, 250),
        (20, 2, False, 250),
        (20.1, 2, False, 400),
        (10, 10.1, False, 400),
        (10, 12, False, 400),
        (10, 5, True, 450),
        (50, 10, False, 400),
    ],
)
def test_delivery_cost(distance, weight, express, expected):
    result = calculate_delivery_cost(distance, weight, express)
    assert result == expected


@pytest.mark.parametrize(
    "distance, weight",
    [
        (0, 5),
        (-1, 5),
        (10, 0),
        (10, -2),
        (50.1, 5),
    ],
)
def test_invalid_delivery_parameters(distance, weight):
    with pytest.raises(ValueError):
        calculate_delivery_cost(distance, weight)


@pytest.mark.parametrize(
    "amount, customer_type, expected",
    [
        (1000, "regular", 1000),
        (4999, "regular", 4999),
        (5000, "regular", 4750),
        (1000, "premium", 900),
        (5000, "premium", 4500),
    ],
)
def test_discount(amount, customer_type, expected):
    result = apply_discount(amount, customer_type)
    assert result == pytest.approx(expected)


@pytest.mark.parametrize(
    "amount, customer_type",
    [
        (0, "regular"),
        (-100, "regular"),
        (1000, "vip"),
        (1000, ""),
    ],
)
def test_invalid_discount_parameters(amount, customer_type):
    with pytest.raises(ValueError):
        apply_discount(amount, customer_type)


@pytest.mark.parametrize(
    "amount, distance, weight, customer_type, express, expected",
    [
        (3000, 3, 2, "regular", False, 3150),
        (5000, 10, 2, "regular", False, 5000),
        (2000, 25, 12, "premium", True, 2550),
        (6000, 5, 10, "premium", False, 5550),
    ],
)
def test_final_cost(
    amount,
    distance,
    weight,
    customer_type,
    express,
    expected,
):
    result = calculate_final_cost(
        amount,
        distance,
        weight,
        customer_type,
        express,
    )
    assert result == pytest.approx(expected)
