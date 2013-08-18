#-*- coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def organization(request):
    return render(request, 'organization/list.html')
