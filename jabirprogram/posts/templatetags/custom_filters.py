from django import template

register = template.Library()

@register.filter
def full_datetime(value):
    return value.strftime("%B %-d, %Y · %-I:%M %p")
