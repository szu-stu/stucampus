#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _lazy

from stucampus.account.models import Student
from stucampus.organization.models import Organization


EMAIL_LABEL = _lazy(u'Email address of organization manager')
PHONE_LABEL = _lazy(u'Phone number')
URL_LABEL = _lazy(u'Homepage of organization')
LOGO_LABEL = _lazy(u'Logo of organization')
ORGANIZATION_NAME_LABEL = _lazy('Name of organization')
ORGANIZATION_PHONE_LABEL = _lazy('Phone of organization manager')

EMAIL_REQUIRED = _lazy(u'Email address is required.')
PHONE_REQUIRED = _lazy(u'Phone number is required.')
ORGANIZATION_NAME_REQUIRED = _lazy(u'The name of organization is required.')

URL_MAX_LENGTH_MSG = _lazy(u'URL of homepage must less than 50 characters.')
ORGANIZATION_NAME_MAX_LENGTH_MSG = _lazy(u'URL of homepage must less than '
                                         '20 characters.')
PHONE_MAX_LENGTH_MSG = _lazy(u'Phone number must less than 11 digitals.')

ORGANIZATION_EXISTS = _lazy(u'Organization is already exists.')


class OrganizationManageEditForm(forms.Form):
    phone = forms.CharField(
        label=PHONE_LABEL, max_length=11,
        error_messages={'required': PHONE_REQUIRED,
                        'max_length': PHONE_MAX_LENGTH_MSG})
    url = forms.CharField(label=URL_LABEL, max_length=50, required=False,
                          error_messages={'max_length': URL_MAX_LENGTH})
    logo = forms.CharField(label=LOGO_LABEL, required=False)


class AddOrganizationForm(forms.Form):
    name = forms.CharField(label=ORGANIZATION_NAME_LABEL, max_length=20,
                           error_messages={
                               'required': ORGANIZATION_NAME_REQUIRED,
                               'max_length': ORGANIZATION_NAME_MAX_LENGTH_MSG})
    phone = forms.CharField(label=ORGANIZATION_PHONE_LABEL, max_length=11,
                            error_messages={
                                'required': PHONE_REQUIERD
                                'max_length': PHONE_MAX_LENGTH_MSG})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Organization.objects.filter(name=name).exists():
            raise forms.ValidationError(ORGANIZATION_EXISTS)
        return name


class AddOrganizationManagerForm(forms.Form):
    email = forms.EmailField(label=EMAIL_LABEL,
        error_messages={'required': EMAIL_REQUIRED})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            msg = _lazy('User is not exists')
            raise forms.ValidationError(msg)
        return email
