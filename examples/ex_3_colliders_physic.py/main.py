import sys
sys.path.append('./')

from src.app import AppWindow



window = AppWindow([1500, 800], "Colliders!!", vsync=False)
window.set_view_information_in_window()
window.set_waited_fps(1000)



while window.is_opened:
    window.fill()

    window.update()