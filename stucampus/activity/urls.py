from django.conf.urls import url, patterns
from stucampus.activity.views import index, add_message, manage


urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^manage/$', manage, name='manage'),
    url(r'^add_message/$', add_message, name='add_message'),
    )
