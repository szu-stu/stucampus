from django.conf.urls import url, patterns
from stucampus.activity.views import index, add_activity, manage, submit


urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^manage/$', manage, name='manage'),
    url(r'^manage/(?P<page_num>\d+)/$', manage, name='manage'),
    url(r'^submit/$', submit, name='submit'),
    url(r'^add_activity/$', add_activity, name='add_activity'),
    )
