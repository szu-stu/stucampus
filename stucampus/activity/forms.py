from django.forms import forms, ModelForm
from django.forms.models import modelformset_factory
from django.core.paginator import Paginator

from stucampus.activity.models import ActivityMessage


class ActivityMessageForm(ModelForm):
    class Meta:
        model = ActivityMessage


ActivityMessageFormSet = modelformset_factory(ActivityMessage, extra=0)


class FormsetPaginator(Paginator):

    def __init__(self, model_class, object_list, per_page, orphans=0,
                 allow_empty_first_page=True):
        self.model_class = model_class
        self.Formset = modelformset_factory(model_class, extra=0) 
        super(FormsetPaginator, self).__init__(
            object_list, per_page, orphans=0, allow_empty_first_page=True)

    def page(self, page_num):
        page = super(FormsetPaginator, self).page(page_num)
        query = self.model_class.objects.filter(
            id__in=[k.id for k in page])
        page.formset = self.Formset(queryset=query)
        return page
