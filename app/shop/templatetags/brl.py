from django import template

from ..utils import values

register = template.Library()

@register.filter('brl')
def brl(value):
    return values.brl(value)

@register.filter('percent')
def percent(value):
    return '%.2f' % value
