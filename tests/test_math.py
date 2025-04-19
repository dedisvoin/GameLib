import importer
from src.app import AppWindow
from src.core.settings import CONST_WINDOW_MAX_FPS, CONST_WINDOW_CONSOLE_FPS

from src.maths import *

from src.render.base import draw_polygon, draw_circle, draw_rect
from src.inputs import MouseObject

window = AppWindow(vsync=False).\
         set_waited_fps(CONST_WINDOW_MAX_FPS)   # Устанавливаем желаемую частоту кадров и выключаем вертикальную синхронизацию

window.set_view_information_in_title() # Включаем отображение информации в заголовке окна



points = [
    [200, 200],
    [300, 180],
    [350, 250],
    [300, 300],
    [200, 300],
    [200, 400],
    [100, 200]
]


while window.is_opened:
    window.fill()
    if point_in_polygon(MouseObject.get_position_on_window(), points):
        draw_polygon(window.surf, points, "green")
    else:
        draw_polygon(window.surf, points, "red")

    if point_in_circle(MouseObject.get_position_on_window(), [500, 250, 100]):
        draw_circle(window.surf, [500, 250], 100, "green")
    else:
        draw_circle(window.surf, [500, 250], 100, "red")
    window.update()