#-*- coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from stucampus.infor.models import Infor
from stucampus.organization.models import Organization
from stucampus.master.forms import InforCreateForm, InforEditForm
from stucampus.custom.permission import admin_group_check
from stucampus.utils import spec_json, get_http_data


@user_passes_test(admin_group_check)
def list(request):
    if request.method == 'GET':
        if not request.user.has_perm('infor.infor_list'):
            return HttpResponse(status=403)
        infors = Infor.objects.all()
        return render(request, 'master/infor-list.html', {'infors': infors})


@user_passes_test(admin_group_check)
def post(request):
    if request.method == 'GET':
        if not request.user.has_perm('infor.infor_create'):
            return HttpResponse(status=403)
        else:
            orgs = request.user.student.orgs_as_manager.all()
            return render(request, 'master/infor-post.html', {'orgs': orgs})
    elif request.method == 'POST':
        if not request.user.has_perm('infor.infor_create'):
            return HttpResponse(status=403)
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


@user_passes_test(admin_group_check)
def infor(request, id):
    if request.method == 'GET':
        if not request.user.has_perm('infor.infor_view'):
            return HttpResponse(status=403)
        else:
            orgs = request.user.student.orgs_as_manager.all()
            infor = get_object_or_404(Infor, id=id)
            return render(request, 'master/infor-post.html',
                          {'infor': infor, 'orgs': orgs})
    elif request.method == 'DELETE':
        if not request.user.has_perm('infor.infor_del'):
            return HttpResponse(status=403)
        else:
            infor = get_object_or_404(Infor, id=id)
            infor.delete()
            return spec_json(True, [u'删除成功'])
    elif request.method == 'PUT':
        if not request.user.has_perm('infor.infor_edit'):
            return HttpResponse(status=403)
        else:
            data = get_http_data(request)
            infor = get_object_or_404(Infor, id=id)
            form = InforEditForm(data)
            if form.is_valid():
                infor.title = data['title']
                infor.content = data['content']
                infor.organization_id = data['organization_id']
                infor.save()
                success = True
                messages = [u'修改成功']
            else:
                success = False
                messages = forms.errors.values()
            return spec_json(success, messages)
