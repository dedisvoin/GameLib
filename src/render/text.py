import pygame
from src.render.colors import Color

class TextField:
    """Класс для создания текстового поля."""

    def __init__(self, font: str, font_size: int, color: tuple[int, int, int] | Color, bold: bool = False, italic: bool = False, ):
        self.__font = font
        self.__font_size = font_size
        self.__color = color
        self.__bold = bold
        self.__italic = italic
        self.__font_object = pygame.font.SysFont(self.__font, self.__font_size, self.__bold, self.__italic)
        self.__text: str

    def render(self, surf: pygame.Surface, pos: tuple[int, int] = (0, 0), antialias: bool = True,
               left_or_right: bool = True, up_or_down: bool = True):
        
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
        """Установить текст."""
        self.__text = text

    def set_color(self, color: tuple[int, int, int] | Color):
        """Установить цвет текста."""
        self.__color = color

    def set_font_size(self, font_size: int):
        """Установить размер шрифта."""
        self.__font_size = font_size
        self.__font_object = pygame.font.SysFont(self.__font, self.__font_size, self.__bold, self.__italic)

    def set_bold(self, bold: bool = True):
        """Установить жирность шрифта."""
        self.__bold = bold
        self.__font_object = pygame.font.SysFont(self.__font, self.__font_size, self.__bold, self.__italic)

    def set_italic(self, italic: bool = True):
        """Установить курсив шрифта."""
        self.__italic = italic
        self.__font_object = pygame.font.SysFont(self.__font, self.__font_size, self.__bold, self.__italic)