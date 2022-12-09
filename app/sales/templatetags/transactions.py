from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter('render_itens')
def render_itens(transaction):
    items = transaction.get_products()
    html = '<ul>'
    for item in items:
        html += '<li>%s</li>' % str(item)
    html += '</ul>'
    return format_html(html)
