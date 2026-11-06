def calculate_delivery_cost(distance_km, weight_kg, express=False):
    if distance_km <= 0:
        raise ValueError("Distance must be greater than 0")

    if weight_kg <= 0:
        raise ValueError("Weight must be greater than 0")

    if distance_km <= 5:
        cost = 150
    elif distance_km <= 20:
        cost = 250
    elif distance_km <= 50:
        cost = 400
    else:
        raise ValueError("Delivery is unavailable for this distance")

    if weight_kg > 10:
        cost += 150

    if express:
        cost += 200

    return cost


def apply_discount(order_amount, customer_type):
    if order_amount <= 0:
        raise ValueError("Order amount must be greater than 0")

    if customer_type not in ("regular", "premium"):
        raise ValueError("Unknown customer type")

    if customer_type == "premium":
        return order_amount * 0.90

    if order_amount >= 5000:
        return order_amount * 0.95

    return order_amount


def calculate_final_cost(
    order_amount,
    distance_km,
    weight_kg,
    customer_type="regular",
    express=False,
):
    discounted_amount = apply_discount(order_amount, customer_type)
    delivery_cost = calculate_delivery_cost(distance_km, weight_kg, express)

    return discounted_amount + delivery_cost
