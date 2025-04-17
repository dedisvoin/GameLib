import importer

from src.app import AppWindow, AppProcess, AppProcessesPool, AppSubProcess

from src.inputs import KeyboardObject

from math import sin
from src.render.base import draw_circle

window = AppWindow([1000, 600], "AppSubProcessesPool Tests", vsync=False)
window.set_waited_fps(240)

window.set_view_information_in_title()




pool = AppProcessesPool(window)

timer_1 = 0
radius_1 = 0
def update():
    global timer_1, radius_1
    timer_1 += 0.1
    radius_1 = 100 + sin(timer_1) * 50


pool.add_process(
    AppProcess(update, True, 1,  'update').start()
)

timer_2 = 0
radius_2 = 0
def update_2():
    global timer_2, radius_2
    timer_2 += 0.1
    radius_2 = 100 + sin(timer_2) * 50

pool.add_process(
    AppSubProcess(update_2, 1 / 60,  "update_2").start()
)



while window.is_opened:
    window.fill()
    pool.update()
    # Круг будет анимироваться с не постоянной частотой, а в зависимости от FPS
    draw_circle(window.surf, [650, 350], radius_1, "red")

    # Круг будет анимироваться с постоянной частотой не зависимо от FPS
    draw_circle(window.surf, [250, 350], radius_2, "blue")
    window.update()

pool.clear()
