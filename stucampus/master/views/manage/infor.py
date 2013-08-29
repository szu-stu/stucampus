#-*- coding: utf-8
from django.http import HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import (user_passes_test,
                                            permission_required)

from stucampus.infor.models import Infor
from stucampus.organization.models import Organization
from stucampus.organization.services import find_organization
from stucampus.master.forms import InforCreateForm, InforEditForm
from stucampus.custom.permission import admin_group_check
from stucampus.utils import spec_json, get_http_data


class ListInfor(View):

    @method_decorator(permission_required('infor.infor_list'))
    @method_decorator(user_passes_test(admin_group_check))
    def get(self, request):
        infors = Infor.objects.all()
        return render(request, 'master/infor-list.html', {'infors': infors})


class PostInfor(View):

    @method_decorator(permission_required('infor.infor_create'))
    @method_decorator(user_passes_test(admin_group_check))
    def get(self, request):
        orgs = request.user.student.orgs_as_manager.all()
        return render(request, 'master/infor-post.html', {'orgs': orgs})

    @method_decorator(permission_required('infor.infor_create'))
    @method_decorator(user_passes_test(admin_group_check))
    def post(self, request):
        form = InforCreateForm(request.POST)
        if form.is_valid():
            title = request.POST['title']
            content = request.POST['content']
            organization_id = request.POST['organization_id']
            author = request.user.student
            organization = find_organization(organization_id)
            Infor.objects.create(title=title, content=content,
                                 author=author, organization=organization)
            success = True
            messages = '发布成功'
        else:
            success = False
            messages = form.errors.values()
        return spec_json(success, messages)


class Information(View):

    @method_decorator(permission_required('infor.infor_show'))
    @method_decorator(user_passes_test(admin_group_check))
    def get(self, request, id):
        orgs = request.user.student.orgs_as_manager.all()
        infor = get_object_or_404(Infor, id=id)
        return render(request, 'master/infor-post.html',
                      {'infor': infor, 'orgs': orgs})

    @method_decorator(permission_required('infor.infor_del'))
    @method_decorator(user_passes_test(admin_group_check))
    def delete(self, request, id):
        infor = get_object_or_404(Infor, id=id)
        infor.delete()
        return spec_json(success=True, messages='删除成功')

    @method_decorator(permission_required('infor.infor_edit'))
    @method_decorator(user_passes_test(admin_group_check))
    def put(self, request, id):
        data = get_http_data(request)
        infor = get_object_or_404(Infor, id=id)
        form = InforEditForm(data)
        if form.is_valid():
            infor.title = data['title']
            infor.content = data['content']
            infor.organization_id = data['organization_id']
            infor.save()
            success = True
            messages = '修改成功'
        else:
            success = False
            messages = forms.errors.values()
        return spec_json(success, messages)
