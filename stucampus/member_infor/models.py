#-*- coding: utf-8
#@author:jimczj
#@email:jimczj@gmail.com
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
	nick_name = models.CharField(verbose_name=u'绰号',blank=True,max_length=20)
	mobile_phone_number = models.CharField(verbose_name=u'手机号',max_length=11)
	szu_no = models.CharField(verbose_name=u'学号',max_length=10,unique=True)
	approved = models.BooleanField(verbose_name =u'通过认证',default=False)
	birthday = models.DateField(verbose_name =u'生日',blank=True, null=True)
	e_mail =models.EmailField(verbose_name =u'邮箱',blank=True,max_length = 30)
