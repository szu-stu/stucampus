from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^$', 'stucampus.master.views.manage.status.redirect',
        name='admin_index'),

    url(r'^status$',
        'stucampus.master.views.manage.status.status', name='admin_status'),

    url(r'^organization/list$',
        'stucampus.master.views.manage.organization.list',
        name='manage_organization_list'),
    url(r'^organization/(?P<id>\d+)$',
        'stucampus.master.views.manage.organization.view',
        name='manage_organization_view'),
    url(r'^organization/(?P<id>\d+)/manager$',
        'stucampus.master.views.manage.organization.manager',
        name='manage_organization_manage'),

    url(r'^account/list$',
        'stucampus.master.views.manage.account.list',
        name='manage_account_list'),
    url(r'^account/(?P<id>\d+)$',
        'stucampus.master.views.manage.account.view',
        name='manage_account_view'),

    url(r'^infor/list$',
        'stucampus.master.views.manage.infor.list',
        name='manage_infor_list'),
    url(r'^infor/post$',
        'stucampus.master.views.manage.infor.post',
        name='manage_infor_post'),
    url(r'^infor$',
        'stucampus.master.views.manage.infor.infor',
        name='manage_infor_infor'),

    url(r'^organization$',
        'stucampus.organization.views.organization_manage',
        name='organization_manage'),
    url(r'^organization/(?P<id>\d+)/edit$',
        'stucampus.organization.views.organization_edit',
        name='organization_edit'),

)
