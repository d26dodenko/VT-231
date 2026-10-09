def calculate_rental_cost(minutes: int, distance_km: float, is_student: bool) -> float:
    """
    Расчёт стоимости аренды электросамоката.

    Бизнес-правила:
    1. Если minutes < 0 или distance_km < 0 — ValueError.
    2. Если minutes == 0 — поездка не состоялась, стоимость 0.
    3. Иначе:
       - первая часть поездки до 30 минут: 100 (базовый тариф)
       - 30 < minutes <= 60: 100 + (minutes - 30) * 5
       - minutes > 60: 250 + (minutes - 60) * 8
    4. За каждый км свыше 10 добавляется 20 (доплата за износ).
    5. Для is_student=True применяется скидка 30% на итоговую стоимость.
    """
    if minutes < 0:
        raise ValueError("minutes must be >= 0")
    if distance_km < 0:
        raise ValueError("distance_km must be >= 0")

    if minutes == 0:
        base = 0.0
    elif minutes <= 30:
        base = 100.0
    elif minutes <= 60:
        base = 100.0 + (minutes - 30) * 5.0
    else:
        base = 250.0 + (minutes - 60) * 8.0

    if distance_km > 10:
        base += (distance_km - 10) * 20.0

    if is_student:
        base *= 0.7

    return base
