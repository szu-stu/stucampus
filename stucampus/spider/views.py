from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic

from stucampus.spider.models import Announcement


class AnnouncementList(generic.ListView):
    template_name = 'spider/index.html'
    context_object_name = 'announcement_list'
    model = Announcement


def update(request):
    num_of_update = Announcement.update_announcements()
    return HttpResponse(str(num_of_update))
    #return HttpResponseRedirect(reverse('spider:index'))
