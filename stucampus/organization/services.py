#-*- coding: utf-8
from stucampus.organization.models import Organization


def is_exist(name):
    try:
        org = Organization.objects.get(name=name)
    except Organization.DoesNotExist:
        return False
    return True
