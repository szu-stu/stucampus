#-*- coding: utf-8 -*-
import django.db.models

from stucampus.custom.models import models
from stucampus.spider.data_for_models import PUBLISHER_CHOICES
from stucampus.spider.announcement_spider import get_announcement_content


CATEGORY_CHOICES = (
    ('teach', 'teach'),
    ('daily', 'daily'),
    )
class Announcement(django.db.models.Model):
    
    url_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=40)
    published_date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    publisher = models.CharField(max_length=20, choices=PUBLISHER_CHOICES)
    content = models.TextField(max_length=5000, blank=True)

    def get_content(self, url_id):
        if not self.content:
            content = get_announcement_content(url_id)
            self.content = content
            self.save()
        return self.content
