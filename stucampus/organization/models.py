from django.db import models
from django.contrib.auth.models import Group

from stucampus.account.models import Student


class Organization(models.Model):
    group = models.OneToOneField(Group)
    phone = models.CharField(max_length=11)
    url = models.URLField()
    logo = models.CharField(max_length=50)
    isBanned = models.BooleanField(default=False)
    banReason = models.CharField(max_length=250, null=True, blank=True)