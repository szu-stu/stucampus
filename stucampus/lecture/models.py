from django.db import models

from stucampus.activity.utils import Generate_Messages_Table
from stucampus.activity.utils import MORNING, AFTERNOON


class LectureMessage(models.Model):

    TIME = (
        (MORNING, MORNING),
        (AFTERNOON, AFTERNOON),
    )

    title = models.CharField(null=True, max_length=150)
    date = models.DateField(null=True)
    time = models.CharField(null=True, max_length=100, choices=TIME)
    place = models.CharField(null=True, max_length=150)
    speaker = models.CharField(null=True, max_length=150)
    url_id = models.CharField(max_length=20, null=True, blank=True)

    download_date = models.DateTimeField(editable=False, auto_now_add=True)
    checked = models.BooleanField(default=False)

    @classmethod
    def generate_messages_table(cls):
        message_table = Generate_Messages_Table(cls)

        return message_table
