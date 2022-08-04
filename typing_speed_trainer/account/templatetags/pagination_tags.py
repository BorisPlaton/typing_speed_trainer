from django import template


register = template.Library()


@register.filter(name='is_number')
def is_number(value) -> bool:
    """
    Фильтр, который проверяет, является ли переданное
    значение числом.
    """
    try:
        float(value)
    except ValueError:
        return False
    return True
