#-*- coding: utf-8 -*-
from django import forms as d_forms

from stucampus.custom import forms


class SignInForm(d_forms.Form):
    email = forms.EmailField(label='邮箱')
    password = forms.CharField(label='密码', max_length=32,
                               error_messages={'required': '密码不能为空'})