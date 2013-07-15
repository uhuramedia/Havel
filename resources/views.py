from django.core.urlresolvers import resolve
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, \
    HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.base import TemplateDoesNotExist
from django.utils import translation
from resources.models import Resource, Page

def page(request):
    path = request.path.strip('/').split('/')
    slug = path[-1]
    language = translation.get_language()
    resource = get_object_or_404(Resource, slug=slug, language=language)
    if resource.get_absolute_url() != request.path:
        qs = "?" + request.META['QUERY_STRING'] if request.META['QUERY_STRING'] != "" else ""
        return HttpResponsePermanentRedirect(resource.get_absolute_url() + qs)
    try:
        return resource.get_object().get_response(request)
    except TemplateDoesNotExist:
        return HttpResponse(status=503)


def search(request):
    context = {}
    language = translation.get_language()
    context['q'] = q = request.GET.get('q', '')
    context['pages'] = Page.objects.filter(Q(title__icontains=q) | Q(text__icontains=q), language=language)
    return render(request, 'resources/search.html', context)
