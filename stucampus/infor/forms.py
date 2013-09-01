#-*- coding: utf-8
from django import forms as d_forms

from stucampus.custom import forms


class InforPostForm(d_forms.Form):
    title = forms.CharField(max_length=50,
                            error_messages={'required': '请输入标题',
                                            'max_length': 50})
    organization_id = forms.IntegerField(
        error_messages={'required': '请选择发布组织'})
    content = forms.CharField(error_messages={'required': '请填写正文'})


class InforEditForm(d_forms.Form):
    title = forms.CharField(max_length=50,
                            error_messages={'required': '请输入标题',
                                            'max_length': 50})
    organization_id = forms.IntegerField(
        error_messages={'required': '请选择发布组织'})
    content = forms.CharField(error_messages={'required': '请填写正文'})

