from django.conf.urls import url, patterns

from .views import AddPlan,like,search,plan_list,self_plan


urlpatterns = [
    url(r'^(?P<category_english_name>\D*)/$', plan_list, name='list'),
    url(r'^(?P<category_english_name>\D*)/add_plan/?$',AddPlan.as_view(),name='add_plan'),
    url(r'^(?P<category_english_name>\D*)/like/?$',like,name='like'),
    url(r'^(?P<category_english_name>\D*)/search/?$',search,name='search'),
    url(r'^(?P<category_english_name>\D*)/self_plan/?$',self_plan,name='self_plan'),
]
