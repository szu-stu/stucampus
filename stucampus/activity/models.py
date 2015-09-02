from django.db import models

from stucampus.activity.utils import Generate_Messages_Table
from stucampus.activity.utils import MORNING, AFTERNOON


class ActivityMessage(models.Model):

    TIME = (
        (MORNING, MORNING),
        (AFTERNOON, AFTERNOON),
    )

    title = models.CharField(max_length=30)
    date = models.DateField()
    time = models.CharField(max_length=10, choices=TIME)
    specific_time = models.CharField(max_length=20)
    place = models.CharField(max_length=20)
    summary = models.CharField(max_length=140)

    modified_date_time = models.DateTimeField(editable=False, auto_now=True)
    checked = models.BooleanField(default=False)

    @classmethod
    def generate_messages_table(cls):
        message_table = Generate_Messages_Table(cls)

        return message_table
