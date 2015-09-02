from django.conf.urls import url, patterns

from stucampus.lecture.views import index, mobile, ManageView, auto_add


urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^manage/$', ManageView.as_view(), name='manage'),
    url(r'^mobile/$', mobile, name='mobile'),
    url(r'^auto_add/$', auto_add, name='auto_add'),
)
