#-*- coding: utf-8
#@author:jimczj
#@email:jimczj@gmail.com
from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    AVATAR_COLOR_CHOICES = (
            (1,"#A0C1E5"),(2,"#506B90"),(3,"#E5A1A0"),(4,"#D6A0E5"),(5,"#DAE5A0")
        )
    avatar_color = models.IntegerField(default=1,choices=AVATAR_COLOR_CHOICES)
    szu_no = models.CharField(max_length=10,null=False,unique=True)
    szu_name = models.CharField(max_length=30,null=False)
    szu_ic = models.CharField(max_length=6,null=False)
    szu_org_name = models.CharField(max_length=50,null=True)
    szu_sex = models.CharField(max_length=4,null=True)
    email = models.EmailField(null=True,blank=True)

    def __unicode__(self):
        return self.szu_name+"_"+self.szu_ic

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
    content = models.TextField(verbose_name=u'内容',max_length=1000)
    thought = models.CharField(verbose_name=u'感悟',max_length=1000,null=True,blank=True)
    like_count = models.IntegerField(default=0, editable=False)
    deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True,editable=True)
    like_persons = models.ManyToManyField(User,blank=True,related_name="like_persons")
    is_anon = models.BooleanField(verbose_name=u'是否匿名',default=False,blank=True)
    alias = models.CharField(verbose_name=u'匿名昵称',max_length=10,null=True,blank=True,default="匿名")
    def __unicode__(self):
        return self.content

class PlanRecord(models.Model):
    '''
        记录
    '''
    plan = models.ForeignKey(Plan,null=False,related_name="plan_record")
    content = models.TextField(verbose_name=u'记录的内容',max_length=1000)
    create_date = models.DateTimeField(auto_now_add=True,editable=True)

    def __unicode__(self):
        return self.content


class Lottery(models.Model):
    '''
        抽奖彩票
    '''
    name = models.CharField(max_length=20,null=True,blank=True)
    person = models.ForeignKey(User,null=False)
    result = models.IntegerField(default=0,editable=False)

    def __unicode__(self):
        return u"%s_%s%s的彩票" %(self.person.szu_name,self.person.szu_ic,self.name)

class LotteryList(models.Model):
    '''
        抽奖名单
    '''
    name = models.CharField(verbose_name=u'名称',max_length=20,null=True,blank=True)
    category = models.ForeignKey(PlanCategory, null=False,related_name="lottery_list")
    lottery = models.ManyToManyField(Lottery,blank=True)
    start_date = models.DateField(verbose_name =u'开启抽奖的时间',blank=False, null=False)
    end_date = models.DateField(verbose_name =u'关闭抽奖的时间',blank=False, null=False)
    is_on = models.BooleanField(verbose_name=u'是否开启',default=False,blank=True)

    def __unicode__(self):
        return u"%s_%s抽奖名单" %(self.category.name,self.name)
