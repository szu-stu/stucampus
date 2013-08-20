#-*- coding: utf-8
from django import forms as d_forms

from stucampus.custom import forms


class AddOrganizationForm(d_forms.Form):
    name = forms.CharField(max_length=20,
                           error_messages={
                               'required': '组织名称不能为空',
                               'max_length': '组织名称不能超过20个字'})
    phone = forms.CharField(max_length=11,
                            error_messages={
                                'required': '联系电话不能为空',
                                'max_length': '联系电话不能大于11个字符'})


class AddOrganizationManagerForm(d_forms.Form):
    email = forms.EmailField(error_messages={'required': '请输入邮箱'})
