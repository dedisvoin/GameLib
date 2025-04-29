"""
Модуль приложения, содержащий основной класс для создания и управления окном приложения.

Этот модуль предоставляет класс AppWindow, который наследуется от базового класса _Window
и реализует основные функции для работы с окном приложения, включая управление частотой кадров,
обработку событий и отображение информации.

Classes:
    AppWindow: Основной класс для создания и управления окном приложения
    AppProcess: Класс для управления отдельным процессом приложения
    AppSubProcess: Класс для управления подпроцессом приложения в отдельном потоке
    AppProcessesPool: Класс для управления пулом процессов приложения

Dependencies:
    pygame: Библиотека для создания игр и мультимедийных приложений
    src.core.settings: Модуль с настройками окна
    src.core.window: Базовый модуль для работы с окном
"""

from src.core.settings import WINDOW_FPS_CHECK_TIMEOUT, WINDOW_SIZE, WINDOW_TITLE, WINDOW_VSYNC, WINDOW_WAITED_FPS, WINDOW_BG_COLOR, WINDOW_DELTA_MATCH_FPS
from src.core import window

from src.render.text import TextField

from typing import Tuple, Callable, Any
import pygame

pygame.init()


class AppWindow(window._Window):
    """Класс приложения для создания и управления окном.
    
    Этот класс предоставляет функционал для:
    - Создания окна приложения с заданными параметрами
    - Управления частотой кадров
    - Отображения информации в заголовке окна
    - Управления фоном окна
    - Обработки базовых событий
    
    Attributes:
        __clock: Объект для управления временем и FPS
        __waited_fps: Желаемая частота кадров
        __bg_color: Цвет фона окна
        __view_information_in_title: Флаг отображения информации в заголовке
    """
    def __init__(self, size: Tuple[int, int] = WINDOW_SIZE, title: str = WINDOW_TITLE, flags: int | None = None, 
                 vsync: bool = WINDOW_VSYNC) -> "AppWindow":
        """Инициализация приложения.
        
        Args:
            size: Размер окна в пикселях (ширина, высота)
            title: Заголовок окна
            flags: Флаги pygame для создания окна
            vsync: Включение/выключение вертикальной синхронизации
        """
        super().__init__(size, title, flags, vsync)
        self.__clock = pygame.time.Clock()
        self.__waited_fps = WINDOW_WAITED_FPS

        self.__bg_color = (255, 255, 255)

        self.__view_information_in_title = False
        self.__view_information_in_window = False

        self.__smoth_deltas = []

        self.__text_field_fps = TextField("arial", 20, "black", True)
        self.__text_field_delta = TextField("arial", 16, "black", False)
        self.__text_field_render_timer = TextField("arial", 16, "black", False)
        self.__text_field_vsync = TextField("arial", 16, "black", False)
        self.__text_field_frame_grafic_fps = TextField("arial", 12, "black", True)

        self.__frame_time_array = []

    def get_size(self) -> tuple[int, int]:
        """Получить размер окна в пикселях (ширина, высота).
        Returns:
            tuple[int, int]: Размер окна в пикселях (ширина, высота)
        """
        return self._size
    
    def get_at_size(self) -> tuple[int, int]:
        """Получить размер окна в пикселях (ширина, высота).
        Returns:
            tuple[int, int]: Размер окна в пикселях (ширина, высота)
        """
        return pygame.display.get_window_size()

    def close(self):
        """Закрыть окно приложения."""
        pygame.display.quit()

    def set_view_information_in_title(self, view_information_in_title: bool = True):
        """Установить отображение информации о частоте кадров в заголовке окна.
        
        Args:
            view_information_in_title: Отображение информации о частоте кадров в заголовке окна. По умолчанию True.
        """
        self.__view_information_in_title = view_information_in_title

    def set_view_information_in_window(self, view_information_in_window: bool = True):
        """Установить отображение информации о частоте кадров в окне.

        Args:
            view_information_in_window: Отображение информации о частоте кадров в окне. По умолчанию True.
        """
        self.__view_information_in_window = view_information_in_window

    def set_quit_key(self, quit_key: str = 'esc'):
        """Установить клавишу для выхода из приложения.
        
        Args:
            quit_key: Клавиша для выхода из приложения. По умолчанию 'esc'.
        """
        super()._windows_handler._set_quit_key(quit_key)

    def set_waited_fps(self, waited_fps: int):
        """Установить желаемую частоту кадров.
        
        Args:
            waited_fps: Желаемая частота кадров.
            
        Returns:
            self: Возвращает текущий экземпляр класса для цепочки вызовов.
        """
        self.__waited_fps = waited_fps
        return self

    def get_fps(self) -> float:
        """Получить текущую частоту кадров.
        
        Returns:
            float: Текущая частота кадров.
        """
        return self.__clock.get_fps()

    def get_render_time(self) -> float:
        """Получить время, прошедшее с последнего кадра.
        
        Returns:
            float: Время в миллисекундах между текущим и предыдущим кадром.
        """
        return self.__clock.get_time()

    def get_delta(self, smooth: bool = False) -> float:
        """Получить дельту времени между текущим и предыдущим кадром.

        Args:
            smooth: Использовать сглаженное значение дельты времени.

        Returns:
            float: Дельта времени в секундах.
        """
        if not smooth:
            try:
                return WINDOW_DELTA_MATCH_FPS / self.get_fps()
            except ZeroDivisionError:
                return 1
        else:
            try:
                return sum(self.__smoth_deltas) / len(self.__smoth_deltas)
            except ZeroDivisionError:
                return 1
        
    def fill(self, color: tuple[int, int, int] | None = None) -> None:
        """Заполнить фон окна указанным цветом.
        
        Если цвет не указан, используется текущий цвет фона (__bg_color).
        
        Args:
            color: Цвет фона в формате RGB (красный, зеленый, синий). По умолчанию None.
        """
        
        if color is None:
            color = self.__bg_color
        self._surf.fill(color)

    def render_information_in_window(self) -> None:
        """
        Отображение информации о частоте кадров в окне.
        Обычно включается методом set_view_information_in_window(). Но если вы используете OpenGL, то нужен этот прямой вызов.
        """
        if self.__view_information_in_window:
            
            self.__text_field_fps.set_text(f"FPS: {int(self.get_fps())} / {self.__waited_fps}")
            self.__text_field_fps.render(self.surf, (5, 0))
            self.__text_field_render_timer.set_text(f"render time: {self.get_render_time()} ms")
            self.__text_field_render_timer.render(self.surf, (5, 20))
            self.__text_field_delta.set_text(f"delta: {self.get_delta(smooth=True):.2f}")
            self.__text_field_delta.render(self.surf, (5, 35))
            if self._vsync:
                self.__text_field_vsync.set_color('green')
                self.__text_field_vsync.set_text(f"vsync: on")
            else:
                self.__text_field_vsync.set_color('black')
                self.__text_field_vsync.set_text(f"vsync: off")
            self.__text_field_vsync.render(self.surf, (5, 50))

            # График frametime
            current_time = pygame.time.get_ticks()
            if not hasattr(self, '_last_sample_time'):
                self._last_sample_time = current_time
                
            # Обновляем график каждые 100мс
            if current_time - self._last_sample_time >= WINDOW_FPS_CHECK_TIMEOUT:
                current_fps = self.get_fps()
                self.__frame_time_array.append(current_fps)
                if len(self.__frame_time_array) > 100:
                    self.__frame_time_array.pop(0)
                self._last_sample_time = current_time
            
            # Отрисовка графика
            graph_height = 90
            graph_width = 200
            graph_x = 5
            graph_y = 70
            
            # Фон графика
            pygame.draw.rect(self.surf, (1, 1, 1), (graph_x, graph_y, graph_width, graph_height), 1)
            
            # Отрисовка линий графика
            if len(self.__frame_time_array) > 1:
                max_fps = max(max(self.__frame_time_array), 120)  # Фиксированный максимум для стабильной шкалы
                for i in range(len(self.__frame_time_array)-1):
                    x1 = graph_x + (i * graph_width / 100)
                    x2 = graph_x + ((i+1) * graph_width / 100)
                    try:
                        y1 = graph_y + graph_height - (self.__frame_time_array[i] * graph_height / max_fps)
                        y2 = graph_y + graph_height - (self.__frame_time_array[i+1] * graph_height / max_fps)
                        pygame.draw.line(self.surf, (0,0,0), (x1,y1), (x2,y2), 1)
                    except: ...

                # Отрисовка отметок FPS
                fps_marks = [30, 60, 120]  # Отметки FPS для отображения
                for fps in fps_marks:
                    if fps <= max_fps:
                        y = graph_y + graph_height - (fps * graph_height / max_fps)
                        pygame.draw.line(self.surf, (200,0,0), (graph_x, y-3), (graph_x + graph_width, y - 3), 1)
                        self.__text_field_frame_grafic_fps.set_text(f"FPS: {fps}")
                        self.__text_field_frame_grafic_fps.set_color('red')
                        self.__text_field_frame_grafic_fps.render(self.surf, (graph_x + graph_width + 5, y - 8)) 


    def update(self) -> None:
        """Обновление состояния приложения.
        
        Вызывает внутренние методы для обновления состояния окна и обработки событий.
        Обновляет информацию в заголовке окна, если включено отображение.
        Контролирует частоту кадров.
        """
        
        

        try:
            delta = WINDOW_DELTA_MATCH_FPS / self.get_fps()
        except ZeroDivisionError:
            delta = 1
        self.__smoth_deltas.append(delta)

        if len(self.__smoth_deltas) > 50:
            self.__smoth_deltas.pop(0)
        

        if self.__view_information_in_title:
            pygame.display.set_caption(f"{self._title} | FPS: {int(self.get_fps())}/{self.__waited_fps} | RENDER TIME: {self.get_render_time()}ms | DELTA: {self.get_delta(True):.2f}")
        if self.__view_information_in_window:
            self.render_information_in_window()

        
        self._update()
        
            
        self._update_state()
        
        self.__clock.tick(self.__waited_fps)    

    def flip(self) -> None:
        """Обновление окна.
        Обновляет содержимое окна, отображая изменения.
        """
        pygame.display.flip()
        
    @property
    def surf(self) -> pygame.Surface:
        """Получить поверхность окна.

        Returns:
            pygame.Surface: Поверхность окна.
        """
        return self._surf
        
class AppProcess:
    """Класс для управления отдельным процессом приложения.
    Используется вместе с AppProcessesPool. 
    Необходимо запустить прроцесс с помощью метода start().

    >>> timer = 0
        radius = 0

    >>> def update():
            global timer, radius
            timer += 0.1
            radius = 100 + sin(timer) * 50
            return timer


    >>> pool = AppProcessesPool(window)
    >>> pool.add_process(
            AppProcess(update, True, 1, 'update').start()
        )
    
    >>> while True:
            pool.update() # Обновление процессов AppProcess (AppSubProcess не нужнадются в постоянном обновлении в цикле)
    
    Attributes:
        __identifier: Идентификатор процесса
        __callable: Вызываемая функция процесса
        __cyclic: Флаг циклического выполнения
        __dellay: Задержка между выполнениями для циклических процессов
        __counter: Счетчик для отслеживания времени
        __return_values: Значения, возвращаемые процессом
        __started: Флаг активности процесса
    """
    def __init__(self, callable: Callable | None = None, cyclic: bool = False, dellay: float = 0, identifier: str | int | None = None) -> None:
        """Инициализация процесса.
        
        Args:
            callable: Функция для выполнения
            cyclic: Флаг циклического выполнения
            dellay: Задержка между выполнениями
            identifier: Идентификатор процесса
        """
        self.__identifier = identifier
        self.__callable = callable


        self.__cyclic = cyclic
        self.__dellay = dellay
        self.__counter = 0

        self.__return_values = []

        self.__started = False

    def start(self):
        """Запустить процесс."""
        self.__started = True
        return self

    def stop(self):
        """Остановить процесс."""
        self.__started = False
        return self

    def init(self):
        """Инициализировать счетчик процесса."""
        self.__counter = 0
        return self

    def update(self, delta,  *_args, **_kwargs):
        """Обновить состояние процесса.
        
        Args:
            delta: Время, прошедшее с последнего обновления
            *_args: Позиционные аргументы для вызываемой функции
            **_kwargs: Именованные аргументы для вызываемой функции
        """
        if self.__started:
            if self.__cyclic:
                self.__counter += delta
                if self.__counter >= self.__dellay:
                    self.__counter = 0
                    self.__return_values = self.__callable(*_args, **_kwargs)
            
            else:
                if self.__counter == 0: self.__return_values = self.__callable(*_args, **_kwargs)
                self.__counter = 1

    def get_return_values(self) -> Any:
        """Получить значения, возвращаемые процессом."""
        return self.__return_values
    
    def get_identifier(self) -> str | int:
        """Получить идентификатор процесса."""
        return self.__identifier



from threading import Thread
from time import sleep
class AppSubProcess:
    """Класс для управления подпроцессом приложения.

    
    Attributes:
        __callable: Вызываемая функция подпроцесса
        __identifier: Идентификатор подпроцесса
        __dellay: Задержка между выполнениями
        __started: Флаг активности подпроцесса
        __thread: Поток выполнения подпроцесса
    """
    def __init__(self, callable: Callable | None = None, dellay: float = 0, identifier: str | int | None = None) -> None:
        """Инициализация подпроцесса.
        Если вы хотите чтобы процесс выполнялся с частатой как у приложения используйте формулу 1 / fps
        >>> dellay = 1 / 60 # будет выполняться с частотой 60 раз в секунду.
        
        Args:
            callable: Функция для выполнения
            identifier: Идентификатор подпроцесса
            dellay: Задержка между выполнениями
        """
        self.__callable = callable
        self.__identifier = identifier
        self.__dellay = dellay

        self.__started = False
        self.__thread: Thread | None = None

    def __process(self):
        """Внутренний метод для выполнения подпроцесса в отдельном потоке."""
        while self.__started:
            self.__callable()
            sleep(self.__dellay)
        
    def start(self):
        """Запустить подпроцесс в отдельном потоке."""
        self.__started = True
        self.__thread = Thread(target=self.__process, daemon=True)
        self.__thread.start()
        return self
    
    def stop(self):
        """Остановить выполнение подпроцесса."""
        self.__started = False
        return self
    
    def set_dellay(self, dellay: float):
        """Установить задержку между выполнениями подпроцесса.

        Args:
            dellay: Новая задержка
        """
        self.__dellay = dellay
        return self
    
    def get_dellay(self) -> float:
        """Получить задержку между выполнениями подпроцесса.

        Returns:
            float: Задержка между выполнениями
        """
        return self.__dellay
    
    def get_identifier(self) -> str | int:
        """Получить идентификатор подпроцесса.
        
        Returns:
            str | int: Идентификатор подпроцесса
        """
        return self.__identifier    
    
    def get_thread(self) -> Thread:
        """Получить поток выполнения подпроцесса.

        Returns:
            Thread: Поток выполнения подпроцесса
        """
        return self.__thread

class AppProcessesPool:
    """Класс для управления пулом процессов приложения.
    
    Attributes:
        __subprocesses: Список активных процессов
        __app: Ссылка на основное окно приложения
    """
    def __init__(self, app: AppWindow) -> None:
        """Инициализация пула процессов.
        
        Args:
            app: Экземпляр основного окна приложения
        """
        self.__processes: list[AppProcess] = []
        self.__subprocesses: list[AppSubProcess] = []
        self.__app = app

    def clear(self) -> None:
        """Очистить пул процессов."""
        self.__processes.clear()
        self.__subprocesses.clear()
        return self

    def add_process(self, process: AppProcess | AppSubProcess) -> None:
        """Добавляет процесс в пул.
        AppSubProcess добавляются в отделный список, не требующий обновления.

        Args:
            process: Экземпляр процесса для добавления
        """
        if isinstance(process, AppProcess):
            self.__processes.append(process)
        elif isinstance(process, AppSubProcess):
            self.__subprocesses.append(process)

    def get_process_or_subprocess(self, identifier: str | int) -> AppProcess | AppSubProcess | None:
        """Получить процесс или подпроцесс по идентификатору.

        Args:
            identifier: Идентификатор процесса или подпроцесса
        Returns:
            AppProcess | AppSubProcess | None: Экземпляр процесса или подпроцесса
        """
        for process in self.__processes:
            if process.get_identifier() == identifier:
                return process
        for process in self.__subprocesses:
            if process.get_identifier() == identifier:
                return process
        return None

    def update(self, *_args, **_kwargs):
        """Обновить все процессы в пуле.
        
        Args:
            *_args: Позиционные аргументы для процессов
            **_kwargs: Именованные аргументы для процессов
        """
        for process in self.__processes:
            process.update(self.__app.get_delta(True), *_args, **_kwargs)

    def delete_process(self, identifier: str | int) -> None:
        """Удалить процесс из пула по идентификатору.
        
        Args:
            identifier: Идентификатор процесса для удаления
        """
        for process in self.__processes:
            if process.get_identifier() == identifier:
                process.stop()
                self.__processes.remove(process)
                break

        for process in self.__subprocesses:
            if process.get_identifier() == identifier:
                process.stop()
                self.__subprocesses.remove(process)
                break
    
    def get_all_return_values(self) -> list[Any]:
        """Получить значения, возвращаемые всеми процессами, кроме подпроцессов.
        
        Returns:
            list[Any]: Список значений от всех процессов
        """
        return_values = []
        for process in self.__processes:
            return_values.append(process.get_return_values())
        return return_values
    
    def get_return_value(self, identifier: str | int) -> Any:
        """Получить значение, возвращаемое конкретным процессом, кроме подпроцессов.
        
        Args:
            identifier: Идентификатор процесса
            
        Returns:
            Any: Значение от указанного процесса или None, если процесс не найден
        """
        for process in self.__processes:
            if process.get_identifier() == identifier:
                return process.get_return_values()
        return None