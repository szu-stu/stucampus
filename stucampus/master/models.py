from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=11)
    websiteAddress = models.CharField(max_length=255)
    logo = models.CharField(max_length=150)
    isBanned = models.BooleanField()
    banDay = models.DateTimeField()
    isDelete = models.BooleanField()
    banReason = models.CharField(max_length=250)
