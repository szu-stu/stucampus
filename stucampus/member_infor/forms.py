#-*- coding: utf-8
from django import forms

from .models import Member

class MemberForm(forms.ModelForm):
	class Meta:
		model = Member
		fields = ['name','mobile_phone_number','szu_no']


class MemberListForm(forms.Form):
	file = forms.FileField(label='请选择xlsx文件')

	def clean_file(self):
		file = self.cleaned_data.get('file')
		if  not file.name.endswith("xlsx"):
			raise forms.ValidationError((u'只能批量处理xlsx文件'))
		return file


