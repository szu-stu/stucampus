from datetime import datetime, timedelta
import django.db.models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from stucampus.stucampus_custom import models


class LectureMessage(django.db.models.Model):

    title = models.CharField(max_length=100)
    content = models.CharField(max_length=3000)
    date_time = models.DateTimeField()
    place = models.CharField(max_length=40)

    @staticmethod
    def get_messages_table():
        message_table = LectureMessage.creat_empty_table()
        message_table = LectureMessage.fill_in_table(message_table)
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
        for msg in messages_this_week:
            if msg.date_time.hour < 12:
                message_table['morning'][msg.date_time.weekday()].append(msg)
            else:
                message_table['afternoon'][msg.date_time.weekday()].append(msg)
        return message_table

    @staticmethod
    def get_messages_this_week():
        now = datetime.now()
        date_of_this_Monday = now - timedelta(days=now.weekday())
        date_of_next_Monday = date_of_this_Monday + timedelta(days=7)
        return LectureMessage.objects.filter(
            date_time__gte=date_of_this_Monday,
            date_time__lt=date_of_next_Monday,
            )
