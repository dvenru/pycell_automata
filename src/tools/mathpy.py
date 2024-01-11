def lerpi(start_value: int | float, end_value: int | float, steps: int) -> list[int | float]:
    if start_value > end_value:
        start_value, end_value = end_value, start_value

    inc = (end_value - start_value) / (steps + 1)
    return_list = [start_value]
    for _ in range(steps):
        return_list.append(return_list[-1] + inc)
    return_list.append(end_value)

    return return_list
