from django.conf.urls import *

urlpatterns = patterns('HavelCMS.views',
    url(r'^$', 'page', name="resources-single"),
    (r'search/$', 'search'),
    url(r'.*/$', 'page'),
)
