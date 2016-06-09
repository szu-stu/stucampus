#-*- coding: utf-8
#@author:jimczj
#@email:jimczj@gmail.com
from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    szu_no = models.CharField(max_length=10,null=False,unique=True)
    szu_name = models.CharField(max_length=30,null=False)
    szu_ic = models.CharField(max_length=6,null=False)
    szu_org_name = models.CharField(max_length=50,null=True)
    szu_sex = models.CharField(max_length=4,null=True)
    email = models.EmailField(null=True,blank=True)

    def __unicode__(self):
        return self.szu_name

class PlanCategory(models.Model):
    class Meta:
        permissions =(
            ('send_email', u'发送邮件'),
        )
    name = models.CharField(verbose_name=u'分类名',
                            max_length=30)
    english_name = models.CharField(max_length=20, unique=True)
    is_on = models.BooleanField(verbose_name=u'是否开启',default=False)
    tip_time = models.DateField(verbose_name =u'开启感悟留言的时间',blank=True, null=True) #当前时间超过该之后可以显示感悟图标
    # used in ArticleForm.category to display category name in template
    def __unicode__(self):
        return self.name

class Plan(models.Model):
    category = models.ForeignKey(PlanCategory, null=False)
    author = models.ForeignKey(User,null=False,related_name="author")
    content = models.CharField(verbose_name=u'内容',max_length=1000)
    thought = models.CharField(verbose_name=u'感悟',max_length=1000,null=True,blank=True)
    like_count = models.IntegerField(default=0, editable=False)
    deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True,editable=True)
    like_persons = models.ManyToManyField(User,blank=True,related_name="like_persons")

    def __unicode__(self):
        return self.content


