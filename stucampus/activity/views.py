from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage

from stucampus.activity.models import ActivityMessage
from stucampus.activity.forms import ActivityMessageForm, FormsetPaginator
from stucampus.activity.forms import ActivityMessageFormSet


def index(request):
    activities = ActivityMessage.get_activity_list()
    return render_to_response('activity/index.html',
                              {'activities': activities})


def add_activity(request):
    form = ActivityMessageForm()
    if request.method == 'POST':
        form = ActivityMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('activity:manage'))
    return render(request, 'activity/add_activity.html', {'form': form})


def manage(request):
    paginator = FormsetPaginator(ActivityMessage,
                                 ActivityMessage.objects.all(), 2)
    formset = paginator.get_formset_on_page(1)
    return render(request, 'activity/manage.html', {'formset': formset})


def submit(request):
    formset = ActivityMessageFormSet(request.POST)
    for form in formset:
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(reverse('activity:manage'))
