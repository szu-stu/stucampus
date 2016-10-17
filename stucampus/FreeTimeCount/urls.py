from django.conf.urls import include, url
from django.contrib import admin

from .views import index,date,member,distribute

urlpatterns = [
    url(r'^$', index,name="index"),
    url(r'^date/?$', date,name="date"),
    url(r'^member/?$', member,name="member"),
    url(r'^distribute/?$',distribute,name="distribute"),
    url(r'^insert/', 'stucampus.FreeTimeCount.views.insert'),
]
