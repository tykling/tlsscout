from django import template
from datetime import timedelta
register = template.Library()

@register.filter(expects_localtime=True)
def relative_date_hours(value, arg):
    """add or substract a given number of hours from a datetime"""
    return value + timedelta(hours=arg)

