import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

def apply_shader_effect(surface):
    """Фейковый 'шейдер' (инверсия цветов)"""
    pixels = pygame.surfarray.pixels3d(surface)
    pixels[:, :, :] = 255 - pixels  # Инвертируем цвета
    del pixels  # Важно: отпускаем блокировку Surface

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50, 100, 200))
    pygame.draw.circle(screen, (255, 255, 0), (400, 300), 100)

    apply_shader_effect(screen)  # Применяем эффект

    pygame.display.flip()
    clock.tick(6000)
    print(clock.get_fps())

pygame.quit()