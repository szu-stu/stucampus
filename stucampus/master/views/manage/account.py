from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import (user_passes_test,
                                            permission_required)
from django.core.paginator import InvalidPage, Paginator

from stucampus.account.models import Student
from stucampus.account.permission import check_perms
from stucampus.utils import spec_json


class ListAccount(View):
    """List all accounts class-base view"""
    @method_decorator(check_perms('account.student_manager'))
    def get(self, request):
        paginator = Paginator(Student.objects.all().order_by('-pk'), 4)
        try:
            page = paginator.page(request.GET.get('page'))
        except InvalidPage:
            page = paginator.page(1)
        return render(request, 'master/account-list.html',
                      {'page': page})


class ShowAccount(View):
    """Show a specific account class-base view"""
    @method_decorator(check_perms('account.student_manager'))
    def get(self, request, id):
        student = get_object_or_404(Student, id=id)
        return render(request, 'master/account-view.html',
                      {'student': student})

    @method_decorator(check_perms('account.student_manager'))
    def put(self, request, id):
        student = get_object_or_404(Student, id=id)

        if student.user.has_perm('website_admin'):
            return spec_json(status='user_is_admin')

        student.user.is_active = not student.user.is_active
        student.user.save()
        return spec_json(status='success')

    @method_decorator(check_perms('account.student_manager'))
    def delete(self, request, id):
        student = get_object_or_404(Student, id=id)
        if student.user.has_perm('website_admin'):
            return spec_json(status='user_is_admin')

        student.user.delete()
        student.delete()
        return spec_json(status='success')
