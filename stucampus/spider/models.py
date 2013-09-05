#-*- coding: utf-8 -*-
import django.db.models
from django.db import IntegrityError

from stucampus.custom.models import models
from stucampus.spider.data_for_models import PUBLISHER_CHOICES
from stucampus.spider.notification_spider import search_notifications
from stucampus.spider.notification_spider import get_notification_content


CATEGORY_CHOICES = (
    (u'学术', u'学术'),
    (u'校园', u'校园'),
    (u'行政', u'行政'),
    (u'学工', u'学工'),
    (u'教务', u'教务'),
    )


class Notification(django.db.models.Model):

    url_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=40)
    published_date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    publisher = models.CharField(max_length=20, choices=PUBLISHER_CHOICES)
    content = models.TextField(max_length=5000, blank=True)

    def get_content(self):
        if not self.content:
            self.content = get_notification_content(self.url_id)
            self.save()
        return self.content

    @classmethod
    def fetch_new_notification(cls, days=1):
        num_of_new_get = 0
        for notification in search_notifications(days):
            try:
                notification.save()
                num_of_new_get += 1
            except IntegrityError:
                raise Exception('repeat saving:'+notification.url_id)
        return num_of_new_get

    @classmethod
    def already_exist(cls, to_check):
        return Notification.objects.filter(url_id=to_check).exists()
