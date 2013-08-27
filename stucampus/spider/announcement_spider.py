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
    attrs = {}

    attrs['date'] = element.xpath('td[6]/text()')[0]
    attrs['publisher'] = element.xpath('td[3]/a/text()')[0]
    attrs['category'] = element.xpath('td[2]/text()')[0]

    attrs['title'] = ''.join(element.xpath('td[4]/*//text()'))
    # sample: |置顶|·XXXXXXXXXXX or ·XXXXXXXXXXX
    if u'|置顶|' in attrs['title']:
        is_stikcy = True
        attrs['title'] = attrs['title'][4:]
    else:
        is_stikcy = False
    attrs['title'] = attrs['title'][1:]  # delete the point prefix '·'

    # sample: view.asp?id=262297
    # [12:] to cut view.asp?id=
    attrs['url_id'] = element.xpath('td[4]/a/@href')[0][12:]
    return attrs


def get_announcement_content(url_id):
    url = 'http://www.szu.edu.cn/board/view.asp?id=' + url_id
    html = get_html(url, code='gbk')
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
