#-*- coding: UTF-8 -*-   
from django import forms

class Register_Form(forms.Form):
    DEPT = (
        ('xzb', u'行政部'),
        ('sjb', u'设计部'),
        ('jsb', u'技术部'),
        ('cbb', u'采编部'),
        ('yyb', u'运营部'),
        )

    name = forms.CharField(max_length = 20)
    gender = forms.CharField(max_length = 6)
    stu_ID = forms.IntegerField(max_value = 2015999999, min_value = 2010000000)
    college = forms.CharField(max_length = 30)
    mobile = forms.CharField(max_length = 11)
    dept1 = forms.ChoiceField(choices = DEPT)
    dept2 = forms.ChoiceField(choices = DEPT)
    self_intro = forms.CharField(widget = forms.Textarea({'max_length': 500}))
