from django.conf.urls import url

from .views import SearchMember,del_member,manage,ModifyMember,AddMember,AddMemberList



urlpatterns = [
    url(r'^search/$', SearchMember.as_view(), name='search'),
    url(r'^add/$', AddMember.as_view(), name='add'),
    url(r'^modify/$', ModifyMember.as_view(), name='modify'),
    url(r'^add_list/$', AddMemberList.as_view(), name='add_list'),
    url(r'^manage/$', manage, name='manage'),
    url(r'^del_member/$', del_member, name='delete'),
]
