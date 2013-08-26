from django.forms import forms
from django.forms.models import modelformset_factory

from stucampus.activity.models import ActivityMessage


class ActivityMessageForm(ModelForm):
    class Meta:
        model = ActivityMessage


ActivityMessageFormSet = modelformset_factory(ActivityMessage)


def get_formset():
    return ActivityMessageFormSet(queryset=ActivityMessage.get_activity_list)
