#-*- coding: UTF-8 -*-   
from django import forms
from .models import Register

import re

class Register_Form(forms.ModelForm):
    email = forms.CharField(label=u"邮箱",required=True,error_messages={'required':u'邮箱不能为空'},
                            )
    mobile = forms.CharField(label=u"手机",required=True,error_messages={'required':u'手机号码不能为空'})
    self_intro = forms.CharField(label=u"自我介绍",required=False,max_length=500,error_messages={'max_length':u'自我介绍不能超过五百字'})
    class Meta:
        model = Register
        fields = ['name','gender','stu_ID','grade','college','mobile','dept1','dept2','email','self_intro']
    def clean_dept1(self):
        dept1=self.cleaned_data.get("dept1")
        if dept1==u"--":
            raise forms.ValidationError((u'第一志愿部门必填'))
        return dept1
    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        p2=re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        if p2.match(mobile):
            return mobile
        raise forms.ValidationError((u'手机号码格式有误'))

    	
