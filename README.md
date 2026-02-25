# 🏦 Bank Widget Masks

Учебный проект для курса по Python. Реализует функции маскирования банковских данных, обработки операций и работы с
генераторами для виджета личного кабинета пользователя банка.

---

## 📋 Цель проекта

IT-отдел крупного банка разрабатывает новый виджет для личного кабинета клиента. Виджет отображает последние банковские
операции клиента, но для обеспечения безопасности необходимо:

1. **Маскировать конфиденциальные данные** - номера карт и счетов
2. **Фильтровать операции** - по статусу выполнения и валюте
3. **Сортировать операции** - по дате для удобного отображения
4. **Форматировать даты** - в понятный для пользователя формат
5. **Эффективно обрабатывать большие объёмы данных** - через генераторы

Проект демонстрирует практическое применение Python для решения реальных задач финтех-индустрии с соблюдением стандартов
безопасности данных (PCI DSS).

---

## 🎯 Функциональность

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

---

## 📁 Структура проекта

```
bank-widget-masks/
│
├── src/                           # Исходный код проекта
│   ├── __init__.py               # Инициализация пакета
│   ├── masks.py                  # Функции маскирования
│   ├── widget.py                 # Функции виджета
│   ├── processing.py             # Функции обработки операций
│   └── generators.py             # Генераторы для работы с данными
│
├── tests/                         # Тесты проекта
│   ├── __init__.py               # Инициализация пакета тестов
│   ├── test_masks.py             # Тесты для masks
│   ├── test_widget.py            # Тесты для widget
│   ├── test_processing.py        # Тесты для processing
│   └── test_generators.py        # Тесты для generators
│
├── main.py                        # Главный файл с демонстрацией
├── pyproject.toml                # Конфигурация Poetry и зависимостей
├── .flake8                       # Конфигурация линтера
├── .gitignore                    # Игнорируемые файлы для Git
└── README.md                     # Документация проекта
```

---

## 💻 Требования

- **Python**: 3.11 или выше
- **Poetry**: для управления зависимостями

---

## 🚀 Установка и настройка

### Шаг 1: Клонирование репозитория

```bash
# Клонируйте репозиторий
git clone git@github.com:ivanitch/bank-widget-masks.git
cd bank-widget-masks
```

### Шаг 2: Установка зависимостей

```bash
# Активируйте виртуальное окружение Poetry
poetry shell

# Установите все зависимости проекта
poetry install
```

После выполнения этих команд Poetry:

- Создаст виртуальное окружение
- Установит все необходимые библиотеки (pytest, flake8, black, isort, mypy)
- Подготовит проект к работе

---

## 📚 Описание функций

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

---

#### `transaction_descriptions(transactions: list[dict]) -> Iterator[str]`

Генератор описаний банковских транзакций. Возвращает **итератор** строк.

**Пример:**

```python
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)
print(next(descriptions))  # Перевод организации
print(next(descriptions))  # Перевод с карты на карту
```

---

#### `card_number_generator(start: int, stop: int) -> Iterator[str]`

Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

**Пример:**

```python
from src.generators import card_number_generator

for card in card_number_generator(1, 5):
    print(card)
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005
```

**Диапазон:** от 0000 0000 0000 0001 до 9999 9999 9999 9999.

---

## 🎮 Запуск проекта

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

---

## 🧪 Тестирование

### Запуск всех тестов

```bash
pytest tests

# Запуск всех тестов с подробным выводом
pytest tests -v

# Запуск с покрытием кода
pytest tests -v --cov=src --cov-report=html

# Запуск конкретного тестового файла
pytest tests/test_masks.py -v
pytest tests/test_generators.py -v
```

### Тестовое покрытие

Проект содержит комплексные unit-тесты:

- `test_masks.py` - тесты для маскирования
- `test_widget.py` - тесты для виджета
- `test_processing.py` - тесты для обработки
- `test_generators.py` - тесты для генераторов

Посмотреть отчет в консоли или красивый HTML-отчет

- `coverage report` - читает `.coverage` и выводит таблицу в консоль
- `coverage html` - читает `.coverage` и создает папку `htmlcov` с интерактивным сайтом.
  Открыть сайт можно по адресу `path/to/project/htmlcov/index.html`

---

## 🔍 Проверка качества кода

### Запуск всех проверок

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

### Запуск всех проверок одной командой

```bash
flake8 main.py src && \
black --check main.py src && \
isort --check-only main.py src && \
mypy main.py src && \
pytest tests -v
```

Или можно запустить скрипт:

```bash
./lint.sh
```

---

## 📖 Примеры использования

### Пример 1: Работа с генераторами

```python
from src.generators import filter_by_currency, card_number_generator

# Эффективная фильтрация по валюте (не загружает всё в память)
usd_transactions = filter_by_currency(all_transactions, 'USD')
for t in usd_transactions:
    print(f"USD операция: {t['id']}")

# Генерация тестовых номеров карт
for card in card_number_generator(1, 100):
    print(card)  # 0000 0000 0000 0001, 0000 0000 0000 0002, ...
```

### Пример 2: Комбинирование модулей

```python
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date
from src.generators import filter_by_currency


# Получить последние 5 USD-операций с маскированием
def get_recent_usd_operations(transactions, n=5):
    # Фильтруем по валюте
    usd_ops = list(filter_by_currency(transactions, 'USD'))
    # Сортируем по дате
    sorted_ops = sort_by_date(usd_ops, reverse=True)
    # Берём последние N
    recent = sorted_ops[:n]

    # Выводим с маскировкой
    for op in recent:
        date = get_date(op['date'])
        card = mask_account_card(op.get('from', ''))
        print(f"{date} - {card}")
```

---

## 🎓 Что реализовано в проекте

### Технические навыки:

- Работа со строками (slicing, форматирование)
- Функции с параметрами по умолчанию
- Type hints (аннотации типов)
- Работа со словарями и списками
- Обработка исключений
- Работа с датами (модуль datetime)
- Генераторы и итераторы (yield)
- Эффективная работа с памятью

### Профессиональные практики:

- Модульная архитектура (4 модуля)
- Подробная документация (docstrings)
- Unit-тестирование (50+ тестов)
- Фикстуры pytest
- Параметризация тестов
- Соответствие PEP 8
- Управление зависимостями (Poetry)
- Контроль версий (Git)

---

## 🛡️ Безопасность данных

Проект следует лучшим практикам защиты конфиденциальных данных:

- **PCI DSS Compliance** - маскирование карт соответствует стандарту
- **Минимизация данных** - показываем только необходимый минимум
- **Не храним** - функции не сохраняют оригинальные данные
- **Только обработка** - фокус на преобразовании, а не хранении
- **Эффективность** - генераторы не загружают всё в память

---

## 💡 Зачем генераторы?

### Проблема с обычными функциями:

```python
# ❌ Загружает ВСЕ результаты в память сразу
def get_all_usd(transactions):
    result = []
    for t in transactions:
        if t['currency'] == 'USD':
            result.append(t)
    return result  # Список из миллионов элементов в памяти!
```

### Решение через генератор:

```python
# ✅ Выдаёт по одному элементу, экономит память
def filter_by_currency(transactions, currency):
    for t in transactions:
        if t['currency'] == currency:
            yield t  # Генерирует элементы по требованию
```

**Преимущества:**

- 🚀 Меньше использует памяти
- ⚡ Начинает работу мгновенно (не ждёт обработки всех данных)
- 🔄 Можно остановить в любой момент

---

## 🔗 Полезные ссылки

- [Документация Python](https://docs.python.org/3/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [PEP 8 Style Guide](https://pep8.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [PCI DSS Requirements](https://www.pcisecuritystandards.org/)
- [Python Testing with pytest (Brian Okken)](https://tisten.ir/blog/wp-content/uploads/2019/01/Python-Testing-with-pytest-Pragmatic-Bookshelf-2017-Brian-Okken.pdf)
- [Pytest-Cheatsheet](https://github.com/mananrg/Pytest-Cheatsheet)
- [Раздел про тестирование в Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/tests/)

---

*Этот проект создан с ❤️ для изучения Python и best practices разработки*
