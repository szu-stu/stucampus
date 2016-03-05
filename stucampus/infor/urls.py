from django.conf.urls import patterns, url
from .views import list

urlpatterns = [
    url(r'^$', list, name='list'),
]
