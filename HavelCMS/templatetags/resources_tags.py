from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils import translation
from resources.models import Page, ResourceCollection, ResourceCollectionItem, \
    Resource

register = template.Library()

@register.inclusion_tag('resources/menu.html', takes_context=True)
def show_menu(context, onepage=False):
    lang = translation.get_language()
    pages = Resource.tree.filter(in_menu=True, language=lang, level=0).select_related('page', 'weblink')
    return {'page': context.get('page', None),
            'pages': pages,
            'onepage': onepage}

@register.inclusion_tag('resources/menu.html', takes_context=True)
def show_menu_below(context, page_pk, parent_if_empty=1):
    lang = translation.get_language()
    pages = Resource.objects.none()
    if page_pk:
        resource = Resource.objects.get(pk=page_pk)
        children = resource.get_children()
        if not children and parent_if_empty and resource.parent:
            children = resource.parent.get_children()
        pages = children.filter(in_menu=True, language=lang).select_related('page', 'weblink')
    return {'page': context.get('page', None),
            'pages': pages}

@register.inclusion_tag('resources/submenu.html', takes_context=True)
def show_submenu(context, res, in_menu=True):
    lang = translation.get_language()
    pages = res.get_descendants().\
                filter(level=1,
                       in_menu=in_menu,
                       language=lang).\
                select_related('page', 'weblink')

    return {'page': context.get('page', None),
            'pages': pages,
            'parent': res.pk}


@register.inclusion_tag('resources/list.html', takes_context=True)
def breadcrumbs(context, page=None):
    lang = translation.get_language()
    page = page or context.get('page', None)
    if not page:
        return
    pages = page.get_ancestors(include_self=True).\
                filter(language=lang)
    return {'page': context.get('page', None),
            'pages': pages}


@register.assignment_tag(takes_context=True)
def breadcrumbs_items(context, page=None):
    lang = translation.get_language()
    page = page or context.get('page', None)
    pages = page.get_ancestors(include_self=True).filter(language=lang)
    return pages


@register.inclusion_tag('resources/menu.html', takes_context=True)
def show_menu_at_level(context, level, page=None):
    #      0
    #   1     1
    #  2 2   2 2
    lang = translation.get_language()
    target = page = page or context.get('page', None)
    if not page:
        return

    try:
        if page.level > level:
            # if this page sits deeper than target level
            target = page.get_ancestors().filter(level=level)[0]
        elif page.level < level:
            # if this page sits higher than target level
            target = page.get_descendants().filter(level=level)[0]
    except IndexError:
        target = None

    pages = Page.objects.none()
    if target:
        pages = target.get_siblings(include_self=True).\
                    filter(in_menu=True, language=lang)

    return {'page': context.get('page', None),
            'pages': pages}

@register.inclusion_tag('resources/collection.html', takes_context=True)
def page_collection(context, collection_slug, onepage=False):
    try:
        items = ResourceCollectionItem.objects.collection(collection_slug)
        return {'page': context.get('page', None),
                'items': items,
                'onepage': onepage}
    except ResourceCollection.DoesNotExist:
        pass

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
