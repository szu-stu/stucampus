#-*- coding: utf-8
from django import forms
from django.utils.translation import ugettext_ as _

from stucampus.infor.models import Infor


class InforPostForm(forms.Form):

    title = forms.CharField(
        label=_(u'Title'), max_length=50,
        error_messages={
            'required': _(u'Title is required.'),
            'max_length': _(u'Title must less than 50 characters.')
        }
    )
    organization = forms.ModelChoiceField(
        label=_(u'Organization'), queryset=None,
        error_messages={'required': _(u'Select an organization.')}
    )
    content = forms.CharField(
        error_messages={'required': _(u'Content is required.')}
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(InforPostForm, self).__init__(*args, **kwargs)
        orgs_query_set = user.student.orgs_as_manager.all()
        self.fields['organization'].queryset = orgs_query_set


class InforEditForm(forms.ModelForm):
    title = forms.CharField(label=_(u'Title'), max_length=50,
        error_messages={
            'required': _(u'Title is required.'),
            'max_length': _(u'Title must less than 50 characters.')
        }
    )
    organization = forms.ModelChoiceField(
        label=_(u'Organization'), queryset=None,
        error_messages={'required': _(u'Select an organization.')}
    )
    content = forms.CharField(
        label=_(u'Content'),
        error_messages={'required': _(u'Content is required.')}
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(InforEditForm, self).__init__(*args, **kwargs)
        orgs_query_set = user.student.orgs_as_manager.all()
        self.fields['organization'].queryset = orgs_query_set

    class Meta:
        model = Infor
        fields = ('title', 'organization', 'content')
