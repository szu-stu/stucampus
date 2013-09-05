#-*- coding:utf-8 -*-
import re
from django.db import IntegrityError
import lxml.html

from stucampus.spider.spider import fetch_html_by_post, fetch_html_by_get
from stucampus.spider.spider import MatchError
import stucampus.spider.models


BOARD_URL = 'http://www.szu.edu.cn/board/'
DAYS_CHOICE = {1: '1#一天',
               3: '3#三天',
               7: '7#一周',
               15: '15#半个月',
               30: '30#一个月',
               90: '90#三个月',
               182: '182#半年',
               365: '365#一年',}


def search_notifications(days=30, keyword='', search_type='title',
                         keyword_user='', searchb1='搜索'):
    ''' return a list containing Notification object '''

    # the number of days should be in the range of days_choice
    form_data = {'dayy': DAYS_CHOICE[days],
                 'search_type': search_type,
                 'keyword': keyword,
                 'keyword_user': keyword_user,
                 'searchb1': searchb1}
    html = fetch_html_by_post(BOARD_URL, form_data, encoding='gbk')
    etree = lxml.html.fromstring(html)
    # fetch all elements containing notification information
    xpath = ('/html/body/table/tr[2]/td/table/tr[3]/td/table'
             '/tr[3]/td/table/tr[position()>2]')
    elist = etree.xpath(xpath) 

    notif_list = []
    for element in elist:
        notification = factory_notification(element)
        if notification != None:
            notif_list.append(notification)
    notif_list.reverse()
    return notif_list


def factory_notification(element):
    ''' extract notification attributes value from element
        return notification produce from the value
        return None when the notification has been saved before
    '''

    date = element.findtext('td[6]')
    publisher = element.findtext('td[3]/a')
    category = element.findtext('td[2]')
    title = ''.join(element.xpath('td[4]/*//text()'))
    # sample:    |置顶|·XXXXXXXXXXX
    #         or ·XXXXXXXXXXX
    title.lstrip(u'|置顶|')
    title.lstrip(u'·')
    # sample: view.asp?id=262297
    url_id = element.xpath('td[4]/a/@href')[0].lstrip('view.asp?id=')

    if stucampus.spider.models.Notification.already_exist(url_id):
        return None
    return stucampus.spider.models.Notification(title=title, 
                                                published_date=date,
                                                publisher=publisher,
                                                category=category,
                                                url_id=url_id)


def get_notification_content(url_id):
    url = BOARD_URL + 'view.asp?id=' + url_id
    html = fetch_html_by_get(url, encoding='gbk')
    etree = lxml.html.fromstring(html)
    xp = '/html/body/table/tr[2]/td/table/tr[3]/td/table/tr/td/table/tr[3]'
    try:
        element_contain_content = etree.xpath(xp)[0]
    except IndexError:
        return ''
    content = element_contain_content.text_content()
    return content.replace('\r', '\n')
