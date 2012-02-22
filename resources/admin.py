from django.contrib import admin
from resources.models import Page, Weblink

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'slug', 'created', 'author', 'get_absolute_url')

admin.site.register(Page, PageAdmin)
admin.site.register(Weblink)
