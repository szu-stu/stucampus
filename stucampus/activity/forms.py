from django.forms import forms, ModelForm
from django.forms.models import modelformset_factory
from django.forms.extras.widgets import SelectDateWidget

from stucampus.activity.models import ActivityMessage


class ActivityMessageForm(ModelForm):
    class Meta:
        model = ActivityMessage
        widgets = {'date': SelectDateWidget()}
        exclude=['modified_date_time']


ActivityMessageFormSet = modelformset_factory(ActivityMessage,
                                              form=ActivityMessageForm,
                                              can_delete=True,
                                              extra=1)
