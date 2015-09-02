# -*- coding: utf-8 -*-
from datetime import date, time, datetime

from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist

import requests
import lxml
import html2text

from stucampus.spider.models import Notification
from stucampus.lecture.models import LectureMessage
from stucampus.lecture.implementation import update_lecture_from_notification
from stucampus.lecture.implementation import parse_content


def fetch_notification_content(url_id):
    url = 'http://www.szu.edu.cn/board/view.asp?id=' + str(url_id)
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'gbk'
    content = response.text
    etree = lxml.html.fromstring(content)
    xp = ('/html/body/table/tr[2]/td/table/tr[3]/td/'
          'table/tr/td/table/tr[3]')
    try:
        element = etree.xpath(xp)[0]
    except IndexError:
        raise Exception("can't find node")
        element = None
    h = html2text.HTML2Text()
    h.ignore_emphasis = True
    return h.handle(lxml.html.etree.tostring(element))

class ParseTest(TestCase):

    def test_update(self):
        content = fetch_notification_content(274085)
        attrs = parse_content(content)
        for attr in attrs:
            print attr, attrs[attr]
