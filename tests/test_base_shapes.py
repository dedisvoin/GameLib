import importer
from src.app import AppWindow
from src.core.settings import CONST_WINDOW_MAX_FPS, CONST_WINDOW_CONSOLE_FPS

from src.render.base import draw_rect, draw_circle, draw_outline_rect
from src.render.colors import *

from src.inputs import *

window = AppWindow(vsync=False)  # Устанавливаем желаемую частоту кадров и выключаем вертикальную синхронизацию
window.set_view_information_in_title() # Включаем отображение информации в заголовке окна

mouse_object = Mouse()


colors = [
    COLOR_RED(),
    COLOR_ORANGE(),
    COLOR_YELLOW(),
    COLOR_GREEN(),
    COLOR_BLUE(),
    COLOR_PURPLE(),
    COLOR_PINK(),
    COLOR_GRAY(),
    COLOR_BLACK(),
    COLOR_WHITE(),
]
color_index = 0

while window.is_opened:
    window.fill()   
    draw_rect(window.surf, (100, 100), (100, 100), colors[color_index])
    draw_circle(window.surf, (300, 100), 100, COLOR_RED())
    draw_outline_rect(window.surf, mouse_object.get_position_on_windiw(), (300, 100), COLOR_GOLD(), radius=20)
    

    if mouse_object.get_click():
        color_index += 1
        if color_index >= len(colors):
            color_index = 0

    window.update()
    
    
    
    
    
    