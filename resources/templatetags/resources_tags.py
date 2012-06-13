from django import template
from resources.models import Page, ResourceCollection
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

@register.inclusion_tag('resources/collection.html', takes_context=True)
def page_collection(context, collection_slug):
    collection = ResourceCollection.objects.get(name=collection_slug)
    return {'page': context.get('page', None),
            'collection': collection}

@register.inclusion_tag('resources/translations.html', takes_context=True)
def translations(context, label_type="full"):
    site = Site.objects.get_current()
    language = translation.get_language()
    page = context.get('page', None)
    translations = []
    for l in settings.LANGUAGES:
        code = subdomain = l[0]
        if page is None:
            path = context['request'].path
        else:
            v = page.translation_pool.get_by_language(code)
            if v is not None:
                path = v.get_absolute_url()
            else:
                path = "/"
        if code == settings.LANGUAGE_CODE:
            subdomain = "www"
        if label_type == "code1":
            label = l[0][0].upper()
        elif label_type == "code":
            label = l[0].upper()
        else:
            label = l[1]
        translations.append({'code': code, 
                             'url': "http://%s.%s%s" % (subdomain,
                                                        site.domain.replace("www.", ""),
                                                        path),
                             'language': l[1],
                             'label': label})
    return locals()