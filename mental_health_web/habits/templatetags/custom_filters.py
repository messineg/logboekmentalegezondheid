# habits/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def dict_key(dictionary, key):
    """ Haalt een waarde op uit een dictionary in een Django template """
    return dictionary.get(key, {})