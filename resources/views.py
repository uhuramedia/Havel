from django.shortcuts import render, get_object_or_404
from resources.models import Resource
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect,\
    Http404
from django.core.urlresolvers import resolve
from portlet.models import PortletAssignment, split_path

def page(request):
    path = request.path.strip('/').split('/')
    slug = path[-1]
    resource = get_object_or_404(Resource, slug=slug)
    if hasattr(resource, "page"):
        page = resource.page
        return render(request, page.get_template(), {'page': page})
    else:
        return HttpResponseRedirect(resource.weblink.target)
