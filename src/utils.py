import json
import os
from typing import Any, Optional

from src.logger import get_logger

logger = get_logger(__name__)


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
        logger.error("Файл не найден: %s", file_path)
        return []
    except json.JSONDecodeError:
        logger.error("Не удалось декодировать JSON из файла: %s", file_path)
        return []

    if not isinstance(data, list):
        logger.error("JSON-файл не содержит список: %s", file_path)
        return []

    logger.info("Успешно загружено %d транзакций из файла: %s", len(data), file_path)

    return data


def log_message(message: str, filename: Optional[str] = None) -> None:
    """
    Функция для вывода лога.

    :param message: Сообщение для логирования.
    :param filename: Имя файла или None для вывода в консоль.
    """
    if filename is None:
        print(message)
    else:
        write_to_file(message, filename)


def write_to_file(message: str, filename: str) -> None:
    """
    Функция для записи сообщения в лог-файл.

    :param message: Сообщение для записи.
    :param filename: Имя файла.
    """
    src_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(src_path)
    log_dir = os.path.join(project_root, "logs")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, filename)

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")
