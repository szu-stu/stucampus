from django.conf.urls import url, patterns
from stucampus.activity.views import index, mobile, ManageView


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^manage/?$', ManageView.as_view(), name='manage'),
    url(r'^mobile/?$', mobile, name='mobile'),
]
