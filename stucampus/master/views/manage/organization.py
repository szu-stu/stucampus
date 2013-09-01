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

    @method_decorator(permission_required('organization.organizations_list'))
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
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='form_errors', messages=messages)

        data = request.POST
        name = data['name']
        if is_org_exist(name):
            return spec_json(status='org_name_exist')

        Organization.objects.create(name=name, phone=data['phone'])
        return spec_json(status='success')


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
            return spec_json(status='org_not_exist')
        else:
            org.is_deleted = True
            org.save()
            return spec_json(status='success')


class OrganzationManager(View):

    @method_decorator(permission_required('organization.organization_create'))
    @method_decorator(user_passes_test(admin_group_check))
    def get(self, request, id):
        org = get_object_or_404(Organization, id=id)
        form = AddOrganizationManagerForm(request.POST)
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='form_errors', messages=messages)

        email = request.POST['email']
        student = find_by_email(email)
        if student is None:
            return spec_json(status='email_not_exist')

        if not org in student.orgs_as_member.all():
            org.members.add(student)
        org.managers.add(student)
        org_mng_group = get_group_by_name(name='organization_manager')
        student.user.groups.add(org_mng_group)
        return spec_json(status='success')
