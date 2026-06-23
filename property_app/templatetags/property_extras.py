from django import template

register = template.Library()


@register.filter
def split(value, delimiter=","):
    """Split a comma-separated string inside a Django template."""
    if value is None:
        return []
    return str(value).split(delimiter)


@register.filter
def trim(value):
    """Strip whitespace from a string inside a Django template."""
    if value is None:
        return ""
    return str(value).strip()

