from django import template

register = template.Library()

@register.filter
def lookup(d, key):
    """Returns the value for the given key from a dictionary."""
    return d.get(key, None)
