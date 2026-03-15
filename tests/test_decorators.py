"""
Тесты для модуля decorators.

Проверяет корректность работы декоратора @log.
"""

import os

import pytest

from src.decorators import log


@pytest.fixture
def log_file_path():
    """Путь к тестовому лог-файлу."""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(test_dir)
    log_dir = os.path.join(project_root, "logs")
    log_file = os.path.join(log_dir, "test_log.txt")

    if os.path.exists(log_file):
        os.remove(log_file)

    yield log_file

    if os.path.exists(log_file):
        os.remove(log_file)


@pytest.fixture
def sample_function():
    """Простая функция для тестирования."""

    @log(filename="test_log.txt")
    def add(x, y):
        return x + y

    return add


@pytest.fixture
def error_function():
    """Функция, которая вызывает ошибку."""

    @log(filename="test_log.txt")
    def divide(x, y):
        return x / y

    return divide


def test_log_decorator_successful_execution(sample_function, log_file_path):
    """Декоратор записывает 'start' и 'stop' при успешном выполнении."""
    result = sample_function(2, 3)

    assert result == 5

    with open(log_file_path, "r", encoding="utf-8") as f:
        log_content = f.read()

    assert "add start" in log_content
    assert "add stop" in log_content


def test_log_decorator_multiple_calls(sample_function, log_file_path):
    """Декоратор записывает каждый вызов функции."""
    sample_function(1, 2)
    sample_function(3, 4)
    sample_function(5, 6)

    with open(log_file_path, "r", encoding="utf-8") as f:
        log_content = f.read()

    assert log_content.count("add start") == 3
    assert log_content.count("add stop") == 3


def test_log_file_created(sample_function, log_file_path):
    """Лог-файл создаётся автоматически."""
    if os.path.exists(log_file_path):
        os.remove(log_file_path)

    sample_function(1, 1)

    assert os.path.exists(log_file_path)


def test_log_decorator_error_handling(error_function, log_file_path):
    """Декоратор записывает информацию об ошибке."""
    with pytest.raises(ZeroDivisionError):
        error_function(10, 0)

    with open(log_file_path, "r", encoding="utf-8") as f:
        log_content = f.read()

    assert "divide error: ZeroDivisionError" in log_content
    assert "Inputs: (10, 0)" in log_content


def test_log_decorator_error_with_kwargs(log_file_path):
    """Декоратор логирует kwargs при ошибке."""

    @log(filename="test_log.txt")
    def problematic_function(a, b=None):
        return a / b

    with pytest.raises(TypeError):
        problematic_function(5, b=None)

    with open(log_file_path, "r", encoding="utf-8") as f:
        log_content = f.read()

    assert "problematic_function error: TypeError" in log_content
    assert "{'b': None}" in log_content


def test_log_decorator_preserves_exception(error_function):
    """Декоратор пробрасывает исключение дальше."""
    with pytest.raises(ZeroDivisionError) as exc_info:
        error_function(1, 0)

    assert exc_info.type == ZeroDivisionError


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (1, 2, 3),
        (10, 20, 30),
        (-5, 5, 0),
        (0, 0, 0),
    ],
)
def test_log_decorator_parametrized(x, y, expected, log_file_path):
    """Параметризованный тест для разных входных данных."""

    @log(filename="test_log.txt")
    def add(a, b):
        return a + b

    result = add(x, y)
    assert result == expected

    with open(log_file_path, "r", encoding="utf-8") as f:
        log_content = f.read()

    assert "add start" in log_content
    assert "add stop" in log_content


def test_log_decorator_console_by_default(capsys):
    """Декоратор @log() без параметров логирует в консоль."""

    @log()
    def console_default_function():
        return "console output"

    result = console_default_function()
    assert result == "console output"

    captured = capsys.readouterr()
    assert "console_default_function start" in captured.out
    assert "console_default_function stop" in captured.out


def test_log_decorator_default_to_console(capsys):
    """Декоратор без параметров выводит в консоль."""

    @log()
    def default_function():
        return True

    result = default_function()
    assert result is True

    captured = capsys.readouterr()
    assert "default_function start" in captured.out
    assert "default_function stop" in captured.out


def test_log_creates_directory_if_not_exists():
    """Декоратор создаёт директорию logs/, если её нет."""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(test_dir)
    log_dir = os.path.join(project_root, "logs")

    @log(filename="dir_test.log")
    def test_func():
        return "stop"

    test_func()

    assert os.path.exists(log_dir)


def test_log_decorator_with_print_statements(capsys, log_file_path):
    """Декоратор работает с функциями, которые печатают в консоль."""

    @log(filename="test_log.txt")
    def print_function(message):
        print(message)
        return message

    result = print_function("Hello, World!")

    assert result == "Hello, World!"

    captured = capsys.readouterr()
    assert "Hello, World!" in captured.out

    with open(log_file_path, "r", encoding="utf-8") as f:
        log_content = f.read()

    assert "print_function start" in log_content
    assert "print_function stop" in log_content


# ─── Тесты логирования в консоль ──────────────────────────────────────────────


def test_log_to_console_success(capsys):
    """Декоратор выводит в консоль при filename=None."""

    @log()
    def console_function(x):
        return x * 2

    result = console_function(5)

    assert result == 10

    captured = capsys.readouterr()
    assert "console_function stop" in captured.out


def test_log_to_console_error(capsys):
    """Декоратор выводит ошибку в консоль при filename=None."""

    @log()
    def error_console_function():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        error_console_function()

    captured = capsys.readouterr()
    assert "error_console_function error: ValueError" in captured.out
    assert "Inputs: ()" in captured.out


def test_log_to_console_with_none_explicit(capsys):
    """Декоратор с явным filename=None выводит в консоль."""

    @log(filename=None)
    def explicit_none_function():
        return "success"

    result = explicit_none_function()
    assert result == "success"

    captured = capsys.readouterr()
    assert "explicit_none_function stop" in captured.out


def test_log_to_console_multiple_calls(capsys):
    """Декоратор выводит в консоль несколько вызовов."""

    @log()
    def multi_console(x):
        return x + 1

    multi_console(1)
    multi_console(2)
    multi_console(3)

    captured = capsys.readouterr()
    assert captured.out.count("multi_console stop") == 3


def test_log_file_vs_console(capsys, log_file_path):
    """Декоратор с filename пишет в файл, без - в консоль."""

    @log(filename="test_log.txt")
    def file_function():
        return "file"

    @log()
    def console_function():
        return "console"

    file_result = file_function()
    console_result = console_function()

    assert file_result == "file"
    assert console_result == "console"

    captured = capsys.readouterr()
    assert "console_function stop" in captured.out
    assert "file_function stop" not in captured.out

    with open(log_file_path, "r", encoding="utf-8") as f:
        log_content = f.read()

    assert "file_function stop" in log_content
    assert "console_function stop" not in log_content
