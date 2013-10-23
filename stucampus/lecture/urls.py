from django.conf.urls import url, patterns
from stucampus.lecture.views import index, manage, add_lecture


urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^manage/$', manage, name='manage'),
    url(r'^add_lecture/$', add_lecture, name='add_lecture'),
)
