from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'stucampus.master.views.admin_redirect', name='admin_index'),
    url(r'^status$',
        'stucampus.master.views.admin_status', name='admin_status'),
    url(r'^organization$',
        'stucampus.master.views.admin_organization',
        name='admin_organization'),
)
