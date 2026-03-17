# Bank Widget Masks

Учебный проект для курса по Python. Реализует функции маскирования банковских данных, обработки операций и работы с
генераторами для виджета личного кабинета пользователя банка.

---

## Цель проекта

IT-отдел крупного банка разрабатывает новый виджет для личного кабинета клиента. Виджет отображает последние банковские
операции клиента, но для обеспечения безопасности необходимо:

1. **Маскировать конфиденциальные данные** - номера карт и счетов
2. **Фильтровать операции** - по статусу выполнения и валюте
3. **Сортировать операции** - по дате для удобного отображения
4. **Форматировать даты** - в понятный для пользователя формат
5. **Эффективно обрабатывать большие объёмы данных** - через генераторы
6. **Декорировать функции** - через декораторы
7. **Читать данные из JSON-файлов** - загрузка списка транзакций из файла
8. **Читать данные из CSV и Excel** - загрузка транзакций через pandas
9. **Конвертировать валюты** - получение актуального курса через внешний API
10. **Логировать события** - запись в файл с временной меткой, модулем и уровнем

Проект демонстрирует практическое применение Python для решения реальных задач финтех-индустрии с соблюдением стандартов
безопасности данных (PCI DSS).

---

## Функциональность

### Модуль `masks.py` - Маскирование данных

- **Маскирование номера банковской карты** - показывает первые 6 и последние 4 цифры
- **Маскирование номера банковского счета** - показывает только последние 4 цифры

### Модуль `widget.py` - Работа с виджетом

- **Маскирование карт и счетов с названием** - обрабатывает строки типа "Visa Platinum 7000792289606361"
- **Форматирование дат** - преобразует ISO формат в читаемый вид (ДД.ММ.ГГГГ)

### Модуль `processing.py` - Обработка операций

- **Фильтрация операций по статусу** - отбор операций по состоянию (EXECUTED, CANCELED и др.)
- **Сортировка операций по дате** - упорядочивание от новых к старым или наоборот

### Модуль `generators.py` - Генераторы для работы с данными

- **Фильтрация транзакций по валюте** - эффективный отбор по коду валюты (USD, RUB, EUR)
- **Генератор описаний транзакций** - поочерёдная выдача описаний операций
- **Генератор номеров банковских карт** - создание номеров в формате XXXX XXXX XXXX XXXX

### Модуль `decorators.py` - Декораторы функций

- **Логирование процесса выполнения функций** - записывает в файл или выводит в консоль результат выполнения функции

### Модуль `file_reader.py`

#### `get_transactions_from_csv(file_path: str) -> list[dict]`

Читает финансовые операции из CSV-файла (разделитель — `;`).

**Пример:**

```python
from src.file_reader import get_transactions_from_csv

transactions = get_transactions_from_csv("data/transactions.csv")
print(len(transactions))         # 5
print(transactions[0]["state"])  # EXECUTED
```

#### `get_transactions_from_excel(file_path: str) -> list[dict]`

Читает финансовые операции из Excel-файла (`.xlsx`).

**Пример:**

```python
from src.file_reader import get_transactions_from_excel

transactions = get_transactions_from_excel("data/transactions.xlsx")
print(len(transactions))                  # 5
print(transactions[0]["currency_code"])   # USD
```

Ожидаемые колонки: `id`, `state`, `date`, `amount`, `currency_name`, `currency_code`, `from`, `to`, `description`.
Отсутствующие значения конвертируются в `None`. При ошибке чтения возвращается пустой список.

---

### Модуль `utils.py` - Утилиты для работы с данными

- **Чтение транзакций из JSON-файла** - загружает список операций, возвращает пустой список при отсутствии файла или некорректных данных

### Модуль `file_reader.py` - Чтение CSV и Excel

- **Чтение транзакций из CSV-файла** — разбор файла с разделителем `;`, возвращает список словарей
- **Чтение транзакций из Excel-файла** — разбор `.xlsx`-файла через pandas, возвращает список словарей
- В обоих случаях при отсутствии файла или ошибке чтения возвращается пустой список

### Модуль `external_api.py` - Работа с внешним API

- **Конвертация суммы транзакции в рубли** - возвращает сумму в RUB; для USD и EUR обращается к Exchange Rates Data API за актуальным курсом

### Модуль `logger.py` - Настройка логирования

- **Фабрика логеров** - создаёт и возвращает настроенный логер для указанного модуля
- Логи записываются в папку `logs/` в корне проекта в файлы `<имя_модуля>.log`
- Формат записи: `дата-время - модуль - уровень - сообщение`
- Файл перезаписывается при каждом запуске

---

## Структура проекта

```
bank-widget-masks/
│
├── src/                          # Исходный код проекта
│   ├── __init__.py               # Инициализация пакета
│   ├── masks.py                  # Функции маскирования
│   ├── widget.py                 # Функции виджета
│   ├── processing.py             # Функции обработки операций
│   ├── generators.py             # Генераторы для работы с данными
│   ├── decorators.py             # Декораторы
│   ├── utils.py                  # Утилиты: чтение JSON-файлов
│   ├── file_reader.py            # Чтение транзакций из CSV и Excel
│   ├── external_api.py           # Конвертация валют через внешний API
│   └── logger.py                 # Фабрика логеров
│
├── tests/                        # Тесты проекта
│   ├── __init__.py               # Инициализация пакета тестов
│   ├── test_masks.py             # Тесты для masks
│   ├── test_widget.py            # Тесты для widget
│   ├── test_processing.py        # Тесты для processing
│   ├── test_generators.py        # Тесты для generators
│   ├── test_decorators.py        # Тесты для decorators
│   ├── test_utils.py             # Тесты для utils
│   ├── test_file_reader.py       # Тесты для file_reader (CSV и Excel)
│   └── test_external_api.py      # Тесты для external_api
│
├── data/                         # Данные проекта
│   └── operations.json           # Файл с банковскими операциями
│
├── logs/                         # Директория для лог-файлов (создаётся автоматически)
│   ├── masks.log                 # Логи модуля masks
│   ├── utils.log                 # Логи модуля utils
│   └── operations.log            # Логи декоратора @log
│
├── main.py                       # Главный файл с демонстрацией
├── pyproject.toml                # Конфигурация Poetry и зависимостей
├── .env                          # Переменные окружения (не хранится в Git)
├── .env.template                 # Шаблон переменных окружения
├── .flake8                       # Конфигурация линтера
├── .gitignore                    # Игнорируемые файлы для Git
└── README.md                     # Документация проекта
```

---

## Требования

- **Python**: 3.11 или выше
- **Poetry**: для управления зависимостями
- **pandas** и **openpyxl**: для чтения CSV и Excel-файлов

---

## Установка и настройка

### Шаг 1: Клонирование репозитория

```bash
git clone git@github.com:ivanitch/bank-widget-masks.git
cd bank-widget-masks
```

### Шаг 2: Установка зависимостей

```bash
poetry shell
poetry install
```

После выполнения этих команд Poetry:

- Создаст виртуальное окружение
- Установит все необходимые библиотеки (pytest, flake8, black, isort, mypy, requests, python-dotenv)
- Подготовит проект к работе

### Шаг 3: Настройка переменных окружения

```bash
cp .env.template .env
```

Откройте `.env` и укажите API-ключ для конвертации валют:

```
EXCHANGE_RATES_API_KEY=your_api_key_here
```

Получить ключ можно бесплатно на [apilayer.com](https://apilayer.com/marketplace/exchangerates_data-api).

> Файл `.env` добавлен в `.gitignore` и не попадает в репозиторий.

---

## Описание функций

### Модуль `masks.py`

#### `get_mask_card_number(card_number: str) -> str`

Маскирует номер банковской карты, оставляя видимыми первые 6 и последние 4 цифры.

**Пример:**

```python
from src.masks import get_mask_card_number

card = "7000792289606361"
print(get_mask_card_number(card))  # 7000 79** **** 6361
```

#### `get_mask_account(account_number: str) -> str`

Маскирует номер банковского счета, оставляя видимыми только последние 4 цифры.

**Пример:**

```python
from src.masks import get_mask_account

account = "73654108430135874305"
print(get_mask_account(account))  # **4305
```

---

### Модуль `widget.py`

#### `mask_account_card(card_or_account: str) -> str`

Универсальная функция для маскирования карт и счетов вместе с их названием.

**Примеры:**

```python
from src.widget import mask_account_card

print(mask_account_card("Visa Platinum 7000792289606361"))
# Visa Platinum 7000 79** **** 6361

print(mask_account_card("Счет 73654108430135874305"))
# Счет **4305
```

#### `get_date(date_string: str) -> str`

Преобразует дату из ISO 8601 формата в формат ДД.ММ.ГГГГ.

**Пример:**

```python
from src.widget import get_date

print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
```

---

### Модуль `processing.py`

#### `filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]`

Фильтрует список операций по статусу выполнения.

**Пример:**

```python
from src.processing import filter_by_state

operations = [
    {'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25'}
]

executed = filter_by_state(operations, state='EXECUTED')
print(len(executed))  # 1
```

#### `sort_by_date(data: list[dict], reverse: bool = True) -> list[dict]`

Сортирует список операций по дате.

**Пример:**

```python
from src.processing import sort_by_date

sorted_ops = sort_by_date(operations, reverse=True)  # От новых к старым
```

---

### Модуль `generators.py`

#### `filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]`

Фильтрует транзакции по коду валюты операции. Возвращает **итератор**.

**Пример:**

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, 'USD')
for t in usd_transactions:
    print(t['id'])
```

#### `transaction_descriptions(transactions: list[dict]) -> Iterator[str]`

Генератор описаний банковских транзакций. Возвращает **итератор** строк.

**Пример:**

```python
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)
print(next(descriptions))  # Перевод организации
print(next(descriptions))  # Перевод с карты на карту
```

#### `card_number_generator(start: int, stop: int) -> Iterator[str]`

Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

**Пример:**

```python
from src.generators import card_number_generator

for card in card_number_generator(1, 5):
    print(card)
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# ...
```

---

### Модуль `decorators.py`

#### `log(filename: str | None = None)`

Декоратор для логирования вызова функции. При `filename=None` выводит в консоль,
при указании имени файла — записывает в `logs/<filename>`.

**Пример:**

```python
from src.decorators import log

@log()
def add(a, b):
    return a + b

@log(filename="operations.log")
def multiply(a, b):
    return a * b
```

---

### Модуль `utils.py`

#### `get_transactions_from_json(file_path: str) -> list[dict]`

Читает JSON-файл и возвращает список транзакций. При отсутствии файла,
невалидном JSON или не-списковом содержимом возвращает пустой список.

**Пример:**

```python
from src.utils import get_transactions_from_json

transactions = get_transactions_from_json("data/operations.json")
print(len(transactions))  # 5

empty = get_transactions_from_json("data/missing.json")
print(empty)  # []
```

---

### Модуль `external_api.py`

#### `convert_transaction_amount(transaction: dict) -> float`

Возвращает сумму транзакции в рублях. Если валюта RUB — возвращает исходную сумму.
Если валюта USD или EUR — обращается к Exchange Rates Data API для получения актуального курса.

**Пример:**

```python
from src.external_api import convert_transaction_amount

rub_transaction = {
    "operationAmount": {
        "amount": "5000.00",
        "currency": {"name": "руб.", "code": "RUB"}
    }
}
print(convert_transaction_amount(rub_transaction))  # 5000.0
```

Требует заполненного `EXCHANGE_RATES_API_KEY` в файле `.env`.

---

### Модуль `logger.py`

#### `get_logger(name: str) -> logging.Logger`

Возвращает настроенный логер для модуля с именем `name`.
Файл лога создаётся в `logs/<name>.log` и перезаписывается при каждом запуске.

**Пример:**

```python
from src.logger import get_logger

logger = get_logger("my_module")
logger.info("Операция выполнена")
logger.error("Произошла ошибка: %s", error)
```

---

### Демонстрация всех функций

```bash
python main.py
```

Эта команда запустит демонстрацию работы всех модулей:

- Маскирование карт и счетов
- Форматирование дат
- Фильтрация и сортировка операций
- Генераторы для работы с данными
- Фильтрация по валюте
- Генерация номеров карт
- Логирование выполнения функций
- Чтение транзакций из JSON-файла
- Конвертация суммы транзакции в рубли

---

## Тестирование

### Запуск всех тестов

```bash
pytest tests

# С подробным выводом
pytest tests -v

# С покрытием кода
pytest tests -v --cov=src --cov-report=html
```

### Запуск конкретного тестового файла

```bash
pytest tests/test_masks.py -v
pytest tests/test_generators.py -v
pytest tests/test_decorators.py -v
pytest tests/test_utils.py -v
pytest tests/test_external_api.py -v
```

### Тестовое покрытие

Проект содержит комплексные unit-тесты:

- `test_masks.py` - тесты для маскирования
- `test_widget.py` - тесты для виджета
- `test_processing.py` - тесты для обработки
- `test_generators.py` - тесты для генераторов
- `test_decorators.py` - тесты для декораторов
- `test_utils.py` - тесты для чтения JSON-файлов
- `test_file_reader.py` - тесты для чтения CSV и Excel (Mock и patch)
- `test_external_api.py` - тесты для конвертации валют (Mock и patch)

Посмотреть отчет в консоли или HTML-отчет:

- `coverage report` - выводит таблицу в консоль
- `coverage html` - создаёт папку `htmlcov` с интерактивным сайтом.
  Открыть: `path/to/project/htmlcov/index.html`

---

## Проверка качества кода

```bash
# Проверка стиля кода (PEP 8)
flake8 main.py src

# Автоформатирование кода
black main.py src

# Сортировка импортов
isort main.py src

# Проверка типов
mypy main.py src
```

### Все проверки одной командой

```bash
flake8 main.py src && \
black --check main.py src && \
isort --check-only main.py src && \
mypy main.py src && \
pytest tests -v
```

Или через скрипт:

```bash
./lint.sh
```

---

## Примеры использования

### Пример 1: Работа с генераторами

```python
from src.generators import filter_by_currency, card_number_generator

usd_transactions = filter_by_currency(all_transactions, 'USD')
for t in usd_transactions:
    print(f"USD операция: {t['id']}")

for card in card_number_generator(1, 100):
    print(card)  # 0000 0000 0000 0001, 0000 0000 0000 0002, ...
```

### Пример 2: Комбинирование модулей

```python
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date
from src.generators import filter_by_currency


def get_recent_usd_operations(transactions, n=5):
    usd_ops = list(filter_by_currency(transactions, 'USD'))
    sorted_ops = sort_by_date(usd_ops, reverse=True)
    recent = sorted_ops[:n]

    for op in recent:
        date = get_date(op['date'])
        card = mask_account_card(op.get('from', ''))
        print(f"{date} - {card}")
```

### Пример 3: Загрузка из файла и конвертация валюты

```python
from src.utils import get_transactions_from_json
from src.external_api import convert_transaction_amount

transactions = get_transactions_from_json("data/operations.json")

for t in transactions:
    amount_rub = convert_transaction_amount(t)
    currency = t["operationAmount"]["currency"]["code"]
    print(f"ID {t['id']}: {t['operationAmount']['amount']} {currency} = {amount_rub:.2f} RUB")
```

---

## Технические навыки

- Работа со строками (slicing, форматирование)
- Функции с параметрами по умолчанию
- Type hints (аннотации типов)
- Работа со словарями и списками
- Обработка исключений
- Работа с датами (модуль datetime)
- Генераторы и итераторы (yield)
- Эффективная работа с памятью
- Логирование (модуль logging)
- Чтение и парсинг JSON-файлов
- HTTP-запросы к внешним API (библиотека requests)
- Переменные окружения (python-dotenv)

## Профессиональные практики

- Модульная архитектура (8 модулей)
- Подробная документация (docstrings)
- Unit-тестирование (80+ тестов)
- Мокирование внешних зависимостей (Mock и patch)
- Фикстуры pytest
- Параметризация тестов
- Соответствие PEP 8
- Управление зависимостями (Poetry)
- Контроль версий (Git)
- Защита чувствительных данных (.env)

---

## Безопасность данных

Проект следует лучшим практикам защиты конфиденциальных данных:

- **PCI DSS Compliance** - маскирование карт соответствует стандарту
- **Минимизация данных** - показываем только необходимый минимум
- **Не храним** - функции не сохраняют оригинальные данные
- **Только обработка** - фокус на преобразовании, а не хранении
- **Эффективность** - генераторы не загружают всё в память
- **Защита ключей** - API-ключи хранятся в `.env`, не попадают в репозиторий

---

## Зачем генераторы?

### Проблема с обычными функциями:

```python
def get_all_usd(transactions):
    result = []
    for t in transactions:
        if t['currency'] == 'USD':
            result.append(t)
    return result  # Список из миллионов элементов в памяти
```

### Решение через генератор:

```python
def filter_by_currency(transactions, currency):
    for t in transactions:
        if t['currency'] == currency:
            yield t  # Генерирует элементы по требованию
```

Преимущества: меньше памяти, мгновенный старт, можно остановить в любой момент.

---

## Полезные ссылки

- [Документация Python](https://docs.python.org/3/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [PEP 8 Style Guide](https://pep8.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [Exchange Rates Data API](https://apilayer.com/marketplace/exchangerates_data-api)
- [python-dotenv Documentation](https://pypi.org/project/python-dotenv/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [PCI DSS Requirements](https://www.pcisecuritystandards.org/)
- [Python Testing with pytest (Brian Okken)](https://tisten.ir/blog/wp-content/uploads/2019/01/Python-Testing-with-pytest-Pragmatic-Bookshelf-2017-Brian-Okken.pdf)
- [Pytest-Cheatsheet](https://github.com/mananrg/Pytest-Cheatsheet)
- [Раздел про тестирование в Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/tests/)
