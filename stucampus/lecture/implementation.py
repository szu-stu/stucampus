#-*- coding: utf-8 -*-
import re

from stucampus.spider.models import Announcement
from stucampus.spider.spider import find_content_between_two_tags


def get_lecture_messages():
    lecture_announcements = find_lecture_announcement()
    lecture_messages= convert(lecture_announcements)
    return lecture_messages


def find_lecture_announcement():
    academic_announcements = Announcement.objects.filter(category='学术')
    lecture_announcements = []
    for a in academic_announcements:
        content = a.get_content()
        if about_lecture(content):
            lecture_announcements.append(a)
    return lecture_announcements


def about_lecture(content):
    keywords = (u'报告题目',
                u'报告地点',
                u'报告时间',
                u'报告',)
    for word in keywords:
        if word in content:
            return True
    return False


def convert(announcements):
    lecture_messages = []
    for a in announcements:
        content = a.get_content()
        title = find_content_between_two_tags(u'报告题目：', r'',
                                              content, r'.+')
        place = find_content_between_two_tags(u'报告地点：', '\n', content)
        r = r'\d{4}'+u'年'+r'\d{1,2}'+u'月'+r'\d{1,2}'
        date = find_content_between_two_tags(u'报告时间：', u'日', content, r)
        date = date.replace(u'年','-').replace(u'月','-')
        r = r'\d{1,2}:\d{1,2}-\d{1,2}:\d{1,2}'
        time = find_content_between_two_tags('', '', content, r)
        time = time.split('-')[0]
        date_time=date + ' ' + time

        d = dict(title=title, place=place, date_time=date_time,
                 url_id=a.url_id)
        lecture_messages.append(d)
    return lecture_messages
