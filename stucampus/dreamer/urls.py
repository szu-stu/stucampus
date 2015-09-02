from django.conf.urls import patterns, url

from stucampus.dreamer.views import *

urlpatterns = patterns(
    '',
    url(r'index$', index),
    url(r'^signup/$', SignUp.as_view(), name='signup'),
    url(r'check_msg/$', CheckMsg.as_view(), name='check'),
    url(r'succeed/$', succeed),
    url(r'^sunup/$', alldetail, name='sunup'),
    url(r'^management/$', alllist, name='list'),
    url(r'^management/delete/$', delete, name='delete'),
    url(r'^management/search/$', search, name='search'),
    url(r'^management/detail/$', detail, name='detail'),
)
