import sys
sys.path.append('./')

from src.app import AppWindow, AppSubProcess
from src.colliders import RectCollideLayer, BaseRectCollider, COLLIDER_DYNAMIC, COLLIDER_KINEMATIC, COLLIDER_STATIC
from src.inputs import KeyboardObject

window = AppWindow([1500, 800], "Colliders!!", vsync=False)
window.set_view_information_in_window()
window.set_waited_fps(1000)


layer_1 = RectCollideLayer(0.5)
layer_1.add_collider(BaseRectCollider([1500, 50], COLLIDER_STATIC).create((0, 750)))
layer_1.add_collider(BaseRectCollider([50, 50], COLLIDER_DYNAMIC).create((700, 500), 'player'))

border = BaseRectCollider([20, 500])
layer_1.add_collider(border.create([0, 500]))
layer_1.add_collider(border.create([1000, 500]))

player = layer_1.get_collider_by_id('player')
player.bouncing = 0.1


moving_box = BaseRectCollider([200, 50], COLLIDER_KINEMATIC)
layer_1.add_collider(moving_box.create((400, 600), 'moving_box'))
layer_1.get_collider_by_id('moving_box').speed.y = -3

layer_1.add_collider(moving_box.create((100, 700), 'moving_box_2'))
layer_1.get_collider_by_id('moving_box_2').speed.x = 3




def process_update():
    layer_1.update()

    if KeyboardObject.get_pressed('left'):
        player.speed.x =- 5
    if KeyboardObject.get_pressed('right'):
        player.speed.x = 5
    if KeyboardObject.get_click('up'):
        player.speed.y = - 10

    if layer_1.get_collider_by_id('moving_box').pos.y < 100 or layer_1.get_collider_by_id('moving_box').pos.y > 600:
        layer_1.get_collider_by_id('moving_box').speed.y *= -1
    
    if layer_1.get_collider_by_id('moving_box_2').pos.x < 100 or layer_1.get_collider_by_id('moving_box_2').pos.x > 900:
        layer_1.get_collider_by_id('moving_box_2').speed.x *= -1
    
    

AppSubProcess(process_update, 1 / 60, 'update').start()


while window.is_opened:
    window.fill()


    layer_1.view(window.surf)
    
    window.update()