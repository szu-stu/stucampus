from django.contrib.auth.models import Group


def admin_group_check(user):
    '''Admin group check function for user_passes_test.'''
    admin_group = Group.objects.get(name='StuCampus')
    return (admin_group in user.groups.all())
