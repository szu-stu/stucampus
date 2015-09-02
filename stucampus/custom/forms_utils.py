from django.forms.models import modelformset_factory
from django.core.paginator import Paginator


class FormsetPaginator(Paginator):
    ''' formset will be automatically sorted in descending order '''

    def __init__(self, model_class, object_list, per_page,
            formset,
            orphans=0, allow_empty_first_page=True):
        ''' object_list must be QuerySet '''
        self.model_class = model_class
        self.Formset = formset
        object_list = object_list.order_by('-pk')
        super(FormsetPaginator, self).__init__(
            object_list, per_page, orphans=0, allow_empty_first_page=True)

    def page(self, page_num):
        page = super(FormsetPaginator, self).page(page_num)
        query = self.model_class.objects.order_by('-pk').filter(
            id__in=[k.id for k in page])
        page.formset = self.Formset(queryset=query)
        return page

