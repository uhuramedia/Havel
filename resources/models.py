from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager
import datetime
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core import urlresolvers
from django.conf import settings

class Resource(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)
    objects = TreeManager()
    content_type = models.SlugField(editable=False)
    
    title = models.CharField(max_length=100)
    menu_title = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(blank=True)

    in_menu = models.BooleanField(default=False, db_index=True)
    noindex = models.BooleanField("Do not index", default=False)

    created = models.DateTimeField(default=datetime.datetime.now, editable=False)
    modified = models.DateTimeField(auto_now=True, default=datetime.datetime.now)

    is_published = models.BooleanField(default=False, db_index=True)
    published = models.DateTimeField(blank=True, null=True)
    unpublished = models.DateTimeField(blank=True, null=True)
    
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    
    translation_pool = models.ForeignKey("ResourceTranslation", editable=False)
    language = models.CharField(max_length=5, db_index=True, 
                                choices=settings.LANGUAGES, 
                                default=settings.LANGUAGES[0])
    
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
        if not hasattr(self, 'translation_pool'):
            tp = ResourceTranslation.objects.create()
            self.translation_pool = tp
        super(Resource, self).save(*args, **kwargs)

    def get_object(self):
        return getattr(self, self.content_type.lower())
    
    def resolve(self):
        return self.get_object().resolve()
    
    def get_edit_link(self):
        # reverse admin url to get link to specific object
        return urlresolvers.reverse('admin:%s_%s_change' % (self._meta.app_label,
                                                            self.content_type.lower()),
                                    args=(self.pk,))
    
    def get_menu_title(self):
        if self.menu_title == "":
            return self.title
        return self.menu_title
    
    def get_translated_version(self, language):
        return self.translation_pool.get_by_language(language)
    
    def get_translated_versions(self):
        return self.translation_pool.get_versions()
    
    
    class Meta:
        unique_together = (('translation_pool', 'language'),
                           ('slug', 'language'))
    
    
class ResourceTranslation(models.Model):
    """ resources can be associated with their versions in other languages
    by putting them in the same translation pool"""
    
    def __unicode__(self):
        return " ".join(["[%s] %s" % (obj.language, obj.title) for obj in self.resource_set.all()])

    def get_versions(self):
        try:
            return Resource.objects.get(translation_pool=self)
        except Resource.DoesNotExist:
            pass
        
    def get_by_language(self, language=None):
        try:
            return Resource.objects.get(translation_pool=self, language=language)
        except Resource.DoesNotExist:
            pass


class ResourceProperty(models.Model):
    resource = models.ForeignKey(Resource)
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=255)
    
    class Meta:
        unique_together = ('resource', 'key')
        
        
class ResourceCollection(models.Model):
    name = models.SlugField(max_length=100, unique=True)
    
    def __unicode__(self):
        return self.name
    
    def items(self):
        return self.resourcecollectionitem_set.all().select_related().order_by('sort')
    
    
class ResourceCollectionItem(models.Model):
    collection = models.ForeignKey(ResourceCollection)
    resource = models.ForeignKey(Resource)
    sort = models.PositiveSmallIntegerField()
    

class Weblink(Resource):
    target = models.CharField(max_length=255)
    
    def get_absolute_url(self):
        return self.target
    
    def get_response(self, request):
        return HttpResponseRedirect(self.target)
    
    def resolve(self):
        return self.target


def template_choices():
    try:
        return settings.RESOURCES_TEMPLATES
    except AttributeError:
        pass

def template_default():
    try:
        return settings.RESOURCES_TEMPLATES[settings.RESOURCES_TEMPLATE_DEFAULT][0]
    except AttributeError:
        pass

class Page(Resource):
    show_title = models.BooleanField(default=True)
    meta_summary = models.TextField(blank=True)
    text = models.TextField(blank=True)
    template = models.CharField(max_length=100, blank=True, 
                                choices=template_choices(),
                                default=template_default(),
                                help_text="Inherit if empty")
    
    def get_template(self):
        if self.template == "":
            return self.parent.get_object().get_template()
        return self.template
    
    def get_response(self, request):
        return render(request, self.get_template(), {'page': self})
    
    def resolve(self):
        return self.get_absolute_url()
