#-*- coding: utf-8 -*-
from django import forms as d_forms

from stucampus.custom import forms


class SignInForm(d_forms.Form):
    email = forms.EmailField(label='邮箱')
    password = forms.CharField(label='密码',
                               error_messages={'required': '密码不能为空'})


class SignUpForm(d_forms.Form):
    email = forms.EmailField(label='邮箱',
                             help_text='常用的邮箱，作为登录用户名')
    password = forms.CharField(label='密码', help_text='最少 6 位')
    confirm = forms.CharField(label='密码确认', help_text='再输入一次密码')