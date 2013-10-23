# -*- coding:utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.core.paginator import InvalidPage

from stucampus.activity.models import ActivityMessage
from stucampus.activity.forms import ActivityMessageForm, FormsetPaginator
from stucampus.activity.forms import ActivityMessageFormSet
from stucampus.utils import spec_json


def index(request):
    table = ActivityMessage.generate_messages_table()
    return render_to_response('activity/home.html', {'table': table})


def add_activity(request):
    form = ActivityMessageForm()
    if request.method == 'POST':
        form = ActivityMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return spec_json('success', '讲座信息添加成功')
        else:
            return spec_json('errors', form.errors)
    return render(request, 'activity/add_activity.html', {'form': form})


def manage(request):
    if request.method == 'POST':
        return submit(request)

    paginator = FormsetPaginator(ActivityMessage, 
                                 ActivityMessage.objects.all(), 5)
    try:
        page = paginator.page(request.GET.get('page'))
    except InvalidPage:
        page = paginator.page(1)
    return render(request, 'activity/manage.html', {'page': page})


def submit(request):
    formset = ActivityMessageFormSet(request.POST)
    for form in formset:
        if form.is_valid():
            form.save()

    queryset = ActivityMessage.objects.all()
    paginator = FormsetPaginator(ActivityMessage, queryset, 5)
    page = paginator.page(request.GET.get('page'))
    page.formset = formset
    return render(request, 'activity/manage.html', {'page': page})
