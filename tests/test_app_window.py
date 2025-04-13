import importer
from src.app import AppWindow
from src.core.settings import CONST_WINDOW_MAX_FPS, CONST_WINDOW_CONSOLE_FPS

window = AppWindow(vsync=False).\
         set_waited_fps(CONST_WINDOW_MAX_FPS)   # Устанавливаем желаемую частоту кадров и выключаем вертикальную синхронизацию



window.set_view_information_in_title() # Включаем отображение информации в заголовке окна

while window.is_opened:
    window.fill()
    window.update()