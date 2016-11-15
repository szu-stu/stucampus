#coding:utf-8
from django.db import models

# Create your models here.
class Item(models.Model):
    UID = models.IntegerField('公文通编号')
    type = models.CharField('类别', max_length=10)
    unit = models.CharField('发文单位', max_length=20)
    title = models.CharField('标题', max_length=100)
    date = models.DateField('日期')
    content = models.CharField('内容', max_length=50000)
    isShow = models.BooleanField('是否展示', default=False)
    isTop = models.BooleanField('是否置顶', default=False)
    hasFile = models.BooleanField('是否有附件', default=False)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = '标题'
        verbose_name_plural = verbose_name
        ordering = ['-date']
        permissions = (
            ('manager', u'公文通信息管理员'),
        )

