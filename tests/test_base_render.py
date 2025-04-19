import importer
from src.app import AppWindow
from src.render import base
from src.render import colors
import pygame


window = AppWindow([1000, 600], "Base Render Tests", vsync=False)
window.set_view_information_in_title()
window.set_waited_fps(120)
angle = 0

while window.is_opened:
    angle += 0.01
    window.fill()

    base.draw_rect(window.surf, (50, 50), (100, 100), colors.COLOR_RED())
    base.draw_circle(window.surf, (200, 100), 50, colors.COLOR_BLUE())
    base.draw_outline_rect(window.surf, (300, 50), (100, 100), colors.COLOR_GREEN(), outline_color=colors.COLOR_WHITE())
    base.draw_outline_circle(window.surf, (500, 100), 50, colors.COLOR_YELLOW(), outline_color=colors.COLOR_BLACK())
    base.draw_line(window.surf, (600, 50), (700, 150), colors.COLOR_PURPLE(), 3)
    
    points = [(800, 50), (900, 50), (850, 150)]
    base.draw_polygon(window.surf, points, colors.COLOR_ORANGE())
    
    base.draw_ellipse(window.surf, pygame.Rect(50, 200, 100, 50), colors.COLOR_CYAN())
    base.draw_arc(window.surf, pygame.Rect(200, 200, 100, 100), 0, 3.14, colors.COLOR_MAGENTA())

    base.draw_polygon_circle(window.surf, (500, 200), 100, 'red', 0, 3, angle)

    base.draw_polygon_circle(window.surf, (500, 300), 100, 'green', 10, 5, -angle)

    window.update()