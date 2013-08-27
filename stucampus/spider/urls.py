from django.conf.urls import url, patterns
from stucampus.spider.views import index, update, delete


urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^update/$', update, name='update'),
    url(r'^delete/$', delete, name='delete'),
    )
