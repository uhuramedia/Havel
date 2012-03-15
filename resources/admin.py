from django.conf import settings
from django.contrib import admin
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _
from feincms.admin.tree_editor import TreeEditor as _feincms_tree_editor
from mptt.admin import MPTTModelAdmin
from mptt.forms import MPTTAdminForm, TreeNodeChoiceField
from resources.models import ResourceProperty, Page, Weblink, Resource, \
    ResourceTranslation, ResourceCollection, ResourceCollectionItem
import datetime

class ResourcePropertyInline(admin.TabularInline):
    model = ResourceProperty
    
    
class FeinCMSModelAdmin(_feincms_tree_editor):
    """
    A ModelAdmin to add changelist tree view and editing capabilities.
    Requires FeinCMS to be installed.
    """

    form = MPTTAdminForm

    def _actions_column(self, obj):
        actions = super(FeinCMSModelAdmin, self)._actions_column(obj)
        if hasattr(obj, 'get_absolute_url'):
            actions.insert(0,
                u'<a href="%s" title="%s" target="_blank"><img src="%simg/admin/selector-search.gif" alt="%s" /></a>' % (
                    obj.get_absolute_url(),
                    _('View on site'),
                    settings.ADMIN_MEDIA_PREFIX,
                    _('View on site')))
        actions.insert(0,
            u'<a href="%s?%s=%s" title="%s">%s</a>' % (
                urlresolvers.reverse('admin:resources_page_add'),                                                                                         
                self.model._mptt_meta.parent_attr,
                obj.pk,
                _('Add page'),
                _('Add page')))
        actions.insert(0,
            u'<a href="%s?%s=%s" title="%s">%s</a>' % (
                urlresolvers.reverse('admin:resources_weblink_add'),                                                                                         
                self.model._mptt_meta.parent_attr,
                obj.pk,
                _('Add weblink'),
                _('Add weblink')))
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
    list_display = ('title', 
                    'title_link', 
                    'get_absolute_url',
                    'created', 
                    'modified', 
                    'is_published', 
                    'translation_pool',
                    'in_menu',
                    'language',
                    'author')
    list_filter = ('is_published', 'in_menu', 'author', 'language')
    inlines = (ResourcePropertyInline,)
    actions = ('make_published', 'make_unpublished', 'link')
    prepopulated_fields = {'slug': ('title',)}
    
    def __init__(self, *args, **kwargs): 
        super(ResourceAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )
    
    def has_add_permission(self, request):
        return False
    
    def title_link(self,obj):
        return u'<a href="%s">%s</a>' % (obj.get_edit_link(),
                                         obj.content_type)
    title_link.allow_tags = True
    title_link.short_description = "Edit"
    
    def make_do(self, request, queryset, label, *args, **make):
        rows_updated = queryset.update(**make)
        if rows_updated == 1:
            message_bit = "1 resource was"
        else:
            message_bit = "%s resources were" % rows_updated
        self.message_user(request, "%s successfully %s." % (message_bit, label))
    
    def make_published(self, request, queryset):
        return self.make_do(request, queryset, "marked as published", 
                            is_published=True, published=datetime.datetime.now())

    make_published.short_description = "Mark selected resources as published"
    
    def make_unpublished(self, request, queryset):
        return self.make_do(request, queryset, "marked as unpublished",
                            is_published=False, published=None)

    make_unpublished.short_description = "Mark selected resources as unpublished"
    
    def link(self, request, queryset):
        rt = ResourceTranslation.objects.create()
        for obj in queryset:
            obj.translation_pool = rt
            obj.save()

admin.site.register(Resource, ResourceAdmin)

class PageAdmin(MPTTModelAdmin):
    list_display = ('title', 'parent', 'slug', 'created', 'author', 'get_absolute_url')
    inlines = (ResourcePropertyInline,)

admin.site.register(Page, PageAdmin)
admin.site.register(Weblink)

class ResourceCollectionItemInline(admin.TabularInline):
    model = ResourceCollectionItem

class ResourceCollectionAdmin(admin.ModelAdmin):
    inlines = (ResourceCollectionItemInline,)

admin.site.register(ResourceCollection, ResourceCollectionAdmin)
