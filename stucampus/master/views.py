from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def page_not_found(request):
    return render(request, "404.html")
