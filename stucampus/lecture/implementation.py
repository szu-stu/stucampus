#-*- coding: utf-8 -*-
import re

from stucampus.spider.models import Announcement
from stucampus.spider.spider import find_content_between_two_tags, MatchError


def get_lecture_messages():
    lecture_announcements = find_lecture_announcement()
    lecture_messages = []
    for a in lecture_announcements:
        lecture_message_dict = convert(a)
        lecture_messages.append(lecture_message_dict)
    return lecture_messages


def find_lecture_announcement():
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


def convert(announcement):
    content = announcement.get_content()

    try:
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
    except MatchError:
        title = ''
        place = ''
        date_time = ''

    dic = dict(title=title, place=place, date_time=date_time,
               url_id=announcement.url_id)
    return dic
