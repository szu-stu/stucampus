#-*- coding: utf-8
import re
import datetime
import xlrd

from django import forms
from django.core.exceptions import ValidationError

from .models import Member

def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')

def szu_no_validate(value):
    if len(value)!=10:
        raise ValidationError('学号格式错误')



class MemberForm(forms.ModelForm):
    MONTHS = {
        1:u'1月', 2:u'2月', 3:u'3月', 4:u'4月',
        5:u'5月', 6:u'6月', 7:u'7月', 8:u'8月',
        9:u'9月', 10:u'10月', 11:u'11月', 12:u'12月'
    }
    name = forms.CharField(label=u"姓名",required=True,max_length=20,error_messages={'required':u'姓名不能为空'},
                            widget=forms.TextInput(attrs={'class':'form-control','placeholder':u'请输入姓名'}))
    mobile_phone_number = forms.CharField(label=u"手机号",required=True,max_length=11,validators=[mobile_validate,],error_messages={'required':u'手机号不能为空'},
                            widget=forms.NumberInput(attrs={'class':'form-control','placeholder':u'请输入手机号'}))
    szu_no = forms.CharField(label=u"学号",required=True,validators=[szu_no_validate,],error_messages={'required':u'学号不能为空'},
                            widget=forms.NumberInput(attrs={'class':'form-control','placeholder':u'请输入学号'}))

    birthday = forms.DateField(label=u"生日",required=False,widget=forms.SelectDateWidget(empty_label=("年", "月", "日"),attrs={'class':'form-control'},years=range(datetime.datetime.now().year-30,datetime.datetime.now().year-15),months = MONTHS))

    e_mail = forms.EmailField(label=u"邮箱",required=False,max_length = 30,widget = forms.EmailInput(attrs={'class':'form-control','placeholder':u'请输入邮箱'}))
    nick_name = forms.CharField(label=u"昵称",required=False,max_length = 30,widget = forms.TextInput(attrs={'class':'form-control','placeholder':u'请输入昵称'}))
    class Meta:
        model = Member
        fields = ['name','nick_name','szu_no','mobile_phone_number','birthday','e_mail']


class MemberListForm(forms.Form):
    file = forms.FileField(label='请选择xlsx文件')

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file is None:
            raise ValidationError((u'文件不能为空'))
            return file
        if  not file.name.endswith("xlsx"):
            raise ValidationError((u'只能批量处理xlsx文件'))
        try:
            data = xlrd.open_workbook(file_contents = file.read(),encoding_override="utf-8")
            table = data.sheets()[0]
            ncols = table.ncols
            if ncols < 6:
                raise ValidationError((u'文件第一行为标签，填写姓名，学号，电话号码，生日，邮箱，昵称,即文件至少六列，未知信息留空白即可'))
        except Exception, e:
            raise ValidationError((u'只能批量处理xlsx文件,你的文件格式不对'))
        finally:
            file.seek(0)
        return file
        



