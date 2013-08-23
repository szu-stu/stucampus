from django.conf.urls import url, patterns
from stucampus.spider.views import index


urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    )
