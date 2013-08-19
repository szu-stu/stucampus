from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'stucampus.organization.views.organization',
        name='organization')
)
