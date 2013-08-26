from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse

from stucampus.activity.models import ActivityMessage
from stucampus.activity.forms import ActivityMessageForm, get_formset
from stucampus.activity.forms import ActivityMessageFormSet


def index(request):
    activities = ActivityMessage.get_activity_list()
    return render_to_response('activity/index.html',
                              {'activities': activities})


def add_message(request):
    form = ActivityMessageForm()
    if request.method == 'POST':
        form = ActivityMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('activity:index'))
    return render(request, 'activity/add_message.html', {'form': form})


def manage(request):
    formset = get_formset()
    return render(request, 'activity/manage.html', {'formset': formset})


def submit(request):
    formset = ActivityMessageFormSet(request.POST)
    for form in formset:
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(reverse('activity:manage'))
