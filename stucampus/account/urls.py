from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^signin$', 'stucampus.account.views.sign_in', name='sign_in'),
)
