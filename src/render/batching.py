import pygame
from src.app import AppWindow

class Batch:
    """
    Класс для управления пакетами объектов для отрисовки.
    """
    def __init__(self, window: AppWindow, batch_size: int = 1000):
        self.__window = window
        self.__batch_size = batch_size
        self.__window_size = window.get_size()
        self.__surf = pygame.Surface(self.__window_size, pygame.SRCALPHA).convert_alpha()
        self.__render_calls_count = 0

    @property
    def surf(self):
        """
        Возвращает буферную поверхность для отрисовки.
        """
        self.__render_calls_count += 1
        return self.__surf

    def update(self):
        """
        Обновление буферной поверхности для отрисовки.
        """
        self.__render_calls_count = 0
        self.__surf.fill((0, 0, 0, 0))

    def render(self):
        """
        Отрисовка пакета объектов на экране.
        """
        self.__window.surf.blit(self.__surf, (0, 0), (0, 0, self.__window_size[0], self.__window_size[1]))
        

    