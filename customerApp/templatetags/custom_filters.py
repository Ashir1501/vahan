from django import template

register = template.Library()

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.simple_tag
def addmulti(*args):
    total = 0
    for val in args:
        total+=int(val)
    return total