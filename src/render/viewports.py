"""
Модуль viewports.py предоставляет классы для работы с областями отображения (вьюпортами) в приложении.
"""

import pygame
from src.app import AppWindow

class BaseViewport:
    """
    Базовый класс для создания и управления вьюпортом.
    
    Attributes:
        __size (tuple[int, int]): Размер вьюпорта (ширина, высота).
        __pos (tuple[int, int]): Позиция вьюпорта (x, y).
    """

    def __init__(self, size: tuple[int, int], pos: tuple[int, int] = (0, 0)) -> None:
        """
        Инициализация вьюпорта.

        Args:
            size (tuple[int, int]): Размер вьюпорта.
            pos (tuple[int, int], optional): Позиция вьюпорта. По умолчанию (0, 0).
        """
        self.__size = size
        self.__pos = pos

    def get_size(self) -> tuple[int, int]:
        """Возвращает текущий размер вьюпорта."""
        return self.__size
    
    def get_pos(self) -> tuple[int, int]:
        """Возвращает текущую позицию вьюпорта."""
        return self.__pos
    
    def set_size(self, size: tuple[int, int]) -> None:
        """Устанавливает новый размер вьюпорта."""
        self.__size = size

    def set_pos(self, pos: tuple[int, int]) -> None:
        """Устанавливает новую позицию вьюпорта."""
        self.__pos = pos

    def set_width(self, width: int) -> None:
        """Устанавливает новую ширину вьюпорта."""
        self.__size = (width, self.__size[1])

    def set_height(self, height: int) -> None:
        """Устанавливает новую высоту вьюпорта."""
        self.__size = (self.__size[0], height)


class Viewport(BaseViewport):
    """
    Класс для создания и управления вьюпортом.
    Attributes:
        __size (tuple[int, int]): Размер вьюпорта (ширина, высота).
        __pos (tuple[int, int]): Позиция вьюпорта (x, y).
        __angle (float): Угол поворота вьюпорта.
    """
    def __init__(self, size: tuple[int, int], pos: tuple[int, int] = (0, 0), angle: float = 0) -> None:
        """
        Инициализация вьюпорта.
        Args:
            size (tuple[int, int]): Размер вьюпорта (ширина, высота).
            pos (tuple[int, int], optional): Позиция вьюпорта (x, y). По умолчанию (0, 0).
            angle (float, optional): Угол поворота вьюпорта. По умолчанию 0.
        """
        super().__init__(size, pos)
        self.__angle = angle

    def get_angle(self) -> float:
        """Возвращает угол поворота вьюпорта."""
        return self.__angle
    
    def set_angle(self, angle: float) -> None:
        """Устанавливает угол поворота вьюпорта."""
        self.__angle = angle


class ViewportRenderer:
    def __init__(self, viewport: BaseViewport, window: AppWindow, size: tuple[int, int] | None = None, scale: float = 1) -> None:
        self.__viewport = viewport
        self.__window = window
        self.__scale = scale
        self.__size = size if size else viewport.get_size()
        self.__viewport_color = (0, 0, 0, 0)
        
        # Кэшированные параметры
        self.__last_viewport_size = (-1, -1)
        self.__last_angle = None
        self.__last_scale = scale
        
        # Поверхности
        self.__base_surface = pygame.Surface(
            (int(self.__size[0] * scale), int(self.__size[1] * scale)),
            pygame.SRCALPHA
        ).convert_alpha()
        
        self.__scaled_surface = None
        self.__rotated_surface = None

    def get_viewport(self) -> BaseViewport:
        return self.__viewport

    @property
    def surf(self):
        return self.__base_surface

    def get_scale(self) -> float:
        return self.__scale

    def get_size(self) -> tuple[int, int]:
        return self.__size

    def __update_surfaces(self):
        """Обновляет поверхности при изменении параметров"""
        viewport_size = self.__viewport.get_size()
        
        # Обновление масштабированной поверхности
        if viewport_size != self.__last_viewport_size:
            self.__scaled_surface = pygame.transform.scale(self.__base_surface, viewport_size)
            self.__last_viewport_size = viewport_size
        
        # Обновление повернутой поверхности
        if isinstance(self.__viewport, Viewport):
            current_angle = self.__viewport.get_angle()
            if current_angle != self.__last_angle:
                self.__rotated_surface = pygame.transform.rotate(self.__scaled_surface, current_angle)
                self.__last_angle = current_angle

    def clear(self, color: tuple[int, int, int, int] = (0, 0, 0, 0)) -> None:
        self.__viewport_color = color
        self.__base_surface.fill(color)

    def render(self) -> None:
        self.__update_surfaces()
        
        # Отрисовка на целевую поверхность
        if isinstance(self.__viewport, Viewport) and self.__viewport.get_angle() != 0:
            if self.__rotated_surface:
                self.__window.surf.blit(
                    self.__rotated_surface,
                    self.__viewport.get_pos()
                )
        else:
            if self.__scaled_surface:
                self.__window.surf.blit(
                    self.__scaled_surface,
                    self.__viewport.get_pos()
                )
        
        # Очистка базовой поверхности
        self.__base_surface.fill(self.__viewport_color)

