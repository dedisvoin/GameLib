import importer
from src.app import AppWindow
from src.core.settings import CONST_WINDOW_MAX_FPS, CONST_WINDOW_CONSOLE_FPS

from src.render.base import draw_rect, draw_circle, draw_outline_rect
from src.render.colors import *

from src.inputs import MouseObject

window = AppWindow(vsync=False)  # Устанавливаем желаемую частоту кадров и выключаем вертикальную синхронизацию
window.set_view_information_in_title() # Включаем отображение информации в заголовке окна

mouse_object = MouseObject()

while window.is_window_opened:
    window.fill_bg()   
    draw_rect(window.surf, (100, 100), (100, 100), COLOR_ORANGE())
    draw_circle(window.surf, (300, 100), 100, COLOR_RED())
    draw_outline_rect(window.surf, mouse_object.get_position_on_windiw(), (300, 100), COLOR_GOLD(), radius=20)
    
    print(window.get_window_pos)

    window.update()
    
    
    
    
    
    