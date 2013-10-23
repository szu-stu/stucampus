from django.conf.urls import url, patterns
from stucampus.activity.views import index, add_activity, manage


urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^manage/$', manage, name='manage'),
    url(r'^add_activity/$', add_activity, name='add_activity'),
    )
