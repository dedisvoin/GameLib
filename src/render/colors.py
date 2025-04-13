"""
Модуль colors.py содержит класс Color для работы с цветами и предопределенные константы цветов.
"""

class Color:
    """
    Класс для представления цвета в формате RGBA.
    
    Атрибуты:
        r (int): Значение красного компонента (0-255)
        g (int): Значение зеленого компонента (0-255)
        b (int): Значение синего компонента (0-255)
        a (int): Значение альфа-канала (0-255), по умолчанию 255
    """
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        """
        Инициализация объекта Color.
        
        Аргументы:
            r (int): Значение красного компонента
            g (int): Значение зеленого компонента
            b (int): Значение синего компонента
            a (int): Значение альфа-канала, по умолчанию 255
        """
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    
    @property
    def rgb(self):
        """
        Возвращает кортеж из RGB компонентов цвета.
        
        Возвращает:
            tuple: Кортеж (r, g, b)
        """
        return (self.r, self.g, self.b)
    
    @property
    def rgba(self):
        """
        Возвращает кортеж из RGBA компонентов цвета.
        
        Возвращает:
            tuple: Кортеж (r, g, b, a)
        """
        return (self.r, self.g, self.b, self.a)

    def hex(self):
        """
        Возвращает строковое представление цвета в шестнадцатеричном формате.
        
        Возвращает:
            str: Цвет в формате '#RRGGBB'
        """
        return "#{:02x}{:02x}{:02x}".format(self.r, self.g, self.b)

    def __call__(self):
        """
        Возвращает кортеж из RGBA компонентов цвета.

        Возвращает:
            tuple: Кортеж (r, g, b, a)
        """
        return self.rgba


# Предопределенные константы цветов
COLOR_RED = Color(255, 0, 0)
COLOR_GREEN = Color(0, 255, 0)
COLOR_BLUE = Color(0, 0, 255)
COLOR_YELLOW = Color(255, 255, 0)
COLOR_CYAN = Color(0, 255, 255)
COLOR_MAGENTA = Color(255, 0, 255)
COLOR_WHITE = Color(255, 255, 255)
COLOR_BLACK = Color(0, 0, 0)
COLOR_GRAY = Color(128, 128, 128)
COLOR_DARK_GRAY = Color(64, 64, 64)
COLOR_LIGHT_GRAY = Color(192, 192, 192)
COLOR_ORANGE = Color(255, 165, 0)
COLOR_PURPLE = Color(128, 0, 128)
COLOR_PINK = Color(255, 192, 203)
COLOR_BROWN = Color(165, 42, 42)
COLOR_GOLD = Color(255, 215, 0)
COLOR_SILVER = Color(192, 192, 192)
COLOR_BRONZE = Color(205, 127, 50)
    
