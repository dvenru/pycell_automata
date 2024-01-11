import pyglet as pgl
from pyglet.math import Vec2
from pyglet.window import key, mouse

from src.env.tilemap import TileMap
from src.env.automat import Automat
from src.env.cursor import TileMapCursor


class AppWindow(pgl.window.Window):

    def __init__(self, *args, **kwargs) -> None:
        super(AppWindow, self).__init__(*args, **kwargs)

        self.tile_map = TileMap((100, 100), 15)
        self.tile_map.set_position_from_center(Vec2(self.width / 2, self.height / 2))

        self.cursor = TileMapCursor(self.tile_map)

        custom_rule = {
            "life": [0, 3, 4, 5],
            "birth": [2]
        }

        self.automat = Automat(self.tile_map, custom_rule)
        self.automat.life_rule.set_states(11, [(0, 0, 0), (230, 57, 70)], True)
        self.automat.update_colors()

        self.fps_label = pgl.window.FPSDisplay(window = self)

        pgl.clock.schedule_interval(self.automat.update, 1.0/self.automat.speed)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.cursor.focused_on_map:
            if button == mouse.LEFT:
                self.automat.set_tile(self.cursor.on_map_pos)
            elif button == mouse.RIGHT:
                self.automat.set_tile(self.cursor.on_map_pos, False)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        self.cursor.update_position((x, y))

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons, modifiers) -> None:
        self.cursor.update_position((x, y))

    def on_key_press(self, symbol, modifiers) -> None:
        # Speed control
        if symbol == key.SPACE:
            if self.automat.is_paused:
                self.automat.is_paused = False
                pgl.clock.schedule_interval(self.automat.update, 1.0/self.automat.speed)
            else:
                self.automat.is_paused = True
                pgl.clock.unschedule(self.automat.update)

        elif symbol == key.RIGHT:
            pgl.clock.unschedule(self.automat.update)
            self.automat.update_speed(self.automat.SPEED_UP)
            pgl.clock.schedule_interval(self.automat.update, 1.0/self.automat.speed)
        elif symbol == key.LEFT:
            pgl.clock.unschedule(self.automat.update)
            self.automat.update_speed(self.automat.SPEED_DOWN)
            pgl.clock.schedule_interval(self.automat.update, 1.0/self.automat.speed)

    def on_draw(self) -> None:
        self.clear()
        self.tile_map.map_batch.draw()
        self.cursor.cursor_rect.draw()
        self.fps_label.draw()
