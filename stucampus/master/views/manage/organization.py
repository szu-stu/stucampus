from django.views.generic import View
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import (user_passes_test,
                                            permission_required)

from stucampus.organization.forms import AddOrganizationForm
from stucampus.organization.forms import AddOrganizationManagerForm
from stucampus.organization.models import Organization
from stucampus.organization.services import organization_manager_update
from stucampus.custom.permission import admin_group_check
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
            return spec_json(status='errors', messages=messages)

        name = form.cleaned_data['name']
        phone = form.cleaned_data['phone']
        Organization.objects.create(name=name, phone=phone)
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
        org = get_object_or_404(Organization, id=id)
        org.is_deleted = True
        org.save()
        return spec_json(status='success')


class OrganzationManager(View):

    @method_decorator(permission_required('organization.organization_create'))
    @method_decorator(user_passes_test(admin_group_check))
    def get(self, request, id):
        organization = get_object_or_404(Organization, id=id)
        form = AddOrganizationManagerForm(request.POST)
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='errors', messages=messages)

        email = form.cleaned_data['email']
        user = get_object_or_404(User, username=email)
        student = user.student
        organization_manager_update(student, organization)

        return spec_json(status='success')
