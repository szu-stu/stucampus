#-*- coding: utf-8 -*-
import django.db.models

from stucampus.custom.models import models
from stucampus.spider.data_for_models import PUBLISHER_CHOICES
from stucampus.spider.announcement_spider import get_announcement,\
                                                 get_announcement_content


CATEGORY_CHOICES = (
    ('学术', '学术'),
    ('校园', '校园'),
    ('行政', '行政'),
    ('学工', '学工'),
    ('教务', '教务'),
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

    @staticmethod
    def update_announcements():
        num_of_new_announcement = 0
        for a in get_announcement():
            announcement = Announcement(title=a['title'],
                                        publisher=a['publisher'],
                                        published_date=a['date'],
                                        category=a['category'],
                                        url_id=a['url_id'])
            if not announcement.content_already_exist():
                announcement.save()
                num_of_new_announcement += 1

        return num_of_new_announcement
