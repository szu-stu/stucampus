#-*- coding: utf-8 -*-
import django.db.models

from stucampus.custom.models import models
from stucampus.spider.data_for_models import PUBLISHER_CHOICES
from stucampus.spider.announcement_spider import get_announcement,\
                                                 get_announcement_content


CATEGORY_CHOICES = (
    (u'学术', u'学术'),
    (u'校园', u'校园'),
    (u'行政', u'行政'),
    (u'学工', u'学工'),
    (u'教务', u'教务'),
    )


class Announcement(django.db.models.Model):
    
    url_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=40)
    published_date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    publisher = models.CharField(max_length=20, choices=PUBLISHER_CHOICES)
    content = models.TextField(max_length=5000, blank=True)

    def get_content(self):
        if not self.content:
            self.content = get_announcement_content(self.url_id)
            self.save()
        return self.content

    def content_already_exist(self):
        return Announcement.objects.filter(url_id=self.url_id).exists()

    @classmethod
    def update_announcements(cls):
        num_of_new_announcement = 0
        latest_url_id_in_db = SpiderManager.get_latest_url_id_in_db()
        for a in get_announcement():
            announcement = Announcement(title=a['title'],
                                        publisher=a['publisher'],
                                        published_date=a['date'],
                                        category=a['category'],
                                        url_id=a['url_id'])
            if not announcement.content_already_exist():
                announcement.save()
                num_of_new_announcement += 1
            elif a['url_id'] == latest_url_id_in_db:
                break
        # it ignore the case that announcement is sticky
        if num_of_new_announcement > 0
            SpiderManager.update_the_lastest_url_id_in_db(a['url_id'])
        return num_of_new_announcement


class SpiderManager(django.db.models.Model):
    latest_url_id_in_db = models.CharField(max_length=20, null=True)

    @classmethod
    def get_latest_url_id_in_db(cls):
        sm_list = cls.objects.all()
        if sm_list:
            return sm_list[0].latest_url_id_in_db
        else:
            return None

    @classmethod
    def update_the_lastest_url_id_in_db(cls, url_id):
        the_only_one_object, created = cls.objects.get_or_create(
                   latest_url_id_in_db=cls.get_latest_url_id_in_db())
        the_only_one_object.latest_url_id_in_db= url_id
        the_only_one_object.save()
