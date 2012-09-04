from django.conf.urls.defaults import *

urlpatterns = patterns('resources.views',
    (r'^$', 'page'),
    (r'search/$', 'search'),
    (r'.*/$', 'page'),
)
