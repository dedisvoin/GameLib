import importer

from src.maths import Vector2D

from src.app import AppWindow

from src.render.base import d

window = AppWindow([1000, 600], "Vector2D Tests")


while window.is_opened:
    window.fill()
    window.update()
    