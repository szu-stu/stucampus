#-*- coding: utf-8 -*-
from django import forms as d_forms

from stucampus.account.models import Student
from stucampus.custom import forms


class OrganizationManageEditForm(d_forms.Form):
    phone = forms.CharField(label='联系电话', required=False,
                            error_messages={'required': '请输入联系电话'})
    url = forms.CharField(label='官方主页', max_length=50, required=False,
                          error_messages={'required': '密码不能为空'})
    logo = forms.CharField(label='Logo', required=False,
                           error_messages={'required': 'Logo不能为空'})
