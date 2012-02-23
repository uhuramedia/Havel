from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager
import datetime
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core import urlresolvers

class Resource(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    objects = TreeManager()
    content_type = models.SlugField(editable=False)
    
    title = models.CharField(max_length=100)
    menu_title = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(blank=True, unique=True)

    in_menu = models.BooleanField(default=False)
    noindex = models.BooleanField("Searchable", default=False)

    created = models.DateTimeField(default=datetime.datetime.now, editable=False)
    modified = models.DateTimeField(auto_now=True, default=datetime.datetime.now)

    is_published = models.BooleanField(default=False)
    published = models.DateTimeField(blank=True, null=True)
    unpublished = models.DateTimeField(blank=True, null=True)
    
    author = models.ForeignKey(User, blank=True, null=True)
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        if self.parent is not None:
            return "%s%s/" % (self.parent.get_absolute_url(), self.slug)
        elif self.slug == "":
            return "/"
        return "/%s/" % self.slug

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = self.__class__.__name__
        super(Resource, self).save(*args, **kwargs)

    def get_object(self):
        return getattr(self, self.content_type.lower())
    
    def get_edit_link(self):
        # reverse admin url to get link to specific object
        return urlresolvers.reverse('admin:%s_%s_change' % (self._meta.app_label,
                                                            self.content_type.lower()),
                                    args=(self.pk,))


class ResourceProperty(models.Model):
    resource = models.ForeignKey(Resource)
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=255)
    
    class Meta:
        unique_together = ('resource', 'key')
    

class Weblink(Resource):
    target = models.CharField(max_length=255)
    
    def get_absolute_url(self):
        return self.target
    
    def get_response(self, request):
        return HttpResponseRedirect(self.target)



class Page(Resource):
    show_title = models.BooleanField(default=True)
    meta_summary = models.TextField(blank=True)
    text = models.TextField(blank=True)
    template = models.CharField(max_length=100, blank=True, help_text="Inherit if empty")
    
    def get_template(self):
        if self.template == "":
            return self.parent.get_object().get_template()
        return self.template
    
    def get_response(self, request):
        return render(request, self.get_template(), {'page': self})
