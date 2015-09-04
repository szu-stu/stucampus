# -*- coding: utf-8 -*-

from django.db import models

SEX = (
    ('male', u'男'),
    ('female', u'女'),
    )

DEPT = (
    ('xzb', u'行政部'),
    ('sjb', u'设计部'),
    ('jsb', u'技术部'),
    ('cbb', u'采编部'),
    ('yyb', u'运营部'),
    )

class Register(models.Model):
    class Meta:
        permissions = (
            ('manager', u'报名信息管理员'),
        )
    name = models.CharField(max_length = 20)
    gender = models.CharField(max_length = 6, choices = SEX, default="male")
    stu_ID = models.IntegerField(max_length = 10)
    college = models.CharField(max_length = 30)
    mobile = models.CharField(max_length = 11)
    dept1 = models.CharField(max_length = 4, choices=DEPT, default="cbb")
    dept2 = models.CharField(max_length = 4, choices=DEPT, default="jsb")
    ip = models.IPAddressField()
    sign_up_date = models.DateField(auto_now_add = True)
    self_intro = models.CharField(max_length = 500)
    status = models.BooleanField(default = True)


