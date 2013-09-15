from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import (user_passes_test,
                                            permission_required)

from stucampus.account.forms import AccountBanForm
from stucampus.account.models import Student
from stucampus.custom.permission import admin_group_check
from stucampus.utils import spec_json


class ListAccount(View):
    """List all accounts class-base view"""
    @method_decorator(permission_required('account.students_list'))
    @method_decorator(user_passes_test(admin_group_check))
    def get(self, request):
        students = Student.objects.all()
        return render(request, 'master/account-list.html',
                      {'students': students})


class ShowAccount(View):
    """Show a specific account class-base view"""
    @method_decorator(permission_required('account.student_show'))
    @method_decorator(user_passes_test(admin_group_check))
    def get(self, request, id):
        student = get_object_or_404(Student, id=id)
        return render(request, 'master/account-view.html',
                      {'student': student})

    @method_decorator(permission_required('account.student_edit'))
    @method_decorator(user_passes_test(admin_group_check))
    def put(self, request, id):
        form = AccountBanForm(request.PUT)
        student = get_object_or_404(Student, id=id)
        try:
            admin_group = Group.objects.get(name=name)
        except Group.DoesNotExist:
            return HttpResponse(status=403)

        if admin_group in student.user.groups.all():
            return spec_json(status='user_is_admin')

        student.user.is_active = False
        student.user.save()
        return spec_json(status='success')

    @method_decorator(permission_required('account.student_del'))
    @method_decorator(user_passes_test(admin_group_check))
    def delete(self, request, id):
        student = get_object_or_404(Student, id=id)
        try:
            admin_group = Group.objects.get(name=name)
        except Group.DoesNotExist:
            return HttpResponse(status=403)

        student = get_object_or_404(Student, id=id)

        if admin_group in student.user.groups.all():
            return spec_json(status='user_is_admin')

        student.user.delete()
        student.delete()
        return spec_json(status='success')
