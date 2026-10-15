
import pytest
from lab1 import calculate_delivery_cost



def test_free_delivery_from_5000():
    # Сумма 5000 доставка бесплатная
    assert calculate_delivery_cost(5000, 10, False) == 0.0


def test_free_delivery__premium():
    #бесплатная доставка и премиум
    assert calculate_delivery_cost(5000, 10, True) == 0.0


def test_premium_long_distance():
    #премиум и большая дистанция больше 20 км
    assert calculate_delivery_cost(2000, 30, True) == 400.0


def test_paid_delivery_below_5000():
    # Сумма 4999.99 доставка платная
    assert calculate_delivery_cost(4999.99, 10, False) == 500.0

def test_zero_order_amount():
    # 0 рублей, доставка платная
    assert calculate_delivery_cost(0, 2, False) == 200.0


def test_short_distance():
    # До 5 км тариф 200
    assert calculate_delivery_cost(1000, 5, False) == 200.0


def test_middle_distance():
    # От 5 до 20 км — тариф 500
    assert calculate_delivery_cost(1000, 20, False) == 500.0


def test_long_distance():
    # Больше 20 км — 500 + 30 за каждый км
    assert calculate_delivery_cost(1000, 30, False) == 800.0


def test_premium_discount():
    # Premium — скидка 50%
    assert calculate_delivery_cost(1000, 10, True) == 250.0


def test_negative_order_amount():
    # Отрицательная сумма — ошибка
    with pytest.raises(ValueError):
        calculate_delivery_cost(-1, 10, False)


def test_negative_distance():
    # Отрицательное расстояние, то есть ошибка
    with pytest.raises(ValueError):
        calculate_delivery_cost(1000, -1, False)


def test_zero_distance():
    # тариф 200 (граница снизу) и 0
    assert calculate_delivery_cost(1000, 0, False) == 200.0


def test_boundary_5_1_km():
    # 5.1 км тариф меняется на 500
    assert calculate_delivery_cost(1000, 5.1, False) == 500.0


def test_boundary_20_1_km():
    # 500 + (20.1 - 20) * 30 = 503
    assert calculate_delivery_cost(1000, 20.1, False) == pytest.approx(503.0)


def test_boundary_4999_99_premium():
    # 4999.99 + премиум: 500 * 0.5 = 250
    assert calculate_delivery_cost(4999.99, 10, True) == 250.0


def test_boundary_5000_exact():
    # Ровно 5000 граница бесплатной доставки (даже с длинной дистанцией)
    assert calculate_delivery_cost(5000, 100, False) == 0.0