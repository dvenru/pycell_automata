def lerp(start_value: int | float, end_value: int | float, steps: int) -> list[float]:
    """
    Implementation of linear interpolation. The function returns a list[float] with initial
    values and intermediate values. The intermediate values are on equal segments.

    :param start_value:
    :param end_value:
    :param steps:
    :return:
    """

    inc = (end_value - start_value) / (steps + 1)
    return_list = [start_value]
    for _ in range(steps):
        return_list.append(return_list[-1] + inc)
    return_list.append(end_value)

    return return_list


def lerp_color(
        start_value: tuple[int, int, int] | tuple[int, int, int, int],
        end_value: tuple[int, int, int] | tuple[int, int, int, int],
        steps: int
) -> list[tuple[int, int, int] | tuple[int, int, int, int]]:
    """
    Implementation of linear interpolation. The function returns a list[tuple] with initial
    values and intermediate values. The intermediate values are on equal segments. The color
    can be transmitted in rgb(0 - 255) or rgba(0 - 255) format.

    :param start_value:
    :param end_value:
    :param steps:
    :return:
    """

    return_list = []
    for step in range(steps + 1):
        color = (
            lerp(start_value[0], end_value[0], steps)[step],
            lerp(start_value[1], end_value[1], steps)[step],
            lerp(start_value[2], end_value[2], steps)[step]
        )
        if len(start_value) == 4:
            color += (lerp(start_value[3], end_value[3], steps)[step])
        return_list.append(color)
    return_list.append(end_value)

    return return_list


print(lerp_color((0, 0, 0), (255, 255, 255), 4))
