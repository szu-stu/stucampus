#-*- coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _lazy

from stucampus.infor.models import Infor


TITLE_LABEL = _lazy(u'Title')
ORGANIZATION_LABEL = _lazy(u'Organization')
CONTENT_LABEL = _lazy(u'Content')

TITLE_REQUIRED = _lazy(u'Title is required.')
ORGANIZATION_REQUIRED = _lazy(u'Select an organization.')
CONTENT_REQUIRED = _lazy(u'Content is required.')

TITLE_MAX_LENGTH_MSG = _lazy(u'Title must less than 50 characters.')


class InforPostForm(forms.Form):

    title = forms.CharField(
        label=TITLE_LABEL, max_length=50,
        error_messages={'required': TITLE_REQUIRED,
                        'max_length': TITLE_MAX_LENGTH_MSG})
    organization = forms.ModelChoiceField(
        label=ORGANIZATION_LABEL, queryset=None,
        error_messages={'required': ORGANIZATION_REQUIRED})
    content = forms.CharField(error_messages={'required': CONTENT_REQUIRED})

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(InforPostForm, self).__init__(*args, **kwargs)
        orgs_query_set = user.student.orgs_as_manager.all()
        self.fields['organization'].queryset = orgs_query_set


class InforEditForm(forms.ModelForm):
    title = forms.CharField(label=TITLE_LABEL, max_length=50,
        error_messages={'required': TITLE_REQUIRED,
                        'max_length': TITLE_MAX_LENGTH_MSG})
    organization = forms.ModelChoiceField(
        label=ORGANIZATION_LABEL, queryset=None,
        error_messages={'required': ORGANIZATION_REQUIRED})
    content = forms.CharField(label=CONTENT_LABEL,
                              error_messages={'required': CONTENT_REQUIRED})

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(InforEditForm, self).__init__(*args, **kwargs)
        orgs_query_set = user.student.orgs_as_manager.all()
        self.fields['organization'].queryset = orgs_query_set

    class Meta:
        model = Infor
        fields = ('title', 'organization', 'content')
