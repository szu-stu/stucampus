from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'stucampus.FreeTimeCount.views.index'),
    url(r'^date/', 'stucampus.FreeTimeCount.views.date'),
    url(r'^member/', 'stucampus.FreeTimeCount.views.member'),
    url(r'^distribute/', 'stucampus.FreeTimeCount.views.distribute'),
    url(r'^insert/', 'stucampus.FreeTimeCount.views.insert'),
]
