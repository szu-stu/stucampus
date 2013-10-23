from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext
from django.core.paginator import InvalidPage

from stucampus.utils import spec_json
from stucampus.lecture.models import LectureMessage
from stucampus.lecture.forms import LectureForm, LectureFormset
from stucampus.activity.forms import FormsetPaginator


def index(request):
    table = LectureMessage.generate_messages_table()
    return render_to_response('lecture/home.html', {'table': table})


def manage(request):
    if request.method == 'POST':
        return submit(request)

    paginator = FormsetPaginator(LectureMessage,
                                 LectureMessage.objects.all(), 5)
    try:
        page = paginator.page(request.GET.get('page'))
    except InvalidPage:
        page = paginator.page(1)
    return render(request, 'lecture/manage.html', {'page': page})


def submit(request):
    formset = LectureFormset(request.POST)
    for form in formset:
        if form.is_valid():
            form.save()

    queryset = LectureMessage.objects.all()
    paginator = FormsetPaginator(LectureMessage, queryset, 5)
    page = paginator.page(request.GET.get('page'))
    page.formset = formset
    return render(request, 'lecture/manage.html', {'page': page})


def add_lecture(request):
    form = LectureForm()
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            form.save()
            return spec_json('success', 'add success');
        else:
            return spec_json('errors', form.errors)
    return render(request, 'lecture/add_lecture.html', {'form': form})
