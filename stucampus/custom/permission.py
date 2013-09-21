from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth import REDIRECT_FIELD_NAME


def guest_or_redirect(function=None):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated(),
        login_url='/',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def admin_group_check(user):
    '''Admin group check function for user_passes_test.'''
    try:
        admin_group = Group.objects.get(name='StuCampus')
    except Group.DoesNotExist:
        return False
    return (admin_group in user.groups.all())


def org_manage_group_check(user):
    try:
        org_manage_group = Group.objects.get(name='organization_manager')
    except Group.DoesNotExist:
        return False
    return (org_manage_group in user.groups.all())
