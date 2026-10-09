# test_rental.py
import pytest
from rental import calculate_rental_cost


#  Позитивные тесты (TC01 - TC04)

def test_minimal_ride():
    """TC01: минимальная поездка — базовый тариф."""
    assert calculate_rental_cost(1, 5, False) == 100.0


def test_base_tariff_middle():
    """TC02: середина базового тарифа."""
    assert calculate_rental_cost(15, 5, False) == 100.0


def test_second_tariff_middle():
    """TC03: второй тариф, середина (45 мин)."""
    assert calculate_rental_cost(45, 5, False) == 175.0


def test_distance_surcharge():
    """TC04: доплата за расстояние (15 км)."""
    assert calculate_rental_cost(30, 15, False) == 200.0


#  Граничные тесты (TC05 - TC09)

def test_base_tariff_upper_bound():
    """TC05: ровно 30 минут — верхняя граница базового тарифа."""
    assert calculate_rental_cost(30, 5, False) == 100.0


def test_second_tariff_start():
    """TC06: 31 минута — начало второго тарифа."""
    assert calculate_rental_cost(31, 5, False) == 105.0


def test_second_tariff_upper_bound():
    """TC07: ровно 60 минут — верхняя граница второго тарифа."""
    assert calculate_rental_cost(60, 5, False) == 250.0


def test_third_tariff_start():
    """TC08: 61 минута — начало третьего тарифа."""
    assert calculate_rental_cost(61, 5, False) == 258.0


def test_no_distance_surcharge_at_10():
    """TC09: ровно 10 км — доплаты нет."""
    assert calculate_rental_cost(30, 10, False) == 100.0


#  Негативные тесты (TC10 - TC11)

def test_negative_minutes():
    """TC10: отрицательное время — ValueError."""
    with pytest.raises(ValueError):
        calculate_rental_cost(-1, 5, False)


def test_negative_distance():
    """TC11: отрицательное расстояние — ValueError."""
    with pytest.raises(ValueError):
        calculate_rental_cost(10, -1, False)


#  Скидка (TC12 - TC13)

def test_student_discount():
    """TC12: скидка студента 30% (базовая)."""
    assert calculate_rental_cost(30, 5, True) == 70.0


def test_student_discount_with_surcharge():
    """TC13: скидка студента + доплата за километры."""
    # база 250 + 1*8 = 258; доплата (15-10)*20 = 100; итого 358; скидка 358*0.7 = 250.6
    assert calculate_rental_cost(61, 15, True) == pytest.approx(250.6)


#  Бесплатная поездка (TC14 - TC15)

def test_zero_minutes():
    """TC14: нулевая поездка — стоимость 0."""
    assert calculate_rental_cost(0, 5, False) == 0.0


def test_zero_minutes_with_student():
    """TC15: нулевая поездка со скидкой — всё равно 0."""
    assert calculate_rental_cost(0, 5, True) == 0.0
