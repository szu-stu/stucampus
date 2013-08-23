from django.http import HttpResponse
from stucampus.spider.models import Announcement


def index(request):
    return HttpResponse(output)
