from django.conf.urls import patterns, include, url

from .views import SignUpView, resource_list, verify, details, index, resource_delete, LoginView, votes


urlpatterns = [
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^list/$', resource_list, name='resource_list'),
    url(r'^verify/$', verify, name='verify'),
    url(r'^$', index, name='index'),
    url(r'^details/$', details, name='details'),
    url(r'^delete/$',resource_delete,name="delete"),
    #url(r'^login/$',LoginView.as_view(),name="login"),
    #url(r'^votes/$',votes,name="votes")
]
