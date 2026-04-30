#!/usr/bin/env python
# Главный файл для запуска команд Django (запуск сервера, миграции и т.д.)
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_platform.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. "
            "Убедитесь, что он установлен и активировано виртуальное окружение."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
