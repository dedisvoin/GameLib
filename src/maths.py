from math import sqrt, sin, cos, pi, degrees, radians, atan2
from typing import Any

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
    
    @property
    def xy(self) -> tuple[float, float]:
        """
        Возвращает координаты вектора в виде кортежа.
        Returns:
            tuple[float, float]: Координаты вектора.
        """
        return (self.x, self.y)

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
