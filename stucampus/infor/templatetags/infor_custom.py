#-*- coding: utf-8
from django import template


register = template.Library()


@register.filter(name='get_infor_status')
def get_infor_status(infor):
    if infor.is_deleted is True:
        return '已删除'
    else:
        return '正常'
