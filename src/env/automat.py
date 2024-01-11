from pyglet.shapes import Rectangle
from pyglet.math import clamp
from copy import deepcopy

from src.env.life import LifeRule
from src.env.tilemap import TileMap


class Automat:
    SPEED_UP = 1
    SPEED_DOWN = 0

    def __init__(self, tile_map: TileMap) -> None:
        size = tile_map.get_size_map()
        self.present_map = [[0 for _ in range(size[0])] for _ in range(size[1])]
        self.future_map = [[0 for _ in range(size[0])] for _ in range(size[1])]

        self.tile_map = tile_map
        self.life_rule = LifeRule()
        self._init_tile_map_tiles()

        self.speed = 8.0
        self.is_paused = False

    def update_speed(self, speed_state: int) -> None:
        new_speed = clamp(self.speed * 2.0 if speed_state else self.speed / 2.0, 1.0, 32.0)
        self.speed = new_speed

    def _init_tile_map_tiles(self) -> None:
        for num_line in range(len(self.present_map)):
            for num_tile in range(len(self.present_map[0])):
                self.tile_map.set_tile(
                    (num_tile, num_line),
                    Rectangle(
                        x = 0,
                        y = 0,
                        width = self.tile_map.tile_size,
                        height = self.tile_map.tile_size,
                        color = self.life_rule.state_colors[self.present_map[num_line][num_tile]]
                    )
                )

    def set_tile(self, position: tuple[int, int], is_birth: bool = True) -> None:
        if 0 <= position[1] < len(self.present_map) and 0 <= position[0] < len(self.present_map[0]):
            self.present_map[position[1]][position[0]] = self.life_rule.states - 1 if is_birth else 0
            self.tile_map.get_tile((position[0], position[1])).color = self.life_rule.state_colors[self.present_map[position[1]][position[0]]]

    def update(self, _dt) -> None:
        for num_line in range(1, len(self.present_map) - 1):
            for num_tile in range(1, len(self.present_map[0]) - 1):

                if self.present_map[num_line][num_tile] == 0:
                    self.future_map[num_line][num_tile] = self.life_rule.states - 1 if self._get_neighbors_count((num_tile, num_line)) in self.life_rule.birth else 0
                elif self.present_map[num_line][num_tile] == self.life_rule.states - 1:
                    self.future_map[num_line][num_tile] = self.life_rule.states - 1 if self._get_neighbors_count((num_tile, num_line)) in self.life_rule.life else int(clamp(self.present_map[num_line][num_tile] - 1, 0, self.life_rule.states - 1))
                else:
                    self.future_map[num_line][num_tile] = int(clamp(self.present_map[num_line][num_tile] - 1, 0, self.life_rule.states - 1))

                if self.present_map[num_line][num_tile] != self.future_map[num_line][num_tile]:
                    self.tile_map.get_tile((num_tile, num_line)).color = self.life_rule.state_colors[self.future_map[num_line][num_tile]]

        self.present_map = deepcopy(self.future_map)

    def _get_neighbors_count(self, position: tuple[int, int]) -> int:
        neighbor_count = 0
        for num_line in range(position[1] - 1, position[1] + 2):
            for num_tile in range(position[0] - 1, position[0] + 2):
                if self.present_map[num_line][num_tile] == self.life_rule.states - 1 and (num_line != position[1] or num_tile != position[0]):
                    neighbor_count += 1

        return neighbor_count
