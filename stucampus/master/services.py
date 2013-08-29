from django.contrib.auth.models import Group


def find_group(id):
    try:
        group = Group.objects.get(id=id)
    except Group.DoesNotExist:
        group = None
    return group


def get_group_by_name(name):
    try:
        group = Group.objects.get(name=name)
    except Group.DoesNotExist:
        group = None
    return group
