import importer
from src.beta.shaders import Shader

from src.app import AppWindow
from src.core.settings import CONST_WINDOW_USE_OPENGL, CONST_WINDOW_MAX_FPS, CONST_WINDOW_USE_DOUBLE_BUFFER
from src.inputs import  MouseObject
from src.render.base import draw_circle
from src.render.viewports import BaseViewport, ViewportRenderer

window = AppWindow([1000, 800], "Test shader", flags=CONST_WINDOW_USE_DOUBLE_BUFFER | CONST_WINDOW_USE_OPENGL, vsync=False)

window.set_view_information_in_title()
window.set_waited_fps(CONST_WINDOW_MAX_FPS)
window.set_view_information_in_window()


base_shader = Shader(
    vertex_shader="""
        #version 330
        in vec2 in_vert;
        in vec2 in_uv;
        out vec2 uv;
        uniform vec2 resolution;
        void main() {
            gl_Position = vec4(in_vert.x, -in_vert.y, 0.0, 1.0);
            uv = in_uv;
        }
    """,
    fragment_shader="""
        #version 330
        in vec2 uv;
        out vec4 color;
        uniform sampler2D tex;
        uniform vec2 resolution;
        void main() {
            float pixel_size = 5.0;
            vec2 pixelated_uv = floor(uv * resolution / pixel_size) * pixel_size / resolution;
            color = texture(tex, pixelated_uv);
        }
    """
)

view_port = BaseViewport([1920, 1080], [0, 0])
view_port_renderer = ViewportRenderer(view_port, window, [1920, 1080], 1)

while window.is_opened:
    window.fill()
    
    
    draw_circle(view_port_renderer.surf, MouseObject.get_position_on_window(), 100, (255, 0, 0))
    base_shader.send("resolution", view_port.get_size())
    base_shader.render_from_surf(view_port_renderer.surf)

    view_port_renderer.clear((255, 255, 255))
    
    window.render_information_in_window()
 

    window.update()
    

    