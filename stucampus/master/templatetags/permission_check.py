from django import template

from stucampus.custom.permission import admin_group_check


register = template.Library()


@register.filter(name='is_admin')
def is_admin(user):
    return admin_group_check(user)


@register.filter(name='is_org_manage')
def is_org_manage(user):
    for group in user.groups.all():
        if group.name == 'organization_manager':
            return True
    return False