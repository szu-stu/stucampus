#-*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.utils import timezone
import django.db.models

from stucampus.custom import models
from stucampus.lecture.implementation import get_lecture_messages


class LectureMessage(django.db.models.Model):

    title = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    place = models.CharField(max_length=40)

    url_id = models.CharField(max_length=20, unique=True)
    url_id_backup = models.CharField(max_length=20, unique=True)
    is_check = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    @classmethod
    def get_message_from_announcement(cls):
        count_get = 0
        repeat = 0
        for lm in get_lecture_messages():
            count_get += 1
            lecture_message, created = cls.objects.get_or_create(
                                   title=lm['title'],
                                   date_time=lm['date_time'],
                                   place=lm['place'],
                                   url_id=lm['url_id'],
                                   url_id_backup=lm['url_id'])
            if not created:
                lecture_message.save()
            else:
                repeat += 1
        return (count_get, repeat)

    @classmethod
    def generate_messages_table(cls):
        message_table = cls.creat_empty_table()
        message_table = cls.fill_in_table(message_table)
        return message_table

    @staticmethod
    def creat_empty_table():
        message_table = {}
        message_table['morning'] = []
        message_table['afternoon'] = []
        for i in range(0, 7):
            message_table['morning'].append([])
            message_table['afternoon'].append([])
        return message_table

    @staticmethod
    def fill_in_table(message_table):
        messages_this_week = LectureMessage.get_messages_this_week()
        checked_messages_this_week = messages_this_week.filter(is_check=True)
        for msg in checked_messages_this_week:
            if msg.date_time.hour < 12:
                message_table['morning'][msg.date_time.weekday()].append(msg)
            else:
                message_table['afternoon'][msg.date_time.weekday()].append(msg)
        return message_table

    @classmethod
    def get_messages_this_week(cls):
        now = timezone.now()
        date_of_this_Monday = now - timedelta(days=now.weekday())
        date_of_next_Monday = date_of_this_Monday + timedelta(days=7)
        return cls.objects.filter(date_time__gte=date_of_this_Monday,
                                  date_time__lt=date_of_next_Monday)
