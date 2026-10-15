from decimal import Decimal

import pytest

from Lab1.order_pricing import calculate_order, OrderItem, Order, OrderValidationError, PromoCodeError

def item(
    name="Товар",
    price="1000",
    quantity=1,
    weight="1"
):
    return OrderItem(
        name=name,
        price=Decimal(price),
        quantity=quantity,
        weight_kg=Decimal(weight),
    )

#1. Сумма меньше 5000, стандартная платная доставка
def test_order_without_discount_with_standard_delivery():
    order = Order(
        items=[item(price="1000", quantity=2)],
        delivery_type="standard",
    )

    result = calculate_order(order)

    assert result.items_total == Decimal("2000.00")
    assert result.regular_discount == Decimal("0.00")
    assert result.promo_discount == Decimal("0.00")
    assert result.delivery_cost == Decimal("300.00")
    assert result.final_total == Decimal("2300.00")

#2. Сумма ровно 5000, должна примениться скидка 5%
def test_discount_starts_at_5000():
    order = Order(
        items=[item(price="5000")],
        delivery_type="standard",
    )

    result = calculate_order(order)

    assert result.regular_discount == Decimal("250.00")
    assert result.delivery_cost == Decimal("0.00")
    assert result.final_total == Decimal("4750.00")

#3. Сумма чуть меньше 5000, скидка отсутствует
def test_no_discount_below_5000():
    order = Order(
        items=[item(price="4999.99")],
        delivery_type="standard",
    )

    result = calculate_order(order)

    assert result.regular_discount == Decimal("0.00")
    assert result.delivery_cost == Decimal("0.00")
    assert result.final_total == Decimal("4999.99")

#4. Сумма ровно 10000, должна примениться скидка 10%
def test_discount_10_percent_starts_at_10000():
    order = Order(
        items=[item(price="10000")],
        delivery_type="standard",
    )

    result = calculate_order(order)

    assert result.regular_discount == Decimal("1000.00")
    assert result.delivery_cost == Decimal("0.00")
    assert result.final_total == Decimal("9000.00")

#5. Промокод WELCOME10
def test_welcome10_promo_code():
    order = Order(
        items=[item(price="5000")],
        promo_code="WELCOME10",
        delivery_type="standard",
    )

    result = calculate_order(order)

    assert result.regular_discount == Decimal("250.00")
    assert result.promo_discount == Decimal("475.00")
    assert result.final_total == Decimal("4275.00")

#6. Промокод SALE500
def test_sale500_promo_code():
    order = Order(
        items=[item(price="7000")],
        promo_code="SALE500",
        delivery_type="standard",
    )

    result = calculate_order(order)

    assert result.regular_discount == Decimal("350.00")
    assert result.promo_discount == Decimal("500.00")
    assert result.final_total == Decimal("6150.00")

#7. Бесплатная доставка при сумме после скидок ровно 3000
def test_free_delivery_at_exactly_3000_after_discount():
    order = Order(
        items=[item(price="3000.00")],
        delivery_type="standard",
    )

    result = calculate_order(order)

    # Скидка отсутствует, итог 3000.
    assert result.delivery_cost == Decimal("0.00")

#8. Бесплатная доставка при большой сумме
def test_free_delivery_for_large_order():
    order = Order(
        items=[item(price="10000")],
        delivery_type="express",
    )

    result = calculate_order(order)

    assert result.delivery_cost == Decimal("0.00")

#9. Вес экспресс-доставки ровно 20 кг разрешён
def test_express_delivery_allowed_at_20_kg():
    order = Order(
        items=[item(price="1000", weight="20")],
        delivery_type="express",
    )

    result = calculate_order(order)

    assert result.final_total == Decimal("1600.00")

#10. Вес больше 20 кг запрещает экспресс-доставку
def test_express_delivery_forbidden_over_20_kg():
    order = Order(
        items=[item(price="1000", weight="20.01")],
        delivery_type="express",
    )

    with pytest.raises(
        OrderValidationError,
        match="тяжелее 20 кг"
    ):
        calculate_order(order)

#11. Пустой заказ
def test_empty_order_is_invalid():
    order = Order(items=[])

    with pytest.raises(
        OrderValidationError,
        match="хотя бы один товар"
    ):
        calculate_order(order)

#12. Цена равна нулю
def test_zero_price_is_invalid():
    order = Order(
        items=[item(price="0")]
    )

    with pytest.raises(
        OrderValidationError,
        match="Цена товара"
    ):
        calculate_order(order)

#13. Отрицательная цена
def test_negative_price_is_invalid():
    order = Order(
        items=[item(price="-100")]
    )

    with pytest.raises(
        OrderValidationError,
        match="Цена товара"
    ):
        calculate_order(order)

#14. Количество равно нулю
def test_zero_quantity_is_invalid():
    order = Order(
        items=[item(quantity=0)]
    )

    with pytest.raises(
        OrderValidationError,
        match="Количество товара"
    ):
        calculate_order(order)

#15. Отрицательное количество
def test_negative_quantity_is_invalid():
    order = Order(
        items=[item(quantity=-1)]
    )

    with pytest.raises(
        OrderValidationError,
        match="Количество товара"
    ):
        calculate_order(order)

#16. Количество является дробным
def test_fractional_quantity_is_invalid():
    order = Order(
        items=[item(quantity=1.5)]
    )

    with pytest.raises(
        OrderValidationError,
        match="целым числом"
    ):
        calculate_order(order)

#17. Неизвестный промокод
def test_unknown_promo_code_is_invalid():
    order = Order(
        items=[item(price="5000")],
        promo_code="UNKNOWN",
    )

    with pytest.raises(
        PromoCodeError,
        match="Неизвестный промокод"
    ):
        calculate_order(order)

#18. Пустой промокод считается неизвестным
def test_empty_promo_code_is_invalid():
    order = Order(
        items=[item(price="5000")],
        promo_code="",
    )

    with pytest.raises(
        PromoCodeError,
        match="Неизвестный промокод"
    ):
        calculate_order(order)

#19. Неизвестный тип доставки
def test_unknown_delivery_type_is_invalid():
    order = Order(
        items=[item(price="1000")],
        delivery_type="drone",
    )

    with pytest.raises(
        OrderValidationError,
        match="Тип доставки"
    ):
        calculate_order(order)

#20. Несколько товаров
def test_order_with_multiple_items():
    order = Order(
        items=[
            item(name="Ноутбук", price="7000", quantity=1),
            item(name="Мышь", price="1000", quantity=2),
        ],
        delivery_type="standard",
    )

    result = calculate_order(order)

    assert result.items_total == Decimal("9000.00")
    assert result.regular_discount == Decimal("450.00")
    assert result.delivery_cost == Decimal("0.00")
    assert result.final_total == Decimal("8550.00")

#21. скидка ограничивается суммой 3000 рублей
def test_regular_discount_is_limited_to_3000():
    order = Order(
        items=[item(price="100000")],
        delivery_type="standard",
    )

    result = calculate_order(order)

    assert result.regular_discount == Decimal("3000.00")
    assert result.delivery_cost == Decimal("0.00")
    assert result.final_total == Decimal("97000.00")

#22. Пустое название товара
def test_empty_item_name_is_invalid():
    order = Order(
        items=[item(name="   ")]
    )

    with pytest.raises(
        OrderValidationError,
        match="Наименование товара"
    ):
        calculate_order(order)

#23. Нулевой вес товара
def test_zero_weight_is_invalid():
    order = Order(
        items=[item(weight="0")]
    )

    with pytest.raises(
        OrderValidationError,
        match="Вес товара"
    ):
        calculate_order(order)