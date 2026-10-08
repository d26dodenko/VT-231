import math

BOARD_NOMINAL_WIDTH_MM = {
    "edge": 145.0,    # крайние доски
    "center": 145.0,  # центральная доска
    "inner": 100.0,   # промежуточные доски
}

POSITION_TOLERANCE_MM = 5.0
WIDTH_TOLERANCE_MM = 3.0
STRICT_FACTOR = 0.5


def inspect_board(offset_mm: float, width_mm: float, board_type: str, strict: bool = False) -> str:
    """проверка одной доски"""
    if board_type not in BOARD_NOMINAL_WIDTH_MM:
        raise ValueError(f"unknown board_type: {board_type!r}")

    if offset_mm is None or width_mm is None:
        return "missing"

    if math.isnan(offset_mm) or math.isnan(width_mm):
        raise ValueError("measurements must not be NaN")
    if width_mm <= 0:
        raise ValueError("width_mm must be > 0")

    factor = STRICT_FACTOR if strict else 1.0
    pos_tol = POSITION_TOLERANCE_MM * factor
    width_tol = WIDTH_TOLERANCE_MM * factor

    if abs(width_mm - BOARD_NOMINAL_WIDTH_MM[board_type]) > width_tol:
        return "damaged"

    shift = abs(offset_mm)
    if shift <= pos_tol:
        return "ok"
    if shift <= 2 * pos_tol:
        return "shifted"
    return "rejected"
