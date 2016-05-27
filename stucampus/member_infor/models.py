#-*- coding: utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Member(models.Model):
	class Meta:
		permissions =(
			('member_add', u'通讯录人员添加'),
			('member_manage', u'通讯录人员管理'),
		)

	name = models.CharField(verbose_name=u'姓名',blank=False,max_length=20)
	mobile_phone_number = models.CharField(verbose_name=u'手机号',max_length=11)
	szu_no = models.CharField(verbose_name=u'学号',max_length=10,unique=True)
