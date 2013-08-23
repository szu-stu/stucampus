#-*- coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from stucampus.infor.models import Infor
from stucampus.organization.models import Organization
from stucampus.master.forms import InforCreateForm
from stucampus.custom.permission import admin_group_check
from stucampus.utils import spec_json


@user_passes_test(admin_group_check)
def list(request):
    if request.method == 'GET':
        if not request.user.has_perm('infor.infor_list'):
            return HttpResponse(status=405)
        infors = Infor.objects.all()
        return render(request, 'master/infor_list.html', {'infors': infors})


@user_passes_test(admin_group_check)
def post(request):
    if request.method == 'GET':
        if not request.user.has_perm('infor.infor_create'):
            return HttpResponse(status=405)
        else:
            orgs = request.user.student.orgs_as_manager.all()
            return render(request, 'master/infor_post.html', {'orgs': orgs})


@user_passes_test(admin_group_check)
def infor(request):
    if request.method == 'POST':
        if not request.user.has_perm('infor.infor_create'):
            return HttpResponse(status=405)
        else:
            form = InforCreateForm(request.POST)
            if form.is_valid():
                data = request.POST
                title = data['title']
                content = data['content']
                organization_id = data['organization_id']
                author = request.user.student
                organization = Organization.objects.get(id=organization_id)
                Infor.objects.create(title=title, content=content,
                                     author=author, organization=organization)
                success = True
                messages = [u'发布成功']
            else:
                success = False
                messages = form.errors.values()
            return spec_json(success, messages)
