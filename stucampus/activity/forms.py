from django.forms import forms, ModelForm
from django.forms.models import modelformset_factory

from stucampus.activity.models import ActivityMessage


class ActivityMessageForm(ModelForm):
    class Meta:
        model = ActivityMessage


ActivityMessageFormSet = modelformset_factory(ActivityMessage, extra=0)


def get_formset():
    return ActivityMessageFormSet(queryset=ActivityMessage.get_activity_list())
