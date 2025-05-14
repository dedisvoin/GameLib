from math import acos, sqrt, sin, cos, pi, degrees, radians, atan2
from typing import Any
from random import uniform, randint

import perlin_noise
from noise import pnoise2

class Vector2D:
    """
    Класс для представления двумерного вектора.
    """
    def __init__(self, x: float, y: float):
        """
        Инициализация вектора с заданными координатами.
        Args:
            x (float): Координата x.
            y (float): Координата y.
        """
        self.x = x
        self.y = y

    def copy(self) -> 'Vector2D':
        """
        Возвращает копию вектора.
        Returns:
            Vector2D: Копия вектора.
        """
        return Vector2D(self.x, self.y)

    @classmethod
    def between(cls, start: tuple[int, int], end: tuple[int, int]) -> 'Vector2D':
        """
        Возвращает вектор между двумя точками.
        Args:
            start (tuple[int, int]): Начальная точка.
            end (tuple[int, int]): Конечная точка.
        Returns:
            Vector2D: Вектор между двумя точками.
        """
        return cls(end[0] - start[0], end[1] - start[1])

    @classmethod
    def from_tuple(cls, tuple: tuple[int, int]) -> 'Vector2D':
        """
        Возвращает вектор из кортежа с координатами.
        Args:
            tuple (tuple[int, int]): Кортеж с координатами.
        Returns:
            Vector2D: Вектор из кортежа с координатами.
        """
        return cls(tuple[0], tuple[1])
    
    @classmethod
    def random(cls, min_value: int = 0, max_value: int = 100) -> 'Vector2D':
        """
        Возвращает случайный вектор с координатами в заданном диапазоне.
        Args:
            min_value (int): Минимальное значение координаты.
            max_value (int): Максимальное значение координаты.
        returns:
            Vector2D: Случайный вектор.
        """
        return cls(randint(min_value, max_value), randint(min_value, max_value))
    
    @classmethod
    def random_angle(cls, min_angle: float = 0, max_angle: float = 360) -> 'Vector2D':
        """
        Возвращает случайный вектор с углом в заданном диапазоне.
        Args:
            min_angle (float): Минимальный угол в градусах.
            max_angle (float): Максимальный угол в градусах.
        Returns:
            Vector2D: Случайный вектор с углом.
        """
        angle = uniform(min_angle, max_angle)
        return cls(cos(radians(angle)), sin(radians(angle)))
    
    @classmethod
    def from_angle(cls, lenght: float) -> 'Vector2D':
        """
        Возвращает вектор с заданной длиной и углом 0 градусов.
        Args:
            lenght (float): Длина вектора.
        Returns:
            Vector2D: Вектор с заданной длиной и углом 0 градусов.
        """
        return cls.random_angle(0, 360) * lenght
    
    @property
    def xy(self) -> tuple[float, float]:
        """
        Возвращает координаты вектора в виде кортежа.
        Returns:
            tuple[float, float]: Координаты вектора.
        """
        return [self.x, self.y]

    @xy.setter
    def xy(self, value: tuple[float, float]) -> None:
        """
        Устанавливает координаты вектора.
        Args:
            value (tuple[float, float]): Координаты вектора.
        """
        self.x, self.y = value
    
    def __add__(self, other: Any) -> 'Vector2D':
        """
        Сложение векторов.
        Args:
            other (Vector2D): Второй вектор для сложения.
        Returns:
            Vector2D: Результат сложения.
        """
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Any) -> 'Vector2D':
        """
        Вычитание векторов.
        Args:
            other (Vector2D): Второй вектор для вычитания.
        Returns:
            Vector2D: Результат вычитания.
        """
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float | Any) -> 'Vector2D':
        """
        Умножение вектора на число или другой вектор.
        Args:
            other (float | Vector2D): Число или другой вектор для умножения.
        Returns:
                Vector2D: Результат умножения.
        """
        if isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        else:
            return Vector2D(self.x * other, self.y * other)

    def __truediv__(self, other: float | Any) -> 'Vector2D':
        """
        Деление вектора на число или другой вектор.
        Args:
            other (float | Vector2D): Число или другой вектор для деления.
        Returns:
            Vector2D: Результат деления.
        """
        if isinstance(other, Vector2D):
            return Vector2D(self.x / other.x, self.y / other.y)
        else:
            return Vector2D(self.x / other, self.y / other)

    def __neg__(self) -> 'Vector2D':
        """
        Возвращает вектор с противоположными координатами.
        Returns:
            Vector2D: Вектор с противоположными координатами.
        """
        return Vector2D(-self.x, -self.y)
    
    def __abs__(self) -> float:
        """
        Возвращает вектор с полоожительными координатами.
        Returns:
            Vector2D: Вектор с полоожительными координатами.
        """
        return Vector2D(abs(self.x), abs(self.y))

    def __len__(self) -> float:
        """
        Возвращает длину вектора.
        Returns:
            float: Длина вектора.
        """
        return sqrt(self.x ** 2 + self.y ** 2)

    def __round__(self, n: int = 2) -> 'Vector2D':
        """
        Округляет координаты вектора до заданного количества знаков после запятой.
        Args:
            n (int): Количество знаков после запятой.
        Returns:
            Vector2D: Вектор с округленными координатами.
        """
        return Vector2D(round(self.x, n), round(self.y, n))

    def lenght(self) -> float:
        """
        Возвращает длину вектора.
        Returns:
            float: Длина вектора.
        """
        return sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self) -> 'Vector2D':
        """
        Возвращает нормализованный вектор.
        Returns:
            Vector2D: Нормализованный вектор.
        """
        length = self.lenght()
        if length == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / length, self.y / length)

    def normalize_at(self) -> None:
        """
        Нормализует вектор, изменяя его длину.
        Returns:
            Vector2D: Нормализованный вектор.
        """
        length = self.lenght()
        if length == 0:
            self.x = 0
            self.y = 0
        else:
            self.x /= length
            self.y /= length
        return self

    def normalize_at_to(self, length: float) -> 'Vector2D':
        """
        Нормализует вектор, изменяя его длину.
        Args:
            length (float): Длина нормализованного вектора.
        Returns:
            Vector2D: Нормализованный вектор с заданной длиной.
        """
        self.normalize_at()
        self.x *= length
        self.y *= length
        return self

    def normalize_to(self, length: float) -> 'Vector2D':
        """
        Возвращает нормализованный вектор с заданной длиной.
        Args:
            length (float): Длина нормализованного вектора.
        Returns:
            Vector2D: Нормализованный вектор с заданной длиной.
        """
        return self.normalize() * length

    def dot(self, other: Any) -> float:
        """
        Возвращает скалярное произведение векторов.
        Args:
            other (Vector2D): Второй вектор для скалярного произведения.
        Returns:
            float: Скалярное произведение векторов.
        """
        return self.x * other.x + self.y * other.y
    
    def set_angle(self, angle: float) -> None:
        """
        Устанавливает угол вектора в градусах.
        Args:
            angle (float): Угол в градусах.
        """
        length = self.lenght()
        angle = radians(angle)
        self.x = cos(angle) * length
        self.y = sin(angle) * length

    def rotate(self, angle: float) -> 'Vector2D':
        """
        Поворачивает вектор на заданный угол в градусах.
        Args:
            angle (float): Угол поворота в градусах.
        Returns:
            Vector2D: Повернутый вектор.
        """
        before_angle = self.get_angle_degrees()
        self.set_angle(before_angle + angle)
        
    def get_angle(self) -> float:
        """
        Возвращает угол вектора в радианах.
        Returns:
            float: Угол вектора в радианах.
        """
        return atan2(self.y, self.x)
    
    def get_angle_degrees(self) -> float:
        """
        Возвращает угол вектора в градусах.
        Returns:
            float: Угол вектора в градусах.
        """
        return degrees(self.get_angle())

    def get_angle_between(self, other: Any) -> float:
        """
        Возвращает угол между двумя векторами в радианах.
        Args:
            other (Vector2D): Второй вектор для сравнения.
        Returns:
            float: Угол между векторами в радианах.
        """
        return acos(self.dot(other) / (self.lenght() * other.lenght()))

    def get_angle_between_degrees(self, other: Any) -> float:
        """
        Возвращает угол между двумя векторами в градусах.
        Args:
            other (Vector2D): Второй вектор для сравнения.
        Returns:
            float: Угол между векторами в градусах.
        """
        return degrees(self.get_angle_between(other))

def point_in_rect(point: tuple[float, float], rect: tuple[float, float, float, float]) -> bool:
    """
    Проверяет, находится ли точка внутри прямоугольника.
    Args:
        point (tuple[float, float]): Координаты точки.
        rect (tuple[float, float, float, float]): Координаты прямоугольника (x, y, width, height).
    Returns:
        bool: True, если точка внутри прямоугольника, иначе False.
    """
    return rect[0] <= point[0] <= rect[0] + rect[2] and rect[1] <= point[1] <= rect[1] + rect[3]

def point_in_circle(point: tuple[float, float], circle: tuple[float, float, float]) -> bool:
    """
    Проверяет, находится ли точка внутри окружности.
    Args:
        point (tuple[float, float]): Координаты точки.
        circle (tuple[float, float, float]): Координаты окружности (x, y, radius).
    Returns:
        bool: True, если точка внутри окружности, иначе False.
    """
    return (point[0] - circle[0]) ** 2 + (point[1] - circle[1]) ** 2 <= circle[2] ** 2

def point_in_polygon(point: tuple[float, float], polygon: list[tuple[float, float]]) -> bool:
    """
    Проверяет, находится ли точка внутри многоугольника.
    Args:
        point (tuple[float, float]): Координаты точки.
        polygon (list[tuple[float, float]]): Список координат вершин многоугольника.
    Returns:
        bool: True, если точка внутри многоугольника, иначе False.
    """
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if point[1] > min(p1y, p2y):
            if point[1] <= max(p1y, p2y):
                if point[0] <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (point[1] - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or point[0] <= xinters:
                            inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def collision_rect_rect(rect1: tuple[float, float, float, float], rect2: tuple[float, float, float, float]) -> bool:
    """
    Проверяет, есть ли пересечение между двумя прямоугольниками.
    Args:
        rect1 (tuple[float, float, float, float]): Координаты первого прямоугольника (x, y, width, height).
        rect2 (tuple[float, float, float, float]): Координаты второго прямоугольника (x, y, width, height).
    Returns:
        bool: True, если прямоугольники пересекаются, иначе False.
    """
    return (
        rect1[0] < rect2[0] + rect2[2] and
        rect1[0] + rect1[2] > rect2[0] and
        rect1[1] < rect2[1] + rect2[3] and
        rect1[1] + rect1[3] > rect2[1]
    )

def collision_rect_circle(rect: tuple[float, float, float, float], circle: tuple[float, float, float]) -> bool:
    """
    Проверяет, есть ли пересечение между прямоугольником и окружностью.
    Args:
        rect (tuple[float, float, float, float]): Координаты прямоугольника (x, y, width, height).
        circle (tuple[float, float, float]): Координаты окружности (x, y, radius).
    Returns:
        bool: True, если прямоугольник и окружность пересекаются, иначе False.
    """
    closest_x = max(rect[0], min(circle[0], rect[0] + rect[2]))
    closest_y = max(rect[1], min(circle[1], rect[1] + rect[3]))
    return (circle[0] - closest_x) ** 2 + (circle[1] - closest_y) ** 2 <= circle[2] ** 2

def collision_circle_circle(circle1: tuple[float, float, float], circle2: tuple[float, float, float]) -> bool:
    """
    Проверяет, есть ли пересечение между двумя окружностями.
    Args:
        circle1 (tuple[float, float, float]): Координаты первой окружности (x, y, radius).
        circle2 (tuple[float, float, float]): Координаты второй окружности (x, y, radius).
    Returns:
        bool: True, если окружности пересекаются, иначе False.
    """
    return (circle1[0] - circle2[0]) ** 2 + (circle1[1] - circle2[1]) ** 2 <= (circle1[2] + circle2[2]) ** 2

def get_perlin_noise(nx: int, ny: int, octaves: int, persistence: float = 1, scale: float = 1) -> float:
    """
    Генерирует шум Перлина для заданных параметров.
    Args:
        nx (int): Размерность шума по оси x.
        ny (int): Размерность шума по оси y.
        octaves (float): Количество октав.
        persistence (float): Значение persistence.
        scale (float): Масштаб шума.
    Returns:
        list[list[float]]: Массив шума Перлина.
    """
    return pnoise2(nx * scale, ny * scale, octaves, persistence, scale)