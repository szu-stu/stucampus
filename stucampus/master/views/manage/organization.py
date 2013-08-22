#-*- coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from stucampus.account.services import find_by_email
from stucampus.master.forms import AddOrganizationForm
from stucampus.master.forms import AddOrganizationManagerForm
from stucampus.organization.models import Organization
from stucampus.custom.permission import admin_group_check
from stucampus.organization.services import org_is_exist, find_organization
from stucampus.utils import spec_json


@user_passes_test(admin_group_check)
def list(request):
    if request.method == 'GET':
        if not request.user.has_perm('organization.organization_list'):
            return HttpResponse(status=405)
        orgs = Organization.objects.all()
        normal_orgs = Organization.objects.filter(is_banned=False,
                                                  is_deleted=False)
        baned_orgs = Organization.objects.filter(is_banned=True)
        deleted_orgs = Organization.objects.filter(is_deleted=True)
        param = {'orgs': orgs, 'normal_orgs': normal_orgs,
                 'baned_orgs': baned_orgs, 'deleted_orgs': deleted_orgs}
        return render(request, 'master/organization_list.html', param)
    elif request.method == 'POST':
        if not request.user.has_perm('organization.organization_create'):
            return HttpResponse(status=405)
        form = AddOrganizationForm(request.POST)
        if form.is_valid():
            data = request.POST
            name = data['name']
            if not org_is_exist(name):
                Organization.objects.create(name=name, phone=data['phone'])
                success = True
                messages = [u'添加成功']
            else:
                success = False
                messages = [u'组织已存在']
        else:
            success = False
            messages = form.errors.values()
        return spec_json(success, messages)


@user_passes_test(admin_group_check)
def view(request, id):
    if request.method == 'GET':
        if not request.user.has_perm('organization.organization_view'):
            return HttpResponse(status=405)
        org = get_object_or_404(Organization, id=id)
        return render(request, 'master/organization_view.html', {'org': org})
    elif request.method == 'DELETE':
        if not request.user.has_perm('organization.organization_del'):
            return HttpResponse(status=405)
        org = find_organization(id)
        if org is None:
            success = False
            messages = [u'该组织不存在']
        else:
            org.is_deleted = True
            org.save()
            success = True
            messages = [u'删除陈功']
        return spec_json(success, messages)


@user_passes_test(admin_group_check)
def manager(request, id):
    if request.method == 'POST':
        if not request.user.has_perm('account.org_manager_create'):
            return HttpResponse(status=405)
        org = get_object_or_404(Organization, id=id)
        form = AddOrganizationManagerForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            student = find_by_email(email)
            if student is None:
                success = False
                messages = [u'该邮箱不存在']
            else:
                if not org in student.orgs_as_member.all():
                    org.members.add(student)
                org.managers.add(student)
                messages = [u'添加成功']
                success = True
        else:
            messages = form.errors.values()
            success = False
        return spec_json(success, messages)
