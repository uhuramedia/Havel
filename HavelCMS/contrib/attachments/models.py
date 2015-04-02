# -*- coding: utf-8 -*-

from django.db import models

from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

from model_utils.managers import InheritanceManager

@python_2_unicode_compatible
class RelatedLink(models.Model):
    content_type = models.ForeignKey(ContentType)
    title = models.CharField(max_length=255, verbose_name='Title')
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = InheritanceManager()

    def __str__(self):
        return self.title

    def get_bs_icon(self):
        """
        Helper method to give Bootstrap 3 icon class name based on link type. See subclasses
        """
        return 'glyphicon-link'

    def get_url(self):
        return self.url


@python_2_unicode_compatible
class WebLink(RelatedLink):
    WEB = 'Web'
    EVE = 'Event'

    TYPES = (
        (WEB, 'Web Page'),
        (EVE, 'Event Link')
    )

    link_type = models.CharField(choices=TYPES, default='Web', max_length=10)
    url = models.URLField(max_length=400)

    def __str__(self):
        return '%s: %s' % (self.link_type, self.title)

    def get_bs_icon(self):

        if self.link_type == 'Event':
            return 'glyphicon-calendar'

        return 'glyphicon-link'


@python_2_unicode_compatible
class FileLink(RelatedLink):

    link_type = 'Doc'

    file = models.FileField(upload_to='files', help_text='Audio MP3 or PDF, MS word files.')

    def __str__(self):
        return '%s: %s' % (self.link_type, self.title)

    def get_bs_icon(self):
        return 'glyphicon-file'

    def get_url(self):
        return self.file.url
