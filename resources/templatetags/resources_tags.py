from django import template
from resources.models import Page
from django.utils import translation
from django.conf import settings
from django.contrib.sites.models import Site

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

@register.inclusion_tag('resources/translations.html', takes_context=True)
def translations(context):
    site = Site.objects.get_current()
    page = context['page']
    translations = []
    for l in settings.LANGUAGES:
        code = subdomain = l[0]
        v = page.translation_pool.get_by_language(code)
        if v is not None:
            path = v.get_absolute_url()
        else:
            path = "/"
        if code == settings.LANGUAGE_CODE:
            subdomain = "www"
        translations.append({'code': code, 
                             'url': "http://%s.%s%s" % (subdomain,
                                                        site.domain,
                                                        path),
                             'language': l[1]})
    return locals()
