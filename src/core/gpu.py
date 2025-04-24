"""
GPU модуль для выполнения вычислений на графическом процессоре с использованием OpenCL.

Этот модуль предоставляет класс GPUKernel для удобной работы с OpenCL.
Он позволяет компилировать и выполнять OpenCL ядра на GPU или других OpenCL-совместимых устройствах.

Примеры использования:
    # Простое сложение массивов
    gpu = GPUKernel()
    
    kernel_code = '''
    __kernel void add_arrays(
        __global const float* a,
        __global const float* b,
        __global float* result
    ) {
        int idx = get_global_id(0);
        result[idx] = a[idx] + b[idx];
    }
    '''
    
    gpu.compile_kernel(kernel_code, "add_arrays")
    a = np.array([1, 2, 3], dtype=np.float32)
    b = np.array([4, 5, 6], dtype=np.float32)
    result = np.empty_like(a)
    result = gpu.run_kernel("add_arrays", (3,), None, a, b, result=result)
    
    # Матричное умножение
    kernel_code = '''
    __kernel void matrix_multiply(
        __global const float* A,
        __global const float* B,
        __global float* C,
        const int N
    ) {
        int row = get_global_id(0);
        int col = get_global_id(1);
        
        float sum = 0.0f;
        for (int k = 0; k < N; k++) {
            sum += A[row * N + k] * B[k * N + col];
        }
        C[row * N + col] = sum;
    }
    '''
    
    gpu.compile_kernel(kernel_code, "matrix_multiply")
    N = 3
    A = np.random.rand(N, N).astype(np.float32)
    B = np.random.rand(N, N).astype(np.float32)
    C = np.empty((N, N), dtype=np.float32)
    result = gpu.run_kernel("matrix_multiply", (N, N), None, A, B, C=C, N=np.int32(N))
"""

import pyopencl as cl
import numpy as np
from typing import Optional, Union, List

class GPUKernel:
    """
    Класс для работы с OpenCL ядрами на GPU.
    
    Этот класс предоставляет удобный интерфейс для:
    - Инициализации OpenCL контекста
    - Компиляции OpenCL программ
    - Выполнения ядер на GPU
    - Управления памятью и буферами
    
    Аргументы:
        platform_idx (int): Индекс OpenCL платформы (по умолчанию 0)
        device_idx (int): Индекс устройства на выбранной платформе (по умолчанию 0)
    
    Примеры:
        >>> # Создание экземпляра для работы с первым доступным GPU
        gpu = GPUKernel()
        
        >>> # Использование конкретной платформы и устройства
        gpu = GPUKernel(platform_idx=1, device_idx=2)
    """

    def __init__(self, platform_idx: int = 0, device_idx: int = 0):
        """
        Инициализация контекста и очереди команд для выбранного устройства.
        
        Аргументы:
            platform_idx (int): Индекс OpenCL платформы
            device_idx (int): Индекс устройства
        
        Исключения:
            RuntimeError: Если не найдены OpenCL платформы или устройства
        """
        platforms = cl.get_platforms()
        if not platforms:
            raise RuntimeError("Не найдены OpenCL-платформы!")
        
        self.platform = platforms[platform_idx]
        devices = self.platform.get_devices()
        if not devices:
            raise RuntimeError("Не найдены устройства!")
        
        self.device = devices[device_idx]
        self.ctx = cl.Context([self.device])
        self.queue = cl.CommandQueue(self.ctx)
        self.programs = {}  # Кэш скомпилированных программ

    def compile_kernel(self, kernel_code: str, kernel_name: str) -> None:
        """
        Компилирует и кэширует OpenCL-ядро.
        
        Эта функция компилирует OpenCL код и сохраняет скомпилированную программу
        в кэше для последующего использования.
        
        Аргументы:
            kernel_code (str): Исходный код OpenCL ядра
            kernel_name (str): Имя функции ядра
        
        Исключения:
            RuntimeError: При ошибке компиляции ядра
        
        Примеры:
            >>> # Компиляция простого ядра
            kernel_code = '''
            __kernel void square(
                __global const float* input,
                __global float* output
            ) {
                int idx = get_global_id(0);
                output[idx] = input[idx] * input[idx];
            }
            '''
            gpu.compile_kernel(kernel_code, "square")
        """
        if kernel_name in self.programs:
            return
        
        try:
            program = cl.Program(self.ctx, kernel_code).build()
            self.programs[kernel_name] = program
        except cl.RuntimeError as e:
            raise RuntimeError(f"Ошибка компиляции ядра {kernel_name}:\n{e}")

    def run_kernel(
        self,
        kernel_name: str,
        global_size: tuple,
        local_size: Optional[tuple],
        *args,
        **kwargs
    ) -> Union[np.ndarray, List[np.ndarray]]:
        """
        Запускает ядро и возвращает результат.
        
        Эта функция выполняет скомпилированное ядро на GPU, передавая ему
        указанные аргументы и возвращая результаты вычислений.
        
        Аргументы:
            kernel_name (str): Имя ядра для выполнения
            global_size (tuple): Глобальный размер работы (количество потоков)
            local_size (Optional[tuple]): Локальный размер работы (размер рабочей группы)
            *args: Позиционные аргументы для ядра (входные массивы или скаляры)
            **kwargs: Именованные аргументы для ядра (выходные массивы)
        
        Возвращает:
            Union[np.ndarray, List[np.ndarray]]: Результат выполнения ядра
        
        Исключения:
            ValueError: Если ядро не было скомпилировано
        
        Примеры:
            >>> # Возведение в квадрат элементов массива
            input_data = np.array([1, 2, 3, 4], dtype=np.float32)
            output_data = np.empty_like(input_data)
            result = gpu.run_kernel(
                "square",
                global_size=(4,),
                local_size=None,
                input_data,
                output=output_data
            )
            
            >>> # Матричное умножение
            A = np.random.rand(100, 100).astype(np.float32)
            B = np.random.rand(100, 100).astype(np.float32)
            C = np.empty((100, 100), dtype=np.float32)
            result = gpu.run_kernel(
                "matrix_multiply",
                global_size=(100, 100),
                local_size=(10, 10),
                A, B,
                C=C,
                N=np.int32(100)
            )
        """
        if kernel_name not in self.programs:
            raise ValueError(f"Ядро '{kernel_name}' не скомпилировано!")
        
        kernel = getattr(self.programs[kernel_name], kernel_name)
        
        # Преобразуем аргументы в буферы, если это необходимо
        cl_args = []
        output_buffers = []
        output_arrays = []
        
        for arg in args:
            if isinstance(arg, np.ndarray):
                # Входные данные (READ_ONLY)
                buf = cl.Buffer(
                    self.ctx,
                    cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
                    hostbuf=arg
                )
                cl_args.append(buf)
            else:
                cl_args.append(arg)
        
        # Выходные буферы (WRITE_ONLY)
        for name, value in kwargs.items():
            if isinstance(value, np.ndarray):
                buf = cl.Buffer(
                    self.ctx,
                    cl.mem_flags.WRITE_ONLY,
                    value.nbytes
                )
                cl_args.append(buf)
                output_buffers.append(buf)
                output_arrays.append(value)
        
        # Запуск ядра
        kernel.set_args(*cl_args)
        cl.enqueue_nd_range_kernel(
            self.queue,
            kernel,
            global_size,
            local_size
        )
        
        # Копирование результатов
        for i, buf in enumerate(output_buffers):
            cl.enqueue_copy(self.queue, output_arrays[i], buf)
        
        self.queue.finish()  # Ожидаем завершения
        
        return output_arrays[0] if len(output_arrays) == 1 else output_arrays

    def __del__(self):
        """
        Очистка ресурсов.
        
        Этот метод вызывается при удалении объекта и обеспечивает корректное
        освобождение ресурсов OpenCL.
        """
        if hasattr(self, 'queue'):
            self.queue.finish()

if __name__ == "__main__":
    # Пример использования класса GPUKernel

    # Инициализация
    gpu = GPUKernel()

    # Код ядра для сложения массивов
    add_kernel = """
    __kernel void add_arrays(
        __global const int* a,
        __global const int* b,
        __global int* result
    ) {
        int idx = get_global_id(0);
        result[idx] = a[idx] + b[idx];
    }
    """

    # Компиляция ядра
    gpu.compile_kernel(add_kernel, "add_arrays")

    # Подготовка входных данных
    a = np.array([1, 2, 3], dtype=np.int16)
    b = np.array([4, 5, 6], dtype=np.int16)
    result = np.empty_like(a)

    # Запуск ядра и получение результата
    result = gpu.run_kernel(
        "add_arrays",
        (3,), 
        None,
        a, b, 
        result=result,
    )

    print(result)  # [5, 7, 9]