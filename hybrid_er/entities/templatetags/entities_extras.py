from django import template

register = template.Library()

@register.filter
def lookup(d, key):
    return d[key]

@register.filter
def dir_it(d):
    return str(dir(d))
