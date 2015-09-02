#-*- coding: utf-8 -*-
import django.db.models
from django.db import IntegrityError

import lxml.html
import html2text

from stucampus.custom.models import models
from stucampus.spider.data_for_models import PUBLISHER_CHOICES
from stucampus.spider.spider import fetch_html_by_get


CATEGORY_CHOICES = (
    (u'学术', u'学术'),
    (u'校园', u'校园'),
    (u'行政', u'行政'),
    (u'学工', u'学工'),
    (u'教务', u'教务'),
    )


class Notification(django.db.models.Model):

    class Meta:
        permissions = (
            ('spider_manager', u'爬虫管理员'),
        )

    url_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=150)
    published_date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    publisher = models.CharField(max_length=20, choices=PUBLISHER_CHOICES)
    content = models.TextField(max_length=5000, blank=True)

    def get_content(self):
        if not self.content:
            self.content = Notification.download_content(self.url_id)
            self.save()
        return self.content

    @classmethod
    def download_content(cls, url_id):
        url = 'http://www.szu.edu.cn/board/view.asp?id=' + url_id
        html = fetch_html_by_get(url, encoding='gbk')
        etree = lxml.html.fromstring(html)
        xp = ('/html/body/table/tr[2]/td/table/tr[3]/td/'
              'table/tr/td/table/tr[3]')
        try:
            element_contain_content = etree.xpath(xp)[0]
        except IndexError:  # can not find
            return ''
        h = html2text.HTML2Text()
        h.ignore_emphasis = True
        content = h.handle(lxml.html.etree.tostring(element_contain_content))
        #content = element_contain_content.text_content()
        return content.replace('\r', '\n')

    @classmethod
    def save_new_notification(cls, new_notif):
        num_of_new_get = 0
        for notification in new_notif: 
            try:
                notification.save()
                num_of_new_get += 1
            except IntegrityError:
                raise Exception('repeat saving:'+notification.url_id)
        return num_of_new_get
