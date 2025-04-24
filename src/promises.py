from threading import Thread, Event
from typing import Callable, Any, Optional
from time import time, sleep
from uuid import uuid4
import math


PROMISE_INDEX: int = 0

class CancelledError(Exception):
    """Исключение при отмене выполнения промиса."""

class BasePromise:
    def __init__(self, callable: Callable, timeout: Optional[float] = None, id: Optional[str | int] = None):
        global PROMISE_INDEX
        self.__callable = callable
        self.__result = None
        self.__error = None
        self.__waited_time = 0
        self.__id = uuid4() if id is None else id
        self.__index = PROMISE_INDEX
        self.__timeout = timeout
        self.__completed = Event()
        self.__cancelled = Event()
        self.__started = False
        PROMISE_INDEX += 1

    def get_index(self) -> int:
        return self.__index

    def get_id(self) -> str | int:
        return self.__id

    def get_result(self) -> Any:
        return self.__result
    
    def get_waited_time(self) -> float:
        return self.__waited_time
    
    def get_error(self) -> Optional[Exception]:
        return self.__error
    
    def is_ready(self) -> bool:
        return self.__completed.is_set()
    
    def is_cancelled(self) -> bool:
        return self.__cancelled.is_set()

    def cancel(self) -> None:
        """Устанавливает флаг отмены выполнения задачи."""
        self.__cancelled.set()

    def __thread_target(self, *args, **kwargs):
        try:
            if self.is_cancelled():
                raise CancelledError("Promise was cancelled")
            result = self.__callable(self, *args, **kwargs)
            if self.is_cancelled():
                raise CancelledError("Promise was cancelled during execution")
            self.__result = result
        except Exception as e:
            self.__error = e
        finally:
            self.__completed.set()
        
    def __call__(self, daemon: bool = False, *args, **kwargs):
        if self.__started:
            return self
        self.__started = True
        Thread(
            target=self.__thread_target,
            args=args,
            kwargs=kwargs,
            daemon=daemon
        ).start()
        return self    

    def await_result(self, timeout: Optional[float] = None) -> Any:
        start_time = time()
        used_timeout = timeout or self.__timeout
        
        if not self.__completed.wait(used_timeout):
            self.cancel()
            raise TimeoutError("Promise execution timed out")
            
        self.__waited_time = time() - start_time
        
        if self.__error:
            raise self.__error
        return self.__result


class PromisePool:
    """Пул для управления несколькими промисами.

    Позволяет создавать и управлять группой промисов с ограничением их максимального количества
    и общим таймаутом выполнения.
    """

    def __init__(self, max_promises: int = 10, timeout: Optional[float] = None):
        """Инициализация пула промисов.

        Args:
            max_promises: Максимальное количество промисов в пуле
            timeout: Таймаут выполнения промисов в секундах
        """
        self.__promises: list[BasePromise] = []
        self.__promises_args: list[list[Any]] = []
        self.__max_promises = max_promises
        self.__timeout = timeout

    def add_promise(self, callable: Callable, id: Optional[int | str], *args, **kvargs) -> BasePromise:
        """Добавляет новый промис в пул.

        Args:
            callable: Функция для выполнения
            id: Идентификатор промиса
            *args: Позиционные аргументы для функции
            **kvargs: Именованные аргументы для функции

        Returns:
            BasePromise: Созданный промис
        """
        if len(self.__promises) >= self.__max_promises:
            print("Promise pool is full. Waiting for a free slot...")
        promise = BasePromise(callable, self.__timeout, id)
        self.__promises.append(promise)
        self.__promises_args.append(args)
        return promise
    
    def add_promises(self, calable: Callable, data_array: list[Any]) -> list[BasePromise]:
        """Добавляет несколько промисов в пул. Для разбиения вычисления на несколько потоков можно использовать этот метод.
        Args:
            calable: Функция для выполнения
            data_array: Массив данных для выполнения
        returns:
            list[BasePromise]: Созданные промисы
        """

        data_batchs = math.ceil(len(data_array) / self.__max_promises)

        for i in range(0, len(data_array), data_batchs):
            batch = data_array[i:i+data_batchs]
            self.__promises.append(BasePromise(calable, self.__timeout, calable.__name__ + "_" + str(i)))
            self.__promises_args.append([batch])
        

    def get_promise(self, promise_id: str) -> Optional[BasePromise]:
        """Получает промис по его идентификатору.

        Args:
            promise_id: Идентификатор промиса

        Returns:
            Optional[BasePromise]: Найденный промис или None
        """
        for promise in self.__promises:
            if promise.get_id() == promise_id:
                return promise
        return None
    
    def start_all(self, daemon: bool = False) -> None:
        """Запускает все промисы в пуле.

        Args:
            daemon: Флаг, указывающий запускать ли промисы как демоны
        """
        for promise in self.__promises:
            
            promise(True, *self.__promises_args.pop(0))

    def await_all(self, timeout: Optional[float] = None) -> list[Any]:
        """Ожидает завершения всех промисов.

        Args:
            timeout: Таймаут ожидания в секундах

        Returns:
            list[Any]: Список результатов всех промисов
        """
        results = []
        for promise in self.__promises:
            results.append(promise.await_result(timeout))
        return results

test_type = 1

if __name__ == "__main__":
    if test_type == 0:
        def calculate_factorial(promise: BasePromise, n: int) -> int:
            """Вычисляет факториал числа."""
            result = 1
            for i in range(1, n + 1):
                result *= i
                sleep(0.1)  # Имитация сложных вычислений
            print('factorial:', result)
            return result

        def calculate_fibonacci(promise: BasePromise, n: int) -> int:
            """Вычисляет n-ное число Фибоначчи."""
            if n <= 0:
                return 0
            elif n == 1:
                return 1
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
                sleep(0.1)  # Имитация сложных вычислений
            print('fibonacci:', b)
            return b

        def calculate_prime_count(promise: BasePromise, n: int) -> int:
            """Вычисляет количество простых чисел до n."""
            def is_prime(num):
                if num < 2:
                    return False
                for i in range(2, int(math.sqrt(num)) + 1):
                    if num % i == 0:
                        return False
                return True
            
            count = 0
            for i in range(2, n + 1):
                if is_prime(i):
                    count += 1
                    print('prime:', i)
                sleep(0.01)  # Имитация сложных вычислений
            return count



        # Создаем пул с максимум 3 промисами и таймаутом 10 секунд
        pool = PromisePool(max_promises=3, timeout=10.0)
        
        # Добавляем задачи в пул
        factorial_promise = pool.add_promise(calculate_factorial, "factorial", 10)
        fibonacci_promise = pool.add_promise(calculate_fibonacci, "fibonacci", 20)
        prime_promise = pool.add_promise(calculate_prime_count, "primes", 1000)
        
        # Запускаем все промисы
        pool.start_all()
        
        try:
            # Ждем результаты
            results = pool.await_all()
            
            print(f"Факториал 10: {results[0]}")
            print(f"20-е число Фибоначчи: {results[1]}")
            print(f"Количество простых чисел до 1000: {results[2]}")
            
            # Получаем время ожидания для каждого промиса
            print(f"\nВремя выполнения:")
            print(f"Факториал: {factorial_promise.get_waited_time():.2f} сек")
            print(f"Фибоначчи: {fibonacci_promise.get_waited_time():.2f} сек")
            print(f"Простые числа: {prime_promise.get_waited_time():.2f} сек")
            
        except TimeoutError:
            print("Превышено время ожидания!")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    elif test_type == 1:
            # Создаем большой массив данных для обработки
            data = [i for i in range(1, 10000001)]

            def complex_calculation(promise: BasePromise, numbers: list[int]) -> dict:
                print(f"Запущен промис: {promise.get_id()} {promise.get_index()}")
                """Выполняет сложные вычисления над массивом чисел."""
                results = {
                    'sum_squares': 0,
                    'sum_cubes': 0,
                    'prime_count': 0,
                    'factorial_sum': 0
                }
            
                def is_prime(n):
                    if n < 2:
                        return False
                    for i in range(2, int(math.sqrt(n)) + 1):
                        if n % i == 0:
                            return False
                    return True
            
                def factorial(n):
                    if n <= 1:
                        return 1
                    return n * factorial(n - 1)
            
                for num in numbers:
                    # Вычисляем квадраты
                    results['sum_squares'] += num * num
                
                    # Вычисляем кубы
                    results['sum_cubes'] += num * num * num
                
                    # Считаем простые числа
                    if is_prime(num):
                        results['prime_count'] += 1
                
                    # Считаем сумму факториалов для небольших чисел
                    if num <= 10:
                        results['factorial_sum'] += factorial(num)
                    
                    
                
                    # Проверка на отмену
                    if promise.is_cancelled():
                        raise CancelledError("Calculation was cancelled")
                print(f"[ + ] Завершен промис: {promise.get_id()} {promise.get_index()}")
                return results

            # Создаем пул с 4 промисами и таймаутом 200 секунд
            pool = PromisePool(max_promises=20, timeout=200.0)
        
            # Разбиваем данные на части и добавляем в пул
            pool.add_promises(complex_calculation, data)
        
            print("Starting calculations...")
            start_time = time()
        
            # Запускаем все промисы
            pool.start_all()
        
            try:
                # Получаем результаты
                results = pool.await_all()
                print(results)
            
                # Суммируем результаты всех частей
                total_results = {
                    'sum_squares': 0,
                    'sum_cubes': 0,
                    'prime_count': 0,
                    'factorial_sum': 0
                }
            
                for result in results:
                    for key in total_results:
                        total_results[key] += result[key]
            
                end_time = time()
            
                print("\nResults:")
                print(f"Sum of squares: {total_results['sum_squares']}")
                print(f"Sum of cubes: {total_results['sum_cubes']}")
                print(f"Number of primes: {total_results['prime_count']}")
                print(f"Sum of factorials (1-10): {total_results['factorial_sum']}")
                print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")
            except TimeoutError:
                print("Timeout exceeded!")
            except Exception as e:
                print(f"An error occurred: {e}")