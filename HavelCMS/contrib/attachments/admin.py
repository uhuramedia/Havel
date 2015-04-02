# -*- coding: utf-8 -*-

from django.contrib.contenttypes.admin import GenericTabularInline

from .models import WebLink, FileLink


class WebLinkInline(GenericTabularInline):
    model = WebLink
    extra = 1


class FileLinkInline(GenericTabularInline):
    model = FileLink
    extra = 1