#-*- coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _lazy


TITLE_LABEL = _lazy(u'Title')

TITLE_REQUIRED = _lazy(u'Title is required.')
ORGANIZATION_REQUIRED = _lazy(u'Select an organization.')
CONTENT_REQUIRED = _lazy(u'Content is required.')

TITLE_MAX_LENGTH_MSG = _lazy(u'Title must less than 50 characters.')


class InforPostForm(forms.Form):
    title = forms.CharField(
        label=TITLE_LABEL, max_length=50,
        error_messages={'required': TITLE_REQUIRED,
                        'max_length': TITLE_MAX_LENGTH_MSG})
    organization_id = forms.IntegerField(
        error_messages={'required': ORGANIZATION_REQUIRED})
    content = forms.CharField(error_messages={'required': CONTENT_REQUIRED})


class InforEditForm(forms.Form):
    title = forms.CharField(
        max_length=50,
        error_messages={'required': TITLE_REQUIRED,
                        'max_length': TITLE_MAX_LENGTH_MSG})
    organization_id = forms.IntegerField(
        error_messages={'required': ORGANIZATION_REQUIRED})
    content = forms.CharField(error_messages={'required': CONTENT_REQUIRED})
