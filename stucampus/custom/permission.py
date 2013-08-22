from django.contrib.auth.models import Group


def admin_group_check(user):
    '''Admin group check function for user_passes_test.'''
    admin_group = Group.objects.get(name='StuCampus')
    return (admin_group in user.groups.all())


def org_manage_group_check(user):
    org_manage_group = Group.objects.get(name='organization_manager')
    return (org_manage_group in user.groups.all())
    