"""
# Классы для работы с мышью и клавиатурой

Методы Mouse:
- get_position_on_screen() -> tuple[int, int]: Возвращает текущие координаты курсора на экране
- get_position_on_window() -> tuple[int, int]: Возвращает текущие координаты курсора в окне
- get_speed() -> tuple[int, int]: Возвращает скорость движения мыши
- get_pressed(button: int) -> bool: Проверяет, нажата ли указанная кнопка мыши
- get_pressed_buttons() -> list[bool]: Возвращает список состояний всех кнопок мыши
- get_click(button: str) -> bool: Проверяет, была ли нажата указанная кнопка мыши


Методы Keyboard:
- get_pressed(key: str) -> bool: Проверяет, нажата ли указанная клавиша
- get_pressed_keys() -> list[bool]: Возвращает список состояний всех клавиш
- get_click(key: str) -> bool: Проверяет, была ли нажата указанная клавиша


Методы InputsHandler:
- add_event(event_type: str, id: int|str|None, key_or_btn: str) -> int|str: Добавляет событие для обработки
- remove_event(id: int|str): Удаляет событие из обработки
- update(): Обновляет состояния событий
- get_event(id: int|str) -> bool: Получает состояние события
- get_events_list() -> list[bool]: Получает список состояний всех событий


Глобальные переменные:
* MouseObject: Глобальный экземпляр класса Mouse для работы с мышью
* KeyboardObject: Глобальный экземпляр класса Keyboard для работы с клавиатурой


Примеры использования:

# Работа с мышью
>>> mouse_pos = MouseObject.get_position_on_window()  # Получить позицию мыши в окне
is_left_pressed = MouseObject.get_pressed(CONST_MOUSE_BUTTON_LEFT)  # Проверить нажатие левой кнопки
is_right_clicked = MouseObject.get_click(CONST_MOUSE_BUTTON_RIGHT)  # Проверить клик правой кнопкой
mouse_buttons = MouseObject.get_pressed_buttons()  # Получить состояния всех кнопок

# Работа с клавиатурой
>>> is_space_pressed = KeyboardObject.get_pressed("space")  # Проверить нажатие пробела
is_enter_clicked = KeyboardObject.get_click("return")  # Проверить клик клавиши Enter
keyboard_keys = KeyboardObject.get_pressed_keys()  # Получить состояния всех клавиш

# Работа с обработчиком событий
>>> handler = InputsHandler()

# Добавление событий
>>> jump_event = handler.add_event(CONST_KEY_PRESS_EVENT, "jump", "space")  # Событие прыжка
shoot_event = handler.add_event(CONST_MOUSE_BUTTON_CLICK_EVENT, "shoot", CONST_MOUSE_BUTTON_LEFT)  # Событие выстрела

# Обновление и получение состояний
>>> handler.update()  # Обновить состояния
is_jumping = handler.get_event("jump")  # Проверить событие прыжка
is_shooting = handler.get_event("shoot")  # Проверить событие выстрела

# Удаление события
>>> handler.remove_event("jump")  # Удалить событие прыжка
"""

from src.core.settings import (
    CONST_MOUSE_BUTTON_LEFT, CONST_MOUSE_BUTTON_RIGHT, CONST_MOUSE_BUTTON_MIDDLE,
    CONST_MOUSE_BUTTON_PRESS_EVENT, CONST_MOUSE_BUTTON_CLICK_EVENT, CONST_KEY_CLICK_EVENT, CONST_KEY_PRESS_EVENT
)

import mouse
import pygame
from uuid import uuid4

class Mouse:
    def __init__(self):
        """Инициализация объекта мыши."""
        self.clicked = False
    
    def get_position_on_screen(self) -> tuple[int, int]:
        """Получить текущую позицию мыши на экране."""
        return mouse.get_position()

    def get_position_on_window(self) -> tuple[int, int]:
        """Получить текущую позицию мыши в окне."""
        return pygame.mouse.get_pos()

    def get_speed(self) -> tuple[int, int]:
        """Получить скорость движения мыши."""
        return pygame.mouse.get_rel()

    def get_pressed(self, button: int = CONST_MOUSE_BUTTON_LEFT) -> bool:
        """Проверить, нажата ли кнопка мыши в окне."""
        return pygame.mouse.get_pressed()[{
            CONST_MOUSE_BUTTON_LEFT: 0,
            CONST_MOUSE_BUTTON_RIGHT: 1,
            CONST_MOUSE_BUTTON_MIDDLE: 2
        }[button]]

    def get_pressed_buttons(self) -> list[bool]:
        """Получить список нажатых кнопок мыши."""
        return list(pygame.mouse.get_pressed())

    def get_click(self, button: str = CONST_MOUSE_BUTTON_LEFT) -> bool:
        """Проверить, был ли клик кнопкой мыши."""
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


# Объект мыши для работы с мышью
MouseObject = Mouse()

class Keyboard:
    def __init__(self):
        """Инициализация объекта клавиатуры."""
        self.pressed = False

    def get_pressed(self, key: str) -> bool:
        """Проверить, нажата ли клавиша."""
        return pygame.key.get_pressed()[pygame.key.key_code(key)]

    def get_pressed_keys(self) -> list[bool]:
        """Получить список нажатых клавиш."""
        return list(pygame.key.get_pressed())

    def get_click(self, key: str) -> bool:
        """Проверить, была ли нажата клавиша."""
        is_pressed = pygame.key.get_pressed()[pygame.key.key_code(key)]

        if is_pressed and not self.pressed:
            self.pressed = True
            return True
        elif not is_pressed:
            self.pressed = False

        return False

# Объект клавиатуры для работы с клавиатурой
KeyboardObject = Keyboard()


class InputsHandler:
    def __init__(self):
        """Инициализация объекта обработчика событий."""
        self.__events: dict[int | str, tuple[str, str, bool]] = {}
    
    def add_event(self, event_type: str = CONST_MOUSE_BUTTON_PRESS_EVENT, id: int | str | None = None, key_or_btn: str = None) -> int | str:
        """Добавить событие для обработки."""
        object_id = id if id else uuid4()
        self.__events[object_id] = (event_type, key_or_btn, False)
        return object_id

    def remove_event(self, id: int | str):
        """Удалить событие из обработки."""
        if id in self.__events:
            self.__events.pop(id)

    def update(self):
        """Обновить состояния событий."""
        for object_id in list(self.__events.keys()):
            event_type, key_or_btn, _ = self.__events[object_id]
            
            if event_type in [CONST_MOUSE_BUTTON_PRESS_EVENT, CONST_MOUSE_BUTTON_CLICK_EVENT]:
                if event_type == CONST_MOUSE_BUTTON_PRESS_EVENT:
                    state = MouseObject.get_pressed(key_or_btn)
                else:
                    state = MouseObject.get_click(key_or_btn)
            else:
                if event_type == CONST_KEY_PRESS_EVENT:
                    state = KeyboardObject.get_pressed(key_or_btn)
                else:
                    state = KeyboardObject.get_click(key_or_btn)
                    
            self.__events[object_id] = (event_type, key_or_btn, state)
    
    def get_event(self, id: int | str) -> bool:
        """Получить состояние события."""
        return self.__events.get(id, (None, None, False))[2]

    def get_events_list(self) -> list[bool]:
        """Получить список состояний всех событий."""
        return [event_data[2] for event_data in self.__events.values()]