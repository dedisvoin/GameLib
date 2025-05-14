import sys
sys.path.append('./')

from src.app import AppWindow
from src.render import sprites, colors, base
from src.inputs import MouseObject

window = AppWindow([1280, 720], "Sprites", vsync=False)
window.set_view_information_in_window()


t = sprites.load_standart_tileset('examples\ex_4_sprites\data\Chocolate_tileset.png', 32)

while window.is_opened:
    window.fill()

    t[1].base_render(window.surf, [300, 300])


    window.update()


