from django import template

register = template.Library()


@register.simple_tag()
def bool_to_ru(var: bool) -> str:
    """
    bool to ru
    """
    return "Да" if var else "Нет"
