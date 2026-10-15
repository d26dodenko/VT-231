from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional


class OrderValidationError(ValueError):
    """Ошибка валидации заказа."""


class PromoCodeError(ValueError):
    """Ошибка применения промокода."""


@dataclass
class OrderItem:
    name: str
    price: Decimal
    quantity: int
    weight_kg: Decimal


@dataclass
class Order:
    items: List[OrderItem]
    delivery_type: str = "standard"
    promo_code: Optional[str] = None


@dataclass
class OrderCalculationResult:
    items_total: Decimal
    regular_discount: Decimal
    promo_discount: Decimal
    delivery_cost: Decimal
    total_discount: Decimal
    final_total: Decimal


def money(value: Decimal) -> Decimal:
    """
    Округление денежных значений до двух знаков.
    """
    return value.quantize(Decimal("0.01"))


def validate_order(order: Order) -> None:
    """
    Проверяет корректность входных данных заказа.
    """

    if not isinstance(order, Order):
        raise OrderValidationError("Заказ должен быть объектом Order")

    if not order.items:
        raise OrderValidationError(
            "Заказ должен содержать хотя бы один товар"
        )

    if order.delivery_type not in {"standard", "express"}:
        raise OrderValidationError(
            "Тип доставки должен быть standard или express"
        )

    total_weight = Decimal("0")

    for item in order.items:
        if not item.name or not item.name.strip():
            raise OrderValidationError(
                "Наименование товара не может быть пустым"
            )

        if item.price <= Decimal("0"):
            raise OrderValidationError(
                "Цена товара должна быть больше нуля"
            )

        if not isinstance(item.quantity, int):
            raise OrderValidationError(
                "Количество товара должно быть целым числом"
            )

        if item.quantity <= 0:
            raise OrderValidationError(
                "Количество товара должно быть больше нуля"
            )

        if item.weight_kg <= Decimal("0"):
            raise OrderValidationError(
                "Вес товара должен быть больше нуля"
            )

        total_weight += item.weight_kg * item.quantity

    if order.delivery_type == "express" and total_weight > Decimal("20"):
        raise OrderValidationError(
            "Экспресс-доставка недоступна для заказов тяжелее 20 кг"
        )

    if order.promo_code not in {None, "WELCOME10", "SALE500"}:
        raise PromoCodeError("Неизвестный промокод")


def calculate_items_total(order: Order) -> Decimal:
    """
    Рассчитывает стоимость всех товаров без скидок и доставки.
    """

    total = sum(
        (
            item.price * item.quantity
            for item in order.items
        ),
        Decimal("0")
    )

    return money(total)


def calculate_regular_discount(items_total: Decimal) -> Decimal:
    """
    Рассчитывает скидку по общей сумме товаров.
    """

    if items_total < Decimal("5000"):
        discount = Decimal("0")
    elif items_total < Decimal("10000"):
        discount = items_total * Decimal("0.05")
    else:
        discount = items_total * Decimal("0.10")

    maximum_discount = Decimal("3000")

    return money(min(discount, maximum_discount))


def calculate_promo_discount(
    promo_code: Optional[str],
    amount_after_regular_discount: Decimal
) -> Decimal:
    """
    Рассчитывает скидку по промокоду.
    """

    if promo_code is None:
        return Decimal("0.00")

    if promo_code == "WELCOME10":
        discount = amount_after_regular_discount * Decimal("0.10")

    elif promo_code == "SALE500":
        discount = Decimal("500")

    else:
        raise PromoCodeError("Неизвестный промокод")

    # Ограничение: итоговая скидка не может быть больше 30%
    # от первоначальной суммы товаров.
    maximum_promo_discount = amount_after_regular_discount * Decimal("0.30")

    return money(min(discount, maximum_promo_discount))


def calculate_delivery_cost(
    order: Order,
    amount_after_discounts: Decimal
) -> Decimal:
    """
    Рассчитывает стоимость доставки.
    """

    # Бесплатная доставка от 3000 рублей после скидок.
    if amount_after_discounts >= Decimal("3000"):
        return Decimal("0.00")

    if order.delivery_type == "standard":
        return Decimal("300.00")

    if order.delivery_type == "express":
        return Decimal("600.00")

    raise OrderValidationError(
        "Неизвестный тип доставки"
    )


def calculate_order(order: Order) -> OrderCalculationResult:
    """
    Основная функция расчёта стоимости заказа.
    """

    validate_order(order)

    items_total = calculate_items_total(order)

    regular_discount = calculate_regular_discount(items_total)

    amount_after_regular_discount = (
        items_total - regular_discount
    )

    promo_discount = calculate_promo_discount(
        order.promo_code,
        amount_after_regular_discount
    )

    amount_after_all_discounts = (
        amount_after_regular_discount - promo_discount
    )

    delivery_cost = calculate_delivery_cost(
        order,
        amount_after_all_discounts
    )

    total_discount = regular_discount + promo_discount

    final_total = (
        amount_after_all_discounts + delivery_cost
    )

    return OrderCalculationResult(
        items_total=money(items_total),
        regular_discount=money(regular_discount),
        promo_discount=money(promo_discount),
        delivery_cost=money(delivery_cost),
        total_discount=money(total_discount),
        final_total=money(final_total),
    )