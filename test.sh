#!/bin/bash

# Останавливать выполнение, если любая команда завершилась с ошибкой
set -e

echo "--- Running tests ---"
pytest tests/
