from django.conf.urls import patterns, url

from stucampus.dreamer.views import *

urlpatterns = [
    url(r'^joinus/$', SignUp.as_view(),name='joinus'),
    url(r'^login_redirect$',login_redirect,name='login_redirect'),
    url(r'^manage/$', alllist, name='list'),
    url(r'^manage/delete/$', delete, name='delete'),
    url(r'^manage/search/$', search, name='search'),
    url(r'^manage/modify/$', modify, name='modify'),
]
