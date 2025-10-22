from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """Allows accessing dictionary items by key in a Django template."""
    return dictionary.get(key)