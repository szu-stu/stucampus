# -*- coding: utf-8 -*-

from django.db import models

SEX = (
    ('boy', u'男'),
    ('girl', u'女'),
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
            ('apply_manage', u'manage the applicant'),
        )
    name = models.CharField(max_length = 20)
    gender = models.CharField(max_length = 6, choices = SEX, default="boy")
    stu_ID = models.IntegerField(max_length = 10)
    college = models.CharField(max_length = 30)
    mobile = models.CharField(max_length = 11)
    dept1 = models.CharField(max_length = 4, choices=DEPT, default="cbb")
    dept2 = models.CharField(max_length = 4, choices=DEPT, default="jsb")
    ip = models.IPAddressField()
    sign_up_date = models.DateField(auto_now_add = True)
    self_intro = models.CharField(max_length = 500)
    status = models.BooleanField(default = True)


