from django.conf.urls import url, patterns
from stucampus.lecture.views import index, manage, submit
from stucampus.lecture.views import delete, add_lecture


urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^manage/$', manage, name='manage'),
    url(r'^manage/(?P<page_num>\d+)/$', manage, name='manage'),
    url(r'^submit/$', submit, name='submit'),
    url(r'^delete/$', delete, name='delete'), # for debug
    url(r'^add_lecture/$', add_lecture, name='add_lecture'),
)
