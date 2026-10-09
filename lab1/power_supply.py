def calculate_total_power(cpu_power, gpu_power, other_power):
    if cpu_power <= 0:
        raise ValueError("CPU power must be greater than 0")

    if gpu_power < 0:
        raise ValueError("GPU power cannot be negative")

    if other_power < 0:
        raise ValueError("Other components power cannot be negative")

    total_power = cpu_power + gpu_power + other_power

    return total_power