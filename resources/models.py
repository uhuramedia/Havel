# -*- coding: UTF-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
import datetime
import os


class cached_property(object):
    '''A read-only @property that is only evaluated once. The value is cached
    on the object itself rather than the function or class; this should prevent
    memory leakage.'''
    def __init__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__
        self.__module__ = fget.__module__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        obj.__dict__[self.__name__] = result = self.fget(obj)
        return result


class ResourceManager(TreeManager):

    def get_query_set(self):
        return super(ResourceManager, self).get_query_set().filter(is_published=True)

class Resource(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)
    content_type = models.SlugField(editable=False)

    title = models.CharField(max_length=100)
    menu_title = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(blank=True)

    in_menu = models.BooleanField(default=True, db_index=True)
    noindex = models.BooleanField("Do not index", default=False)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True)

    is_published = models.BooleanField(default=True, db_index=True)
    published = models.DateTimeField(blank=True, null=True)
    unpublished = models.DateTimeField(blank=True, null=True)

    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    translation_pool = models.ForeignKey("ResourceTranslation", verbose_name=_("Translation pool"), editable=False)
    language = models.CharField(max_length=5, db_index=True,
                                choices=settings.LANGUAGES,
                                default=settings.LANGUAGES[0][0])

    all_objects = TreeManager()
    objects = tree = ResourceManager()

    def __unicode__(self):
        return self.menu_title or self.title

    def get_absolute_url(self):
        if self.slug == "":
            return reverse('resources-single')
        url = self.slug
        for ancestor in self.get_ancestors(ascending=True):
            url = ancestor.slug + '/' + url
        return "%s%s/" % (reverse('resources-single'), url)

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = self.__class__.__name__
        if not hasattr(self, 'translation_pool'):
            tp = ResourceTranslation.objects.create()
            self.translation_pool = tp
        super(Resource, self).save(*args, **kwargs)

    def get_object(self):
        return getattr(self, self.content_type.lower())

    @cached_property
    def get_children_related(self):
        return self.get_children().select_related('page', 'weblink')

    def resolve(self):
        return self.get_object().resolve()

    def get_edit_link(self):
        # reverse admin url to get link to specific object
        return urlresolvers.reverse('admin:%s_%s_change' % (self.get_object()._meta.app_label,
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

    def new(self):
        return self.created > timezone.now() - datetime.timedelta(days=7)

    def fresh(self):
        return self.modified != self.created and (self.modified > timezone.now() - datetime.timedelta(days=14))

    def __getattribute__(self, name):
        if name.startswith("property_"):
            try:
                return self.resourceproperty_set.get(key=name.replace("property_", "")).value
            except:
                pass
        return MPTTModel.__getattribute__(self, name)

    class Meta:
        verbose_name = _('Resource')
        verbose_name_plural = _('Resources')
        unique_together = (('translation_pool', 'language'),
                           ('slug', 'language'))


class ResourceTranslation(models.Model):
    """ resources can be associated with their versions in other languages
    by putting them in the same translation pool"""

    def __unicode__(self):
        return " ".join(["[%s] %s" % (obj.language, unicode(obj)[:20]) for obj in self.resource_set.all()])

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

    class Meta:
        verbose_name = _(u'Resource translation')
        verbose_name_plural = _(u'Resource translations')


class ResourceProperty(models.Model):
    resource = models.ForeignKey(Resource)
    key = models.CharField(max_length=20)
    value = models.TextField()

    class Meta:
        unique_together = ('resource', 'key')


class ResourceCollection(models.Model):
    name = models.SlugField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

    def items(self):
        return self.resourcecollectionitem_set.all().select_related('resource__page', 'resource__weblink').order_by('sort')

    class Meta:
        verbose_name = _(u'Resource collection')
        verbose_name_plural = _(u'Resource collections')


class ResourceCollectionManager(models.Manager):

    def collection(self, name):
        return self.filter(collection__name=name).select_related('resource__page', 'resource__weblink').order_by('sort')


class ResourceCollectionItem(models.Model):
    collection = models.ForeignKey(ResourceCollection)
    resource = models.ForeignKey(Resource)
    sort = models.PositiveSmallIntegerField()
    objects = ResourceCollectionManager()


class Weblink(Resource):
    target = models.CharField(max_length=255)

    def get_absolute_url(self):
        return self.target

    def get_response(self, request):
        return HttpResponsePermanentRedirect(self.target)

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
                                help_text=_("Inherit if empty"))

    class Meta:
        verbose_name = _(u'Page')
        verbose_name_plural = _(u'Page')

    def get_template(self):
        if self.template == "":
            try:
                return self.parent.get_object().get_template()
            except AttributeError: #  no parent
                return template_default() or template_choices()[0][0]
        return self.template

    def get_response(self, request):
        return render(request, self.get_template(), {'page': self})

    def resolve(self):
        return self.get_absolute_url()

    def subpages(self):
        return render_to_string("resources/subpages.html", {'page': self, 'start': 2})

    def subnav(self):
        return render_to_string("resources/subnav.html", {'page': self, 'start': 2})


class File(models.Model):
    data = models.FileField(upload_to="file")

    class Meta:
        verbose_name = _(u'File')
        verbose_name_plural = _(u'Files')

    def __unicode__(self):
        return os.path.basename(self.data.name)
