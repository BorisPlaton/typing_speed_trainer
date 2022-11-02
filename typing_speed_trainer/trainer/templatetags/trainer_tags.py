from datetime import datetime

from django import template


register = template.Library()


@register.filter(name='to_datetime')
def to_datetime(date_in_string: str, date_format: str = '%Y-%m-%dT%H:%M:%S.%fZ') -> datetime:
    """Converts date from string to the datetime object."""
    try:
        return datetime.strptime(date_in_string, date_format)
    except ValueError:
        pass
