from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^signin$', 'stucampus.account.views.sign_in', name='sign_in'),
    url(r'^signup$', 'stucampus.account.views.sign_up', name='sign_up'),
)
