#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_ as _

from stucampus.account.models import Student
from stucampus.organization.models import Organization


class OrganizationManageEditForm(forms.Form):
    phone = forms.CharField(
        label=_(u'Phone number'), max_length=11,
        error_messages={
            'required': _(u'Phone number is required.'),
            'max_length': _(u'Phone number must less than 11 digitals.')
        }
    )
    url = forms.CharField(
        label=_(u'Homepage of organization'), max_length=50, required=False,
        error_messages={
            'max_length': _(u'URL of homepage must less than 50 characters.')
        }
    )
    logo = forms.CharField(label=_(u'Logo of organization'), required=False)


class AddOrganizationForm(forms.Form):
    name = forms.CharField(
        label=_('Name of organization'), max_length=20,
        error_messages={
            'required': _(u'The name of organization is required.'),
            'max_length': _(u'URL of homepage must less than 20 characters.')
        }
    )
    phone = forms.CharField(
        label=_('Phone of organization manager'), max_length=11,
        error_messages={
            'required': _(u'Phone number is required.'),
            'max_length': _(u'Phone number must less than 11 digitals.')
        }
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Organization.objects.filter(name=name).exists():
            raise forms.ValidationError(_(u'Organization is already exists.'))
        return name


class AddOrganizationManagerForm(forms.Form):
    email = forms.EmailField(label=_(u'Email address of organization manager'),
        error_messages={'required': _(u'Email address is required.')})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            msg = _('User is not exists')
            raise forms.ValidationError(msg)
        return email
