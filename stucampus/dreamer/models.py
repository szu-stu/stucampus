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
    ('--' ,u'--'),
)

class Register(models.Model):
    class Meta:
        permissions = (
            ('manager', u'报名信息管理员'),
        )
    name = models.CharField(verbose_name="姓名",max_length = 20,blank=True,null=True)
    gender = models.CharField(verbose_name="性别",max_length = 6, choices = SEX, default="male",blank=True,null=True)
    stu_ID = models.CharField(verbose_name="学号",max_length = 10,blank=True,null=True)
    college = models.CharField(verbose_name="学院",max_length = 30,blank=True,null=True)
    mobile = models.CharField(verbose_name="手机",max_length = 11,blank=True,null=True)
    dept1 = models.CharField(verbose_name="第一志愿",max_length = 4, choices=DEPT, default=u"cbb")
    dept2 = models.CharField(verbose_name="第二志愿",max_length = 4, choices=DEPT, default=u"--",blank=True,null=True)
    sign_up_date = models.DateField(auto_now_add=True,editable=True)
    self_intro = models.CharField(verbose_name="自我介绍",max_length = 500,blank=True,null=True)
    grade = models.CharField(verbose_name="年级",max_length=4,blank=True,null=True)
    email = models.EmailField(verbose_name="email",null=True,blank=True)
    status = models.BooleanField(verbose_name="是否删除",default=True)

    def __unicode__(self):
        return self.name

	


