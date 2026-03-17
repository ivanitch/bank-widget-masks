import pandas as pd

from src.logger import get_logger

logger = get_logger(__name__)


def get_transactions_from_csv(file_path: str) -> list[dict]:
    """
    Читает финансовые операции из CSV-файла с разделителем ';'.

    :param file_path: Путь к CSV-файлу.
    :return: Список словарей с транзакциями или пустой список при ошибке.
    """
    try:
        df = pd.read_csv(file_path, sep=";", dtype=str, encoding="utf-8")
    except FileNotFoundError:
        logger.error("Файл не найден: %s", file_path)
        return []
    except Exception as e:
        logger.error("Ошибка чтения CSV-файла %s: %s", file_path, e)
        return []

    transactions = df.where(pd.notna(df), None).to_dict(orient="records")
    logger.info("Загружено %d транзакций из CSV: %s", len(transactions), file_path)
    return transactions


def get_transactions_from_excel(file_path: str) -> list[dict]:
    """
    Читает финансовые операции из Excel-файла (.xlsx).

    :param file_path: Путь к Excel-файлу.
    :return: Список словарей с транзакциями или пустой список при ошибке.
    """
    try:
        df = pd.read_excel(file_path, dtype=str)
    except FileNotFoundError:
        logger.error("Файл не найден: %s", file_path)
        return []
    except Exception as e:
        logger.error("Ошибка чтения Excel-файла %s: %s", file_path, e)
        return []

    transactions = df.where(pd.notna(df), None).to_dict(orient="records")
    logger.info("Загружено %d транзакций из Excel: %s", len(transactions), file_path)
    return transactions
