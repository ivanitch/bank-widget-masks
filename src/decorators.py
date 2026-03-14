"""
Модуль decorators - декораторы для логирования выполнения функций.
"""

import os
from typing import Any, Callable, Optional
from functools import wraps


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
        - Если filename задан, создаётся /log директория (если нет)
        - Логирует: начало (start), окончание (stop) или ошибку (error)
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Логируем начало выполнения
            start_message = f"{func.__name__} start"
            _log_message(start_message, filename)

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Логируем окончание выполнения
                stop_message = f"{func.__name__} stop"
                _log_message(stop_message, filename)

                return result

            except Exception as e:
                # Логируем ошибку
                error_type = type(e).__name__
                error_message = (
                    f"{func.__name__} error: {error_type}. "
                    f"Inputs: {args}, {kwargs}"
                )
                _log_message(error_message, filename)

                # Пробрасываем исключение дальше
                raise

        return wrapper

    return decorator


def _log_message(message: str, filename: Optional[str]) -> None:
    """
    Вспомогательная функция для вывода лога.

    Аргументы:
        message (str): Сообщение для логирования.
        filename (Optional[str]): Имя файла или None для консоли.
    """
    if filename is None:
        # Вывод в консоль
        print(message)
    else:
        # Запись в файл
        _write_to_file(message, filename)


def _write_to_file(message: str, filename: str) -> None:
    """
    Вспомогательная функция для записи в лог-файл.

    Аргументы:
        message (str): Сообщение для записи.
        filename (str): Имя файла.
    """
    # Определяем пути
    src_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(src_path)
    log_dir = os.path.join(project_root, "log")

    # Создаём директорию для логов, если её нет
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Полный путь к лог-файлу
    log_file = os.path.join(log_dir, filename)

    # Записываем в файл
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")
