import src.tools.mathpy as math


CONWAY_RULE = {
    "life": [2, 3],
    "birth": [3]
}


class LifeRule:
    def __init__(self, rule: dict = None) -> None:
        self.states = 10
        self.life = []
        self.birth = []

        self.state_colors = {
            0: (162, 210, 255),
            1: (69, 123, 157),
            2: (29, 53, 87)
        }

        if rule is None:
            rule = CONWAY_RULE
            self.set_rule_from_dict(rule)
        else:
            self.set_rule_from_dict(rule)

    def set_rule_from_dict(self, rule: dict) -> None:
        for attr, value in rule.items():
            setattr(self, attr, value)

    def set_states(self, count_states: int, colors: list, create_gradient: bool = False) -> None:
        self.states = count_states

        if len(colors) == count_states:
            for index_color in range(len(colors)):
                self.state_colors[index_color] = colors[index_color]
        else:
            if len(colors) == 2 and create_gradient:
                r_list = math.lerpi(colors[0], colors[1], count_states - 2)
                g_list = math.lerpi(colors[0], colors[1], count_states - 2)
                b_list = math.lerpi(colors[0], colors[1], count_states - 2)
                for index_color in range(count_states):
                    self.state_colors[index_color] = (
                        r_list[index_color],
                        g_list[index_color],
                        b_list[index_color]
                    )
            for index_color in range(count_states):
                if index_color == 0:
                    self.state_colors[0] = (0, 0, 0)
                else:
                    self.state_colors[index_color] = (230, 57, 70)
