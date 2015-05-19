# -*- coding: utf-8 -*-

from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Link, FileLink


class LinkInline(GenericTabularInline):
    model = Link
    extra = 1


class FileLinkInline(GenericTabularInline):
    model = FileLink
    extra = 1