#-*- coding: utf-8
from stucampus.organization.models import Organization


def is_org_exist(name):
    try:
        org = Organization.objects.get(name=name)
    except Organization.DoesNotExist:
        return False
    return True


def find_organization(id):
    try:
        org = Organization.objects.get(id=id)
    except Organization.DoesNotExist:
        return None
    return org
