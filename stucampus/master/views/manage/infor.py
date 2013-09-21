from django.views.generic import View
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import (user_passes_test,
                                            permission_required)

from stucampus.infor.models import Infor
from stucampus.infor.services import post_infor
from stucampus.organization.models import Organization
from stucampus.infor.forms import InforPostForm, InforEditForm
from stucampus.custom.permission import admin_group_check
from stucampus.utils import spec_json


class ListInfor(View):

    @method_decorator(permission_required('infor.infors_list'))
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
        form = InforPostForm(request.POST, user=request.user)
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='errors', messages=messages)

        post_infor(request, form.cleaned_data)
        return spec_json(status='success')


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
        return spec_json(status='success')

    @method_decorator(permission_required('infor.infor_edit'))
    @method_decorator(user_passes_test(admin_group_check))
    def put(self, request, id):
        infor = get_object_or_404(Infor, id=id)
        form = InforEditForm(request.PUT, user=request.user, instance=infor)
        if not form.is_valid():
            print form.errors
            messages = form.errors.values()
            return spec_json(status='errors', messages=messages)

        form.save()
        return spec_json(status='success')
