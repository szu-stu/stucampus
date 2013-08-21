#-*- coding: utf-8
import platform

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group

from stucampus.master.forms import AddOrganizationForm
from stucampus.master.forms import AddOrganizationManagerForm
from stucampus.organization.models import Organization
from stucampus.organization.services import org_is_exist, find_organization
from stucampus.account.services import find_by_email, find_student
from stucampus.account.models import Student
from stucampus.custom.permission import admin_group_check
from stucampus.utils import spec_json, get_http_data


@user_passes_test(admin_group_check)
def redirect(request):
    return HttpResponseRedirect('/manage/status')


@user_passes_test(admin_group_check)
def status(request):
    python_version = platform.python_version()
    domain = request.get_host()
    param = {'python_version': python_version,
             'domain': domain}
    return render(request, 'master/status.html', param)


@user_passes_test(admin_group_check)
def organization(request):
    if request.method == 'GET':
        if not request.user.has_perm('organization.organization_list'):
            return HttpResponse(status=403)
        orgs = Organization.objects.all()
        normal_orgs = Organization.objects.filter(is_banned=False,
                                                  is_deleted=False)
        baned_orgs = Organization.objects.filter(is_banned=True)
        deleted_orgs = Organization.objects.filter(is_deleted=True)
        orgs_num = len(orgs)
        normal_orgs_num = len(normal_orgs)
        baned_orgs_num = len(baned_orgs)
        deleted_orgs_num = len(deleted_orgs)
        param = {'orgs': orgs, 'normal_orgs': normal_orgs,
                 'baned_orgs': baned_orgs, 'deleted_orgs': deleted_orgs,
                 'orgs_num': orgs_num, 'normal_orgs_num': normal_orgs_num,
                 'baned_orgs_num': baned_orgs_num,
                 'deleted_orgs_num': deleted_orgs_num}
        return render(request, 'master/organizations.html', param)
    elif request.method == 'POST':
        if not request.user.has_perm('organization.organization_create'):
            return HttpResponse(status=403)
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
def organization_operate(request, id):
    if request.method == 'GET':
        if not request.user.has_perm('organization.organization_view'):
            return HttpResponse(status=403)
        org = get_object_or_404(Organization, id=id)
        return render(request, 'master/organization_view.html', {'org': org})
    elif request.method == 'DELETE':
        if not request.user.has_perm('organization.organization_del'):
            return HttpResponse(status=403)
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
def organization_manager(request, id):
    if request.method == 'POST':
        if not request.user.has_perm('account.org_manager_create'):
            return HttpResponse(status=403)
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


@user_passes_test(admin_group_check)
def account(request):
    if request.method == 'GET':
        if not request.user.has_perm('account.student_list'):
            return HttpResponse(status=403)
        students = Student.objects.all()
        return render(request, 'master/accounts.html', {'students': students})


@user_passes_test(admin_group_check)
def account_operate(request, id):
    if request.method == 'GET':
        if not request.user.has_perm('account.student_list'):
            return HttpResponse(status=403)
        student = get_object_or_404(Student, id=id)
        return render(request, 'master/account_view.html',
                     {'student': student})
    elif request.method == 'PUT':
        if not request.user.has_perm('account.student_edit'):
            return HttpResponse(status=403)
        student = find_student(id)
        admin_group = Group.objects.get(name='StuCampus')
        if student is None:
            success = False
            messages = [u'该用户不存在']
        elif admin_group in student.user.groups.all():
            success = False
            messages = [u'不能禁用管理员']
        else:
            success = True
            messages = [u'禁用成功']
        return spec_json(success, messages)
    elif request.method == 'DELETE':
        if not request.user.has_perm('account.student_del'):
            return HttpResponse(status=403)
        student = find_student(id)
        admin_group = Group.objects.get(name='StuCampus')
        if student is None:
            success = False
            messages = [u'该用户不存在']
        elif admin_group in student.user.groups.all():
            success = False
            messages = [u'不能删除管理员!']
        else:
            student.user.delete()
            student.delete()
            success = False
            messages = [u'删除成功']
        return spec_json(success, messages)
