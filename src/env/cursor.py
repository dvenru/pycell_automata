from pyglet.shapes import Rectangle

from src.env.tilemap import TileMap


class TileMapCursor:
    def __init__(self, tile_map: TileMap, color: tuple[int, int, int, int] = (255, 255, 255, 100)) -> None:
        self.tile_map = tile_map

        self.on_map_pos = (0, 0)

        self.color = color
        self.cursor_rect = Rectangle(
            x = 0,
            y = 0,
            width = self.tile_map.tile_size,
            height = self.tile_map.tile_size,
            color = color,
        )

        self.is_clicked = False
        self.focused_on_map = False

    def update_position(self, position: tuple[int, int]) -> None:
        if (self.tile_map.get_position().x < position[0] < self.tile_map.get_position().x + self.tile_map.get_size()[0]) and \
                (self.tile_map.get_position().y < position[1] < self.tile_map.get_position().y + self.tile_map.get_size()[1]):
            self.focused_on_map = True
            self.cursor_rect.visible = True

            map_x = (position[0] - self.tile_map.get_position().x) // self.tile_map.tile_size
            map_y = (position[1] - self.tile_map.get_position().y) // self.tile_map.tile_size
            self.on_map_pos = (int(map_x), int(map_y))

            self.cursor_rect.x = map_x * self.tile_map.tile_size + self.tile_map.get_position().x
            self.cursor_rect.y = map_y * self.tile_map.tile_size + self.tile_map.get_position().y
        else:
            self.focused_on_map = False
            self.cursor_rect.visible = False
