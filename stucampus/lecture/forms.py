from django.forms import ModelForm
from django.forms.models import modelformset_factory

from stucampus.lecture.models import LectureMessage


class LectureForm(ModelForm):
    class Meta:
        model = LectureMessage


LecureFormSet = modelformset_factory(LectureMessage,
                                     form=LectureForm, extra=0)


def get_formset():
    return LecureFormSet(queryset=LectureMessage.get_messages_this_week())
