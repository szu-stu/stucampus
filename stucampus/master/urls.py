from django.conf.urls import patterns, url

from stucampus.master.views.manage.account import ListAccount, ShowAccount
from stucampus.master.views.manage.infor import ListInfor, PostInfor
from stucampus.master.views.manage.infor import Information
from stucampus.master.views.manage.organization import ListOrganzation
from stucampus.master.views.manage.organization import ShowOrganization
from stucampus.master.views.manage.organization import OrganzationManager
from stucampus.organization.views import EditOrganzation


urlpatterns = patterns(
    '',
    url(r'^$', 'stucampus.master.views.manage.status.redirect',
        name='admin_index'),

    url(r'^status$',
        'stucampus.master.views.manage.status.status', name='admin_status'),

    url(r'^organization/list$', ListOrganzation.as_view(),
        name='manage_organization_list'),
    url(r'^organization/(?P<id>\d+)$', ShowOrganization.as_view(),
        name='manage_organization_show'),
    url(r'^organization/(?P<id>\d+)/manager$', OrganzationManager.as_view(),
        name='manage_organization_manage'),

    url(r'^account/list$', ListAccount.as_view(), name='manage_account_list'),
    url(r'^account/(?P<id>\d+)$', ShowAccount.as_view(),
        name='manage_account_show'),

    url(r'^infor/list$', ListInfor.as_view(), name='manage_infor_list'),
    url(r'^infor/post$', PostInfor.as_view(), name='manage_infor_post'),
    url(r'^infor/(?P<id>\d+)$', Information.as_view(),
        name='manage_infor_infor'),

    url(r'^organization$',
        'stucampus.organization.views.organization_manage',
        name='organization_manage'),
    url(r'^organization/(?P<id>\d+)/edit$', EditOrganzation.as_view(),
        name='organization_edit'),

)
