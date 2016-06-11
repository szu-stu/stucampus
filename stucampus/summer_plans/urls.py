from django.conf.urls import url, patterns

from .views import AddPlan,like,search,plan_list,self_plan,delete,logout,post_thought,like_ranking_list,senf_email_to_plan_author,has_thought_plan_list


urlpatterns = [
	url(r'^(?P<category_english_name>\w*)/logout/?$',logout,name='logout'),
    url(r'^(?P<category_english_name>\w*)/$', plan_list, name='list'),
    url(r'^(?P<category_english_name>\w*)/add_plan/?$',AddPlan.as_view(),name='add_plan'),
    url(r'^(?P<category_english_name>\w*)/like/?$',like,name='like'),
    url(r'^(?P<category_english_name>\w*)/search/?$',search,name='search'),
    url(r'^(?P<category_english_name>\w*)/post_thought/(?P<id>\d*)/?$',post_thought,name='post_thought'),
    url(r'^(?P<category_english_name>\w*)/self_plan/(?P<szu_no>\d*)/?$',self_plan,name='self_plan'),
    url(r'^(?P<category_english_name>\w*)/delete/(?P<id>\d*)/?$',delete,name='delete'),
    url(r'^(?P<category_english_name>\w*)/like_ranking_list/?$',like_ranking_list,name='like_ranking_list'),
    url(r'^(?P<category_english_name>\w*)/senf_email_to_plan_author/?$',senf_email_to_plan_author,name='senf_email_to_plan_author'),
    url(r'^(?P<category_english_name>\w*)/has_thought_plan_list/?$',has_thought_plan_list,name='has_thought_plan_list'),
]	
