from time import time
import sys
sys.path.append('./')

from src.render.text import TextField
from src.render import colors

def get_at_time() -> str:
    hours = int(time() / 3600) % 24
    minutes = int(time() / 60) % 60
    seconds = int(time()) % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


class DebugInfo:
    """Класс для отображения отладочной информации.

    Этот класс предоставляет функционал для отображения отладочной информации в окне приложения.
    Он использует объект TextField для отображения текста.

    """
    def __init__(self) -> None:
        self.__debug_texts: list[list[str, int, colors.Color]] = []
        

        self.__text = TextField("consolas", 15, (1, 1, 1), True, True)

    def render(self, window) -> None:
        """Отображение отладочной информации."""
        if not __debug__:
            for i, text_obj in enumerate(self.__debug_texts[::-1]):
                pos = [0, window.get_at_size()[1] - 15 * (i + 1)]
                if pos[1] > 0:
                
                    self.__text.set_text(text_obj[0]   )
                    self.__text.set_color(text_obj[2]())
                    self.__text.set_alpha(text_obj[3]  )
                    self.__text.render(window.surf, pos, True)

                text_obj[1] -= 0.05 * window.get_delta()
                if text_obj[1] < 0:
                    text_obj[3] -= 5

            for text_obj in self.__debug_texts:
                if text_obj[3] <= 0:
                    self.__debug_texts.remove(text_obj)
        
    
    def add_error(self, text: str) -> None:
        """Добавить ошибку в список отладочной информации."""
        self.__debug_texts.append([get_at_time() + ": " + text, 10, colors.COLOR_RED, 255])

    def add_warning(self, text: str) -> None:
        """Добавить предупреждение в список отладочной информации."""
        self.__debug_texts.append([get_at_time() + ": " + text, 10, colors.COLOR_ORANGE, 255])

    def add_info(self, text: str) -> None:
        """Добавить информацию в список отладочной информации."""
        self.__debug_texts.append([get_at_time() + ": " + text, 10, colors.COLOR_DARK_GRAY, 255])

    def add_custom(self, text: str, time: float, color: colors.Color) -> None:
        """Добавить пользовательскую информацию в список отладочной информации."""
        self.__debug_texts.append([get_at_time() + ": " + text, time, color, 255])


STANDART_DEBUG_STREAM = DebugInfo()

def debug_error(text: str) -> None:
    STANDART_DEBUG_STREAM.add_error(text)

def debug_warning(text: str) -> None:
    STANDART_DEBUG_STREAM.add_warning("[!] " + text)

def debug_info(text: str) -> None:
    STANDART_DEBUG_STREAM.add_info(text)

def debug_success(text: str) -> None:
    STANDART_DEBUG_STREAM.add_custom("[+] " + text, 10, colors.COLOR_GREEN)