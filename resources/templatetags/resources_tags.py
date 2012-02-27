from django import template
from resources.models import Page
from django.utils import translation

register = template.Library()

@register.inclusion_tag('resources/menu.html', takes_context=True)
def show_menu(context):
    lang = translation.get_language()
    pages = Page.tree.filter(in_menu=True, language=lang)
    return {'page': context.get('page', None),
            'pages': pages}

@register.inclusion_tag('resources/menu.html', takes_context=True)
def show_menu_below(context, page_pk):
    lang = translation.get_language()
    pages = Page.objects.get(pk=page_pk).get_children().\
                filter(in_menu=True, language=lang)
    return {'page': context.get('page', None),
            'pages': pages}
