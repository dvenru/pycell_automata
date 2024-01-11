import pyglet as pgl
from pyglet.math import Vec2
from pyglet.shapes import ShapeBase, Rectangle
from pyglet.sprite import Sprite

from typing import Union

# Creating a type for possible tile variations
TileType = Union[ShapeBase | Sprite | None]


class TileMap:

    def __init__(self, size: tuple[int, int], tile_size: int = 12, position: Vec2 = Vec2(0, 0)) -> None:
        self._map = [[None for _ in range(size[0])] for _ in range(size[1])]
        self._mask = [[0 for _ in range(size[0])] for _ in range(size[1])]

        self.tile_size = tile_size
        self._position = position

        self.map_batch = pgl.graphics.Batch()

    def set_position(self, position: Vec2) -> None:
        self._position = position
        self._update_position()

    def set_position_from_center(self, position: Vec2) -> None:
        self._position.x = position.x - (len(self._map[0]) * self.tile_size / 2)
        self._position.y = position.y - (len(self._map) * self.tile_size / 2)
        self._update_position()

    def get_position(self) -> Vec2:
        return self._position

    def set_tile(self, position: tuple[int, int], tile: TileType) -> None:
        if isinstance(tile, (ShapeBase, Sprite)):
            tile.position = position[0] * self.tile_size + self._position.x, position[1] * self.tile_size + self._position.y
            tile.batch = self.map_batch

        self._map[position[1]][position[0]] = tile

    def get_tile(self, position: tuple[int, int]) -> TileType:
        return self._map[position[1]][position[0]]

    def get_map(self) -> list[list[TileType]]:
        return self._map

    def set_mask_value(self, position: tuple[int, int], value: int) -> None:
        self._mask[position[1]][position[0]] = value

    def set_mask_from_dict(self, values: dict[tuple[int, int], int]) -> None:
        for position, value in values.items():
            self._mask[position[1]][position[0]] = value

    def get_mask_value(self, position: tuple[int, int]) -> int:
        return self._mask[position[1]][position[0]]

    def get_mask(self) -> list[list[int]]:
        return self._mask

    def _update_position(self) -> None:
        for y in range(len(self._map)):
            for x in range(len(self._map[0])):
                if isinstance(self._map[y][x], (ShapeBase, Sprite)):
                    self._map[y][x].position = x * self.tile_size + self._position.x, y * self.tile_size + self._position.y

    def get_size_map(self) -> tuple[int, int]:
        return len(self._map[0]), len(self._map)

    def get_size(self) -> tuple[int, int]:
        return len(self._map[0]) * self.tile_size, len(self._map) * self.tile_size