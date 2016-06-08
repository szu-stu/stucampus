#-*- coding: utf-8
from django import forms
from django.core.exceptions import ValidationError

from .models import User,PlanCategory,Plan



class PlanForm(forms.ModelForm):
    content = forms.CharField(label=u"计划",required=True,error_messages={'required':u'内容不能为空'},
                            widget=forms.Textarea(attrs={'class':'form-control','placeholder':u'写下你的计划吧'}))
    email = forms.EmailField(label=u"邮箱",required=True,error_messages={'required':u'email不能为空'},
                            widget=forms.EmailInput(attrs={'class':'form-control','placeholder':u'在暑假过后，我们将通过邮箱提醒您'}))
    class Meta:
        model = Plan
        fields = ['content']