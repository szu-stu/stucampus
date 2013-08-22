#-*- coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, permission_required

from stucampus.custom.permission import org_manage_group_check
from stucampus.organization.models import Organization
from stucampus.organization.forms import OrganizationManageEditForm
from stucampus.utils import spec_json


@login_required
def organization(request):
    return render(request, 'organization/list.html')


@user_passes_test(org_manage_group_check)
@permission_required('organization.organization_list')
def organization_manage(request):
    organzations = request.user.student.orgs_as_manager.all()
    return render(request, 'organization/list.html',
                  {'organzations': organzations})


@user_passes_test(org_manage_group_check)
@permission_required('organization.organization_edit')
def organization_edit(request, id):
    if request.method == 'GET':
        organization = get_object_or_404(Organization, id=id)
        return render(request, 'organization/edit.html',
                      {'organization': organization})
    elif request.method == 'POST':
        form = OrganizationManageEditForm(request.POST)
        if form.is_valid():
            org = get_object_or_404(Organization, id=id)
            org.url = request.POST['url']
            org.phone = request.POST['phone']
            org.logo = request.POST['logo']
            org.save()
            success = True
            messages = [u'修改成功']
        else:
            success = False
            messages = form.errors.values()
        return spec_json(success, messages)
