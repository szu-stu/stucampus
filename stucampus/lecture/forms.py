from django.forms import ModelForm, HiddenInput
from django.forms.models import modelformset_factory

from stucampus.lecture.models import LectureMessage



LecureFormSet = modelformset_factory(LectureMessage, extra=0)
def get_formset():
    return LecureFormSet(queryset=LectureMessage.get_messages_this_week())

