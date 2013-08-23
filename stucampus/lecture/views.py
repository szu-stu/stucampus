from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext

from stucampus.lecture.models import LectureMessage
from stucampus.spider.models import Announcement
from stucampus.lecture.forms import LectureForm, LecureFormSet, get_formset


def index(request):
    table = LectureMessage.generate_messages_table()
    return render_to_response('lecture/index.html', {'table': table})

def manage(request):
    formset = get_formset()
    return render_to_response('lecture/manage.html', {'formset': formset},
                              context_instance=RequestContext(request))

def submit(request):
    formset = LecureFormSet(request.POST)
    for form in formset:
        if form.is_valid():
            model = form.save(commit=False)
            model.url_id = model.url_id_backup
            model.save()
    return HttpResponseRedirect(reverse('lecture:manage'))

def add_new(request):
    form = LectureForm()
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.url_id_backup = model.url_id
            model.save()
            return HttpResponseRedirect(reverse('lecture:manage'))
    return render(request, 'lecture/add_new.html', {'form': form})

def update(request):
    LectureMessage.get_message_from_announcement()
    return HttpResponseRedirect(reverse('lecture:manage'))
