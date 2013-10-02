from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.core.paginator import InvalidPage

from stucampus.activity.models import ActivityMessage
from stucampus.activity.forms import ActivityMessageForm, FormsetPaginator
from stucampus.activity.forms import ActivityMessageFormSet
from stucampus.utils import spec_json


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
            return spec_json('success', 'add success')
        else:
            return spec_json('errors', form.errors)
    return render(request, 'activity/add_activity.html', {'form': form})


def manage(request, page_num='1'):
    paginator = FormsetPaginator(ActivityMessage,
                                 ActivityMessage.objects.all(), 2)
    try:
        page = paginator.page(int(page_num))
    except InvalidPage:
        page = paginator.page(1)
    return render(request, 'activity/manage.html', {'page': page})


def submit(request):
    formset = ActivityMessageFormSet(request.POST)
    for form in formset:
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(reverse('activity:manage'))
