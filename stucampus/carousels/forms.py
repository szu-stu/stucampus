#-*- coding: utf-8
from django import forms

from stucampus.carousels.models import Slide


class SlideForm(forms.ModelForm):
    class Meta:
        model = Slide
        exclude = ['published', 'modifier', 
        		   'author', 'lastModify', 'deleted']
        widgets = {
            'describe' : forms.Textarea(),
        }