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


class InforCreateForm(d_forms.Form):
    title = forms.CharField(max_length=50,
                            error_messages={'required': '请输入标题',
                                            'max_length': 50})
    organization_id = forms.IntegerField(error_messages={
                                             'required': '请选择发布组织'})
    content = forms.CharField(error_messages={'required': '请填写正文'})
