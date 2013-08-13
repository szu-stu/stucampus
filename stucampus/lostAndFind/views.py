from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import Context

from stucampus.lostAndFind.models import Message, MessageForm

class IndexView(generic.ListView):
    template_name  = 'lostAndFind/index.html'
    context_object_name = 'message_list'
    model = Message

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context

def add_message(request):
    form = MessageForm()
    if request.method == 'POST' :
        form = MessageForm( request.POST )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( reverse('lostAndFind:index') )
    return render(request, 'lostAndFind/add_message.html', {'form':form})
