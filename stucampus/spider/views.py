from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.core.paginator import Paginator, InvalidPage

from stucampus.spider.models import Notification


def index(request):
    messages = Notification.objects.order_by('published_date').reverse()
    paginator = Paginator(messages, 30)
    page_num = request.GET.get('page')
    try:
        current_page = paginator.page(page_num)
    except InvalidPage:
        current_page = paginator.page(1)
    return render(request, 'spider/index.html', {'page': current_page})


# for debug
def update(request):
    num_of_update = Notification.fetch_new_notification(30)
    return HttpResponse(str(num_of_update))


# for debug
def delete(request):
    Notification.objects.all().delete()
    return HttpResponseRedirect(reverse('spider:index'))
