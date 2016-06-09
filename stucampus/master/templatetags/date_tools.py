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


    

    