"""
Документация модуля GPU
======================

Этот модуль предоставляет упрощенную обертку для PyOpenCL для облегчения быстрых вычислений на GPU
с минимальными накладными расходами и удобными шаблонами использования.

Классы
-------
GPU
    Класс-обертка для PyOpenCL, который упрощает инициализацию устройства, компиляцию ядер
    и операции передачи данных.

Зависимости
-----------
- pyopencl: Для операций OpenCL
- numpy: Для операций с массивами и структур данных

Класс: GPU
----------
Методы:
    __init__(platform_idx=0, device_idx=0, use_async=False)
        Инициализирует контекст OpenCL, очередь команд и выбирает устройство.
        
        Аргументы:
            platform_idx (int): Индекс платформы OpenCL для использования
            device_idx (int): Индекс устройства на платформе для использования
            use_async (bool): Использовать ли асинхронную передачу данных для лучшей производительности
        
    compile(kernel_source, program_name)
        Компилирует программу OpenCL из исходного кода.
        
        Аргументы:
            kernel_source (str): Исходный код ядра OpenCL
            program_name (str): Имя для ассоциации с программой
        
        Исключения:
            cl.RuntimeError: Если компиляция ядра не удалась
            RuntimeError: Если контекст OpenCL не инициализирован
    
    buffer(data, flags=cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR)
        Создает буфер OpenCL из массива NumPy.
        
        Аргументы:
            data (numpy.ndarray): Массив NumPy для создания буфера
            flags (int): Флаги памяти OpenCL (например, READ_ONLY, COPY_HOST_PTR)
        
        Возвращает:
            pyopencl.Buffer: Созданный буфер OpenCL
        
        Исключения:
            RuntimeError: Если контекст OpenCL не инициализирован
    
    run(program_name, kernel_name, global_size, *args)
        Выполняет ядро OpenCL. Автоматически ждет завершения, если не в асинхронном режиме.
        
        Аргументы:
            program_name (str): Имя загруженной программы, содержащей ядро
            kernel_name (str): Имя функции ядра для выполнения
            global_size (tuple): Размер глобального рабочего пространства (количество рабочих элементов)
            *args: Аргументы для передачи функции ядра (буферы OpenCL, скаляры)
        
        Возвращает:
            None: Если self.use_async == True
            numpy.ndarray: Результат после копирования из буфера если self.use_async == False
        
        Исключения:
            RuntimeError: Если контекст OpenCL не инициализирован
            ValueError: Если program_name не загружена
    
    result(buffer)
        Быстро копирует данные из буфера OpenCL в массив NumPy.
        Ждет завершения всех операций в очереди перед копированием.
        
        Аргументы:
            buffer (pyopencl.Buffer): Буфер OpenCL для получения данных
        
        Возвращает:
            numpy.ndarray: Копия данных из буфера OpenCL в массиве NumPy
    
    finish()
        Ожидает завершения всех поставленных в очередь команд OpenCL.

Пример использования
------------

# Инициализация помощника GPU с асинхронной передачей данных
>>> gpu = GPU(use_async=True)

# Компиляция ядра
>>> kernel_source = '''
__kernel void square(__global float *in, __global float *out) {
    int gid = get_global_id(0);
    out[gid] = in[gid] * in[gid];
}
'''
>>> gpu.compile(kernel_source, "square_program")

# Подготовка данных
>>> data = np.array([1, 2, 3, 4], dtype=np.float32)
>>> input_buf = gpu.buffer(data)
>>> output_buf = gpu.buffer(np.zeros_like(data))

# Запуск ядра
>>> gpu.run("square_program", "square", (len(data),), input_buf, output_buf)

# Получение результатов
>>> result = gpu.result(output_buf)


Примечания
-----
- Класс разработан для простоты и удобства использования, а не для максимальной гибкости
- Асинхронный режим может обеспечить лучшую производительность, но требует ручной синхронизации
- Реализована обработка ошибок для большинства распространенных операций OpenCL
- Класс автоматически управляет жизненным циклом контекста OpenCL и очереди команд
"""

import pyopencl as cl
import numpy as np

class GPU:
    """
    Упрощенная обертка PyOpenCL для быстрой работы и быстрого получения результатов.
    Фокусируется на минимальном оверхеде и удобстве использования.
    """

    def __init__(self, platform_idx=0, device_idx=0, use_async=False):
        """
        Инициализирует контекст OpenCL, очередь команд и выбирает устройство.

        Args:
            platform_idx (int): Индекс OpenCL платформы для использования.
            device_idx (int): Индекс устройства на платформе для использования.
            use_async (bool): Использовать асинхронную передачу данных для повышения производительности.
        """
        try:
            platforms = cl.get_platforms()
            self.platform = platforms[platform_idx]
            devices = self.platform.get_devices()
            self.device = devices[device_idx]
            self.ctx = cl.Context([self.device])
            # Асинхронная очередь или синхронная
            properties = cl.command_queue_properties.OUT_OF_ORDER_EXEC_MODE_ENABLE if use_async else 0
            self.queue = cl.CommandQueue(self.ctx, properties=properties)
            self.programs = {}
            self.use_async = use_async  # Флаг для управления асинхронностью

            print(f"OpenCL инициализирован на {self.device.name}")

        except Exception as e:
            print(f"Ошибка инициализации OpenCL: {e}")
            self.ctx = None  # Индикатор ошибки инициализации
            self.queue = None
            self.platform = None
            self.device = None

    def compile(self, kernel_source, program_name):
        """
        Компилирует программу OpenCL из исходного кода.

        Args:
            kernel_source (str): Исходный код OpenCL ядра.
            program_name (str): Имя для ассоциации с программой.

        Raises:
            cl.RuntimeError: Если компиляция ядра не удалась.
        """
        if not self.ctx:
            raise RuntimeError("Контекст OpenCL не инициализирован.")

        try:
            self.programs[program_name] = cl.Program(self.ctx, kernel_source).build()
        except cl.RuntimeError as e:
            print(f"Ошибка компиляции OpenCL программы '{program_name}': {e}")
            raise

    def buffer(self, data, flags=cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR):
        """
        Создает буфер OpenCL из массива NumPy.

        Args:
            data (numpy.ndarray): Массив NumPy для создания буфера.
            flags (int): Флаги памяти OpenCL (например, READ_ONLY, COPY_HOST_PTR).

        Returns:
            pyopencl.Buffer: Созданный буфер OpenCL.
        """
        if not self.ctx:
            raise RuntimeError("Контекст OpenCL не инициализирован.")

        return cl.Buffer(self.ctx, flags, hostbuf=data)

    def run(self, program_name, kernel_name, global_size, *args):
        """
        Запускает ядро OpenCL.  Автоматически ожидает завершения, если не в async режиме.

        Args:
            program_name (str): Имя загруженной программы, содержащей ядро.
            kernel_name (str): Имя функции ядра для запуска.
            global_size (tuple): Размер глобального рабочего пространства (количество work items).
            *args: Аргументы для передачи в функцию ядра (буферы OpenCL, скаляры).

        Returns:
            None: Если self.use_async == True
            numpy.ndarray: Результат после копирования из буфера если self.use_async == False
        """
        if not self.ctx:
            raise RuntimeError("Контекст OpenCL не инициализирован.")

        if program_name not in self.programs:
            raise ValueError(f"Программа '{program_name}' не загружена.")

        kernel = getattr(self.programs[program_name], kernel_name)
        kernel(self.queue, global_size, None, *args) # Запускаем ядро

        if not self.use_async:
            # Если не асинхронный режим, дожидаемся завершения и сразу копируем результат.
            self.queue.finish()  # Дожидаемся завершения всех операций в очереди

    def result(self, buffer):
        """
        Быстро копирует данные из буфера OpenCL в массив NumPy и возвращает его.
        Ожидает завершения всех операций в очереди перед копированием.

        Args:
            buffer (pyopencl.Buffer): Буфер OpenCL, из которого нужно получить данные.

        Returns:
            numpy.ndarray: Копия данных из буфера OpenCL в массиве NumPy.
        """

        dest = np.empty(buffer.size // np.dtype(np.float32).itemsize, dtype=np.float32) #Создаем подходящий по размеру массив

        if self.use_async: #Если нужно, дожидаемся всех операций
            self.queue.finish() #Если не закончили еще, то ждем

        cl.enqueue_copy(self.queue, dest, buffer).wait() #Копируем данные. await() важно чтобы дождаться

        return dest #Возвращаем

    def finish(self):
        """
        Ожидает завершения всех поставленных в очередь команд OpenCL.
        """
        if self.queue:
            self.queue.finish()
        else:
            print("Очередь не инициализирована")

# Пример использования:
if __name__ == '__main__':
    try:
        # 1. Инициализация с асинхронной передачей данных
        cl_helper = GPU(use_async=False) #True лучше для производительности, но нужно вручную дожидаться finish

        # 2. Исходный код ядра (теперь пишем прямо здесь)
        kernel_source = """
        __kernel void square(__global float *in, __global float *out) {
            int gid = get_global_id(0);
            out[gid] = in[gid] * in[gid];
        }
        """

        # 3. Компиляция ядра
        cl_helper.compile(kernel_source, "my_program")

        # 4. Создание входных данных
        n = 10
        input_data = np.arange(n, dtype=np.float32)

        # 5. Создание буферов OpenCL
        input_buffer = cl_helper.buffer(input_data, flags=cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR)

        output_data = np.zeros_like(input_data)  # Allocate memory for the output
        output_buffer = cl_helper.buffer(output_data) #Let opencl allocate memory itself

        # 6. Запуск ядра OpenCL
        cl_helper.run("my_program", "square", (n,), input_buffer, output_buffer) #Асинхронный запуск

        # 7. Получение результата.
        result = cl_helper.result(output_buffer)

        # 8. Вывод
        print("Вход:", input_data)
        print("Выход:", result)
        print(f"Устройство: {cl_helper.device.name}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")