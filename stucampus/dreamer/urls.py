from django.conf.urls import patterns, url

from stucampus.dreamer.views import *

urlpatterns = patterns(
    '',
    url(r'index$', index,name='index'),
    url(r'^signup/$', SignUp.as_view(), name='signup'),
    url(r'^signup_mobile/$', signup_mobile, name='signup_mobile'),
    url(r'check_msg/$', CheckMsg.as_view(), name='check'),
    url(r'succeed/$', succeed),
    url(r'^sunup/$', alldetail, name='sunup'),
    url(r'^manage/$', alllist, name='list'),
    url(r'^manage/delete/$', delete, name='delete'),
    url(r'^manage/search/$', search, name='search'),
    url(r'^manage/detail/$', detail, name='detail'),
)
