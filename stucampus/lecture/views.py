#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.views import generic
from django.core.paginator import InvalidPage
from django.utils.decorators import method_decorator

from stucampus.lecture.models import LectureMessage
from stucampus.lecture.forms import LectureFormset
from stucampus.custom.forms_utils import FormsetPaginator
from stucampus.spider.models import Notification
from stucampus.lecture.implementation import update_lecture_from_notification
from stucampus.account.permission import check_perms


def index(request):
    table = LectureMessage.generate_messages_table()
    return render(request, 'lecture/home.html', {'table': table})


def mobile(request):
    table = LectureMessage.generate_messages_table()
    return render(request, 'lecture/mobile.html', {'table': table})


@check_perms('spider.spider_manager')
def auto_add(request):
    ''' add lecture from notification '''
    noti_list = Notification.objects.all()
    update_lecture_from_notification(noti_list)
    return HttpResponseRedirect(reverse('lecture:manage'))


class ManageView(generic.View):

    @classmethod
    def __create_page(cls, request):
        paginator = FormsetPaginator(LectureMessage,
                                     LectureMessage.objects.all(), 5,
                                     formset=LectureFormset)
        try:
            page = paginator.page(request.GET.get('page'))
        except InvalidPage:
            page = paginator.page(1)
        return page

    @method_decorator(check_perms('account.website_admin'))
    def get(self, request):
        return render(request, 'lecture/manage.html',
                      {'page': ManageView.__create_page(request)})

    @method_decorator(check_perms('account.website_admin'))
    def post(self, request):
        formset = LectureFormset(request.POST)
        if not formset.is_valid():
            page = ManageView.__create_page(request)
            page.formset = formset
            return render(request, 'lecture/manage.html',
                          {'page': page})
        # 当extra>0的时候，不能循环form来save()
        formset.save()
        page = request.GET.get('page')
        return HttpResponseRedirect(reverse('lecture:index'))
