#-*- coding: utf-8
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import (user_passes_test,
                                            permission_required)

from stucampus.master.services import get_group_by_name
from stucampus.account.services import find_by_email
from stucampus.master.forms import AddOrganizationForm
from stucampus.master.forms import AddOrganizationManagerForm
from stucampus.organization.models import Organization
from stucampus.custom.permission import admin_group_check
from stucampus.organization.services import is_org_exist, find_organization
from stucampus.utils import spec_json


class ListOrganzation(View):

    @method_decorator(permission_required('organization.organization_list'))
    @method_decorator(user_passes_test(admin_group_check))
    def get(self, request):
        orgs = Organization.objects.all()
        normal_orgs = Organization.objects.filter(is_banned=False,
                                                  is_deleted=False)
        baned_orgs = Organization.objects.filter(is_banned=True)
        deleted_orgs = Organization.objects.filter(is_deleted=True)
        param = {'orgs': orgs, 'normal_orgs': normal_orgs,
                 'baned_orgs': baned_orgs, 'deleted_orgs': deleted_orgs}
        return render(request, 'master/organization-list.html', param)

    @method_decorator(permission_required('organization.organization_create'))
    @method_decorator(user_passes_test(admin_group_check))
    def post(self, request):
        form = AddOrganizationForm(request.POST)
        if form.is_valid():
            data = request.POST
            name = data['name']
            if not is_org_exist(name):
                Organization.objects.create(name=name, phone=data['phone'])
                success = True
                messages = '添加成功'
            else:
                success = False
                messages = '组织已存在'
        else:
            success = False
            messages = form.errors.values()
        return spec_json(success, messages)


class ShowOrganization(View):

    @method_decorator(permission_required('organization.organization_show'))
    @method_decorator(user_passes_test(admin_group_check))
    def get(self, request, id):
        org = get_object_or_404(Organization, id=id)
        return render(request, 'master/organization-view.html', {'org': org})

    @method_decorator(permission_required('organization.organization_del'))
    @method_decorator(user_passes_test(admin_group_check))
    def delete(self, request, id):
        org = find_organization(id)
        if org is None:
            success = False
            messages = '该组织不存在'
        else:
            org.is_deleted = True
            org.save()
            success = True
            messages = '删除陈功'
        return spec_json(success, messages)


class OrganzationManager(View):

    @method_decorator(permission_required('organization.organization_create'))
    @method_decorator(user_passes_test(admin_group_check))
    def get(self, request, id):
        org = get_object_or_404(Organization, id=id)
        form = AddOrganizationManagerForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            student = find_by_email(email)
            if student is None:
                success = False
                messages = '该邮箱不存在'
            else:
                if not org in student.orgs_as_member.all():
                    org.members.add(student)
                org.managers.add(student)
                org_mng_group = get_group_by_name(name='organization_manager')
                student.user.groups.add(org_mng_group)
                success = True
                messages = '添加成功'
        else:
            success = False
            messages = form.errors.values()
        return spec_json(success, messages)
