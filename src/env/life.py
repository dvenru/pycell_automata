CONWAY_RULE = {
    "life": [0, 3, 4, 5],
    "birth": [2]
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

    def set_states(self, count_states: int, colors: list) -> None:
        self.states = count_states

        if len(colors) > 0:
            for index_color in range(len(colors)):
                self.state_colors[index_color] = colors[index_color]
        else:
            for index_color in range(count_states):
                if index_color == 0:
                    self.state_colors[0] = (162, 210, 255)
                else:
                    self.state_colors[index_color] = (255, 175, 204)
