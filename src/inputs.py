from src.core.settings import CONST_MOUSE_BUTTON_LEFT, CONST_MOUSE_BUTTON_RIGHT, CONST_MOUSE_BUTTON_MIDDLE

import mouse
import pygame

class MouseObject:
    def __init__(self):
        ...

    def _get_window_pos(self) -> tuple[int, int]:
        """Получить текущую позицию окна."""
        pos_in_screen = self.get_position_on_screen()
        pos_in_window = self.get_position_on_windiw()
        speed = self.get_speed()
        return (pos_in_screen[0] - pos_in_window[0] - speed[0], pos_in_screen[1] - pos_in_window[1] - speed[1])
    
    def get_position_on_screen(self) -> tuple[int, int]:
        """Получить текущую позицию мыши на экране."""
        return mouse.get_position()

    def get_position_on_windiw(self) -> tuple[int, int]:
        """Получить текущую позицию мыши в окне."""
        return pygame.mouse.get_pos()

    def get_speed(self) -> tuple[int, int]:
        """Получить скорость перемещения мыши."""
        return pygame.mouse.get_rel()

    def get_pressed(self, button: int = CONST_MOUSE_BUTTON_LEFT) -> bool:
        """Проверить, нажата ли кнопка мыши."""
        return pygame.mouse.get_pressed()[{
            CONST_MOUSE_BUTTON_LEFT: 0,
            CONST_MOUSE_BUTTON_RIGHT: 1,
            CONST_MOUSE_BUTTON_MIDDLE: 2
        }[button]]

    