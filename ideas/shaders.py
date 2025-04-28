import pygame
import moderngl
import numpy as np
from pygame.locals import *

# Инициализация Pygame и OpenGL
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption("Эффект линзы на мышке")

# Создаем контекст ModernGL
ctx = moderngl.create_context()

# Создаем текстуру для отображения
def create_texture():
    # Рисуем тестовую сцену в Pygame Surface
    surf = pygame.Surface((width, height))
    surf.fill((30, 30, 60))  # Темно-синий фон
    
    # Рисуем несколько кругов для демонстрации
    pygame.draw.circle(surf, (255, 100, 50), (300, 300), 80)
    pygame.draw.circle(surf, (100, 255, 50), (500, 400), 60)
    pygame.draw.circle(surf, (50, 100, 255), (200, 450), 70)
    
    # Конвертируем в текстуру
    texture_data = surf.get_view('1')
    texture = ctx.texture(surf.get_size(), 4, texture_data)
    texture.build_mipmaps()
    return texture

texture = create_texture()

# Вершинные данные (покрывают весь экран)
vertices = np.array([
    # x, y    # u, v
    -1, -1,    0, 0,
     1, -1,    1, 0,
    -1,  1,    0, 1,
     1,  1,    1, 1
], dtype='f4')

# Создаем буферы


# Шейдерная программа
program = ctx.program(
    vertex_shader='''
        #version 330
        in vec2 in_vert;
        in vec2 in_uv;
        out vec2 uv;
        void main() {
            gl_Position = vec4(in_vert, 0.0, 1.0);
            uv = in_uv;
        }
    ''',
    fragment_shader='''
        #version 330
        in vec2 uv;
        out vec4 color;
        uniform sampler2D tex;
        uniform vec2 mouse;
        uniform vec2 resolution;
        
        void main() {
            vec2 tex_uv = uv;
            vec2 dir = tex_uv - mouse;
            float dist = length(dir);
            
            // Параметры линзы
            float lens_radius = 0.15;
            float lens_power = 0.9;
            float edge_width = 0.001;
            
            // Эффект линзы
            if (dist < lens_radius) {
                float percent = dist / lens_radius;
                float distortion = lens_power * pow(1.0 - percent, 1.0);
                tex_uv -= dir * distortion;
            }
            
            // Получаем цвет текстуры
            color = texture(tex, tex_uv);
            
            // Обводка линзы
            if (dist < lens_radius && dist > lens_radius - edge_width) {
                color = mix(color, vec4(1.0, 1.0, 1.0, 1.0), 0.7);
            }
        }
    '''
)


vbo = ctx.buffer(vertices)
vao = ctx.simple_vertex_array(program, vbo, 'in_vert', 'in_uv')
# Основной цикл
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Обновляем позицию мыши
    mx, my = pygame.mouse.get_pos()
    norm_mouse = (mx / width, 1.0 - my / height)
    
    # Очищаем экран
    ctx.clear(0.0, 0.0, 0.0)
    
    # Устанавливаем uniform-переменные
    program['mouse'] = norm_mouse

    program['tex'] = 0
    
    # Рендерим
    texture.use(0)
    vao.render(mode=moderngl.TRIANGLE_STRIP)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()