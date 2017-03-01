from django.conf.urls import patterns, url

from stucampus.comment.views import *

urlpatterns = [
    url(r'^get$', get_comment, name='getComment'),
    url(r'^add$', add_comment, name='addComment'),
    url(r'^getUserInfo', szu_oauth_info, name='getInfo'),
    url(r'^login$', szu_login, name='login')
]
