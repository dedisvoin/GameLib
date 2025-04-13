from src.core.settings import CONST_MOUSE_BUTTON_LEFT, CONST_MOUSE_BUTTON_RIGHT, CONST_MOUSE_BUTTON_MIDDLE

import mouse
import pygame

class Mouse:
    def __init__(self):
        """Инициализация объекта мыши."""
        self.clicked = False
    
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

    def get_pressed_buttons(self) -> list[bool]:
        """Получить список нажатых кнопок мыши."""
        return pygame.mouse.get_pressed()

    def get_click(self, button: int = CONST_MOUSE_BUTTON_LEFT) -> bool:
        """Проверить, был ли совершен клик мышью."""
        button_index = {
            CONST_MOUSE_BUTTON_LEFT: 0,
            CONST_MOUSE_BUTTON_RIGHT: 1,
            CONST_MOUSE_BUTTON_MIDDLE: 2
        }[button]
        
        is_pressed = pygame.mouse.get_pressed()[button_index]
        
        if is_pressed and not self.clicked:
            self.clicked = True
            return True
        elif not is_pressed:
            self.clicked = False
        
        return False


# Обьект для работы с мышью
MouseObject = Mouse()