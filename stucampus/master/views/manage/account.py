from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import (user_passes_test,
                                            permission_required)

from stucampus.master.services import get_group_by_name
from stucampus.account.services import find_student
from stucampus.account.models import Student
from stucampus.custom.permission import admin_group_check
from stucampus.utils import spec_json, get_http_data


class ListAccount(View):

    @method_decorator(permission_required('account.students_list'))
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
            return spec_json(status='wrong_data')

        student = find_student(id)
        admin_group = get_group_by_name(name='StuCampus')
        if student is None:
            return spec_json(status='user_not_exist')

        if admin_group in student.user.groups.all():
            return spec_json(status='user_is_admin')

        student.user.is_active = False
        student.user.save()
        return spec_json(status='success')

    @method_decorator(permission_required('account.student_del'))
    @method_decorator(user_passes_test(admin_group_check))
    def delete(self, request, id):
        student = find_student(id)
        admin_group = get_group_by_name(name='StuCampus')
        if student is None:
            return spec_json(status='user_not_exist')

        if admin_group in student.user.groups.all():
            return spec_json(status='user_is_admin')

        student.user.delete()
        student.delete()
        return spec_json(status='success')
