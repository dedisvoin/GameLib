import importer
from src.inputs import Mouse, Keyboard, MouseObject, KeyboardObject, InputsHandler
from src.core.settings import CONST_MOUSE_BUTTON_MIDDLE, CONST_MOUSE_BUTTON_LEFT, CONST_MOUSE_BUTTON_RIGHT

from src.app import AppWindow
from src.core.settings import CONST_WINDOW_MAX_FPS, CONST_WINDOW_CONSOLE_FPS

from src.core.settings import CONST_MOUSE_BUTTON_PRESS_EVENT, CONST_MOUSE_BUTTON_CLICK_EVENT, CONST_KEY_PRESS_EVENT, CONST_KEY_CLICK_EVENT, CONST_MOUSE_BUTTON_DOUBLE_CLICK_EVENT



window = AppWindow(vsync=False)  # Устанавливаем желаемую частоту кадров и выключаем вертикальную синхронизацию
window.set_view_information_in_title() # Включаем отображение информации в заголовке окна

handler = InputsHandler()
handler.add_event(CONST_MOUSE_BUTTON_PRESS_EVENT, 'mouse_press', CONST_MOUSE_BUTTON_RIGHT)
handler.add_event(CONST_MOUSE_BUTTON_CLICK_EVENT, 'mouse_click', CONST_MOUSE_BUTTON_LEFT)
handler.add_event(CONST_KEY_PRESS_EVENT, 'key_press', 'a')
handler.add_event(CONST_KEY_CLICK_EVENT, 'key_click', 'd')
handler.add_event(CONST_MOUSE_BUTTON_DOUBLE_CLICK_EVENT, 'mous', CONST_MOUSE_BUTTON_MIDDLE)
i = 0
while window.is_opened:
    window.fill()
    handler.update()
    
    if handler.get_event('mouse_press'):
        print('mouse_press')
    if handler.get_event('mouse_click'):
        print('mouse_click')
    if handler.get_event('key_press'):
        print('key_press')
    if handler.get_event('key_click'):
        print('key_click')
    if handler.get_event('mous'):
        print('mouse_double_click')

    window.update()

    

    
