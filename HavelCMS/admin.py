import datetime

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
from django.core import urlresolvers
from django.db import models
#from django.utils.importlib import import_module
from importlib import import_module
from django.utils.translation import ugettext_lazy as _

from feincms.admin.tree_editor import TreeEditor as _feincms_tree_editor
from mptt.admin import MPTTModelAdmin
from mptt.forms import MPTTAdminForm, TreeNodeChoiceField

from HavelCMS.models import ResourceProperty, Page, Weblink, Resource, \
    ResourceTranslation, ResourceCollection, ResourceCollectionItem, File

from contrib.attachments.admin import FileLinkInline, LinkInline

def get_class_from_string(str):
    path = str
    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]
    try:
        mod = import_module(module)
        return getattr(mod, attr)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' % (module, e))

class ResourcePropertyInline(admin.TabularInline):
    model = ResourceProperty
    extra = 0

class FeinCMSModelAdmin(_feincms_tree_editor):
    """
    A ModelAdmin to add changelist tree view and editing capabilities.
    Requires FeinCMS to be installed.
    """

    form = MPTTAdminForm

    def _actions_column(self, obj):
        actions = super(FeinCMSModelAdmin, self)._actions_column(obj)
        actions.insert(0,
            u'<a href="%s?%s=%s" title="%s">%s</a>' % (
                urlresolvers.reverse('admin:HavelCMS_page_add'),
                self.model._mptt_meta.parent_attr,
                obj.pk,
                _('+Page'),
                _('+Page')))
        actions.insert(0,
            u'<a href="%s?%s=%s" title="%s">%s</a>' % (
                urlresolvers.reverse('admin:HavelCMS_weblink_add'),
                self.model._mptt_meta.parent_attr,
                obj.pk,
                _('+Weblink'),
                _('+Weblink')))
        return actions

    def delete_selected_tree(self, modeladmin, request, queryset):
        """
        Deletes multiple instances and makes sure the MPTT fields get recalculated properly.
        (Because merely doing a bulk delete doesn't trigger the post_delete hooks.)
        """
        n = 0
        for obj in queryset:
            obj.delete()
            n += 1
        self.message_user(request, _("Successfully deleted %s items.") % n)

    def get_actions(self, request):
        actions = super(FeinCMSModelAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            actions['delete_selected'] = (self.delete_selected_tree, 'delete_selected', _("Delete selected %(verbose_name_plural)s"))
        return actions


def page_or_else(resource, code):
    v = resource.get_translated_version(code)
    if v is None:
        return "-"
    return v


class ResourceAdmin(FeinCMSModelAdmin):
    list_display = ('__unicode__',
                    'title_link',
                    'is_published',
                    'in_menu',
                    'translation_pool',
                    'language',
                    'author')
    list_filter = ('is_published', 'in_menu', 'author', 'language')
    search_fields = ('title',)
    inlines = (ResourcePropertyInline,)
    actions = ('make_published', 'make_unpublished', 'link')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['tree_id', 'lft']

    def __init__(self, *args, **kwargs):
        super(ResourceAdmin, self).__init__(*args, **kwargs)
        #self.list_display_links = (None,)

    def has_add_permission(self, request, obj=None):
        return False

    def title_link(self, obj):
        return u'<a href="%s">%s</a>' % (obj.get_edit_link(),
                                         obj.content_type)
    title_link.allow_tags = True
    title_link.short_description = _("Edit")

    def make_do(self, request, queryset, label, *args, **make):
        rows_updated = queryset.update(**make)
        if rows_updated == 1:
            message_bit = _("1 resource was")
        else:
            message_bit = _("%s resources were" % rows_updated)
        self.message_user(request, _("%(num)s successfully %(action)s." % {'num': message_bit, 'action': label}))

    def make_published(self, request, queryset):
        return self.make_do(request, queryset, _("marked as published"),
                            is_published=True, published=datetime.datetime.now())

    make_published.short_description = _("Mark selected resources as published")

    def make_unpublished(self, request, queryset):
        return self.make_do(request, queryset, _("marked as unpublished"),
                            is_published=False, published=None)

    make_unpublished.short_description = _("Mark selected resources as unpublished")

    def link(self, request, queryset):
        rt = ResourceTranslation.objects.create()
        for obj in queryset:
            obj.translation_pool = rt
            obj.save()

    link.short_description = _("Link these resources as translation")

admin.site.register(Resource, ResourceAdmin)


class PageAdmin(FeinCMSModelAdmin):
    list_display = ('mptt_title',
                    'is_published',
                    'in_menu',
                    'slug',
                    'language',
                    'author')
    ordering = ('tree_id', 'lft')
    list_filter = ('is_published', 'in_menu', 'author', 'language')
    inlines = (ResourcePropertyInline, LinkInline, FileLinkInline)
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
                'fields': ('parent', ('title', 'slug'), 'language', 'text', 'template')
        }),
        ('Settings', {
            'fields': ('in_menu', 'is_published', 'show_title')
        }),
        ('Timing', {
            'classes': ('collapse',),
            'fields': ('published', 'unpublished')
        }),
         ('Other', {
            'classes': ('collapse',),
            'fields': ('menu_title', 'menu_order', 'meta_summary', 'noindex', 'page_image', 'page_mobile_image')
         }),
    )

    def __init__(self, *args, **kwargs):
        super(PageAdmin, self).__init__(*args, **kwargs)
        setting = "RESOURCES_%s_TEXTWIDGET" % self.model._meta.model_name.upper()
        if hasattr(settings, setting):
            self.formfield_overrides = {
                models.TextField: {'widget': get_class_from_string(getattr(settings, setting)) }
            }
            overrides = FORMFIELD_FOR_DBFIELD_DEFAULTS.copy()
            overrides.update(self.formfield_overrides)
            self.formfield_overrides = overrides

        setting = "RESOURCES_%s_INLINES" % self.model._meta.model_name.upper()
        if hasattr(settings, setting):
            self.inlines = list(self.inlines)
            for i in getattr(settings, setting):
                self.inlines.append(get_class_from_string(i))

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


admin.site.register(Page, PageAdmin)


class WeblinkAdmin(ResourceAdmin):

    def __init__(self, *args, **kwargs):
        super(WeblinkAdmin, self).__init__(*args, **kwargs)

        setting = "RESOURCES_%s_INLINES" % self.model._meta.model_name.upper()
        if hasattr(settings, setting):
            self.inlines = list(self.inlines)
            for i in getattr(settings, setting):
                self.inlines.append(get_class_from_string(i))

    def has_add_permission(self, request, obj=None):
        return True

admin.site.register(Weblink, WeblinkAdmin)

class ResourceCollectionItemInline(admin.TabularInline):
    model = ResourceCollectionItem

class ResourceCollectionAdmin(admin.ModelAdmin):
    inlines = (ResourceCollectionItemInline,)

admin.site.register(ResourceCollection, ResourceCollectionAdmin)

admin.site.register(File)
