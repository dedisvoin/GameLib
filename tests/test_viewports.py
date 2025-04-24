import importer

from src.app import AppWindow
from src.render.viewports import BaseViewport, ViewportRenderer, Viewport
from src.render.base import draw_circle, draw_rect, draw_line, draw_polygon_circle
from math import sin

# Create window
window = AppWindow([800, 600], "Viewport Example", vsync=False)
window.set_waited_fps(6000)
window.set_view_information_in_window()

# Create main viewport
main_viewport = Viewport([400, 400], [200, 100])
main_renderer = ViewportRenderer(main_viewport, window, scale=1)

# Create mini viewport
mini_viewport = BaseViewport([200, 200], [20, 20])
mini_renderer = ViewportRenderer(mini_viewport, window, scale=0.5)

# Animation variables
angle = 0
radius = 50

while window.is_opened:
    window.fill((240, 240, 240))
    
    # Update animation
    angle += 1
    radius = 30 + sin(angle * 0.05) * 10

    
    # Draw in main viewport
    draw_rect(main_renderer.surf, (50, 50), (300, 300), (200, 200, 200))
    draw_polygon_circle(main_renderer.surf, (200, 200), radius, (255, 100, 100), segments_count=6, rotate=angle)
    draw_circle(main_renderer.surf, (200, 200), radius + 20, (100, 100, 255), width=2)
    main_viewport.set_angle(angle * 0.5)
    main_renderer.render()
    
    # Draw in mini viewport
    draw_rect(mini_renderer.surf, (10, 10), (180, 180), (100, 200, 100))
    draw_line(mini_renderer.surf, (20, 20), (180, 180), (50, 50, 50), 3)
    mini_renderer.render()
    
    window.update()