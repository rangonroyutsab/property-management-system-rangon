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


@register.filter
def km_value(value):
    """Return kilometers from a GeoDjango Distance object or a numeric value."""
    if value is None:
        return ""

    km = getattr(value, "km", None)
    if km is not None:
        return km

    try:
        return float(value)
    except (TypeError, ValueError):
        return value
