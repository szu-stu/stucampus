#-*- coding: utf-8 -*-
import re
from django.utils import timezone
import datetime

from stucampus.spider.models import Announcement
from stucampus.spider.spider import find_content_between_two_marks, MatchError


def fetch_lecture_messages():
    academic_announcements = Announcement.objects.filter(category=u'学术')
    lecture_announcements = search_lecture_announcement(academic_announcements)
    lecture_messages = []
    for ancmt in lecture_announcements:
        lecture_infor_dict = parse_content(ancmt.get_content())
        lecture_infor_dict['url_id'] = ancmt.url_id
        lecture_messages.append(lecture_infor_dict)
    return lecture_messages


def search_lecture_announcement(academic_announcements):
    lecture_announcements = []
    for a in academic_announcements:
        content = a.get_content()
        if is_about_lecture(content):
            lecture_announcements.append(a)
    return lecture_announcements


KEYWORDS = (u'报告题目',
            u'报告地点',
            u'报告时间',
            u'报告会',
            u'学术沙龙',
            )


def is_about_lecture(content):
    for word in KEYWORDS:
        if word in content:
            return True
    return False


def parse_content(content):
    ''' annalyse the content and find attributes
        put attributes into a dictionary
    '''
    print content
    title = get_title(content)
    place = get_place(content)
    date_time = get_datetime(content)
    return dict(title=title, place=place, date_time=date_time)


WHITESPACE = u'[　 ]*'


TITLE_PATTERN = (
    (u'讲座题目：' + WHITESPACE, u'\n'),
    (u'报告题目：' + WHITESPACE, u'\n'),
    (u'演讲题目：' + WHITESPACE, u'\n'),
    (u'主题：' + WHITESPACE, u'\n'),
    )

def get_title(content):
    pattern_iter = TITLE_PATTERN.__iter__()
    for left, right in pattern_iter:
        try:
            return find_content_between_two_marks(left, right, content,
                                                  r'.+')
        except MatchError:
            if 0 == pattern_iter.__length_hint__():
                return ''


PLACE_PATTERN = (
    (u'讲座地点：' + WHITESPACE, u'\n'),
    (u'报告地点：' + WHITESPACE, u'\n'),
    (u'地点：' + WHITESPACE, u'\n'),
    )


def get_place(content):
    pattern_iter = PLACE_PATTERN.__iter__()
    for left, right in pattern_iter:
        try:
            return find_content_between_two_marks(left, right, content,
                                                  r'.+')
        except MatchError:
            if 0 == pattern_iter.__length_hint__():
                return ''


SPEAKER_PATTERN = (
    (u'报告人：' + WHITESPACE, u'\n'),
    (u'特邀讲者：' + WHITESPACE, u'\n'),
    (u'主讲：' + WHITESPACE, u'\n'),
    (u'主讲人：' + WHITESPACE, u'\n'),
    (u'\n', u'教授简介：'),
    )


def get_speaker(content):
    pattern_iter = SPEAKER_PATTERN.__iter__()
    for left, right in pattern_iter:
        try:
            return find_content_between_two_marks(left, right, content,
                                                  r'.+')
        except MatchError:
            if 0 == pattern_iter.__length_hint__():
                return ''


DATETIME_PATTERN = (
    (u'讲座时间：' + WHITESPACE, u'\n'),
    (u'报告时间：' + WHITESPACE, u'\n'),
    (u'时间：' + WHITESPACE, u'\n'),
    )


def get_datetime(content):
    prefix_iter = DATETIME_PATTERN.__iter__()
    for left, right in prefix_iter:
        try:
            date_infor = find_content_between_two_marks(left, right, content)
        except MatchError:
            if 0 == prefix_iter.__length_hint__():
                return datetime.datetime.now().isoformat()
        else:
            break
    return get_date(date_infor) + ' ' + get_time(date_infor)
 
DATE_PATTERN = (
    r'\d{4}'+u'年'+r'\d{1,2}'+u'月'+r'\d{1,2}' + u'日',
    r'\d{4}'+r'\w'+r'\d{1,2}'+r'\w'+r'\d{1,2}',
    r'\d{4}'+r'.'+r'\d{1,2}'+r'.'+r'\d{1,2}',
    )                   


def get_date(content):
    pattern_iter = DATE_PATTERN.__iter__()
    for pattern in pattern_iter:
        try:
            date = find_content_between_two_marks('', '', content, pattern)
        except MatchError:
            if 0 == pattern_iter.__length_hint__():
                return datetime.date.today().isoformat()
        else:
            date = date.replace(u'年', '-')\
                       .replace(u'月', '-')\
                       .replace(u'日', '')\
                       .replace('.', '-')
    return date


TIME_PATTERN = (
    r'\d{1,2}:\d{1,2}-\d{1,2}:\d{1,2}',
    r'\d{1,2}' + u'：' + r'\d{1,2}' + u'—' + r'\d{1,2}' + u'：' + r'\d{1,2}',
    r'\d{1,2}:\d{1,2}',
    r'\d{1,2}' + u'：' + r'\d{1,2}',
    )


def get_time(content):
    pattern_iter = TIME_PATTERN.__iter__()
    for pattern in pattern_iter:
        try:
            time_range = find_content_between_two_marks('', '', content,
                                                        pattern)
            time_range = time_range.replace(u'：', ':').replace(u'—', '-')
            start_time = time_range.split('-')[0]
            return start_time
        except MatchError:
            if 0 == pattern_iter.__length_hint__():
                return '00:00'
