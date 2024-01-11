import pyglet as pg

from core.app import AppWindow


if __name__ == '__main__':
    app = AppWindow(
        width = 1600,
        height = 900,
        vsync = False,
        resizable = False,
        caption = "PyCell"
    )
    pg.app.run()
