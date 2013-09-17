from django.forms import forms, ModelForm
from django.forms.models import modelformset_factory
from django.core.paginator import Paginator, InvalidPage

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

    def get_formset_on_page(self, page_num):
        try:
            page = self.page(page_num)
        except InvalidPage:
            page = self.page(1)
        query = self.model_class.objects.filter(
            id__in=[k.id for k in page])
        return self.Formset(queryset=query)
