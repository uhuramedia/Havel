from django.shortcuts import render, get_object_or_404
from resources.models import Resource, Page
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, \
    Http404
from django.core.urlresolvers import resolve
from django.utils import translation
from django.db.models import Q

def page(request):
    path = request.path.strip('/').split('/')
    slug = path[-1]
    language = translation.get_language()
    resource = get_object_or_404(Resource, slug=slug, language=language)
    return resource.get_object().get_response(request)


def search(request):
    context = {}
    language = translation.get_language()
    context['q'] = q = request.GET.get('q', '')
    context['pages'] = Page.objects.filter(Q(title__icontains=q) | Q(text__icontains=q), language=language)
    return render(request, 'resources/search.html', context)
