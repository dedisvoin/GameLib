import importer

from src.app import AppWindow, AppProcessesPool, AppSubProcess
from src.render import batching, base

from src.maths import Vector2D
from random import uniform

WINDOW_SIZE = (1000, 1000)

window = AppWindow(size=WINDOW_SIZE, title="Test Batching", vsync=False)
window.set_waited_fps(500)
window.set_view_information_in_title()

class Ball:
    def __init__(self):
        self.__radius = 20
        self.__position = Vector2D(500, 500)
        self.__speed = Vector2D(uniform(-1, 1)*10, uniform(-1, 1)*10)

    def update(self):
        self.__position += self.__speed
        if self.__position.x < self.__radius or self.__position.x > WINDOW_SIZE[0] - self.__radius:
            self.__speed.x *= -1
        if self.__position.y < self.__radius or self.__position.y > WINDOW_SIZE[1] - self.__radius:
            self.__speed.y *= -1

    def render(self, surf):
        base.draw_circle(surf, self.__position.xy, self.__radius, "red")


balls = [Ball() for _ in range(5000)]


def update():
    for ball in balls:
        ball.update()


update_process = AppSubProcess(update, 1 / 60, 'update').start()

batching_system = batching.Batch(window, batch_size=1000)

while window.is_opened:
    window.fill()
    batching_system.update()
    for ball in balls:
        
        ball.render(batching_system.surf)
    batching_system.render()

    window.update()

    