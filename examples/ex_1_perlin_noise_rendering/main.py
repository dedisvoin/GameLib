import sys
sys.path.append("./")
from src.core import settings

from src.maths import get_perlin_noise
from src.app import AppWindow
from src.render.base import draw_rect


window  =  AppWindow([500, 500], "Example 1", vsync=False)
window.set_waited_fps(settings.CONST_WINDOW_MAX_FPS)
window.set_view_information_in_window()



tile_size = 2
array = []
for i in range(window.get_size()[0] // tile_size):
    arr = []
    for j in range(window.get_size()[1] // tile_size):
        # Scale the coordinates to get more variation in the noise
        scale = 0.05
        value = get_perlin_noise(i * scale, j * scale, 2, scale=1.5)
        arr.append(value)
    array.append(arr)
    

while window.is_opened:
    window.fill()
    for i in range(window.get_size()[0] // tile_size):
        for j in range(window.get_size()[1] // tile_size):
            # Normalize value to be between 0 and 1
            normalized_value = (array[i][j] + 1) * 0.5
            color = (int(255 * ((j * tile_size) / 500) * normalized_value), int(normalized_value * 25), int(normalized_value * 255))
            draw_rect(window.surf, (i * tile_size , j * tile_size), [25, 25], color)
        
    window.update()