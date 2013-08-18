from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^signin$', 'stucampus.account.views.sign_in', name='sign_in'),
    url(r'^signup$', 'stucampus.account.views.sign_up', name='sign_up'),
    url(r'^profile$', 'stucampus.account.views.profile', name='profile'),
    url(r'^profile/edit$',
        'stucampus.account.views.profile_edit', name='profile_edit'),
    url(r'^profile/password$',
        'stucampus.account.views.password', name='password'),
)
