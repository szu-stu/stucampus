#-*- coding: utf-8
import arrow
from django import template
import datetime
register = template.Library()

@register.filter(name='from_now')
def from_now(date):
    '''
        返回距离现在的时间间隔

    '''
    return arrow.get(date).humanize(locale='zh_CN')

@register.filter(name='from_now')
def from_now(date):
    '''
        返回距离现在的时间间隔

    '''
    return arrow.get(date).humanize(locale='zh_CN')

@register.filter(name='time_to_on')
def time_to_on(tip_time):
	'''
		是否开启
	'''
	time_interval = datetime.date.today() -tip_time
	if time_interval.total_seconds()>=0:
		return True
	return False

@register.filter(name='time_to_off')
def time_to_off(tip_time):
    '''
        是否开启
    '''
    time_interval = datetime.date.today() -tip_time
    if time_interval.total_seconds()<=0:
        return False
    return True

@register.filter(name='show_name')
def show_name(person_list):
    '''
        显示人物名字
    '''
    
    person_list =[person.szu_name for person in person_list] 
    person_name=",".join(person_list)
    return person_name

@register.filter(name='show_szu_no')
def show_szu_no(person_list):
    '''
        显示人物名字
    '''
    
    return [person.szu_no for person in person_list] 

@register.filter(name='show_last_name')
def show_last_name(name):
    '''
        显示人物名字最后一个字
    '''
    
    return name[-1:]

@register.filter(name='slice_sort_list')
def slice_sort_list(lottery_list):
    '''
        显示人物名字最后一个字
    '''
    return lottery_list.order_by("-result")[:50]




    

    