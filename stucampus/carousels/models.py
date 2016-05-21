#-*- coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from stucampus.custom.qiniu import upload_content_img_to_qiniu, upload_img

class Slide(models.Model):

    class Meta:
        permissions = (
            ('slide_add', u'首页焦点图添加'),
            ('slide_manage', u'首页焦点图管理'),
        )
    
    title = models.CharField(max_length=30)
    cover = models.ImageField(max_length=200)
    describe = models.CharField(max_length=64)
    
    jumpUrl = models.URLField(blank=True, null=True)
    priority = models.PositiveIntegerField(verbose_name=u'优先级',default=5)
    published = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    author = models.ForeignKey(User,related_name=u'author',verbose_name=u'创建者')
    createDate = models.DateField(auto_now_add=True,editable=True)
    modifier = models.ForeignKey(User,related_name=u'last_modifier',verbose_name=u'最后修改者')
    lastModify = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        '''
        数据库保存的时候，会自动上传图片到七牛
        参考jimczj在stucampus.articles.models上写的
        '''
        if self.cover:
            self.cover.name = upload_img(unicode(self.cover)) 
            
        super(Slide, self).save(*args, **kwargs)
