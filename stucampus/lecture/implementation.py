#-*- coding: utf-8 -*-
import re
from django.utils import timezone

from stucampus.spider.models import Announcement
from stucampus.spider.spider import find_content_between_two_tags, MatchError


def get_lecture_messages():
    lecture_announcements = look_up_lecture_announcement()
    lecture_messages = []
    for a in lecture_announcements:
        lecture_imfor_dict = get_infor(a)
        lecture_messages.append(lecture_imfor_dict)
    return lecture_messages


def look_up_lecture_announcement():
    academic_announcements = Announcement.objects.filter(category=u'学术')
    lecture_announcements = []
    for a in academic_announcements:
        content = a.get_content()
        if is_about_lecture(content):
            lecture_announcements.append(a)
    return lecture_announcements


keywords = (u'报告题目',
            u'报告地点',
            u'报告时间',
            u'报告会',
            )


def is_about_lecture(content):
    for word in keywords:
        if word in content:
            return True
    return False


def get_infor(announcement):
    ''' get lecture information from announcement
        put the information into a dictionary
    '''

    content = announcement.get_content()

    try:
        title = get_title(content)
    except MatchError:
        title = ''

    try:
        place = get_place(content)
    except MatchError:
        place = ''

    try:
        date_time = get_date_time(content)
    except MatchError:
        date_time = timezone.now()

    return dict(title=title, place=place, date_time=date_time,
                url_id=announcement.url_id)


def get_title(content):
    return find_content_between_two_tags(u'报告题目：', r'',
                                         content, r'.+')


def get_place(content):
    return find_content_between_two_tags(u'报告地点：', '\n', content)


def get_date_time(content):
    r = r'\d{4}'+u'年'+r'\d{1,2}'+u'月'+r'\d{1,2}'
    date = find_content_between_two_tags(u'报告时间：', u'日', content, r)
    date = date.replace(u'年', '-').replace(u'月', '-')

    r = r'\d{1,2}:\d{1,2}-\d{1,2}:\d{1,2}'
    time = find_content_between_two_tags('', '', content, r)
    time = time.split('-')[0]

    return date + ' ' + time
