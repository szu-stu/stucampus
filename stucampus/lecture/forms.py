from django import forms
from django.forms.models import modelformset_factory
from django.forms.extras.widgets import SelectDateWidget

from stucampus.lecture.models import LectureMessage


class LectureForm(forms.ModelForm):
    class Meta:
        model = LectureMessage
        widgets = {'date': SelectDateWidget()}


LectureFormset = modelformset_factory(LectureMessage,
                                      form=LectureForm,
                                      can_delete=True,
                                      extra=1)
