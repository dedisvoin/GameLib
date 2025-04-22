from threading import Thread, Event
from typing import Callable, Any, Optional
from time import time, sleep
from uuid import uuid4


PROMISE_INDEX: int = 0

class CancelledError(Exception):
    """Исключение при отмене выполнения промиса."""

class BasePromise:
    def __init__(self, callable: Callable, timeout: Optional[float] = None):
        global PROMISE_INDEX
        self.__callable = callable
        self.__result = None
        self.__error = None
        self.__waited_time = 0
        self.__id = uuid4()
        self.__index = PROMISE_INDEX
        self.__timeout = timeout
        self.__completed = Event()
        self.__cancelled = Event()
        self.__started = False
        PROMISE_INDEX += 1

    def get_index(self) -> int:
        return self.__index

    def get_id(self) -> str:
        return self.__id.hex

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


