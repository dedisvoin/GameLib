import sys

sys.path.append('./')

from src.app import AppWindow
from src.render import sprites, colors
from src.core.settings import CONST_WINDOW_FULLSCREEN
from src.inputs import MouseObject
from src.utils import wait
from src.debuger import debug_error, debug_info, debug_warning

window = AppWindow([1920, 1080], flags=CONST_WINDOW_FULLSCREEN, vsync=False)
window.set_view_information_in_window()
window.set_waited_fps(300)

original_animation = sprites.load_sprite_animation('examples\\ex_4_sprites\\data\\anim*.png', 6, 0.1, True).set_scale(2)

animation_1 = sprites.create_outline(sprites.paint(original_animation, colors.COLOR_MAGENTA).set_alpha_float(0.1), (255, 200, 200), 2)
animation_1.set_pos([400, 400])


animation_2 = sprites.create_outline(original_animation, (100, 100, 255), 2)
animation_2.set_pos([800, 400])



sprite = sprites.load_base_sprite('examples\ex_4_sprites\data\img_2.png', 5).set_scale(2)
sprite_2 = sprite.copy().set_static(False).set_alpha_float(0.5)


while window.is_opened:
    window.fill()

    animation_1.render(window.surf)
    animation_1.update_animation()

    animation_2.render(window.surf)
    animation_2.update_animation()

    

    sprite_2.base_render(window.surf, (1000, 600))
    sprite_2.rotate(1)

    sprite.base_render(window.surf, (1000, 600))
    sprite.rotate(1)

    if MouseObject.get_click():
        debug_error("[Error message] Clicked")

    if MouseObject.get_pressed():
        debug_info("[Info] Pressed")


    if wait(1, "wait"):
        debug_warning("[Warning] Waiting 1 second...")

    

    window.update()