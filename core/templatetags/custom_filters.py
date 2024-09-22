from django import template
from django.utils.dateformat import format
from datetime import date

register = template.Library()

@register.filter
def get_day_name(value):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    try:
        return days[int(value)]
    except (ValueError, IndexError):
        return str(value)
