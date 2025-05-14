import sys
sys.path.append('./')

from src.app import AppWindow, AppSubProcess
from src.core.settings import CONST_WINDOW_SCALE, CONST_WINDOW_FULLSCREEN

from src.inputs import MouseObject
from src.vfx.particles import *

window = AppWindow([1920, 1080], "Particles", vsync=False)
window.set_view_information_in_window()
window.set_waited_fps(6000)


p1 = Particle()
p1.set_shape(ParticleShapes.RECT)
p1.start_life_time = 100
p1.speed_spread = 360
p1.min_start_speed = 3
p1.max_start_speed = 10
p1.color = [[200, 200, 240], [240, 200, 200]]
p1.min_start_radius = 5
p1.max_start_radius = 20
p1.min_rotate_speed = 0
p1.max_rotate_speed = 10
p1.radius_resize_speed = 0.1
p1.resize_radius_for_life_time = True
p1.use_speed_vector_for_angle = True
p1.speed_air_friction = Vector2D(0.99, 0.99)
p1.gravity = Vector2D(0, 0)
p1.min_speed_rotation_angle = 0
p1.max_speed_rotation_angle = 5
p1.shadowing = True
p1.shadow_offset = Vector2D(6, 6)
p1.shadow_color = colors.Color(200 / 4, 200 / 4, 240 / 4)

e1 = RectEmitter([0, 0], 1, 1)

ps = ParticleSystem()


def counter():
    print(ps.get_count())

AppSubProcess(counter, 1 / 1, 'counter').start()


def update():
    ps.update()
    ps.emit(e1, p1, 1)

AppSubProcess(update, 1 / 60, 'update').start()

while window.is_opened:
    window.fill()
    e1.set_pos(Vector2D.from_tuple(MouseObject.get_position_on_window()))
    
    ps.render(window.surf)
    

    window.update()