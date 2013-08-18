#-*- coding: utf-8
from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User)
    screen_name = models.CharField(max_length=20)
    is_male = models.BooleanField(default=True,
                                  choices=((True, u'男'), (False, u'女')))
    birthday = models.DateTimeField(blank=True, null=True)
    mphone_num = models.CharField(max_length=11)
    mphone_short_num = models.CharField(max_length=6)
    student_id = models.CharField(max_length=10)
    szucard = models.CharField(max_length=6)
    login_count = models.IntegerField(default=0)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    is_master = models.BooleanField(default=False)