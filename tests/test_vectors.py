import importer

from src.maths import Vector2D

from src.app import AppWindow

from src.render.base import draw_line

from src.inputs import MouseObject

window = AppWindow([1000, 600], "Vector2D Tests")

vector_1 = Vector2D(100, -30)

pos = Vector2D(200, 200)

while window.is_opened:
    window.fill()

    vector_2 = Vector2D.between(pos.xy, MouseObject.get_position_on_window())
    draw_line(window.surf, pos.xy, (pos + vector_1).xy, "red", 2 )
    draw_line(window.surf, pos.xy, (pos + vector_2).xy, "red", 2 )

    print(vector_1.get_angle_between_degrees(vector_2))

    window.update()
    