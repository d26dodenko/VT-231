import pytest
from main import calculate_parking_fee

def test_daily_flat_rate():
    # Ровно 24 часа — суточный тариф
    assert calculate_parking_fee(24, 1.5, False) == 1000.0


def test_daily_flat_rate_boundary():
    # Больше 24 часов — суточный тариф
    assert calculate_parking_fee(30, 2.0, False) == 1000.0


def test_short_parking():
    # До 2 часов — тариф 150
    assert calculate_parking_fee(2, 1.2, False) == 150.0


def test_middle_parking():
    # От 2 до 8 часов — тариф 400
    assert calculate_parking_fee(5, 1.5, False) == 400.0


def test_long_parking():
    # Больше 8 часов — 400 + 50 за каждый час свыше 8
    assert calculate_parking_fee(10, 1.5, False) == 500.0


def test_electric_discount():
    # Электрический автомобиль — скидка 50%
    assert calculate_parking_fee(5, 1.5, True) == 200.0


def test_electric_daily_discount():
    # Суточный тариф со скидкой электрокара
    assert calculate_parking_fee(24, 1.5, True) == 500.0


def test_short_parking_fractional():
    # Дробные часы внутри первой категории
    assert calculate_parking_fee(1.5, 1.0, False) == 150.0


def test_negative_hours():
    # Отрицательное количество часов — ошибка
    with pytest.raises(ValueError):
        calculate_parking_fee(-1, 2.0, False)


def test_negative_weight():
    # Отрицательная масса автомобиля — ошибка
    with pytest.raises(ValueError):
        calculate_parking_fee(5, -0.5, False)


def test_boundary_just_below_24():
    # Граничное значение перед суточным тарифом (23.99 часа)
    assert calculate_parking_fee(23.99, 1.5, False) == 1199.5