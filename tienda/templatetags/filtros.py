from django import template

register = template.Library()

@register.filter
def formato_clp(value):
    try:
        value = int(value)
        return f"${value:,}".replace(",", ".")
    except (ValueError, TypeError):
        return value
