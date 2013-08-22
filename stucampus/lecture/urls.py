from django.conf.urls import url, patterns
from stucampus.lecture.views import index, manage, update

urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^manage$', manage, name='namange'),
    url(r'^update$', update, name='update'),
)
