#-*- coding: utf-8 -*-
import re
import datetime
from stucampus.spider.spider import MatchError
from stucampus.lecture.models import LectureMessage


def update_lecture_from_notification(new_notif_list):
    academic_notif = [ n for n in new_notif_list \
            if n.category == u'学术' \
            and not LectureMessage.objects.filter(url_id=n.url_id).exists()]
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
        if is_about_lecture(a.title) or is_about_lecture(content):
            lecture_notifications.append(a)
    return lecture_notifications


KEYWORDS = (u'报告题目',
            u'报告地点',
            u'报告时间',
            u'报告会',
            u'学术沙龙',
            u'论坛',
            u'讲座',
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
        title = find_by_iter_wrap_pattern(TITLE_PATTERN, content)
    except MatchError:
        title = ''

    try:
        place = find_by_iter_wrap_pattern(PLACE_PATTERN, content)
    except MatchError:
        place = ''

    try:
        date_time_txt = find_by_iter_wrap_pattern(DATETIME_PATTERN, content)
    except MatchError:
        date = None
        time = None
    else:
        try:
            date = parse_date(date_time_txt)
        except MatchError:
            date = None
        try:
            time = parse_time(date_time_txt)
        except MatchError:
            time = None

    try:
        speaker = find_by_iter_wrap_pattern(SPEAKER_PATTERN, content)
    except MatchError:
        speaker = ''

    return dict(title=title, place=place, date=date, time=time,
                speaker=speaker)


WHITESPACE = u'[　 ]*?'
COLON = u'[：:]*'


TITLE_PATTERN = (
    (u'讲.*?座.*?题.*?目' + COLON + WHITESPACE, u'\n'),
    (u'报.*?告.*?题.*?目' + COLON + WHITESPACE, u'\n'),
    (u'演.*?讲.*?题.*?目' + COLON + WHITESPACE, u'\n'),
    (u'题.*?目' + COLON + WHITESPACE, u'\n'),
    (u'题' + COLON + WHITESPACE +u'目：' + WHITESPACE, u'\n'),
    (u'主.*?题' + COLON + WHITESPACE, u'\n'),
    (u'主' + COLON + WHITESPACE + u'题：' + WHITESPACE, u'\n'),
)


PLACE_PATTERN = (
    (u'讲.*?座.*?地.*?点' + COLON + WHITESPACE, u'\n'),
    (u'报.*?告.*?地.*?点' + COLON + WHITESPACE, u'\n'),
    (u'地.*?点' + COLON + WHITESPACE, u'\n'),
    (u'地' + COLON + WHITESPACE + u'点' + WHITESPACE, u'\n'),
)


SPEAKER_PATTERN = (
    (u'报.*?告.*?人' + COLON + WHITESPACE, u'\n'),
    (u'演.*?讲.*?人' + COLON + WHITESPACE, u'\n'),
    (u'特.*?邀.*?讲.*?者' + COLON + WHITESPACE, u'\n'),
    (u'主.*?讲.*?人' + COLON + WHITESPACE, u'\n'),
    (u'主.*?讲：' + COLON + WHITESPACE, u'\n'),
    (u'主' + COLON + WHITESPACE + u'讲' + WHITESPACE, u'\n'),
    (u'\n', u'教.*?授.*?简.*?介'),
)


DATETIME_PATTERN = (
    (u'讲.*?座.*?时.*?间' + COLON + WHITESPACE, u'\n'),
    (u'报.*?告.*?时.*?间' + COLON + WHITESPACE, u'\n'),
    (u'时.*?间' + COLON + WHITESPACE, u'\n'),
    (u'时' + COLON + WHITESPACE + u'间：' + WHITESPACE, u'\n'),
    )


DATE_PATTERN = (
    r'\d{4}'+u'年'+r'\d{1,2}'+u'月'+r'\d{1,2}' + u'日',
    r'\d{4}'+u'年'+r'\d{1,2}'+u'月'+r'\d{1,2}' + u'号',
    r'\d{4}'+r'\w'+r'\d{1,2}'+r'\w'+r'\d{1,2}',
    r'\d{4}'+r'.'+r'\d{1,2}'+r'.'+r'\d{1,2}',
)


def parse_date(content):
    date = find_by_iter_single_pattern(DATE_PATTERN, content)
    reg = r'(?P<year>\d{4}).(?P<month>\d{1,2}).(?P<day>\d{1,2})'
    match = re.search(reg, date)
    if match:
        year = int(match.group('year'))
        month = int(match.group('month'))
        day = int(match.group('day'))
        return datetime.date(year, month, day)
    raise MatchError(date, reg)


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
    if datetime.datetime.strptime(start_time, '%H:%M').hour < 12:
        return u'上午'
    else:
        return  u'下午'


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
        if not LectureMessage.objects.filter(
                url_id=lect['url_id']).exists():
            lecture = LectureMessage()

        for attr in lect:
            if isinstance(lect[attr], (unicode, str)) \
                    and len(lect[attr]) > 100:
                lect[attr] = lect[attr][:100]

        lecture.url_id = lect['url_id']
        lecture.title = lect['title']
        lecture.date = lect['date']
        lecture.time = lect['time']
        lecture.place = lect['place']
        lecture.speaker = lect['speaker']

        lecture.save()
