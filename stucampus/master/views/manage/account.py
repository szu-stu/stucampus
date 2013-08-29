#-*- coding: utf-8
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import (user_passes_test,
                                            permission_required)

from stucampus.account.services import find_student
from stucampus.account.models import Student
from stucampus.custom.permission import admin_group_check
from stucampus.utils import spec_json, get_http_data


class ListAccount(View):

    @method_decorator(permission_required('account.student_list'))
    @method_decorator(user_passes_test(admin_group_check))
    def get(self, request):
        students = Student.objects.all()
        return render(request, 'master/account-list.html',
                      {'students': students})


class ShowAccount(View):

    @method_decorator(permission_required('account.student_show'))
    @method_decorator(user_passes_test(admin_group_check))
    def get(self, request, id):
        student = get_object_or_404(Student, id=id)
        return render(request, 'master/account-view.html',
                      {'student': student})

    @method_decorator(permission_required('account.student_edit'))
    @method_decorator(user_passes_test(admin_group_check))
    def put(self, request, id):
        data = get_http_data(request)
        if data['is_ban'] is not True:
            success = False
            messages = '该用户已被禁用'
        else:
            student = find_student(id)
            admin_group = Group.objects.get(name='StuCampus')
            if student is None:
                success = False
                messages = '该用户不存在'
            elif admin_group in student.user.groups.all():
                success = False
                messages = '不能禁用管理员'
            else:
                student.user.is_active = False
                success = True
                messages = '禁用成功'
            return spec_json(success, messages)

    @method_decorator(permission_required('account.student_del'))
    @method_decorator(user_passes_test(admin_group_check))
    def delete(self, request, id):
        student = find_student(id)
        admin_group = Group.objects.get(name='StuCampus')
        if student is None:
            success = False
            messages = '该用户不存在'
        elif admin_group in student.user.groups.all():
            success = False
            messages = '不能删除管理员!'
        else:
            student.user.delete()
            student.delete()
            success = True
            messages = '删除成功'
        return spec_json(success, messages)
