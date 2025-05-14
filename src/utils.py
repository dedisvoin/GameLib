"""
Этот модуль предоставляет утилиты для операций, основанных на времени, и подсчета тиков.

Классы:
    TickCounter: Класс для управления операциями подсчета тиков на основе времени.

Функции:
    wait: Функция, реализующая неблокирующий таймер с уникальными идентификаторами.

Глобальные переменные:
    TICK_COUNTERS: Словарь, хранящий экземпляры TickCounter, индексированные по их ID.
"""

from uuid import uuid4
from time import time
from typing import final, Final


# Список счетчиков тиков
TICK_COUNTERS: Final[dict[str, 'TickCounter']] = {}

@final
class TickCounter:
    """
    Класс, реализующий счетчик тиков для операций, основанных на времени.

    Атрибуты:
        __before_time (float): Временная метка последнего тика.
        __tick_count (float): Продолжительность каждого тика в секундах.
        __id (str): Уникальный идентификатор счетчика.
        __start_count (bool): Флаг, указывающий, начался ли отсчет.

    Методы:
        get_tick_count(): Возвращает продолжительность тика.
        get_id(): Возвращает уникальный идентификатор счетчика.
        update(): Обновляет состояние счетчика и возвращает True, если тик завершен.
    """
    def __init__(self, tick_count: float, id: str | None = None):
        """
        Инициализация нового экземпляра TickCounter.

        Аргументы:
            tick_count (float): Продолжительность каждого тика в секундах.
            id (str | None, optional): Уникальный идентификатор счетчика. По умолчанию None.
        """
        self.__before_time = 0
        self.__tick_count = tick_count
        self.__id = id if id is not None else str(uuid4())
        self.__start_count = False

    def get_tick_count(self) -> float:
        """
        Получить продолжительность каждого тика.

        Возвращает:
            float: Продолжительность тика в секундах.
        """
        return self.__tick_count

    def get_id(self) -> str:
        """
        Получить уникальный идентификатор счетчика.

        Возвращает:
            str: Уникальный идентификатор.
        """
        return self.__id

    def update(self):
        """
        Обновить состояние счетчика и проверить, завершен ли тик.

        Возвращает:
            bool: True, если тик завершен, False в противном случае.
        """
        if not self.__start_count:
            self.__before_time = time()
            self.__start_count = True
        
        if self.__start_count:
            if time() - self.__before_time > self.__tick_count:
                self.__before_time =  time()
                self.__start_count = False
                return True
        return False

@final
def wait(tick_count: float, id: str | None = None):
    """
    Реализует неблокирующий таймер с уникальными идентификаторами.

    Arguments:
        tick_count (float): Продолжительность ожидания в секундах.
        id (str | None, optional): Уникальный идентификатор для таймера. По умолчанию None.

    Returns:
        bool: True, если период ожидания завершен, False в противном случае.
    """
    global TICK_COUNTERS

    if id not in TICK_COUNTERS.keys():
        TICK_COUNTERS[id] = TickCounter(tick_count, id)
    else:
        return TICK_COUNTERS[id].update()

    return False

@final
def get_tick_counter(id: str) -> TickCounter | None:
    """
    Получить экземпляр TickCounter по его идентификатору.
    Arguments:
        id (str): Уникальный идентификатор счетчика.
    Returns:
        TickCounter | None: Экземпляр TickCounter или None, если идентификатор не найден.
    """
    return TICK_COUNTERS.get(id)