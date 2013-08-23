#-*- coding: utf-8
import platform

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

from stucampus.custom.permission import admin_group_check


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

