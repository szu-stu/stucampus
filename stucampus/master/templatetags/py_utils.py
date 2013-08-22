#-*- coding: utf-8
from datetime import datetime

from django import template
from django.utils.timezone import utc

register = template.Library()


@register.filter(name='as_range')
def as_range(upper, lower=0):
    return range(lower, upper)


@register.filter(name='ellipsis')
def ellipsis(text, input_tuple):
    exec("%s%s" % ("max_length, replacement = ", input_tuple))
    if len(text) > max_length:
        return ("%s%s" % text[:max_length] ,replacement)
    else:
        return text


@register.filter(name='friendly_date')
def friendly_date(time):
    now = datetime.utcnow().replace(tzinfo=utc)
    if type(time) is datetime:
        print time
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days
    if day_diff < 0:
        return ''
    if day_diff == 0:
        if second_diff < 10:
            return "刚刚"
        if second_diff < 60:
            return str(second_diff) + "秒前"
        if second_diff < 120:
            return  "1分钟前"
        if second_diff < 3600:
            return str( second_diff / 60 ) + "分钟前"
        if second_diff < 7200:
            return "1小时前"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + "小时前"
    if day_diff == 1:
        return "昨天"
    if day_diff < 7:
        return str(day_diff) + "天前"
    if day_diff < 31:
        return str(day_diff/7) + "周前"
    if day_diff < 365:
        return str(day_diff/30) + "月前"
    return str(day_diff/365) + "年前"
