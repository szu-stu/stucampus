from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from stucampus.spider.models import Announcement


def index(request):
    messages = Announcement.objects.order_by('published_date').reverse()
    paginator = Paginator(messages, 30)
    page_num = request.GET.get('page')
    try:
        current_page = paginator.page(page_num)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    return render(request, 'spider/index.html', {'page': current_page})


def update(request):
    num_of_update = Announcement.fetch_new_announcement()
    return HttpResponse(str(num_of_update))


def delete(request):
    Announcement.objects.all().delete()
    return HttpResponseRedirect(reverse('spider:index'))
