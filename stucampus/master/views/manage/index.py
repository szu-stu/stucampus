#-*- coding: utf-8
import platform

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator

from stucampus.custom.permission import admin_group_check
from stucampus.account.permission import check_perms


@login_required
def redirect(request):
    return HttpResponseRedirect('/manage/index')


@login_required
def index(request):
    if not request.user.student.true_name or not request.user.student.job_id:
        return HttpResponseRedirect('/account/register')
    return render(request, 'master/index.html')
