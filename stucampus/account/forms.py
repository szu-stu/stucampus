#-*- coding: utf-8 -*-
from django import forms as d_forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from stucampus.account.models import Student
from stucampus.custom import forms


class SignInForm(d_forms.Form):
    email = forms.EmailField(label='邮箱',
                             error_messages={'required': '请输入邮箱'})
    password = forms.CharField(label='密码', min_length=6,
                               error_messages={'required': '密码不能为空',
                                               'min_length': '密码最少6位'})

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if user is None:
            raise d_forms.ValidationError('邮箱或密码错误')

        if not user.is_active:
            raise d_forms.ValidationError('该帐号失效！')

        return self.cleaned_data


class SignUpForm(d_forms.Form):
    email = forms.EmailField(label='邮箱',
                             error_messages={'required': '请输入邮箱'},
                             help_text='常用的邮箱，作为登录用户名')
    password = forms.CharField(label='密码', help_text='最少 6 位',
                               min_length=6,
                               error_messages={'required': '密码不能为空',
                                               'min_length': '密码最少6位'})
    confirm = forms.CharField(label='密码确认', min_length=6,
                              error_messages={
                                  'required': '确认密码不能为空',
                                  'min_length': '确认密码最少6位'},
                              help_text='再输入一次密码')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
            raise d_forms.ValidationError('邮箱已存在')
        return email


    def clean_confirm(self):
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')
        if not confirm:
            raise d_forms.ValidationError('确认密码不能为空')
        if not password == confirm:
            raise d_forms.ValidationError('确认密码不匹配')
        return confirm


class ProfileEditForm(d_forms.Form):
    true_name = forms.CharField(label='真实姓名', required=False)
    college = forms.CharField(label='学院', required=False)
    screen_name = forms.CharField(label='昵称',
                                  error_messages={'required': '昵称不能为空'})
    is_male = forms.ChoiceField(label='性别',
                                choices=((True, '男'), (False, '女')),
                                error_messages={'required': '性别不能为空'})
    student_id = forms.CharField(label='学号', max_length=10, required=False)
    birthday = forms.DateTimeField(label='生日', required=False)
    mphone_num = forms.CharField(label='手机长号',
                                 max_length=11, required=False)
    mphone_short_num = forms.CharField(label='手机短号',
                                       max_length=6, required=False)
    szucard = forms.CharField(label='校园卡号', max_length=6, required=False)


class PasswordForm(d_forms.Form):
    current_email = forms.EmailField(label='邮箱', required=False)
    current_password = forms.CharField(label='当前密码', min_length=6,
                                       error_messages={
                                           'required': '当前密码不能为空',
                                           'min_length': '密码最少6位'})
    new_password = forms.CharField(label='新密码', min_length=6,
                                   error_messages={
                                       'required': '新密码不能为空',
                                       'min_length': '新密码最少6位'})
    confirm = forms.CharField(label='密码确认', min_length=6,
                              error_messages={
                                  'required': '确认密码不能为空',
                                  'min_length': '确认密码最少6位'})

    def clean_current_password(self):
        email = self.cleaned_data.get('current_email')
        password = self.cleaned_data.get('current_password')
        user = authenticate(username=email, password=password)
        if user is None:
            raise d_forms.ValidationError('当前密码错误')
        return password

    def clean_confirm(self):
        password = self.cleaned_data.get('new_password')
        confirm = self.cleaned_data.get('confirm')
        if not confirm:
            raise d_forms.ValidationError('确认密码不能为空')
        if not password == confirm:
            raise d_forms.ValidationError('确认密码不匹配')
        return confirm
