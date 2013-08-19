from django.db.models

from stucampus.custom import models


class Announcement(django.db.models.Model):
    
    url_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=40)
    published_date = models.DateField()
    publisher = models.CharField(max_length=20, choices=PUBLISHER_CHOICES))
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    content = models.TextField(max_length=5000, blank=True)


CATEGORY_CHOICES = (
    ('teach', 'teach'),
    ('daily', 'daily'),
    )


PUBLISHER_CHOICES = (
    ('csse', 'csse'),
    ('lqq', 'liqingquan'),
    )
