from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

from stucampus.activity.models import ActivityMessage
from stucampus.activity.forms import ActivityMessage, get_formset,\
                                     ActivityMessageFormSet

def index(request):
    activities = ActivityMessage.get_activity_list()
    return render_to_response('lecture/index.html', {'activities': activities})


def add_message(request):
    form = ActivityMessageForm()
    if request.method == 'POST':
        form = ActivityMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('activity:index'))
    return render(request, 'activity/add_message', {'form': form})


def manage(request):
    formset = get_formset()
    return render(request, 'activity/manage/', {'formset': form})


def submit(request):
    formset = ActivityMessageFormSet(request.POST)
    for form in formset:
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(reverse('lecture:manage'))
