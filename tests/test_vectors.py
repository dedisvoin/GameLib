import importer

from src.maths import Vector2D

from src.app import AppWindow

from src.render.base import draw_line

from src.inputs import MouseObject

window = AppWindow([1000, 600], "Vector2D Tests")
window.set_view_information_in_title()

vector_1 = Vector2D(100, -30)

pos = Vector2D(200, 200)


vector_3 = Vector2D(0, 200)
pos_2 = Vector2D(500, 300)
angle = 0

while window.is_opened:
    angle += 1
    window.fill()

    vector_2 = Vector2D.between(pos.xy, MouseObject.get_position_on_window())
    draw_line(window.surf, pos.xy, (pos + vector_1).xy, "red", 2 )
    draw_line(window.surf, pos.xy, (pos + vector_2).xy, "red", 2 )

    vector_3.rotate(1)
    draw_line(window.surf, pos_2.xy, (pos_2 + vector_3).xy, "black", 2 )

    # print(vector_1.get_angle_between_degrees(vector_2))

    window.update()
    