"""
Модуль text.py содержит класс для работы с текстовыми полями в pygame.

Классы:
    TextField: Класс для создания и управления текстовым полем.

Зависимости:
    - pygame: Библиотека для создания игр
    - src.render.colors: Модуль с определением цветов
"""

import pygame
from src.render.colors import Color

class TextField:
    """Класс для создания текстового поля.
    
    Атрибуты:
        __font (str): Название шрифта
        __font_size (int): Размер шрифта
        __color (tuple[int, int, int] | Color): Цвет текста
        __bold (bool): Жирное начертание
        __italic (bool): Курсивное начертание
        __font_object: Объект шрифта pygame
        __text (str): Текст для отображения
    """

    def __init__(self, font: str, font_size: int, color: tuple[int, int, int] | Color, bold: bool = False, italic: bool = False, ):
        """Инициализация текстового поля.

        Аргументы:
            font (str): Название шрифта
            font_size (int): Размер шрифта
            color (tuple[int, int, int] | Color): Цвет текста
            bold (bool, optional): Жирное начертание. По умолчанию False
            italic (bool, optional): Курсивное начертание. По умолчанию False
        """
        self.__font = font
        self.__font_size = font_size
        self.__color = color
        self.__bold = bold
        self.__italic = italic
        self.__font_object = pygame.font.SysFont(self.__font, self.__font_size, self.__bold, self.__italic)
        self.__text: str = ''

    def render(self, surf: pygame.Surface, pos: tuple[int, int] = (0, 0), antialias: bool = True,
               left_or_right: bool = True, up_or_down: bool = True):
        """Отрисовка текста на поверхности.
        
        Аргументы:
            surf (pygame.Surface): Поверхность для отрисовки
            pos (tuple[int, int], optional): Позиция текста. По умолчанию (0, 0)
            antialias (bool, optional): Сглаживание текста. По умолчанию True
            left_or_right (bool, optional): Выравнивание по горизонтали. True - слева, False - справа
            up_or_down (bool, optional): Выравнивание по вертикали. True - сверху, False - снизу
        """
        text_surf = self.__font_object.render(self.__text, antialias, self.__color)
        if left_or_right:
            pos = (pos[0], pos[1])
        else:
            pos = (pos[0] - text_surf.get_width(), pos[1])
        
        if up_or_down:
            pos = (pos[0], pos[1])
        else:
            pos = (pos[0], pos[1] - text_surf.get_height())

        surf.blit(text_surf, pos)

    def set_text(self, text: str):
        """Установить текст.
        
        Аргументы:
            text (str): Новый текст для отображения
        """
        self.__text = text

    def set_color(self, color: tuple[int, int, int] | Color):
        """Установить цвет текста.
        
        Аргументы:
            color (tuple[int, int, int] | Color): Новый цвет текста
        """
        self.__color = color

    def set_font_size(self, font_size: int):
        """Установить размер шрифта.
        
        Аргументы:
            font_size (int): Новый размер шрифта
        """
        self.__font_size = font_size
        self.__font_object = pygame.font.SysFont(self.__font, self.__font_size, self.__bold, self.__italic)

    def set_bold(self, bold: bool = True):
        """Установить жирность шрифта.
        
        Аргументы:
            bold (bool, optional): Включить жирное начертание. По умолчанию True
        """
        self.__bold = bold
        self.__font_object = pygame.font.SysFont(self.__font, self.__font_size, self.__bold, self.__italic)

    def set_italic(self, italic: bool = True):
        """Установить курсив шрифта.
        
        Аргументы:
            italic (bool, optional): Включить курсивное начертание. По умолчанию True
        """
        self.__italic = italic
        self.__font_object = pygame.font.SysFont(self.__font, self.__font_size, self.__bold, self.__italic)