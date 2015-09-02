#-*- coding: utf-8
from django import forms
from django.forms.models import modelformset_factory

from stucampus.articles.models import Article, Category


class ArticleForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label=u'请选择分类')
    class Meta:
        model = Article
        exclude = ['editor', 'create_ip', 'click_count',
                   'deleted', 'important', 'publish']
        widgets = {
            'summary' : forms.Textarea(),
        }


CategoryFormset = modelformset_factory(Category, extra=1, can_delete=True)
        
