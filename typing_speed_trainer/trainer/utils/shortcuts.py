from pathlib import Path

from django.conf import settings


def get_correct_template_path(*args: str) -> Path:
    """
    Возвращает путь к файлу из директории шаблонов
    конкретного приложения.
    """
    cur_path = settings.BASE_DIR / 'trainer' / 'templates'
    for path_name in args:
        cur_path /= path_name
    return cur_path
