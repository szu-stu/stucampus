from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext

from stucampus.lecture.models import LectureMessage
from stucampus.lecture.forms import LectureForm, LecureFormSet


def index(request):
    table = LectureMessage.generate_messages_table()
    return render_to_response('lecture/index.html', {'table': table})


def manage(request):
    formset = LecureFormSet(queryset=LectureMessage.get_messages_this_week())
    return render_to_response('lecture/manage.html', {'formset': formset},
                              context_instance=RequestContext(request))

def manage_all(request):
    formset = LecureFormSet()
    return render(request, 'lecture/manage.html', {'formset': formset})


def submit(request):
    formset = LecureFormSet(request.POST)
    for form in formset:
        if form.is_valid():
            lecture_message = form.save(commit=False)
            lecture_message.url_id = lecture_message.url_id_backup
            lecture_message.save()
    return HttpResponseRedirect(reverse('lecture:manage'))


def add_new(request):
    form = LectureForm()
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            lecture_message = form.save(commit=False)
            lecture_message.url_id_backup = lecture_message.url_id
            lecture_message.save()
            return HttpResponseRedirect(reverse('lecture:manage'))
    return render(request, 'lecture/add_new.html', {'form': form})


# just used for debug
def update(request):
    LectureMessage.add_new_lecture_from_announcement()
    return HttpResponseRedirect(reverse('lecture:manage'))


# just used for debug
def delete(request):
    LectureMessage.objects.all().delete()
    return HttpResponseRedirect(reverse('lecture:manage'))
