def is_args_type(is_type, *args) -> bool:
    """Проверяет что все данные в `args` являются типом `is_type`."""
    for arg in args:
        if not isinstance(arg, is_type):
            return False
    return True
