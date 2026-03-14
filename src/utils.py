import os
import json
from typing import Any, Optional


def get_transactions_from_json(file_path: str) -> list[dict[str, Any]]:
    """
    Читает JSON-файл с финансовыми транзакциями и возвращает список словарей.

    :param file_path: Путь до JSON-файла.
    :return: Список словарей с транзакциями. Если файл пустой, содержит
             не список или не найден — возвращает пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        log_message(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError:
        log_message(f"Не удалось декодировать JSON из файла: {file_path}")
        return []

    if not isinstance(data, list):
        log_message(f"JSON-файл не содержит список: {file_path}")
        return []

    return data


def log_message(message: str, filename: Optional[str]) -> None:
    """
    функция для вывода лога

    Аргументы:
        message (str): Сообщение для логирования.
        filename (Optional[str]): Имя файла или None для консоли.
    """
    if filename is None:
        # Вывод в консоль
        print(message)
    else:
        # Запись в файл
        write_to_file(message, filename)


def write_to_file(message: str, filename: str) -> None:
    """
    функция для записи в лог-файл

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
