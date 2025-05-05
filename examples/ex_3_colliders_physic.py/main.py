import sys
import time

sys.path.append('./')

from src.colliders import RectColliderObject, RectColliderSpace, COLLIDER_TYPES
from src.maths import Vector2D
from src.app import AppSubProcess, AppWindow

from src.core.settings import CONST_WINDOW_MAX_FPS

from src.inputs import KeyboardObject, MouseObject



cs = RectColliderSpace(0.3)


cs.add_collider(RectColliderObject(1280, 100, resistance=0.5).new(0, 720 - 100, Vector2D(0, 0), "ground"))
cs.add_collider(RectColliderObject(500, 700).new(200, 600))

person = RectColliderObject(50, 50, COLLIDER_TYPES.DYNAMIC, bouncy=0.01).new(500, 400, Vector2D(0, 0), "person")
cs.add_collider(person)

cs.add_collider(RectColliderObject(200, 50, COLLIDER_TYPES.KINEMATIC, resistance=0.3).new(200, 550, id='moved_box'))
cs.get_collider_by_id('moved_box').speed.x = 2

cs.add_collider(RectColliderObject(100, 50, COLLIDER_TYPES.KINEMATIC, resistance=0.3).new(300, 550, id='moved_2'))
cs.get_collider_by_id('moved_2').speed.y = -1

window = AppWindow([1280, 720], "Colliders", vsync=False)
window.set_view_information_in_window()
window.set_waited_fps(CONST_WINDOW_MAX_FPS)



rect = RectColliderObject(20, 20, COLLIDER_TYPES.DYNAMIC, resistance=0.3)

def update(): 
    cs.update()
    if KeyboardObject.get_pressed('left'):
        person.speed.x = -3
    elif KeyboardObject.get_pressed('right'):
        person.speed.x = 3
    

    if KeyboardObject.get_click('up'):
        person.speed.y = -10

    if cs.get_collider_by_id('moved_box').pos.x > 1280 - 200:
        cs.get_collider_by_id('moved_box').speed.x *= -1
    if cs.get_collider_by_id('moved_box').pos.x < 0:
        cs.get_collider_by_id('moved_box').speed.x *= -1

    if cs.get_collider_by_id('moved_2').pos.y > 720 - 100:
            cs.get_collider_by_id('moved_2').speed.y *= -1
    if cs.get_collider_by_id('moved_2').pos.y < 0:
        cs.get_collider_by_id('moved_2').speed.y *= -1

    if MouseObject.get_pressed():
        cs.add_collider(rect.new(MouseObject.get_position_on_window()[0], MouseObject.get_position_on_window()[1], Vector2D.random_angle(0, 360) * 10))

    

AppSubProcess(update, 1 / 120).start()


AppSubProcess(lambda: print(len(cs.get_dynamic_colliders())), 1 / 10).start()

while window.is_opened:
    window.fill()
    cs.render(window.surf)
    window.update()