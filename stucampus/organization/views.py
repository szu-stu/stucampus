from django.views.generic import View
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, permission_required

from stucampus.custom.permission import org_manage_group_check
from stucampus.organization.models import Organization
from stucampus.organization.forms import OrganizationManageEditForm
from stucampus.utils import spec_json
from stucampus.account.permission import check_perms


def organization(request):
    organizations = request.user.student.orgs_as_manager.all()
    return render(request, 'organization/list.html',
                  {'organizations': organizations})


@check_perms('organization.organization_manager')
def organization_manage(request):
    return render(request, 'organization/list.html',
                  {'organizations': Organization.objects.all()})


class EditOrganization(View):

    def get(self, request, id):
        organization = get_object_or_404(Organization, id=id)
        return render(request, 'organization/edit.html',
                      {'organization': organization})

    def post(self, request, id):
        # TODO: be RESTful
        form = OrganizationManageEditForm(request.POST)
        if not form.is_valid():
            messages = form.errors.values()
            return spec_json(status='errors', messages=messages)

        org = get_object_or_404(Organization, id=id)
        org.url = request.POST['url']
        org.phone = request.POST['phone']
        org.logo = request.POST['logo']
        org.save()
        return spec_json(status='success')
