from django.conf.urls import url, patterns
from stucampus.lecture.views import index, manage, submit,  update

urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^manage$', manage, name='manage'),
    url(r'^submit$', submit, name='submit'),
    url(r'^update$', update, name='update'),
)
