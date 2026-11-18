def calculate_parking_fee(hours: float, vehicle_weight_tons: float, is_electric: bool) -> float:

    if hours < 0:
        raise ValueError("hours must be >= 0")
    if vehicle_weight_tons < 0:
        raise ValueError("vehicle_weight_tons must be >= 0")

    if hours >= 24:
        cost = 1000.0
    elif hours <= 2:
        cost = 150.0
    elif hours <= 8:
        cost = 400.0
    else:
        cost = 400.0 + (hours - 8) * 50.0

    if is_electric:
        cost *= 0.5

    return cost





