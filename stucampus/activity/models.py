import django.db.models
from django.utils import timezone

from stucampus.custom import models


class ActivityMessage(stucampus.db.models):
    title = models.CharField(max_length=30)
    date_time = models.DateTimeField()
    place = CharField(max_length=20)
    summary = CharField(max_length=140)

    @classmethod
    def get_activity_list(cls):
        return cls.objects.filter(date_time__gte==timezone.now())
