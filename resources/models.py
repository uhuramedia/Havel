from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager
import datetime
from django.contrib.auth.models import User
from django.shortcuts import render

class Resource(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    objects = TreeManager()
    
    title = models.CharField(max_length=100)
    menu_title = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(blank=True, unique=True)

    in_menu = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(auto_now=True, default=datetime.datetime.now)
    
    author = models.ForeignKey(User, blank=True, null=True)
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        if self.parent is not None:
            return "%s%s/" % (self.parent.get_absolute_url(), self.slug)
        elif self.slug == "":
            return "/"
        return "/%s/" % self.slug
    

class Weblink(Resource):
    target = models.CharField(max_length=255)
    
    def get_absolute_url(self):
        return self.target


class Page(Resource):
    show_title = models.BooleanField(default=True)
    meta_summary = models.TextField(blank=True)
    text = models.TextField(blank=True)
    template = models.CharField(max_length=100, blank=True)
    inherit_template = models.BooleanField(default=True)
    
    def get_template(self):
        if self.inherit_template:
            return self.parent.get_template()
        return self.template
