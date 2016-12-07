
from django.conf.urls import url
from django.contrib import admin

from views import wechat_main

urlpatterns = [
    url(r'^$', wechat_main, name='main'),
]
