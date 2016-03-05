#-*- coding: utf-8
from django import forms
from django.forms.models import modelformset_factory

from stucampus.magazine.models import Magazine


class MagazineForm(forms.ModelForm):
    NAME_CHOICE = (
            (u'深大青年', u'深大青年'),
            (u'浪淘沙', u'浪淘沙'),
            )
    name = forms.ChoiceField(choices=NAME_CHOICE)
    class Meta:
        model = Magazine
        fields=['name','title','issue','summary','pdf_file']

    
    
    
     

    
    

    def clean(self):
        if 'issue' not in self.cleaned_data or \
           'name' not in self.cleaned_data or \
           'pdf_file' not in self.cleaned_data:
            return super(MagazineForm, self).clean()

        # 用于检查是否存在相同的期数，
        # 但当表单用于修改已经存在的model时，
        # 所修改的model会与自身的期数重复，所以要排除自身
        # model_id要在views里面设置
        try:
            model_id = self.model_id
        except AttributeError:
            model_id = None

        if Magazine.objects.filter(
                name=self.cleaned_data['name'],
                issue=self.cleaned_data['issue']
                ).exclude(id=model_id).exists():
            msg = u'该期数已存在'
            self._errors['issue'] = self.error_class([msg])
            del self.cleaned_data['issue']
        return self.cleaned_data

