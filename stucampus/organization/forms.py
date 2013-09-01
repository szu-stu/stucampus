#-*- coding: utf-8 -*-
from django import forms as d_forms
from django.contrib.auth.models import User

from stucampus.custom import forms
from stucampus.account.models import Student
from stucampus.organization.models import Organization


class OrganizationManageEditForm(d_forms.Form):
    phone = forms.CharField(label='联系电话', required=False,
                            error_messages={'required': '请输入联系电话'})
    url = forms.CharField(label='官方主页', max_length=50, required=False,
                          error_messages={'required': '密码不能为空'})
    logo = forms.CharField(label='Logo', required=False,
                           error_messages={'required': 'Logo不能为空'})


class AddOrganizationForm(d_forms.Form):
    name = forms.CharField(max_length=20,
                           error_messages={
                               'required': '组织名称不能为空',
                               'max_length': '组织名称不能超过20个字'})
    phone = forms.CharField(max_length=11,
                            error_messages={
                                'required': '联系电话不能为空',
                                'max_length': '联系电话不能大于11个字符'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        count = Organization.objects.filter(name=name).count()
        if count > 0:
            raise d_forms.ValidationError('该组织已存在')
        return name


class AddOrganizationManagerForm(d_forms.Form):
    email = forms.EmailField(error_messages={'required': '请输入邮箱'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        count = User.objects.filter(username=email).count()
        if count <= 0:
            raise d_forms.ValidationError('该用户不存在')
        return email
