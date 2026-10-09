def calculate_total_power(cpu_power, gpu_power, other_power):
    if cpu_power <= 0:
        raise ValueError("CPU power must be greater than 0")

    if gpu_power < 0:
        raise ValueError("GPU power cannot be negative")

    if other_power < 0:
        raise ValueError("Other components power cannot be negative")

    total_power = cpu_power + gpu_power + other_power

    return total_power


def recommend_psu(cpu_power, gpu_power, other_power):
    total_power = calculate_total_power(cpu_power, gpu_power, other_power)

    required_power = total_power * 1.2

    psu_options = [450, 550, 650, 750, 850, 1000]

    for psu in psu_options:
        if psu >= required_power:
            return psu

    raise ValueError("No suitable power supply found")