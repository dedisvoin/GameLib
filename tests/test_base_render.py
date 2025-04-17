import importer
from src.app import AppWindow
from src.render import base
from src.render import colors
import pygame


window = AppWindow([1000, 600], "Base Render Tests")

while window.is_opened:
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
    
    base.draw_connected_circles(window.surf, [(400, 250), (500, 250), (450, 350)], 20, colors.COLOR_GREEN())
    
    triangle_points = [[(700, 200), (800, 200), (750, 300)]]
    base.draw_rect_with_triangles(window.surf, (650, 200), (200, 150), triangle_points, colors.COLOR_PINK())
    
    window.update()