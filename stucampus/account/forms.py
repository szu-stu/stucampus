#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _lazy

from stucampus.account.models import Student


EMAIL_LABEL = _lazy(u'Email address')
PASSWORD_LABEL = _lazy(u'Password')
REPEAT_PW_LABEL = _lazy(u'Repeat password')
CURRENT_PW_LABEL = _lazy(u'Current password')
NEW_PW_LABEL = _lazy(u'New password')

EAMIL_REQUIRED = _lazy(u'Email is required.')
PASSWORD_REQUIRED = _lazy(u'Password is required.')
REPEAT_PW_REQUIRED = _lazy(u'Repeat password is required.')
NEW_PW_REQUIRED = _lazy(u'New password is required.')

PASSWORD_MIN_LENGTH_MSG = _lazy(u'Password must be 6 or more characters.')
REPEAT_PW_MIN_LENGTH_MSG = _lazy(u'Repeat password is required.')
NEW_PW_MIN_LENGTH_MSG = _lazy(u'New password must be 6 or more characters.')

PASSWORD_MUST_BE_MATCH = _lazy(u'Password must match')


class SignInForm(forms.Form):
    email = forms.EmailField(
        label=EMAIL_LABEL,
        error_messages={'required': EAMIL_REQUIRED}
    )
    password = forms.CharField(
        label=PASSWORD_LABEL,
        min_length=6,
        error_messages={'required': PASSWORD_REQUIRED,
                        'min_length': PASSWORD_MIN_LENGTH_MSG}
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if user is None:
            msg = _lazy(u'Your email or password were incorrect.')
            raise forms.ValidationError(msg)
        if not user.is_active:
            msg = _lazy(u'Your account is invalid!')
            raise forms.ValidationError(msg)
        return self.cleaned_data


class SignUpForm(forms.Form):
    email = forms.EmailField(
        label=EMAIL_LABEL,
        error_messages={'required': EAMIL_REQUIRED})
    password = forms.CharField(
        label=PASSWORD_LABEL, help_text=PASSWORD_MIN_LENGTH_MSG,
        min_length=6,
        error_messages={'required': PASSWORD_REQUIRED,
                        'min_length': PASSWORD_MIN_LENGTH_MSG})
    confirm = forms.CharField(label=REPEAT_PW_LABEL, min_length=6,
                              error_messages={
                                  'required': REPEAT_PW_REQUIRED,
                                  'min_length': REPEAT_PW_MIN_LENGTH_MSG})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            msg = _lazy(u'Email is already exists.')
            raise forms.ValidationError(msg)
        return email

    def clean_confirm(self):
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')
        if not password == confirm:
            raise forms.ValidationError(PASSWORD_MUST_BE_MATCH)
        return confirm


class ProfileEditForm(forms.Form):
    class Meta:
        model = Student
        fields = ('true_name', 'college', 'screen_name', 'is_male',
                  'student_id', 'mphone_num', 'mphone_short_num', 'szucard',
                  'birthday')


class PasswordForm(forms.Form):
    current_email = forms.EmailField(label=EMAIL_LABEL, required=False))
    current_password = forms.CharField(
        label=CURRENT_PW_LABEL, min_length=6,
        error_messages={'required': PASSWORD_REQUIRED,
                        'min_length': PASSWORD_MIN_LENGTH_MSG})
    new_password = forms.CharField(label=NEW_PW_LABEL, min_length=6,
                                   error_messages={
                                       'required': NEW_PW_REQUIRED,
                                       'min_length': NEW_PW_MIN_LENGTH_MSG})
    confirm = forms.CharField(label=REPEAT_PW_REQUIRED, min_length=6,
                              error_messages={
                                  'required': REPEAT_PW_REQUIRED,
                                  'min_length': REPEAT_PW_MIN_LENGTH_MSG})

    def clean_current_password(self):
        email = self.cleaned_data.get('current_email')
        password = self.cleaned_data.get('current_password')
        user = authenticate(username=email, password=password)
        if user is None:
            msg = _lazy(u'Current password is invalid.')
            raise forms.ValidationError(msg)
        return password

    def clean_confirm(self):
        password = self.cleaned_data.get('new_password')
        confirm = self.cleaned_data.get('confirm')
        if not password == confirm:
            raise forms.ValidationError(PASSWORD_MUST_BE_MATCH)
        return confirm


class AccountBanForm(forms.Form):
    ban = forms.BooleanField()

    def clean_ban(self):
        ban = self.cleaned_data.get('ban')
        if not ban:
            msg = _lazy(u'Data is invalid.')
            raise forms.ValidationError(msg)
        return ban
