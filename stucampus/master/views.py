import platform

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

from stucampus.organization.models import Organization


def index(request):
    return render(request, "index.html")


def about_us(request):
    return render(request, "aboutus.html")


def page_not_found(request):
    return render(request, "404.html")


@permission_required('master.admin_status')
def admin_redirect(request):
    return HttpResponseRedirect('/manage/status')


@permission_required('master.admin_status')
def admin_status(request):
    python_version = platform.python_version()
    domain = request.get_host()
    param = {'python_version': python_version,
             'domain': domain}
    return render(request, 'master/status.html', param)


@permission_required('master.admin_status')
def admin_organization(request):
    orgs = Organization.objects.all()
    normal_orgs = Organization.objects.filter(is_banned=False,
                                              is_deleted=False)
    baned_orgs = Organization.objects.filter(is_banned=True)
    deleted_orgs = Organization.objects.filter(is_deleted=True)
    orgs_num = len(orgs)
    normal_orgs_num = len(normal_orgs)
    baned_orgs_num = len(baned_orgs)
    deleted_orgs_num = len(deleted_orgs)
    param = {'orgs': orgs, 'normal_orgs': normal_orgs,
             'baned_orgs': baned_orgs, 'deleted_orgs': deleted_orgs,
             'orgs_num': orgs_num, 'normal_orgs_num': normal_orgs_num,
             'baned_orgs_num': baned_orgs_num,
             'deleted_orgs_num': deleted_orgs_num}
    return render(request, 'master/organization.html', param)
