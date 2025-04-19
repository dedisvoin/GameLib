import pygame
import math
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

def draw_outline_circle(surf: pygame.Surface, pos: tuple[int, int], radius: int, color: tuple[int, int, int] | colors.Color,
                        outline_width: int = 1, outline_color: tuple[int, int, int] | colors.Color = (0, 0, 0)) -> None:
    """
    Рисует круг с контуром на поверхности.
    Args:
        surf (pygame.Surface): Поверхность, на которой будет нарисован круг.
        pos (tuple[int, int]): Координаты центра круга.
        radius (int): Радиус круга.
        color (tuple[int, int, int] | colors.Color): Цвет круга.
        outline_width (int): Ширина контура.
        outline_color (tuple[int, int, int] | colors.Color): Цвет контура.
    """
    draw_circle(surf, pos, radius, color)
    draw_circle(surf, pos, radius, outline_color, outline_width)

def draw_line(surf: pygame.Surface, pos_1: tuple[int, int], pos_2: tuple[int, int], color: tuple[int, int, int] | colors.Color, width: int = 1) -> None:
    """
    Рисует линию на поверхности.
    Args:
        surf (pygame.Surface): Поверхность, на которой будет нарисована линия.
        pos_1 (tuple[int, int]): Координаты начала линии.
        pos_2 (tuple[int, int]): Координаты конца линии.
        color (tuple[int, int, int] | colors.Color): Цвет линии.
        width (int): Ширина линии.
    """
    pygame.draw.line(surf, color, pos_1, pos_2, width)

def draw_lines(surf: pygame.Surface, points: list[tuple[int, int]], color: tuple[int, int, int] | colors.Color, width: int = 1, closed: bool = False) -> None:
    """
    Рисует линии на поверхности.
    Args:
        surf (pygame.Surface): Поверхность, на которой будут нарисованы линии.
        points (list[tuple[int, int]]): Список координат точек, через которые проходят линии.
        color (tuple[int, int, int] | colors.Color): Цвет линий.
        width (int): Ширина линий.
        closed (bool): Флаг, указывающий, должна ли быть замкнутая линия.
    """
    pygame.draw.lines(surf, color, closed, points, width)

def draw_polygon(surf: pygame.Surface, points: list[tuple[int, int]], color: tuple[int, int, int] | colors.Color, width: int = 0) -> None:
    """
    Рисует многоугольник на поверхности.
    Args:
        surf (pygame.Surface): Поверхность, на которой будет нарисован многоугольник.
        points (list[tuple[int, int]]): Список координат точек, через которые проходит многоугольник.
        color (tuple[int, int, int] | colors.Color): Цвет многоугольника.
        width (int): Ширина линии многоугольника.
    """
    pygame.draw.polygon(surf, color, points, width)

def draw_ellipse(surf: pygame.Surface, rect: pygame.Rect, color: tuple[int, int, int] | colors.Color, width: int = 0) -> None:
    """
    Рисует эллипс на поверхности.
    Args:
        surf (pygame.Surface): Поверхность, на которой будет нарисован эллипс.
        rect (pygame.Rect): Прямоугольник, описывающий эллипс.
        color (tuple[int, int, int] | colors.Color): Цвет эллипса.
        width (int): Ширина линии эллипса.
    """
    pygame.draw.ellipse(surf, color, rect, width)

def draw_arc(surf: pygame.Surface, rect: pygame.Rect, start_angle: float, stop_angle: float, 
             color: tuple[int, int, int] | colors.Color, width: int = 1) -> None:
    """
    Рисует дугу на поверхности.
    Args:
        surf (pygame.Surface): Поверхность, на которой будет нарисована дуга.
        rect (pygame.Rect): Прямоугольник, описывающий дугу.
        start_angle (float): Начальный угол в радианах.
        stop_angle (float): Конечный угол в радианах.
        color (tuple[int, int, int] | colors.Color): Цвет дуги.
        width (int): Ширина линии дуги.
    """
    pygame.draw.arc(surf, color, rect, start_angle, stop_angle, width)

def draw_aaline(surf: pygame.Surface, pos_1: tuple[int, int], pos_2: tuple[int, int], 
                color: tuple[int, int, int] | colors.Color, blend: int = 1) -> None:
    """
    Рисует сглаженную линию на поверхности.
    Args:
        surf (pygame.Surface): Поверхность, на которой будет нарисована линия.
        pos_1 (tuple[int, int]): Координаты начала линии.
        pos_2 (tuple[int, int]): Координаты конца линии.
        color (tuple[int, int, int] | colors.Color): Цвет линии.
        blend (int): Степень сглаживания.
    """
    pygame.draw.aaline(surf, color, pos_1, pos_2, blend)

def draw_aalines(surf: pygame.Surface, points: list[tuple[int, int]], color: tuple[int, int, int] | colors.Color, 
                 closed: bool = False, blend: int = 1) -> None:
    """
    Рисует сглаженные линии на поверхности.
    Args:
        surf (pygame.Surface): Поверхность, на которой будут нарисованы линии.
        points (list[tuple[int, int]]): Список координат точек.
        color (tuple[int, int, int] | colors.Color): Цвет линий.
        closed (bool): Замкнуть линии или нет.
        blend (int): Степень сглаживания.
    """
    pygame.draw.aalines(surf, color, closed, points, blend)

def draw_polygon_circle(surf: pygame.Surface, pos: tuple[int, int], radius: int, color: tuple[int, int, int] | colors.Color, width: int = 0, segments_count: int = 10, rotate: float = 0) -> None:
    """
    Рисует многоугольник на поверхности.
    Args:
        surf (pygame.Surface): Поверхность, на которой будет нарисован многоугольник.
        pos (tuple[int, int]): Координаты центра многоугольника.
        radius (int): Радиус многоугольника.
        color (tuple[int, int, int] | colors.Color): Цвет многоугольника.
        width (int): Ширина линии многоугольника.
        segments_count (int): Количество сегментов многоугольника.
    """
    points = []
    for i in range(segments_count):
        angle = i * 2 * math.pi / segments_count
        x = pos[0] + radius * math.cos(angle + rotate)
        y = pos[1] + radius * math.sin(angle + rotate)
        points.append((x, y))
    
    draw_polygon(surf, points, color, width)