#!/bin/bash
set -e

# Применяем миграции Alembic (файл alembic.ini лежит в LR)
alembic -c LR/alembic.ini upgrade head

# Запускаем приложение
uvicorn LR.app.main:app --host 0.0.0.0 --port 8000