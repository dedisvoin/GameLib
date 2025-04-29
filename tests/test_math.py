import importer
from src.app import AppWindow
from src.core.settings import CONST_WINDOW_MAX_FPS, CONST_WINDOW_CONSOLE_FPS

from src.maths import *

from src.render.base import draw_polygon, draw_circle, draw_rect
from src.inputs import MouseObject

window = AppWindow(vsync=True).\
         set_waited_fps(CONST_WINDOW_MAX_FPS)   # Устанавливаем желаемую частоту кадров и выключаем вертикальную синхронизацию

window.set_view_information_in_title() # Включаем отображение информации в заголовке окна
window.set_view_information_in_window()


points = [
    [200, 200],
    [300, 180],
    [350, 250],
    [300, 300],
    [200, 300],
    [200, 400],
    [100, 200]
]


rect_pos_1 = [800, 600]
rect_size_1 = [200, 100]
rect_size_2 = [70, 100]

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

    if collision_rect_rect([*rect_pos_1, *rect_size_1], [*MouseObject.get_position_on_window(), *rect_size_2]):
        draw_rect(window.surf, rect_pos_1, rect_size_1, "green")
    else:
        draw_rect(window.surf, rect_pos_1, rect_size_1, "red")

    draw_rect(window.surf, MouseObject.get_position_on_window(), rect_size_2, "blue")
    window.update()

    