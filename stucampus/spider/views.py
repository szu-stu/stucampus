from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic

from stucampus.spider.models import Announcement, SpiderManager


class AnnouncementList(generic.ListView):
    template_name = 'spider/index.html'
    context_object_name = 'announcement_list'
    model = Announcement


def update(request):
    num_of_update = Announcement.update_announcements()
    urlid = SpiderManager.get_lastest_url_id_in_db()
    if urlid != None:
        lastest_title = Announcement.objects.get(url_id=urlid)
        return HttpResponse(str(num_of_update)+lastest_title)
    else:
        return HttpResponse(str(num_of_update))
    #return HttpResponseRedirect(reverse('spider:index'))
