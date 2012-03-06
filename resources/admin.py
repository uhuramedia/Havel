from django.contrib import admin
from resources.models import ResourceProperty, Page, Weblink, Resource,\
    ResourceTranslation
from mptt.admin import MPTTModelAdmin, FeinCMSModelAdmin
import datetime
from django.conf import settings

class ResourcePropertyInline(admin.TabularInline):
    model = ResourceProperty

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
