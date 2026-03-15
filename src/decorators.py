"""
Модуль decorators - декораторы для логирования выполнения функций.
"""

from functools import wraps
from typing import Any, Callable, Optional

from src.utils import log_message


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.

    Автоматически записывает в файл или консоль:
    - Начало выполнения функции
    - Окончание выполнения функции
    - Информацию об ошибке при её возникновении

    Аргументы:
        filename (Optional[str]): Имя файла для логирования.
                                  Если None - логи выводятся в консоль.
                                  Если задан - файл создаётся в директории /log.

    Возвращает:
        Callable: Декоратор функции.

    Примеры:
        >>> @log(filename="mylog.txt")
        ... def add(x, y):
        ...     return x + y
        >>> add(1, 2)
        # В mylog.txt:
        # add start
        # add stop

        >>> @log()
        ... def divide(x, y):
        ...     return x / y
        >>> divide(1, 0)
        # В консоль:
        # divide start
        # divide error: ZeroDivisionError. Inputs: (1, 0), {}

    Примечания:
        - Если filename=None, логи выводятся в консоль
        - Если filename задан, создаётся /logs директория (если нет)
        - Логирует: начало (start), окончание (stop) или ошибку (error)
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Логируем начало выполнения
            start_message = f"{func.__name__} start"
            log_message(start_message, filename)

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Логируем окончание выполнения
                stop_message = f"{func.__name__} stop"
                log_message(stop_message, filename)

                return result

            except Exception as e:
                # Логируем ошибку
                error_type = type(e).__name__
                error_message = f"{func.__name__} error: {error_type}. " f"Inputs: {args}, {kwargs}"
                log_message(error_message, filename)

                # Пробрасываем исключение дальше
                raise

        return wrapper

    return decorator
