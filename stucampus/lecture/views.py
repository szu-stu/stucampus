from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.views import generic

from stucampus.lecture.models import LectureMessage
from stucampus.spider.models import Announcement


def index(request):
    return render_to_response('lecture/index.html',
                              {'table': LectureMessage.generate_messages_table()})

def manage(request):
    message = LectureMessage.get_unchecked_message()
    return render_to_response('lecture/manage.html', {'msg': message})

def update(request):
    LectureMessage.get_message_from_announcement()
    return HttpResponseRedirect(reverse('lecture:manage'))
