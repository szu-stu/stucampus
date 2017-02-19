#coding:utf-8
from django.db import models

# Create your models here.

Gender = (
    ('M', u'男'),
    ('F', u'女')
)

class CommentUser(models.Model):
    name = models.CharField(u'姓名', max_length=20)
    nick = models.CharField(u'昵称', max_length=20, default='stu_user~')
    stu_no = models.CharField(u'学号', max_length=10)
    gender = models.CharField(u'性别', choices=Gender, max_length=1, default='M')
    collega = models.CharField(u'学院', max_length=20)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'评论用户'
        verbose_name_plural = verbose_name

class Comment(models.Model):
    content = models.TextField(u'评论内容', max_length=200)
    user = models.ForeignKey("CommentUser")
    create_time = models.DateField(u'创建日期', auto_now_add=True)
    create_ip = models.GenericIPAddressField(editable=False, null=True, blank=True)
    article = models.CharField(u'文章ID', max_length=6)
    def __unicode__(self):
        return self.content[0:3] + '>>>'

    class Meta:
        verbose_name = u'评论'
        verbose_name_plural = verbose_name

