"""
Модуль sprites.py предоставляет классы и функции для работы со спрайтами и анимациями в pygame.

Основные классы:
- BaseSprite - базовый класс для работы с отдельными спрайтами
- BaseSpriteAnimation - класс для создания анимаций из спрайтов
- SpriteObject - расширенный BaseSprite с поддержкой позиционирования
- SpriteAnimationObject - расширенный BaseSpriteAnimation с поддержкой позиционирования

Основные функции:
- load_base_sprite() - загрузка спрайта из файла
- load_base_sprite_animation() - загрузка анимации из последовательности файлов
- load_sprite_sheet() - загрузка спрайтов из спрайтового листа с метками
- load_sprite_sheet_grid() - загрузка спрайтов из спрайтового листа по сетке
- fill() - заливка спрайта цветом
- paint() - окраска спрайта
- create_outline() - создание контура вокруг спрайта

Примеры использования:

1. Загрузка и отрисовка спрайта:

>>> # Создание спрайта из файла
    sprite = load_base_sprite("player.png")

>>> # Настройка спрайта
    sprite.set_scale(2.0)  # Масштаб
    sprite.set_angle(45)   # Поворот
    sprite.set_flip_x(True)  # Отражение по горизонтали

>>> # Отрисовка
    sprite.base_render(screen, (100, 100))


2. Создание и воспроизведение анимации:

>>> # Загрузка анимации из последовательности файлов
    animation = load_base_sprite_animation("walk_*.png", frames_count=8, frame_time=0.1, looped=True)

>>> # Настройка анимации
    animation.set_scale(1.5)
    animation.set_offset(OffSet.CENTER)

>>> # Обновление и отрисовка в игровом цикле
    while running:
        animation.update()
        animation.render(screen, (200, 200))


3. Работа со спрайтовым листом:

>>> # Загрузка спрайтов из листа с метками
    sprites = load_sprite_sheet("spritesheet.png")

>>> # Загрузка спрайтов из листа по сетке
    sprites = load_sprite_sheet_grid("spritesheet.png", sprite_width=32, sprite_height=32)


4. Эффекты со спрайтами:

>>> # Заливка спрайта цветом
    colored_sprite = fill(sprite, (255, 0, 0))

>>> # Окраска спрайта
    painted_sprite = paint(sprite, (0, 255, 0))

>>> # Создание контура
    outlined_sprite = create_outline(sprite, color=(0, 0, 0), thickness=2)


5. Использование SpriteObject для удобного позиционирования:

>>> sprite_obj = SpriteObject()
    sprite_obj.set_pos((100, 100))
    sprite_obj.move(Vector2D(10, 0))
    sprite_obj.render(screen)


6. Создание анимированного объекта:

>>> anim_obj = SpriteAnimationObject()
    anim_obj.add_frame(sprite1)
    anim_obj.add_frame(sprite2)
    anim_obj.set_frame_time(0.2)
    anim_obj.set_looped(True)
    anim_obj.set_pos((150, 150))

>>> # В игровом цикле:
    anim_obj.update()
    anim_obj.render(screen)


Дополнительные возможности:
- Управление прозрачностью через set_alpha()
- Установка точки привязки спрайта через set_offset()
- Копирование спрайтов и анимаций через copy()
- Поддержка различных форматов изображений (.png, .jpg, .bmp)
"""
import pygame
import enum
import time
from typing import Final, final, Literal
from uuid import uuid4

from src.maths import Vector2D
from src.render import colors
from src.debuger import debug_error, debug_info, debug_warning, debug_success
@final
class OffSet(enum.Enum):
    """
    Перечисление для определения точки привязки спрайта.
    
    CENTER - центр спрайта
    TOP_LEFT - верхний левый угол
    TOP_RIGHT - верхний правый угол
    TOP_CENTER - верхний центр
    BOTTOM_LEFT - нижний левый угол
    BOTTOM_RIGHT - нижний правый угол
    BOTTOM_CENTER - нижний центр
    LEFT_CENTER - левый центр
    RIGHT_CENTER - правый центр
    """
    CENTER = 0
    TOP_LEFT = 1
    TOP_RIGHT = 2
    TOP_CENTER = 3
    BOTTOM_LEFT = 4
    BOTTOM_RIGHT = 5
    BOTTOM_CENTER = 6
    LEFT_CENTER = 7
    RIGHT_CENTER = 8
    


"""
    Класс 'BaseSprite' предоставляет базовые функции для работы со спрайтами.
    Позволяет создавать, масштабировать, поворачивать и отрисовывать спрайты.
    Также есть возможность кеширования для ускорения отрисовки спрайта при повороте.

    Этот класс является базовым для других классов, таких как SpriteObject и SpriteAnimationObject, а также для TileSet.

    При помощи специальных методов (`paint`, `fill`, `create_outline`) можно применять различные эффекты к спрайту.
    `paint` позволяет окрасить спрайт в заданный цвет,
    `fill` заполняет спрайт цветом
    `create_outline` создает контур вокруг спрайта.
"""
@final
class BaseSprite:
    """
    Базовый класс для работы со спрайтами.
    
    Attributes:
        __real_sprite: Оригинальное изображение спрайта
        __final_sprite: Финальное изображение после всех трансформаций
        __angle: Угол поворота спрайта
        __scale: Масштаб спрайта
        __offset: Точка привязки спрайта
        __flip_x: Отражение по горизонтали
        __flip_y: Отражение по вертикали
    """
    def __init__(self, surf: pygame.Surface, caching: bool = False, caching_angles_count: int = 360):
        """
        Инициализация спрайта.
        
        Args:
            surf: Поверхность pygame с изображением
        """
        self.__real_sprite = surf.convert_alpha()
        self.__final_sprite: pygame.Surface | None = surf

        self.__angle = 0
        self.__scale = 1
        self.__offset: tuple[int, int] | OffSet = OffSet.CENTER
        self.__flip_x = False
        self.__flip_y = False

        self.__alpha = 255

        # флаг который говорит о том что спрайт будет статичным
        # ~ Спрайт невозможно будет отражать
        self.__static: bool = False

        self.__caching: bool = caching
        
        self.__rotate_cache: dict[int, pygame.Surface] = {}
        self.__caching_angles_count = caching_angles_count
        if self.__caching: 
            self.generate_rotate_cache(self.__caching_angles_count)
            self.__static = True

    def set_static(self, value: bool):
        """
        Установить статичность спрайта
        """
        if not self.__caching and value:
            self.generate_rotate_cache(self.__caching_angles_count)
            self.__static = True
        else:
            self.__static = value
        
        return self

    def is_static(self) -> bool:
        """Проверить является ли спрайт статичным"""
        return self.__static
    
    def is_cached(self) -> bool:
        """Проверить есть ли кэш поворота у спрайта"""
        return len(self.__rotate_cache) > 0
    
    def is_caching(self) -> bool:
        """Проверить включено ли кэширование поворота"""
        return self.__caching   
     
    def normalize_angle_to_caching(self, angle: float) -> int:
        """
        Нормализация угла для кэша поворота
        """
        if angle < 0:
            angle = 360 + angle

        angle = angle % 360
        step = 360 // self.__caching_angles_count
        new_angle = angle - angle % step
        if new_angle + step > 360:
            new_angle = 0
        return new_angle
        

    def generate_rotate_cache(self, angles_count: int = 360):
        """
        Генерация кэша для поворота спрайта

        Args:
            angles_count: Количество углов для кэша
        """
        self.__caching_angles_count = angles_count
        step = 360 // angles_count
        for i in range(angles_count):
            angle = int(round(i * step))
            self.__rotate_cache[angle] = pygame.transform.rotate(self.__real_sprite, angle)
        print(f"BaseSprite: Cache generated for {angles_count} angles.")   

    def get_real_size(self) -> tuple[int, int]:
        """Получить размер оригинального изображения"""
        return self.__real_sprite.get_size()
    
    def get_final_size(self) -> tuple[int, int]:
        """Получить размер финального изображения"""
        if self.__final_sprite is None: self.update()
        return self.__final_sprite.get_size()

    def get_alpha(self) -> int:
        """Получить текущий уровень прозрачности"""
        return self.__alpha
    
    def set_alpha(self, alpha: int):
        """Установить уровень прозрачности от 0 до 255"""
        self.__alpha = alpha
        self.update()
        return self
    
    def set_alpha_percent(self, percent: int):
        """Установить уровень прозрачности от 0 до 100"""
        self.__alpha = int(percent * 2.55)
        self.update()
        return self
    
    def set_alpha_float(self, alpha: float):
        """Установить уровень прозрачности от 0.0 до 1.0"""
        self.__alpha = int(alpha * 255)
        self.update()
        return self

    def set_real_sprite(self, sptite: pygame.Surface):
        """Установить оригинальное изображение"""
        self.__real_sprite = sptite
        self.update()
        return self

    def get_real_sprite(self) -> pygame.Surface:
        """Получить оригинальное изображение"""
        return self.__real_sprite

    def get_real_size(self) -> tuple[int, int]:
        """Получить размер оригинального изображения"""
        return self.__real_sprite.get_size()
    
    def set_flip_x(self, flip_x: bool):
        """Установить отражение по горизонтали"""
        self.__flip_x = flip_x
        self.update()
        return self

    def set_flip_y(self, flip_y: bool):
        """Установить отражение по вертикали"""
        self.__flip_y = flip_y
        self.update()
        return self

    def flip_x(self):
        """Отразить спрайт по горизонтали"""
        self.set_flip_x(not self.__flip_x)
        return self

    def flip_y(self):
        """Отразить спрайт по вертикали"""
        self.set_flip_y(not self.__flip_y)
        return self

    def set_scale(self, scale: float):
        """Установить масштаб спрайта"""
        self.__scale = scale
        self.update()
        return self

    def set_angle(self, angle: float):
        """Установить угол поворота спрайта"""
        self.__angle = angle
        self.update()
        return self

    def rotate(self, angle: float):
        """Повернуть спрайт на заданный угол"""
        self.__angle += angle
        self.update()
        return self

    def get_angle(self) -> float:
        """Получить текущий угол поворота"""
        return self.__angle
    
    def set_offset(self, offset: tuple[int, int] | OffSet):
        """Установить точку привязки спрайта"""
        self.__offset = offset
        return self

    def get_offset(self) -> tuple[int, int]:
        """Получить текущую точку привязки"""
        return self.__offset
    
    def get_scale(self) -> float:
        """Получить текущий масштаб"""
        return self.__scale
    
    def get_flip_x(self) -> bool:
        """Получить состояние отражения по горизонтали"""
        return self.__flip_x
    
    def get_flip_y(self) -> bool:
        """Получить состояние отражения по вертикали"""
        return self.__flip_y

    def update(self):
        """Обновить финальное изображение с учетом всех трансформаций"""
        if not self.__static:
            sprite = pygame.transform.flip(self.__real_sprite, self.__flip_x, self.__flip_y)
            sprite = pygame.transform.scale(sprite, (int(self.__real_sprite.get_width() * self.__scale), int(self.__real_sprite.get_height() * self.__scale)))
            sprite = pygame.transform.rotate(sprite, self.__angle)
        else:
            sprite = self.__rotate_cache[self.normalize_angle_to_caching(self.__angle)]
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * self.__scale), int(sprite.get_height() * self.__scale)))
            sprite = pygame.transform.flip(sprite, self.__flip_x, self.__flip_y)
        sprite.set_alpha(self.__alpha)
        
        self.__final_sprite = sprite

    def copy(self) -> 'BaseSprite':
        """Создать копию спрайта"""
        sprite = BaseSprite(self.__real_sprite)
        sprite.set_angle(self.__angle)
        sprite.set_scale(self.__scale)
        sprite.set_offset(self.__offset)
        sprite.set_flip_x(self.__flip_x)
        sprite.set_flip_y(self.__flip_y)    
        return sprite

    def base_render(self, surf: pygame.Surface, pos: tuple[int, int]):
        """
        Отрисовать спрайт на поверхности.
        
        Args:
            surf: Поверхность для отрисовки
            pos: Позиция отрисовки (x, y)
        """
        if self.__final_sprite is None:
            self.update()
        if isinstance(self.__offset, OffSet):
            if self.__offset == OffSet.CENTER:
                surf.blit(self.__final_sprite, (pos[0] - self.__final_sprite.get_width() / 2, pos[1] - self.__final_sprite.get_height() / 2))
            elif self.__offset == OffSet.TOP_LEFT:
                surf.blit(self.__final_sprite, (pos[0], pos[1]))
            elif self.__offset == OffSet.TOP_RIGHT:
                surf.blit(self.__final_sprite, (pos[0] - self.__final_sprite.get_width(), pos[1]))
            elif self.__offset == OffSet.TOP_CENTER:
                surf.blit(self.__final_sprite, (pos[0] - self.__final_sprite.get_width() / 2, pos[1]))
            elif self.__offset == OffSet.BOTTOM_LEFT:
                surf.blit(self.__final_sprite, (pos[0], pos[1] - self.__final_sprite.get_height()))
            elif self.__offset == OffSet.BOTTOM_RIGHT:
                surf.blit(self.__final_sprite, (pos[0] - self.__final_sprite.get_width(), pos[1] - self.__final_sprite.get_height()))
            elif self.__offset == OffSet.BOTTOM_CENTER:
                surf.blit(self.__final_sprite, (pos[0] - self.__final_sprite.get_width() / 2, pos[1] - self.__final_sprite.get_height()))
            elif self.__offset == OffSet.LEFT_CENTER:
                surf.blit(self.__final_sprite, (pos[0], pos[1] - self.__final_sprite.get_height() / 2))
            elif self.__offset == OffSet.RIGHT_CENTER:
                surf.blit(self.__final_sprite, (pos[0] - self.__final_sprite.get_width(), pos[1] - self.__final_sprite.get_height() / 2))
        else:
            surf.blit(self.__final_sprite, (pos[0] - self.__offset[0], pos[1] - self.__offset[1]))



"""
    Класс 'BaseSpriteAnimation' для создания и управления анимацией спрайтов.
    Является контейнером для класса 'BaseSprite'.
    Позволяет покадрово отображать кадры анимации. Анимация проигрывается не завися от количества кадров, она на прямую связана с временем отображения одного кадра.
"""
@final
class BaseSpriteAnimation:
    """
    Класс для создания и управления анимацией спрайтов.
    
    Attributes:
        __frames: Список кадров анимации
        __looped: Флаг зацикленности анимации
        __current_frame: Индекс текущего кадра
        __frame_time: Время показа одного кадра
        __before_frame_time: Время последней смены кадра
        __angle: Угол поворота анимации
        __scale: Масштаб анимации
        __offset: Точка привязки анимации
        __flip_x: Отражение по горизонтали
        __flip_y: Отражение по вертикали
    """
    def __init__(self):
        """Инициализация анимации"""
        self.__frames: list[BaseSprite] = []
        self.__looped = False
        self.__current_frame = 0
        self.__frame_time = 0

        self.__before_frame_time = 0

        self.__angle = 0
        self.__scale = 1
        self.__offset: tuple[int, int] | OffSet = OffSet.CENTER
        self.__flip_x = False
        self.__flip_y = False
        self.__alpha = 255

    def get_alpha(self) -> int:
        """Получить текущий уровень прозрачности"""
        return self.__alpha
    
    def set_alpha(self, alpha: int):
        """Установить уровень прозрачности для всех кадров от 0 до 255"""
        self.__alpha = alpha
        for frame in self.__frames:
            frame.set_alpha(alpha)
        return self
    
    def set_alpha_percent(self, percent: int):
        """Установить уровень прозрачности для всех кадров в процентах от 0 до 100"""
        self.__alpha = int(2.55 * percent)
        for frame in self.__frames:
            frame.set_alpha(self.__alpha)
        return self
    
    def set_alpha_float(self, alpha: float):
        """Установить уровень прозрачности для всех кадров в процентах от 0.0 до 1.0"""
        self.__alpha = int(255 * alpha)
        for frame in self.__frames:
            frame.set_alpha(self.__alpha)
        return self



    def get_frames(self) -> list[BaseSprite]:
        """Получить список кадров анимации"""
        return self.__frames
    
    def clear_frames(self):
        """Очистить список кадров анимации"""
        self.__frames.clear()
        return self
    
    def set_flip_x(self, flip_x: bool):
        """Установить отражение по горизонтали для всех кадров"""
        self.__flip_x = flip_x
        for frame in self.__frames:
            frame.set_flip_x(flip_x)
        return self

    def set_flip_y(self, flip_y: bool):
        """Установить отражение по вертикали для всех кадров"""
        self.__flip_y = flip_y
        for frame in self.__frames:
            frame.set_flip_y(flip_y)
        return self

    def flip_x(self):
        """Отразить все кадры по горизонтали"""
        self.set_flip_x(not self.__flip_x)
        return self

    def flip_y(self):
        """Отразить все кадры по вертикали"""
        self.set_flip_y(not self.__flip_y)
        return self

    def set_scale(self, scale: float):
        """Установить масштаб для всех кадров"""
        self.__scale = scale
        for frame in self.__frames:
            frame.set_scale(scale)
        return self

    def set_angle(self, angle: float):
        """Установить угол поворота для всех кадров"""
        self.__angle = angle
        for frame in self.__frames:
            frame.set_angle(angle)
        return self

    def rotate(self, angle: float):
        """Повернуть все кадры на заданный угол"""
        self.__angle += angle
        for frame in self.__frames:
            frame.rotate(angle)
        return self

    def get_angle(self) -> float:
        """Получить текущий угол поворота"""
        return self.__angle
    
    def set_offset(self, offset: tuple[int, int] | OffSet):
        """Установить точку привязки анимации"""
        self.__offset = offset
        return self

    def get_offset(self) -> tuple[int, int]:
        """Получить текущую точку привязки"""
        return self.__offset
    
    def get_scale(self) -> float:
        """Получить текущий масштаб"""
        return self.__scale
    
    def get_flip_x(self) -> bool:
        """Получить состояние отражения по горизонтали"""
        return self.__flip_x
    
    def get_flip_y(self) -> bool:
        """Получить состояние отражения по вертикали"""
        return self.__flip_y
    
    def add_frame(self, sprite: BaseSprite):
        """Добавить кадр в анимацию"""
        self.__frames.append(sprite)

    def get_current_frame(self) -> BaseSprite:
        """Получить текущий кадр анимации"""
        return self.__frames[self.__current_frame]
    
    def get_current_frame_index(self) -> int:
        """Получить индекс текущего кадра"""
        return self.__current_frame
    
    def get_frame_time(self) -> float:
        """Получить время показа одного кадра"""
        return self.__frame_time
    
    def get_looped(self) -> bool:
        """Получить состояние зацикленности анимации"""
        return self.__looped
    
    def set_looped(self, looped: bool):
        """Установить зацикленность анимации"""
        self.__looped = looped
        return self

    def set_frame_time(self, frame_time: float):
        """Установить время показа одного кадра"""
        self.__frame_time = frame_time
        return self

    def update_animation(self):
        """Обновить состояние анимации"""
        if self.__before_frame_time == 0:
            self.__before_frame_time = time.time()
            return
        
        if time.time() - self.__before_frame_time > self.__frame_time:
            self.__before_frame_time = time.time()
            self.__current_frame += 1
            if self.__current_frame >= len(self.__frames):
                if self.__looped:
                    self.__current_frame = 0
                else:
                    self.__current_frame = len(self.__frames) - 1

    def copy(self) -> 'BaseSpriteAnimation':
        """Получить копию анимации"""
        animation = BaseSpriteAnimation()
        for frame in self.__frames:
            animation.add_frame(frame.copy())
        animation.set_angle(self.__angle)
        animation.set_scale(self.__scale)
        animation.set_offset(self.__offset)
        animation.set_flip_x(self.__flip_x)
        animation.set_flip_y(self.__flip_y)
        animation.set_looped(self.__looped)
        animation.set_frame_time(self.__frame_time)

        return animation

    def render(self, surf: pygame.Surface, pos: tuple[int, int]):
        """
        Отрисовать текущий кадр анимации.
        
        Args:
            surf: Поверхность для отрисовки
            pos: Позиция отрисовки (x, y)
        """
        self.get_current_frame().base_render(surf, pos)



"""
    Метод позволяющий быстро загрузить и собрать анимацию из некоторой последовательности файлов изображений.
    Формат пути - 'path/to/file_*.png' вмето звездочки подставляется номер кадра.
    Поддерживаемые расширения файлов: `.png`, `.jpg`, `.bmp`
"""
@final
def load_base_sprite_animation(path: str, frames_count: int, frame_time: float, looped: bool = False) -> BaseSpriteAnimation:
    """
    Создает анимацию из файлов изображений.
    Формат пути - 'path/to/file_*.png' вмето звездочки подставляется номер кадра.

    Args:
        path: Путь к файлу изображения (.png, .jpg, .bmp)
        frames_count: Количество кадров
        frame_time: Время показа одного кадра
        looped: Флаг зацикленности анимации

    Returns:
        Animation: Загруженная анимация
    """
    animation = BaseSpriteAnimation()
    for i in range(frames_count):
        animation.add_frame(load_base_sprite(path.replace('*', str(i+1))))
    animation.set_frame_time(frame_time)
    animation.set_looped(looped)
    return animation
   


"""
    Метод позволяющий быстро загрузить и собрать спрайт из файла изображения.
    Поддерживаемые расширения файлов: `.png`, `.jpg`, `.bmp`
    При загрузке можно сразу указать количество углов для кэширования.
    Если указать None, то кэширование не будет использоваться.
"""
@final
def load_base_sprite(path: str, caching_angles: int | None = None) -> BaseSprite:
    """
    Загружает спрайт из файла.
    
    Args:
        path: Путь к файлу изображения (.png, .jpg, .bmp)
        caching_angles: Количество углов для кэширования. Если None, то кэширование не используется.
    
    Returns:
        BaseSprite: Загруженный спрайт
    """
    return BaseSprite(pygame.image.load(path), True if caching_angles is not None else False, caching_angles)



"""
    Класс 'SpriteObject' - это класс, который наследуется от класса BaseSprite и добавляет возможность перемещения спрайта по экрану.
    Имеет методы для получения и установки позиции спрайта.
"""
@final
class SpriteObject(BaseSprite):
    def __init__(self):
        super().__init__()
        self.__pos = Vector2D(0, 0)

    def set_pos(self, pos: tuple[int, int] | Vector2D):
        """Установить позицию спрайта"""
        self.__pos = Vector2D.from_tuple(pos) if isinstance(pos, (tuple, list)) else pos

    def get_pos(self) -> Vector2D:
        """Получить позицию спрайта"""
        return self.__pos
    
    def move(self, move_vector: Vector2D):
        """Переместить спрайт на заданный вектор"""
        self.__pos += move_vector

    def render(self, surf: pygame.Surface):
        """
        Отрисовать спрайт.

        Args:
            surf: Поверхность для отрисовки
            pos: Позиция отрисовки (x, y)
        """
        self.base_render(surf, self.__pos)
    
@final
class SpriteAnimationObject(BaseSpriteAnimation):
    def __init__(self):
        super().__init__()
        self.__pos = Vector2D(0, 0)

    def set_pos(self, pos: tuple[int, int] | Vector2D):
        """Установить позицию спрайта"""
        self.__pos = Vector2D.from_tuple(pos) if isinstance(pos, (tuple, list)) else pos
        return self

    def get_pos(self) -> Vector2D:
        """Получить позицию спрайта"""
        return self.__pos
    
    def move(self, move_vector: Vector2D):
        """Переместить спрайт на заданный вектор"""
        self.__pos += move_vector

    def copy(self) -> 'BaseSpriteAnimation':
        """Получить копию анимации"""
        animation = SpriteAnimationObject()
        for frame in self.get_frames():
            animation.add_frame(frame.copy())
        animation.set_angle(self.get_angle())
        animation.set_scale(self.get_scale())
        animation.set_offset(self.get_offset())
        animation.set_flip_x(self.get_flip_x())
        animation.set_flip_y(self.get_flip_y())
        animation.set_looped(self.get_looped())
        animation.set_frame_time(self.get_frame_time())
        animation.set_pos(self.get_pos())

        return animation

    def render(self, surf: pygame.Surface):
        """
        Отрисовать анимацию.
        Args:
            surf: Поверхность для отрисовки
            pos: Позиция отрисовки (x, y)
        """
        super().render(surf, self.__pos.xy)


# Базовые типы спрайтов и анимаций
type UnionSprite = SpriteObject | BaseSprite
type UnionAnimation = SpriteAnimationObject | BaseSpriteAnimation
type UnionSpriteOrAnimation = UnionSprite | UnionAnimation


@final
def load_sprite_animation(path: str, frames_count: int, frame_time: float, looped: bool = False) -> SpriteAnimationObject:
    """
    Создает анимацию из файлов изображений.
    Формат пути - 'path/to/file_*.png' вмето звездочки подставляется номер кадра.
    Args:
        path: Путь к файлу изображения (.png, .jpg, .bmp)
        frames_count: Количество кадров
        frame_time: Время показа одного кадра
        looped: Флаг зацикленности анимации
    returns:
        Animation: Загруженная анимация
    """
    animation = SpriteAnimationObject()
    for i in range(frames_count):
        animation.add_frame(load_base_sprite(path.replace('*', str(i+1))))
    animation.set_frame_time(frame_time)
    animation.set_looped(looped)
    return animation


@final
def convert_color(color: pygame.Color) -> tuple[int, int, int]:
    """
    Преобразует цвет pygame в кортеж
    """
    return color.r, color.g, color.b


@final
def load_sprite_sheet(path: str, debug: bool = True) -> list[BaseSprite]:
    """
    Загружает спрайты из файла находя их по определенным меткам
    красный пиксель - начало строки со спрайтами
    целеный пиксель - метка начала спрайта левый верхний угол спрайта
    синий пискель метка для указания ширины и высоты спрайта

    args:
        path: Путь к файлу изображения (.png, .jpg, .bmp)
        debug: Флаг для вывода отладочной информации
    returns:
        list[BaseSprite]: Список спрайтов
    """
    sprites = []
    debug_warning(f'Loading sprite sheet from {path}')
    sprite_sheet = pygame.image.load(path)
    sprite_sheet = sprite_sheet.convert_alpha()
    width, height = sprite_sheet.get_size()
    
    start_time = time.time()

    sprite_lines_y = []
    for y in range(height):
        if convert_color(sprite_sheet.get_at((0, y))) == (255, 0, 0):
            sprite_lines_y.append(y)

    for line_y in sprite_lines_y:
        x = 0
        while x < width:
            color = convert_color(sprite_sheet.get_at((x, line_y)))
            if color == (0, 255, 0):
                pos = (x, line_y)
                size = [0, 0]
                
                # Find width
                for dx in range(x, width):
                    color = convert_color(sprite_sheet.get_at((dx, line_y)))
                    if color == (0, 0, 255):
                        size[0] = dx - pos[0]
                        break
                
                # Find height
                for dy in range(line_y, height):
                    color = convert_color(sprite_sheet.get_at((x, dy)))
                    if color == (0, 0, 255):
                        size[1] = dy - pos[1]
                        break
                
                if size[0] > 0 and size[1] > 0:
                    debug_info(f"Found sprite at {pos} with size {size}")
                    pos = [pos[0] + 1, pos[1] + 1]
                    size = [size[0] - 1, size[1] - 1]
                    sprite = BaseSprite(sprite_sheet.subsurface(pygame.Rect(pos, size)))
                    sprites.append(sprite)
                x += max(1, size[0])
            x += 1
    debug_success(f"Loaded {len(sprites)} sprites from '{path}' in {time.time() - start_time} seconds")
    
    return sprites


@final
def load_sprite_sheet_grid(path: str, sprite_width: int, sprite_height: int) -> list[BaseSprite]:
    """
    Загружает спрайты из файла, разделяя его на равные части по сетке.
    Возвращает список BaseSprite.
    
    Args:
        path: Путь к файлу изображения (.png, .jpg, .bmp)
        sprite_width: Ширина одного спрайта
        sprite_height: Высота одного спрайта
        
    Returns:
        list[BaseSprite]: Список спрайтов
    """
    sprites = []
    sprite_sheet = pygame.image.load(path).convert_alpha()
    sheet_width, sheet_height = sprite_sheet.get_size()
    debug_warning(f'Loading sprite sheet gred from {path}')
    for y in range(0, sheet_height, sprite_height):
        for x in range(0, sheet_width, sprite_width):
            sprite_rect = pygame.Rect(x, y, sprite_width, sprite_height)
            sprite = BaseSprite(sprite_sheet.subsurface(sprite_rect))
            sprites.append(sprite)
    debug_success(f"Loaded {len(sprites)} sprites from '{path}'")
    return sprites


@final
def fill(data: UnionSpriteOrAnimation, color: tuple[int, int, int] | colors.Color = (0, 0, 0)) -> UnionSpriteOrAnimation:
    """
    Заполняет спрайт или анимацию заданным цветом. Игнорирует прозрачные пиксели. Возвращает новый спрайт.
    Args:
        data: Спрайт или анимация, которую нужно заполнить.
        color: Цвет, которым нужно заполнить спрайт или анимацию.

    Returns:
        Спрайт или анимация с заполненным цветом.
    """
    color = color() if isinstance(color, colors.Color) else color
    if isinstance(data, (BaseSprite, SpriteObject)):
        sprite = data.get_real_sprite()
        sprite_copy = sprite.copy()
        white_pixels = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
        white_pixels.fill((color[0], color[1], color[2], 255))
        sprite_copy.blit(white_pixels, (0, 0), special_flags=pygame.BLEND_MAX)
        sprite_copy.blit(white_pixels, (0, 0), special_flags=pygame.BLEND_MIN)
        sc = data.copy()
        debug_info(f"Filled sprite with color {color}")
        return sc.set_real_sprite(sprite_copy)
    elif isinstance(data, (BaseSpriteAnimation, SpriteAnimationObject)):
        new_animation = data.copy().clear_frames()
        for frame in data.get_frames():
            new_animation.add_frame(paint(frame, color))
        debug_info(f"Filled animation with color {color}")
        return new_animation


@final
def paint(data: UnionSpriteOrAnimation, color: tuple[int, int, int] | colors.Color = (0, 0, 0)) -> UnionSpriteOrAnimation:
    """
    Красит спрайт или анимацию заданным цветом. Игнорирует прозрачные пиксели. Возвращает новый спрайт.
    Args:
        data: Спрайт или анимация, которую нужно заполнить.
        color: Цвет, которым нужно заполнить спрайт или анимацию.

    Returns:
        Спрайт или анимация с заполненным цветом.
    """
    color = color() if isinstance(color, colors.Color) else color
    if isinstance(data, (BaseSprite, SpriteObject)):
        sprite = data.get_real_sprite()
        sprite_copy = sprite.copy()
        white_pixels = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
        white_pixels.fill((color[0], color[1], color[2], 255))
        sprite_copy.blit(white_pixels, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
        sc = data.copy()
        debug_success(f"Sprite: Painted with color {color}")
        return sc.set_real_sprite(sprite_copy)
    elif isinstance(data, (BaseSpriteAnimation, SpriteAnimationObject)):
        new_animation = data.copy().clear_frames()
        for frame in data.get_frames():
            new_animation.add_frame(paint(frame, color))
        debug_success(f"Animation: Painted with color {color}")
        return new_animation
    

@final
def create_outline(data: UnionSpriteOrAnimation, color: tuple[int, int, int] = (0, 0, 0), thickness: int = 1) -> UnionSpriteOrAnimation:
    """
    Создает контур вокруг спрайта или анимации возвращает новый спрайт или анимацию с контуром.

    Args:
        data: Спрайт или анимация, для которой нужно создать контур.
        color: Цвет контура.
        thickness: Толщина контура.
    Returns:
        Новый спрайт или анимация с контуром.
    """

    if isinstance(data, (BaseSprite, SpriteObject)):
        sprite = data.get_real_sprite()
        sprite_copy = fill(data, color).get_real_sprite() 

        size = [sprite.get_width() + thickness * 2, sprite.get_height() + thickness * 2]
        new_sprite = pygame.Surface(size, pygame.SRCALPHA)
        new_sprite.fill((0, 0, 0, 0))
        for dx in range(-thickness, thickness + 1):
            for dy in range(-thickness, thickness + 1):
                new_sprite.blit(sprite_copy, (dx + thickness, dy + thickness))
        
        new_sprite.blit(sprite, (thickness, thickness))
        debug_success(f"Created outline for sprite with color {color} and thickness {thickness}")
        return data.copy().set_real_sprite(new_sprite)
    
    if isinstance(data, (BaseSpriteAnimation, SpriteAnimationObject)):
        copied_animation = data.copy()
        copied_animation.clear_frames()
        for frame in data.get_frames():
            copied_animation.add_frame(create_outline(frame, color, thickness))
        debug_success(f"Created outline for animation with color {color} and thickness {thickness}")
        return copied_animation
        

@final
def scale_all(self, data: list[UnionSpriteOrAnimation], scale: float) -> UnionSpriteOrAnimation:
    """
    Масштабирует каждый элемент списка.
    Args:
        data: Список спрайтов или анимаций, которые нужно масштабировать.
        scale: Масштаб, на который нужно масштабировать спрайт.

    Returns:
        Новый спрайт или анимация с масштабированными кадрами.
    """
    return list(map(lambda obj: obj.set_scale(scale), data))


@final
def set_flip_all(self, data: list[UnionSpriteOrAnimation], flip_x: bool = False, flip_y: bool = False) -> list[UnionSpriteOrAnimation]:
    """
    Переворачивает спрайт или анимацию по горизонтали или вертикали.
    Если значение указано как True, то обьект будет отражен в лево а если False то в право.
    Args:
        data: Спрайт или анимация, которую нужно перевернуть.
        flip_x: Если True, спрайт будет перевернут по горизонтали.
        flip_y: Если True, спрайт будет перевернут по вертикали.
    Returns:
        Новый спрайт или анимация с перевернутыми кадрами.
    """
    data = list(map(lambda obj: obj.set_flip_x(flip_x)), data)
    data = list(map(lambda obj: obj.set_flip_y(flip_y)), data)
    return data


@final
def flip_all(self, data: list[UnionSpriteOrAnimation], flip_x: bool = False, flip_y: bool = False) -> list[UnionSpriteOrAnimation]:
    """
    Переворачивает спрайт или анимацию по горизонтали или вертикали.
    Если значение указано как True, то обьект будет отражен по выбраной оси. 
    Args:
        data: Спрайт или анимация, которую нужно перевернуть.
        flip_x: Если True, спрайт будет перевернут по горизонтали.
        flip_y: Если True, спрайт будет перевернут по вертикали.
    Returns:
        Новый спрайт или анимация с перевернутыми кадрами.
    """
    if flip_x: data = list(map(lambda obj: obj.flip_x()), data)
    if flip_y: data = list(map(lambda obj: obj.flip_y()), data)
    return data



class TileType:
    """
    Класс для определения типа тайла
    """
    def __init__(self, name: str):
        self.__name = name
    
    def get_name(self) -> str: return self.__name

    def __eq__(self, other: "TileType"):
        if isinstance(other, TileType):
            return self.get_name() == other.get_name()
        return False
    
    def __ne__(self, other: "TileType"):
        if isinstance(other, TileType):
            return self.get_name() != other.get_name()
        return True


DummyTileType = TileType("dummy")


# ! ------- 
# TODO
# ! ------- 
class TileConfig:
    """
    Класс для конфигурации тайла.
    """
    def __init__(self, up_left: bool = None,   up: bool = None,      up_right: bool = None, 
                       left: bool = None,      center: bool = True,  right: bool = None, 
                       down_left: bool = None, down: bool = None,    down_right: bool = None, type: TileType = DummyTileType):
        """
        Инициализирует объект TileConfig.
        Необходипо описать окружение тайла, какую позицию он занимает.
        """
        self.up_left = up_left
        self.up = up
        self.up_right = up_right
        self.left = left
        self.center = center
        self.right = right
        self.down_left = down_left
        self.down = down
        self.down_right = down_right

        self.__type = type

    def get_type(self)  -> TileType:
        return self.__type
    
# ! ------- 
# TODO
# ! ------- 
class Tile(BaseSprite):
    """
    Класс для создания тайла.
    """
    def __init__(self, sprite: pygame.Surface, config: TileConfig):
        """
        Инициализирует объект Tile.
        Args:
            sprite: Прямоугольник, который будет использоваться в качестве тайла.
        """
        super().__init__(sprite)
        self.__config = config

    def get_config(self) -> TileConfig:
        return self.__config
    
# ! ------- 
# TODO
# ! ------- 
class TileSet:
    """
    Класс для создания набора тайлов.
    """
    def __init__(self, tiles: dict[TileConfig, Tile], name: str):
        """
        Инициализирует объект TileSet.
        Args:
            tiles: Список тайлов, которые будут использоваться в наборе.
        """
        self.__tiles = tiles
        self.__name = name

    def get_name(self) -> str:
        return self.__name
    
    def get_tiles(self) -> dict[TileConfig, Tile]:
        return self.__tiles

        

def load_standart_tileset(path: str, tile_size: int = 32, type: str | Literal['base'] = "base") -> TileSet:
    """
    Загружает стандартный набор тайлов (48 тайлов).
    Args:
        path: Путь к файлу с изображению.
        tile_size: Размер тайла.
        type: Тип тайлсета (пока только 'base' поддерживается)
    Returns:
        Набор тайлов.
    """
    # Загружаем все тайлы из спрайтшита
    loaded_base_tiles = load_sprite_sheet_grid(path, tile_size, tile_size)
    
    if len(loaded_base_tiles) != 48:
        debug_warning(f"TileSetLoader: Expected 48 tiles, got {len(loaded_base_tiles)}. Results may be unexpected.")
    
    # Создаем TileType для земли
    ground_type = TileType(type)
    
    # Создаем конфигурации для всех возможных комбинаций
    # Порядок тайлов в стандартном тайлсете обычно следующий:
    
    # 1. Полностью окруженный (внутренний)
    inner_config = TileConfig(
        up_left=True, up=True, up_right=True,
        left=True, center=True, right=True,
        down_left=True, down=True, down_right=True,
        type=ground_type
    )
    
    # 2-17. Края и углы (16 тайлов)
    # Создаем все комбинации для краев
    edge_configs = []
    for up in [False, True]:
        for right in [False, True]:
            for down in [False, True]:
                for left in [False, True]:
                    config = TileConfig(
                        up=up, right=right, down=down, left=left,
                        up_left=up and left, up_right=up and right,
                        down_left=down and left, down_right=down and right,
                        center=True,
                        type=ground_type
                    )
                    edge_configs.append(config)
    
    # 18-33. Внутренние углы (16 тайлов)
    inner_corner_configs = []
    for up in [False, True]:
        for right in [False, True]:
            for down in [False, True]:
                for left in [False, True]:
                    config = TileConfig(
                        up=up, right=right, down=down, left=left,
                        up_left=not (up and left), 
                        up_right=not (up and right),
                        down_left=not (down and left), 
                        down_right=not (down and right),
                        center=True,
                        type=ground_type
                    )
                    inner_corner_configs.append(config)
    
    # 34-41. Одиночные выступы (8 тайлов)
    single_configs = []
    directions = ['up', 'right', 'down', 'left', 'up_right', 'down_right', 'down_left', 'up_left']
    for direction in directions:
        config_dict = {
            'up': False, 'right': False, 'down': False, 'left': False,
            'up_left': False, 'up_right': False, 'down_left': False, 'down_right': False,
            'center': True,
            'type': ground_type
        }
        config_dict[direction] = True
        config = TileConfig(**config_dict)
        single_configs.append(config)
    
    # 42-47. Дополнительные тайлы (6 тайлов) - обычно для особых случаев
    special_configs = [
        # Полностью пустой (но с центром)
        TileConfig(center=True, type=ground_type),
        # Только углы
        TileConfig(up_left=True, up_right=True, down_left=True, down_right=True, center=True, type=ground_type),
        # Горизонтальная линия
        TileConfig(left=True, right=True, center=True, type=ground_type),
        # Вертикальная линия
        TileConfig(up=True, down=True, center=True, type=ground_type),
        # Диагональ \
        TileConfig(up_left=True, down_right=True, center=True, type=ground_type),
        # Диагональ /
        TileConfig(up_right=True, down_left=True, center=True, type=ground_type)
    ]
    
    # Собираем все конфиги в один список в правильном порядке
    all_configs = [inner_config] + edge_configs + inner_corner_configs + single_configs + special_configs
    
    # Создаем словарь тайлов
    tiles_dict = {}
    for i, config in enumerate(all_configs):
        if i < len(loaded_base_tiles):
            tiles_dict[config] = Tile(loaded_base_tiles[i], config)
        else:
            debug_warning(f"TileSetLoader: Not enough tiles for config {i}. Skipping.")
            break
    
    return TileSet(tiles_dict, "standard_ground_tileset")