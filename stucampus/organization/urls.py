from django.conf.urls import patterns, url

from .views import organization

urlpatterns = [
    url(r'^$', organization, name='organization'),
]
