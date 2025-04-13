import pygame
from src.render import colors

def draw_rect(surf: pygame.Surface, pos: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int] | colors.Color, 
              width: int = 0, radius: int = 0) -> None:
    """
    Рисует прямоугольник на поверхности.
    Args:
        surf (pygame.Surface): Поверхность, на которой будет нарисован прямоугольник.
        pos (tuple[int, int]): Координаты левого верхнего угла прямоугольника.
        size (tuple[int, int]): Размеры прямоугольника (ширина, высота).
        color (tuple[int, int, int] | colors.Color): Цвет прямоугольника.
        width (int): Ширина линии, если требуется.
        radius (int): Радиус скругления углов, если требуется.
    """
    
    pygame.draw.rect(surf, color, pygame.Rect(pos, size), width, radius)

def draw_circle(surf: pygame.Surface, pos: tuple[int, int], radius: int, color: tuple[int, int, int] | colors.Color,
                width: int = 0) -> None:
    """
    Рисует круг на поверхности.
    Args:
        surf (pygame.Surface): Поверхность, на которой будет нарисован круг.
        pos (tuple[int, int]): Координаты центра круга.
        radius (int): Радиус круга.
        color (tuple[int, int, int] | colors.Color): Цвет круга.
        width (int): Ширина линии, если требуется.
    """
    pygame.draw.circle(surf, color, pos, radius, width)

def draw_outline_rect(surf: pygame.Surface, pos: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int] | colors.Color,
                      outline_width: int = 1, outline_color: tuple[int, int, int] | colors.Color = (0, 0, 0), radius: int = 0) -> None:
    """
    Рисует прямоугольник с контуром на поверхности.
    Args:
        surf (pygame.Surface): Поверхность, на которой будет нарисован прямоугольник.
        pos (tuple[int, int]): Координаты левого верхнего угла прямоугольника.
        size (tuple[int, int]): Размеры прямоугольника (ширина, высота).
        color (tuple[int, int, int] | colors.Color): Цвет прямоугольника.
        outline_width (int): Ширина контура.
        outline_color (tuple[int, int, int] | colors.Color): Цвет контура.
        radius (int): Радиус скругления углов, если требуется.
    """
    draw_rect(surf, pos, size, color, radius=radius)
    draw_rect(surf, pos, size, outline_color, outline_width, radius)