#-*- coding: utf-8 -*-
from itertools import chain
from datetime import datetime, timedelta
from django.utils import timezone
import django.db.models
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from stucampus.custom import models
from stucampus.lecture.implementation import fetch_lecture


class LectureMessage(django.db.models.Model):

    title = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    place = models.CharField(max_length=40)
    speaker = models.CharField(max_length=40)
    url_id = models.CharField(max_length=20, unique=True)

    download_date = models.DateTimeField(editable=False)
    url_id_backup = models.CharField(max_length=20, unique=True,
                                     editable=False)
    is_check = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    @classmethod
    def add_new_lecture_from_notification(cls):
        try:
            stop_mark = cls.objects.latest('pk').url_id
        except ObjectDoesNotExist:
            stop_mark = None

        count_get = 0
        for lect in fetch_lecture():
            if lect['url_id'] == stop_mark:
                break
            raise Exception(lect['url_id'])
            lecture, created = cls.objects.get_or_create(
                url_id=lect['url_id'])

            lecture.title = lect['title']
            lecture.date_time = lect['date_time']
            lecture.place = lect['place']
            lecture.speaker = lect['speaker'],
            lecture.download_date = timezone.now().isoformat()
            lecture.url_id_backup = lect['url_id']

            lecture.save()
            count_get += 1
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
        now = timezone.now()
        date_of_this_Monday = now - timedelta(days=now.weekday())
        date_of_next_Monday = date_of_this_Monday + timedelta(days=7)
        lecture_held_this_week = cls.objects.filter(
            date_time__gte=date_of_this_Monday,
            date_time__lt=date_of_next_Monday)
        msg_fetch_this_week = cls.objects.filter(
            download_date__gte=date_of_this_Monday,
            download_date__lt=date_of_next_Monday)
        return lecture_held_this_week | msg_fetch_this_week
