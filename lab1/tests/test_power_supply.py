import pytest

from power_supply import calculate_total_power, recommend_psu, check_power_supply


@pytest.mark.parametrize(
    "cpu, gpu, other, expected",
    [
        (125, 320, 55, 500),
        (65, 0, 35, 100),
        (65, 75, 0, 140),
    ]
)
def test_total_power(cpu, gpu, other, expected):
    result = calculate_total_power(cpu, gpu, other)
    assert result == expected


@pytest.mark.parametrize(
    "cpu, gpu, other",
    [
        (0, 200, 50),
        (-10, 200, 50),
        (100, -50, 50),
        (100, 200, -10),
    ]
)
def test_invalid_components(cpu, gpu, other):
    with pytest.raises(ValueError):
        calculate_total_power(cpu, gpu, other)


@pytest.mark.parametrize(
    "cpu, gpu, other, expected",
    [
        (125, 320, 55, 650),
        (181, 360, 60, 750),
        (125, 200, 50, 450),
        (125, 200, 51, 550),
        (125, 450, 50, 750),
        (125, 450, 51, 850),
    ]
)
def test_recommend_psu(cpu, gpu, other, expected):
    result = recommend_psu(cpu, gpu, other)
    assert result == expected


def test_recommend_psu_over_limit():
    with pytest.raises(ValueError):
        recommend_psu(200, 650, 50)


@pytest.mark.parametrize(
    "cpu, gpu, other, psu, expected",
    [
        (125, 320, 55, 650, True),
        (125, 320, 55, 600, True),
        (125, 320, 55, 599, False),
        (65, 0, 35, 120, True),
        (65, 0, 35, 119, False),
        (181, 360, 60, 750, True),
        (181, 360, 60, 700, False),
    ]
)
def test_check_power_supply(cpu, gpu, other, psu, expected):
    result = check_power_supply(cpu, gpu, other, psu)
    assert result == expected


@pytest.mark.parametrize(
    "psu",
    [0, -1]
)
def test_invalid_psu(psu):
    with pytest.raises(ValueError):
        check_power_supply(125, 320, 55, psu)