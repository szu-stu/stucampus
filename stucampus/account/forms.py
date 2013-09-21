#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from stucampus.account.models import Student


class SignInForm(forms.Form):
    email = forms.EmailField(
        label=_(u'Email address'),
        error_messages={'required': _(u'Email is required.')}
    )
    password = forms.CharField(
        label=_(u'Password'), min_length=6,
        error_messages={
            'required': _(u'Password is required.'),
            'min_length': _(u'Password must be 6 or more characters.')
        }
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        self.user = authenticate(username=email, password=password)
        if self.user is None:
            msg = _(u'Your email or password were incorrect.')
            raise forms.ValidationError(msg)
        if not self.user.is_active:
            msg = _(u'Your account is invalid!')
            raise forms.ValidationError(msg)
        return self.cleaned_data

    def get_user(self):
        return self.user


class SignUpForm(forms.Form):
    email = forms.EmailField(
        label=_(u'Email address'),
        error_messages={'required': _(u'Email is required.')}
    )
    password = forms.CharField(
        label=_(u'Password'), min_length=6,
        help_text=_(u'Password must be 6 or more characters.'),
        error_messages={
            'required': _(u'Password is required.'),
            'min_length': _(u'Password must be 6 or more characters.')
        }
    )
    confirm = forms.CharField(
        label=_(u'Repeat password'), min_length=6,
        error_messages={
            'required': _(u'Repeat password is required.'),
            'min_length': _(u'Repeat password is required.')
        }
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            msg = _(u'Email is already exists.')
            raise forms.ValidationError(msg)
        return email

    def clean_confirm(self):
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')
        if not password == confirm:
            raise forms.ValidationError(_(u'Password must match'))
        return confirm


class ProfileEditForm(forms.ModelForm):
    true_name = forms.CharField(max_length=20, required=False)
    college = forms.ChoiceField(choices=Student.COLLEGE_CHOICES)
    screen_name = forms.CharField(max_length=20, required=False)
    gender = forms.ChoiceField(choices=(("M", u'男'), ("F", u'女')))
    birthday = forms.DateTimeField(required=False)
    mobile_phone_number = forms.CharField(max_length=11, required=False)
    internal_phone_number = forms.CharField(max_length=6, required=False)
    job_id = forms.CharField(max_length=10, required=False)
    card_id = forms.CharField(max_length=6, required=False)
    class Meta:
        model = Student
        fields = ('true_name', 'college', 'screen_name', 'gender', 'birthday',
                  'job_id', 'mobile_phone_number', 'internal_phone_number',
                  'card_id')


class PasswordForm(forms.Form):
    current_email = forms.EmailField(label=_(u'Email address'), required=False)
    current_password = forms.CharField(
        label=_(u'Current password'), min_length=6,
        error_messages={
            'required': _(u'Password is required.'),
            'min_length': _(u'Password must be 6 or more characters.')
        }
    )
    new_password = forms.CharField(
        label=_(u'New password'), min_length=6,
        error_messages={
            'required': _(u'New password is required.'),
            'min_length': _(u'New password must be 6 or more characters.')
        }
    )
    confirm = forms.CharField(
        label=_(u'Repeat password is required.'), min_length=6,
        error_messages={
            'required': _(u'Repeat password is required.'),
            'min_length': _(u'Repeat password is required.')
        }
    )

    def clean_current_password(self):
        email = self.cleaned_data.get('current_email')
        password = self.cleaned_data.get('current_password')
        user = authenticate(username=email, password=password)
        if user is None:
            msg = _(u'Current password is invalid.')
            raise forms.ValidationError(msg)
        return password

    def clean_confirm(self):
        password = self.cleaned_data.get('new_password')
        confirm = self.cleaned_data.get('confirm')
        if not password == confirm:
            raise forms.ValidationError(_(u'Password must match'))
        return confirm


class AccountBanForm(forms.Form):
    ban = forms.BooleanField()

    def clean_ban(self):
        ban = self.cleaned_data.get('ban')
        if not ban:
            msg = _(u'Data is invalid.')
            raise forms.ValidationError(msg)
        return ban
