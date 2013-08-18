from django.conf.urls import url, patterns
from stucampus.lecture.views import index

urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
)
