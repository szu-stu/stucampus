#-*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.utils import timezone
import django.db.models
from django.db import IntegrityError

from stucampus.custom import models
from stucampus.lecture.implementation import fetch_lecture_messages


class LectureMessage(django.db.models.Model):

    title = models.CharField(max_length=100, blank=True)
    date_time = models.DateTimeField(blank=True)
    place = models.CharField(max_length=40, blank=True)

    url_id = models.CharField(max_length=20, unique=True)
    url_id_backup = models.CharField(max_length=20, unique=True,
                                     editable=False)
    is_check = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    @classmethod
    def add_new_lecture_from_announcement(cls):
        count_get = 0
        stop_mark = cls.get_latest_url_id_in_db()
        for lm in fetch_lecture_messages():
            if lm['url_id'] == stop_mark:
                break
            count_get += 1
            lecture_message = cls(title=lm['title'],
                                  date_time=lm['date_time'],
                                  place=lm['place'],
                                  url_id=lm['url_id'],
                                  url_id_backup=lm['url_id'])
            try:
                lecture_message.save()
            except IntegrityError:
                raise Exception('repeat saveing:'+lecture_message.url_id)
        return count_get

    @classmethod
    def generate_messages_table(cls):
        message_table = cls.creat_empty_table()
        message_table = cls.fill_in_table(message_table)
        return message_table

    @staticmethod
    def creat_empty_table():
        message_table = {}
        message_table['date'] = []
        message_table['morning'] = []
        message_table['afternoon'] = []
        now = timezone.now()
        date_of_this_Monday = now - timedelta(days=now.weekday())
        for i in range(0, 7):
            date = date_of_this_Monday + timedelta(days=i)
            message_table['date'].append(date)
            message_table['morning'].append([])
            message_table['afternoon'].append([])
        return message_table

    @staticmethod
    def fill_in_table(message_table):
        messages_this_week = LectureMessage.get_messages_this_week()
        needed = messages_this_week.filter(is_check=True, is_delete=False)
        for msg in needed:
            if msg.date_time.hour < 12:
                message_table['morning'][msg.date_time.weekday()].append(msg)
            else:
                message_table['afternoon'][msg.date_time.weekday()].append(msg)
        return message_table

    @classmethod
    def get_messages_this_week(cls):
        now = datetime.now()
        date_of_this_Monday = now - timedelta(days=now.weekday())
        date_of_next_Monday = date_of_this_Monday + timedelta(days=7)
        return cls.objects.filter(date_time__gte=date_of_this_Monday,
                                  date_time__lt=date_of_next_Monday)

    @classmethod
    def get_latest_url_id_in_db(cls):
        if cls.objects.all():
            return cls.objects.reverse()[0].url_id
        else:
            return None
