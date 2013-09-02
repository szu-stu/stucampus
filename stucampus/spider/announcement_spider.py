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


def search_announcements(days=30, keyword='', search_type='title',
                         keyword_user='', searchb1='搜索'):
    ''' return a list containing Announcement object '''

    # the number of days should be in the range of days_choice
    form_data = {'dayy': DAYS_CHOICE[days],
                 'search_type': search_type,
                 'keyword': keyword,
                 'keyword_user': keyword_user,
                 'searchb1': searchb1}
    html = fetch_html_by_post(BOARD_URL, form_data, encoding='gbk')
    etree = lxml.html.fromstring(html)
    # fetch all elements containing announcement information
    xpath = ('/html/body/table/tr[2]/td/table/tr[3]/td/table'
             '/tr[3]/td/table/tr[position()>2]')
    elist = etree.xpath(xpath) 

    collect = []
    for element in elist:
        announcement = factory_announcement(element)
        if announcement != None:
            collect.append(announcement)
    collect.reverse()
    return collect


def factory_announcement(element):
    ''' extract announcement attributes value from element
        return announcement produce from the value
        return None when the announcement has been saved before
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

    if stucampus.spider.models.Announcement.already_exist(url_id):
        return None
    return stucampus.spider.models.Announcement(title=title, 
                                                published_date=date,
                                                publisher=publisher,
                                                category=category,
                                                url_id=url_id)

def get_announcement_content(url_id):
    url = 'http://www.szu.edu.cn/board/view.asp?id=' + url_id
    html = get_html(url, 'gbk')
    left_tag = (r'<td align=center height=30 style="font-size: 9pt">'
                r'<font color=#808080>')
    right_tag = (r'<td height="50" align="right"><table border="0" ce'
                 r'llpadding="0" cellspacing="0" width="90%">')
    text_mixed_with_tags = find_content_between_two_tags(left_tag, right_tag,
                                                         html, r'[\s\S]+?')
    row_text = delete(r'<.+?>', text_mixed_with_tags)
    row_text = delete('\r', row_text)
    row_text = delete(r'&nbsp;', row_text)
    row_text = re.sub('\n+', '\n',  row_text)
    return row_text


def get_announcement_content(url_id):
    url = BOARD_URL + 'view.asp?id=' + url_id
    html = fetch_html_by_get(url, encoding='gbk')
    etree = lxml.html.fromstring(html)
    element_contain_content = etree.xpath('/html/body/table/tr[2]/td/table/'
                                          'tr[3]/td/table/tr[2]/td/table/tr[3]'
                                          )[0]
    content = element_contain_content.text_content()
    #content = ''.join(element_contain_content.xpath('td//text()'))
    return content.replace('\r', '\n')
