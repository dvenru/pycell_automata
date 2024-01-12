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

        self.ui_batch = pgl.graphics.Batch()
        self.fps_label = pgl.window.FPSDisplay(window = self, color = (237, 242, 244, 200))
        self.fps_label.label.batch = self.ui_batch
        self.fps_label.label.x = 10
        self.fps_label.label.y = self.height
        self.fps_label.label.anchor_y = "top"

        self.speed_label = pgl.text.Label(
            x = self.width // 2,
            y = self.height,
            anchor_x = "center",
            anchor_y = "top",
            text = "SPEED: 8.0",
            color = (237, 242, 244, 200),
            font_size = 24,
            bold = True,
            batch = self.ui_batch
        )

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
                self.speed_label.text = f"SPEED: {self.automat.speed}"
            else:
                self.automat.is_paused = True
                pgl.clock.unschedule(self.automat.update)
                self.speed_label.text = "PAUSE"

        elif symbol == key.RIGHT and not self.automat.is_paused:
            pgl.clock.unschedule(self.automat.update)
            self.automat.update_speed(self.automat.SPEED_UP)
            pgl.clock.schedule_interval(self.automat.update, 1.0/self.automat.speed)
            self.speed_label.text = f"SPEED: {self.automat.speed}"
        elif symbol == key.LEFT and not self.automat.is_paused:
            pgl.clock.unschedule(self.automat.update)
            self.automat.update_speed(self.automat.SPEED_DOWN)
            pgl.clock.schedule_interval(self.automat.update, 1.0/self.automat.speed)
            self.speed_label.text = f"SPEED: {self.automat.speed}"

        # App control
        if symbol == key.ESCAPE:
            self.close()
        elif symbol == key.F11:
            self.set_fullscreen(not self.fullscreen)

    def on_draw(self) -> None:
        self.clear()
        self.tile_map.map_batch.draw()
        self.cursor.cursor_rect.draw()
        self.ui_batch.draw()
