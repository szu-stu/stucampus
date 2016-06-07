from django.conf.urls import url, patterns

from .views import index,AddPlan,like


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^add_plan/?$',AddPlan.as_view(),name='add_plan'),
    url(r'^like/?$',like,name='like'),
]
