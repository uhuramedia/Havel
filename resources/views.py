from django.shortcuts import render, get_object_or_404
from resources.models import Resource
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect,\
    Http404
from django.core.urlresolvers import resolve

def page(request):
    path = request.path.strip('/').split('/')
    slug = path[-1]
    resource = get_object_or_404(Resource, slug=slug)
    return resource.get_object().get_response(request)
