from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import Context

from stucampus.lost_and_found.models import Message, MessageForm


class IndexView(generic.ListView):

    template_name = 'lost_and_found/index.html'
    context_object_name = 'message_list'

    def get_queryset(self):
        return Message.objects.order_by('published_date').reverse()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


def add_message(request):
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('lost_and_found:index'))
    return render(request, 'lost_and_found/add_message.html', {'form': form})
