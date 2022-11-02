from django import template


register = template.Library()


@register.filter(name='is_number')
def is_number(value) -> bool:
    """Checks if a given value is a number."""
    try:
        float(value)
    except ValueError:
        return False
    return True
