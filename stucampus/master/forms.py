#-*- coding: utf-8
from django import forms as d_forms
from django.contrib.auth.models import User

from stucampus.custom import forms
from stucampus.organization.models import Organization


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


class InforCreateForm(d_forms.Form):
    title = forms.CharField(max_length=50,
                            error_messages={'required': '请输入标题',
                                            'max_length': 50})
    organization_id = forms.IntegerField(
        error_messages={'required': '请选择发布组织'})
    content = forms.CharField(error_messages={'required': '请填写正文'})


class InforEditForm(d_forms.Form):
    title = forms.CharField(max_length=50,
                            error_messages={'required': '请输入标题',
                                            'max_length': 50})
    organization_id = forms.IntegerField(
        error_messages={'required': '请选择发布组织'})
    content = forms.CharField(error_messages={'required': '请填写正文'})


class AccountBanForm(d_forms.Form):
    ban = forms.BooleanField(error_messages={'required': '数据出错！'})

    def clean_ban(self):
        ban = self.cleaned_data.get('ban')
        if not ban:
            raise d_forms.ValidationError('参数出错！')
        return ban
