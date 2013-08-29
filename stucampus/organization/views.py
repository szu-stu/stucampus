from django.views.generic import View
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, permission_required

from stucampus.custom.permission import org_manage_group_check
from stucampus.organization.models import Organization
from stucampus.organization.forms import OrganizationManageEditForm
from stucampus.utils import spec_json, get_http_data


@login_required
def organization(request):
    return render(request, 'organization/list.html')


@user_passes_test(org_manage_group_check)
@permission_required('organization.organization_list')
def organization_manage(request):
    organzations = request.user.student.orgs_as_manager.all()
    return render(request, 'organization/list.html',
                  {'organzations': organzations})


class EditOrganzation(View):

    @method_decorator(user_passes_test(org_manage_group_check))
    @method_decorator(permission_required('organization.organization_edit'))
    def get(self, request, id):
        organization = get_object_or_404(Organization, id=id)
        return render(request, 'organization/edit.html',
                      {'organization': organization})

    @method_decorator(user_passes_test(org_manage_group_check))
    @method_decorator(permission_required('organization.organization_edit'))
    def post(self, request, id):
        # TODO: be RESTful
        form = OrganizationManageEditForm(request.POST)
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='form_errors', messages=messages)

        org = get_object_or_404(Organization, id=id)
        org.url = request.POST['url']
        org.phone = request.POST['phone']
        org.logo = request.POST['logo']
        org.save()
        return spec_json(status='success')
