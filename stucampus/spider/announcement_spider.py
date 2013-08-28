#-*- coding: utf-8 -*-
import re
from django.db import IntegrityError

from stucampus.spider.spider import get_html, get_etree, MatchError
from stucampus.spider.spider import delete, find_content_between_two_tags


def get_announcement():
    html = get_html('http://www.szu.edu.cn/board/', 'gbk')
    etree = get_etree(html)
    elist = get_needed_element(etree)

    collect = []
    for element in elist:
        dic = extract_imformation_into_dictionary(element)
        collect.append(dic)
    collect.reverse()
    return collect


def get_needed_element(etree):
    path = ('/html/body/table/tr[2]/td/table/tr[3]/td/table'
            '/tr[3]/td/table/tr[position()>2]')
    return etree.xpath(path)


def extract_imformation_into_dictionary(element):
    date = element.xpath('td[6]/text()')[0]
    publisher = element.xpath('td[3]/a/text()')[0]
    category = element.xpath('td[2]/text()')[0]

    title = ''.join(element.xpath('td[4]/*//text()'))
    # sample:    |置顶|·XXXXXXXXXXX
    #         or ·XXXXXXXXXXX
    if u'|置顶|' in title:
        is_stikcy = True
        title = title[4:]
    else:
        is_stikcy = False
    title = title[1:]  # delete the point prefix '·'

    # sample: view.asp?id=262297
    # [12:] to cut view.asp?id=
    url_id = element.xpath('td[4]/a/@href')[0][12:]
    return  dict(title=title, date=date, publisher=publisher,
                 category=category, is_stikcy=is_stikcy, url_id=url_id)


def get_announcement_content(url_id):
    url = 'http://www.szu.edu.cn/board/view.asp?id=' + url_id
    html = get_html(url, code='gbk')
    etree = get_etree(html)
    element_contain_content = etree.xpath('/html/body/table/tr[2]/td/table/'
                                          'tr[3]/td/table/tr[2]/td/table/tr[3]'
                                          )[0]
    return ''.join(element_contain_content.xpath('td//text()'))
