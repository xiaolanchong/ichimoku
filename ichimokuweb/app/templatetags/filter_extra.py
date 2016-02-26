from django import template

register = template.Library()

@register.filter
def sortbyname(value):
    return value.order_by('name')