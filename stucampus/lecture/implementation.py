#-*- coding: utf-8 -*-
import re
from django.utils import timezone
import datetime

from stucampus.spider.models import Notification
from stucampus.spider.spider import find_content_between_two_marks, MatchError
from stucampus.lecture.models import LectureMessage


def update_lecture_from_notification(new_notif_list):
    academic_notif = [ n for n in new_notif_list if n.category == u'学术' ]
    lecture_notif = search_lecture_notification(academic_notif)
    lecture_messages = []
    for notif in lecture_notif:
        lecture_infor_dict = parse_content(notif.get_content())
        lecture_infor_dict['url_id'] = notif.url_id
        lecture_messages.append(lecture_infor_dict)
    lecture_messages.reverse()

    add_new_lecture_from_notification(lecture_messages)


def search_lecture_notification(academic_notifications):
    lecture_notifications = []
    for a in academic_notifications:
        content = a.get_content()
        if is_about_lecture(content):
            lecture_notifications.append(a)
    return lecture_notifications


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
        pack attributes into a dictionary
    '''
    try:
        title = parse_title(content)
    except MatchError:
        title = 'not found'

    try:
        place = parse_place(content)
    except MatchError:
        place = 'not found'

    try:
        date_time = parse_datetime(content)
    except MatchError:
        date_time = None

    try:
        speaker = parse_speaker(content)
    except MatchError:
        speaker = 'not found'

    return dict(title=title, place=place, date_time=date_time,
                speaker=speaker)


WHITESPACE = u'[　 ]*'


TITLE_PATTERN = (
    (u'讲座题目：' + WHITESPACE, u'\n'),
    (u'报告题目：' + WHITESPACE, u'\n'),
    (u'演讲题目：' + WHITESPACE, u'\n'),
    (u'主题：' + WHITESPACE, u'\n'),
    )


def parse_title(content):
    title = find_by_iter_wrap_pattern(TITLE_PATTERN, content)
    return title


PLACE_PATTERN = (
    (u'讲座地点：' + WHITESPACE, u'\n'),
    (u'报告地点：' + WHITESPACE, u'\n'),
    (u'地点：' + WHITESPACE, u'\n'),
    )


def parse_place(content):
    place = find_by_iter_wrap_pattern(PLACE_PATTERN, content)
    return place


SPEAKER_PATTERN = (
    (u'报告人：' + WHITESPACE, u'\n'),
    (u'特邀讲者：' + WHITESPACE, u'\n'),
    (u'主讲：' + WHITESPACE, u'\n'),
    (u'主讲人：' + WHITESPACE, u'\n'),
    (u'\n', u'教授简介：'),
    )


def parse_speaker(content):
    speaker = find_by_iter_wrap_pattern(SPEAKER_PATTERN, content)
    return speaker


DATETIME_PATTERN = (
    (u'讲座时间：' + WHITESPACE, u'\n'),
    (u'报告时间：' + WHITESPACE, u'\n'),
    (u'时间：' + WHITESPACE, u'\n'),
    )


def parse_datetime(content):
    date_infor = find_by_iter_wrap_pattern(DATETIME_PATTERN, content)
    return parse_date(date_infor) + ' ' + parse_time(date_infor)


DATE_PATTERN = (
    r'\d{4}'+u'年'+r'\d{1,2}'+u'月'+r'\d{1,2}' + u'日',
    r'\d{4}'+r'\w'+r'\d{1,2}'+r'\w'+r'\d{1,2}',
    r'\d{4}'+r'.'+r'\d{1,2}'+r'.'+r'\d{1,2}',
    )                   


def parse_date(content):
    date = find_by_iter_single_pattern(DATE_PATTERN, content)
    return date.replace(u'年', '-').replace(u'月', '-')\
               .replace(u'日', '').replace('.', '-')


TIME_PATTERN = (
    r'\d{1,2}:\d{1,2}-\d{1,2}:\d{1,2}',
    r'\d{1,2}' + u'：' + r'\d{1,2}' + u'—' + r'\d{1,2}' + u'：' + r'\d{1,2}',
    r'\d{1,2}:\d{1,2}',
    r'\d{1,2}' + u'：' + r'\d{1,2}',
    )


def parse_time(content):
    time_range = find_by_iter_single_pattern(TIME_PATTERN, content)
    time_range = time_range.replace(u'：', ':').replace(u'—', '-')
    start_time = time_range.split('-')[0]
    return start_time


def find_by_iter_wrap_pattern(patterns, content, to_search=r'.*?'):
    ''' to find and return the text wraped in pattern
        try match all pattern to content until find it
        raise an error if no pattern match
    '''
    for left, right in patterns:
        reg = left+ r'(?P<content>' + to_search + r')' + right
        match = re.search(reg, content)
        if match:
            return match.group('content')
    raise MatchError(content, reg)


def find_by_iter_single_pattern(patterns, content):
    ''' to find and return the text march the pattern
        try match all pattern to content untile find it
        raise an error if no pattern match
    '''
    for pattern in patterns:
        reg = r'(?P<content>' + pattern + r')'
        match = re.search(reg, content)
        if match:
            return match.group('content')
    raise MatchError(content, reg)


def add_new_lecture_from_notification(new_notif):
    for lect in new_notif:
        if LectureMessage.objects.filter(url_id=lect['url_id']).exists():
            lecture = LectureMessage.objects.get(url_id=lect['url_id'])
        else:
            lecture = LectureMessage()

        lecture.url_id = lect['url_id']
        lecture.title = lect['title']
        lecture.date_time = lect['date_time']
        lecture.place = lect['place']
        lecture.speaker = lect['speaker']
        lecture.download_date = timezone.now().isoformat()
        lecture.url_id_backup = lecture.url_id

        lecture.save()
