#-*- coding: utf-8
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group

from stucampus.account.services import find_student
from stucampus.account.models import Student
from stucampus.custom.permission import admin_group_check
from stucampus.utils import spec_json, get_http_data


class ListAccount(View):

    @method_decorator(user_passes_test(admin_group_check))    
    def get(self, request):
        if not request.user.has_perm('account.student_list'):
            return HttpResponse(status=403)
        students = Student.objects.all()
        return render(request, 'master/account-list.html',
                      {'students': students})


class ShowAccount(View):

    @method_decorator(user_passes_test(admin_group_check))
    def get(self, request, id):
        if not request.user.has_perm('account.student_list'):
            return HttpResponse(status=403)
        student = get_object_or_404(Student, id=id)
        return render(request, 'master/account-view.html',
                      {'student': student})

    @method_decorator(user_passes_test(admin_group_check))
    def put(self, request, id):
        if not request.user.has_perm('account.student_edit'):
            return HttpResponse(status=403)
        data = get_http_data(request)
        if data['is_ban'] is not True:
            return HttpResponse(status=405)
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

    def delete(self, request, id):
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
