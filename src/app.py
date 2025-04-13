"""
Модуль приложения, содержащий основной класс для создания и управления окном приложения.

Этот модуль предоставляет класс AppWindow, который наследуется от базового класса _Window
и реализует основные функции для работы с окном приложения, включая управление частотой кадров,
обработку событий и отображение информации.
"""


from src.core.settings import WINDOW_SIZE, WINDOW_TITLE, WINDOW_VSYNC, WINDOW_WAITED_FPS, WINDOW_BG_COLOR, WINDOW_DELTA_MATCH_FPS
from src.core import window

from typing import Tuple
import pygame



pygame.init()

class AppWindow(window._Window):
    """Класс приложения для создания и управления окном.
    
    Этот класс предоставляет функционал для:
    - Создания окна приложения с заданными параметрами
    - Управления частотой кадров
    - Отображения информации в заголовке окна
    - Управления фоном окна
    - Обработки базовых событий
    
    Attributes:
        __clock: Объект для управления временем и FPS
        __waited_fps: Желаемая частота кадров
        __bg_color: Цвет фона окна
        __view_information_in_title: Флаг отображения информации в заголовке
    """
    def __init__(self, size: Tuple[int, int] = WINDOW_SIZE, title: str = WINDOW_TITLE, flags: int | None = None, 
                 vsync: bool = WINDOW_VSYNC) -> "AppWindow":
        """Инициализация приложения.
        
        Args:
            size: Размер окна в пикселях (ширина, высота)
            title: Заголовок окна
            flags: Флаги pygame для создания окна
            vsync: Включение/выключение вертикальной синхронизации
        """
        super().__init__(size, title, flags, vsync)
        self.__clock = pygame.time.Clock()
        self.__waited_fps = WINDOW_WAITED_FPS

        self.__bg_color = (255, 255, 255)

        self.__view_information_in_title = False

    def close(self):
        """Закрыть окно приложения."""
        pygame.display.quit()

    def set_view_information_in_title(self, view_information_in_title: bool = True):
        """Установить отображение информации о частоте кадров в заголовке окна.
        
        Args:
            view_information_in_title: Отображение информации о частоте кадров в заголовке окна. По умолчанию True.
        """
        self.__view_information_in_title = view_information_in_title

    def set_quit_key(self, quit_key: str = 'esc'):
        """Установить клавишу для выхода из приложения.
        
        Args:
            quit_key: Клавиша для выхода из приложения. По умолчанию 'esc'.
        """
        super()._windows_handler._set_quit_key(quit_key)

    def set_waited_fps(self, waited_fps: int):
        """Установить желаемую частоту кадров.
        
        Args:
            waited_fps: Желаемая частота кадров.
            
        Returns:
            self: Возвращает текущий экземпляр класса для цепочки вызовов.
        """
        self.__waited_fps = waited_fps
        return self

    def get_fps(self) -> float:
        """Получить текущую частоту кадров.
        
        Returns:
            float: Текущая частота кадров.
        """
        return self.__clock.get_fps()

    def get_render_time(self) -> float:
        """Получить время, прошедшее с последнего кадра.
        
        Returns:
            float: Время в миллисекундах между текущим и предыдущим кадром.
        """
        return self.__clock.get_time()

    def get_delta(self) -> float:
        """Получить дельту времени между текущим и предыдущим кадром.

        Returns:
            float: Дельта времени в секундах.
        """
        try:
            return WINDOW_DELTA_MATCH_FPS / self.get_fps()
        except ZeroDivisionError:
            return 1

    def fill_bg(self, color: tuple[int, int, int] | None = None) -> None:
        """Заполнить фон окна указанным цветом.
        
        Если цвет не указан, используется текущий цвет фона (__bg_color).
        
        Args:
            color: Цвет фона в формате RGB (красный, зеленый, синий). По умолчанию None.
        """
        
        if color is None:
            color = self.__bg_color
        self._surf.fill(color)

    def update(self) -> None:
        """Обновление состояния приложения.
        
        Вызывает внутренние методы для обновления состояния окна и обработки событий.
        """
        
        self._update()
        self._update_state()

        if self.__view_information_in_title:
            pygame.display.set_caption(f"{self._title} | FPS: {int(self.get_fps())}/{self.__waited_fps} | RENDER TIME: {self.get_render_time()}ms | DELTA: {self.get_delta():.2f}")

        self.__clock.tick(self.__waited_fps)

    @property
    def surf(self) -> pygame.Surface:
        """Получить поверхность окна.

        Returns:
            pygame.Surface: Поверхность окна.
        """
        return self._surf
        