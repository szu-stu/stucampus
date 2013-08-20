from django import template

from stucampus.custom.permission import admin_group_check


register = template.Library()


@register.filter(name='is_admin')
def is_admin(user):
    return admin_group_check(user)
