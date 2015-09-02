#-*- coding: utf-8
from django.db import models

from stucampus.account.models import Student


class Organization(models.Model):

    class Meta:
        permissions = (
            ('organization_manager', u'组织帐号管理员'),
        )

    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    url = models.URLField()
    logo = models.CharField(max_length=50)
    managers = models.ManyToManyField(Student, related_name='orgs_as_manager')
    members = models.ManyToManyField(Student, related_name='orgs_as_member')
    is_banned = models.BooleanField(default=False)
    ban_reason = models.CharField(max_length=250, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
