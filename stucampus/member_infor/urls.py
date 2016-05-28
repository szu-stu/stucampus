from django.conf.urls import url

from .views import AddMemberList,UserModifyMember,ApplyMember,pending_approve_members
from .views import SearchMember,del_member,manage,ModifyMember,AddMember,approve_member


urlpatterns = [
    url(r'^search/$', SearchMember.as_view(), name='search'),
    url(r'^add/$', AddMember.as_view(), name='add'),
    url(r'^modify/$', ModifyMember.as_view(), name='modify'),
    url(r'^add_list/$', AddMemberList.as_view(), name='add_list'),
    url(r'^manage/$', manage, name='manage'),
    url(r'^del_member/$', del_member, name='delete'),
    url(r'^user_modify$',UserModifyMember.as_view(),name="user_modify_member"),
    url(r'^apply$',ApplyMember.as_view(),name="apply"),
    url(r'^pending_approve_members$',pending_approve_members,name="pending_approve_members"),
    url(r'^approve_member$',approve_member,name="approve_member"),
]
