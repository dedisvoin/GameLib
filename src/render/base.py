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

def draw_polygon(surf: pygame.Surface, points: list[tuple[int, int]], color: tuple[int, int, int] | colors.Color, width: int = 1) -> None:
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

def draw_rect_with_circle(surf: pygame.Surface, rect_pos: tuple[int, int], rect_size: tuple[int, int], 
                         circle_pos: tuple[int, int], circle_radius: int, color: tuple[int, int, int] | colors.Color) -> None:
    """
    Рисует прямоугольник с кругом на поверхности.
    Args:
        surf (pygame.Surface): Поверхность для рисования.
        rect_pos (tuple[int, int]): Позиция прямоугольника.
        rect_size (tuple[int, int]): Размер прямоугольника.
        circle_pos (tuple[int, int]): Позиция круга.
        circle_radius (int): Радиус круга.
        color (tuple[int, int, int] | colors.Color): Цвет фигур.
    """
    draw_rect(surf, rect_pos, rect_size, color)
    draw_circle(surf, circle_pos, circle_radius, color)

def draw_connected_circles(surf: pygame.Surface, centers: list[tuple[int, int]], radius: int, 
                         color: tuple[int, int, int] | colors.Color, line_width: int = 1) -> None:
    """
    Рисует соединенные линиями круги.
    Args:
        surf (pygame.Surface): Поверхность для рисования.
        centers (list[tuple[int, int]]): Список центров кругов.
        radius (int): Радиус кругов.
        color (tuple[int, int, int] | colors.Color): Цвет фигур.
        line_width (int): Толщина соединительных линий.
    """
    for center in centers:
        draw_circle(surf, center, radius, color)
    if len(centers) > 1:
        draw_lines(surf, centers, color, line_width)

def draw_rect_with_triangles(surf: pygame.Surface, rect_pos: tuple[int, int], rect_size: tuple[int, int],
                           triangle_points: list[list[tuple[int, int]]], color: tuple[int, int, int] | colors.Color) -> None:
    """
    Рисует прямоугольник с треугольниками.
    Args:
        surf (pygame.Surface): Поверхность для рисования.
        rect_pos (tuple[int, int]): Позиция прямоугольника.
        rect_size (tuple[int, int]): Размер прямоугольника.
        triangle_points (list[list[tuple[int, int]]]): Список точек для каждого треугольника.
        color (tuple[int, int, int] | colors.Color): Цвет фигур.
    """
    draw_rect(surf, rect_pos, rect_size, color)
    for triangle in triangle_points:
        draw_polygon(surf, triangle, color)