from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage

from stucampus.lecture.models import LectureMessage
from stucampus.lecture.forms import LectureForm, LecureFormSet


def index(request):
    table = LectureMessage.generate_messages_table()
    return render_to_response('lecture/index.html', {'table': table})


def manage(request):
    formset = LecureFormSet(queryset=LectureMessage.get_messages_this_week())
    return render(request, 'lecture/manage.html', {'formset': formset})

def manage_all(request):
    formset = LecureFormSet()
    paginator = Paginator(formset, 2)
    page_num = request.GET.get('page')
    try:
        current_page = paginator.page(page_num)
    except InvalidPage:
        current_page = paginator.page(1)
    return render(request, 'lecture/manage_all.html', {'page': current_page})


def submit(request):
    formset = LecureFormSet(request.POST)
    for form in formset:
        if form.is_valid():
            lecture_message = form.save(commit=False)
            lecture_message.url_id = lecture_message.url_id_backup
            lecture_message.save()
    return HttpResponseRedirect(reverse('lecture:manage'))


def add_lecture(request):
    form = LectureForm()
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            lecture_message = form.save(commit=False)
            lecture_message.url_id_backup = lecture_message.url_id
            lecture_message.save()
            return HttpResponseRedirect(reverse('lecture:manage'))
    return render(request, 'lecture/add_lecture.html', {'form': form})


# just used for debug
def update(request):
    num = LectureMessage.add_new_lecture_from_notification()
    return HttpResponse(num)


# just used for debug
def delete(request):
    LectureMessage.objects.all().delete()
    return HttpResponseRedirect(reverse('lecture:manage'))
