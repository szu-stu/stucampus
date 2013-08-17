from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User)
    screen_name = models.CharField(max_length=20)
    is_male = models.BooleanField()
    birthday = models.DateTimeField(auto_now=True)
    mphone_num = models.CharField(max_length=11)
    mphone_short_num = models.CharField(max_length=6)
    student_id = models.CharField(max_length=10)
    szucard = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    login_count = models.IntegerField(default=0)
    last_login_ip = models.CharField(max_length=40)
    last_login_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    token = models.CharField(max_length=32)
    isMaster = models.BooleanField(default=False)