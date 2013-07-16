from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=75)
    password = models.CharField(max_length=32)
    screen_name = models.CharField(max_length=20)
    is_male = models.BooleanField()
    birthday = models.DateTimeField()
    mphone_num = models.CharField(max_length=11)
    mphone_short_num = models.CharField(max_length=6)
    student_id = models.CharField(max_length=10)
    szucard = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    login_count = models.IntegerField()
    last_login_ip = models.CharField(max_length=40)
    last_login_time = models.DateTimeField()
    college = models.IntegerField()
    token = models.CharField(max_length=32)

