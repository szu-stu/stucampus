from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def about_us(request):
    return render(request, "aboutus.html")


def page_not_found(request):
    return render(request, "404.html")
