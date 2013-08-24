from django.conf.urls import url, patterns
from stucampus.spider.views import AnnouncementList, update


urlpatterns = patterns(
    '',
    url(r'^$', AnnouncementList.as_view(), name='index'),
    url(r'^update$', update, name='update'),
    )
