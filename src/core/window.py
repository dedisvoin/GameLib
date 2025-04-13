import pygame
import keyboard

from src.core.settings import (
    WINDOW_RESIZIBLE,
    WINDOW_SIZE,
    WINDOW_TITLE,
    WINDOW_VSYNC,
    WINDOW_QUIT_KEY
)

from typing import (
    List,
    Tuple,
    Any
)

class _WindowHandler:
    """Внутренний класс для управления состоянием окна."""
    def __init__(self, window_quit_key: str = WINDOW_QUIT_KEY) -> None:
        """Инициализация обработчика окна со значениями по умолчанию."""
        self.__window_quit_key = window_quit_key

        self.__window_is_opened = True
        self.__window_is_fullscreen = False # TODO
        self.__window_mouse_whell = 0
        self.__window_pos = [0, 0]

    def _set_quit_key(self, quit_key: str = 'esc') -> None:
        """Установить клавишу для выхода из приложения.
        Args:
            quit_key (str): Клавиша для выхода из приложения.
        """
        self.__window_quit_key = quit_key

    def _update_window_state(self) -> None:
        """Обновление состояния окна."""
        self.__window_is_fullscreen = False
        self.__window_mouse_whell = 0
        self.__window_is_opened = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__window_is_opened = False
            elif event.type == pygame.MOUSEWHEEL:
                self.__window_mouse_whell = event.y
            elif event.type == pygame.WINDOWMOVED:
                self.__window_pos = [event.x, event.y]
        
        if keyboard.is_pressed(self.__window_quit_key):
            self.__window_is_opened = False

    @property
    def window_pos(self) -> tuple[int, int]:
        """Получить позицию окна.

        Returns:
            tuple[int, int]: Позиция окна в пикселях (x, y)
        """
        return self.__window_pos

    @property
    def window_is_opened(self) -> bool:
        """Получить состояние открытия окна.
    
        Returns:
            bool: True если окно открыто, False в противном случае
        """
        return self.__window_is_opened

    @property
    def window_is_fullscreen(self) -> bool:
        """Получить состояние полноэкранного режима окна.
    
        Returns:
            bool: True если окно в полноэкранном режиме, False в противном случае
        """
        return self.__window_is_fullscreen

    @property
    def window_mouse_whell(self) -> int:
        """Получить значение колеса мыши.
    
        Returns:
            int: Текущее значение колеса мыши
        """
        return self.__window_mouse_whell

class _Window:
    """Основной класс окна для управления отображением pygame."""
    def __init__(self, size: Tuple[int, int] = WINDOW_SIZE, title: str = WINDOW_TITLE, flags: int | None = None, vsync: bool = WINDOW_VSYNC) -> "_Window" :
        """Инициализация окна с указанными параметрами.
    
        Args:
            size (Tuple[int, int], optional): Размеры окна. По умолчанию WINDOW_SIZE.
            title (str, optional): Заголовок окна. По умолчанию WINDOW_TITLE.
            flags (int | None, optional): Флаги отображения Pygame. По умолчанию None.
            vsync (bool, optional): Включена вертикальная синхронизация. По умолчанию WINDOW_VSYNC.
        """
        self.__size = size
        self.__title = title
        self.__surf: pygame.Surface = None
        self.__flags = self._generate_flags(flags)
        self.__window_handler = _WindowHandler()
        self._construct_window(self.__size, self.__flags, vsync, self.__title)

    @property
    def _surf(self) -> pygame.Surface:
        """Получить поверхность окна.
        Returns:
            pygame.Surface: Поверхность окна
        """
        return self.__surf

    @property
    def _title(self) -> str:
        return self.__title

    @property
    def _windows_handler(self) -> _WindowHandler:
        """Получить обработчик окна.

        Returns:
            _WindowHandler: Обработчик окна
        """
        return self.__window_handler

    def _generate_flags(self, flags: int | None = None) -> int:
        """Генерация флагов отображения pygame.
    
        Args:
            flags (int | None, optional): Дополнительные флаги для объединения. По умолчанию None.
        
        Returns:
            int: Объединенные флаги отображения pygame
        """
        f = 0
        if WINDOW_RESIZIBLE:
            f |= pygame.RESIZABLE
        if flags is not None:
            f |= flags
        return f

    def _construct_window(self, size: Tuple[int, int], flags: int, vsync: bool, title: str) -> None:
        """Создание окна pygame с указанными параметрами.
    
        Args:
            size (Tuple[int, int]): Размеры окна
            flags (int): Флаги отображения Pygame
            vsync (bool): Включена вертикальная синхронизация
            title (str): Заголовок окна
        """
        self.__surf = pygame.display.set_mode(size, flags, vsync=vsync)
        pygame.display.set_caption(title)

    def _update(self) -> None:
        """Обновление окна pygame."""
        pygame.display.update()

    def _update_state(self) -> None:
        """Обновление состояния окна pygame."""
        self.__window_handler._update_window_state()
    
    @property
    def is_opened(self) -> bool:
        """Проверка, открыто ли окно pygame.

        Returns:
            bool: True, если окно открыто, False в противном случае
        """
        return self.__window_handler.window_is_opened

    @property
    def is_fullscreen(self) -> bool:
        """Проверка, находится ли окно в полноэкранном режиме.
        Returns:
            bool: True, если окно в полноэкранном режиме, False в противном случае
        """
        return self.__window_handler.window_is_fullscreen

    @property
    def get_mouse_whell(self) -> int:
        """Получение значения колеса мыши.
        Returns:
            int: Текущее значение колеса мыши
        """
        return self.__window_handler.window_mouse_whell

    @property
    def get_pos(self) -> Tuple[int, int]:
        """Получение позиции окна.
        Returns:
            Tuple[int, int]: Позиция окна в пикселях (x, y)
        """
        return self.__window_handler.window_pos