#-*- coding: utf-8


from django.db import models
from django.contrib.auth.models import User

from DjangoUeditor.models import UEditorField


from stucampus.custom.qiniu import upload_content_img_to_qiniu, upload_img


class Category(models.Model):
    name = models.CharField(verbose_name=u'分类名',
                            max_length=30, unique=True)
    english_name = models.CharField(max_length=20, unique=True)
    # priority 越小，越先放在前面
    priority = models.PositiveIntegerField(verbose_name=u'优先级')

    # used in ArticleForm.category to display category name in template
    def __unicode__(self):
        return self.name


class Article(models.Model):

    class Meta:
        permissions = (
            ('article_add', u'添加文章'),
            ('article_manage', u'编审文章'),
        )

    title = models.CharField(max_length=20)
    summary = models.CharField(max_length=50)
    content = UEditorField(height=500, width=900, toolbars='full')
    category = models.ForeignKey(Category, null=True,
                                 on_delete=models.SET_NULL)

    author = models.CharField(max_length=30)
    editor = models.ForeignKey(User)
    source = models.CharField(max_length=50, blank=True, null=True)
    source_link = models.URLField(blank=True, null=True)
    cover = models.ImageField(max_length=200,default="default_cover.png")
    create_date = models.DateField(auto_now_add=True,editable=True)
    modify_date = models.DateField(auto_now=True)
    create_ip = models.GenericIPAddressField(editable=False,null=True)
    click_count = models.IntegerField(default=0, editable=False)
    deleted = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    publish = models.BooleanField(default=False)
    likes=models.IntegerField(default=0,blank=True,null=True)#该字段由多说负责
    comments=models.IntegerField(default=0,blank=True,null=True)#该字段由多说负责

    def save(self, *args, **kwargs):
        '''
        数据库保存的时候，会自动上传图片到七牛
        @author:jimczj
        '''
        if self.content:
            self.content = upload_content_img_to_qiniu(unicode(self.content))

        super(Article, self).save(*args, **kwargs)

        if self.cover:
            upload_img(unicode(self.cover)) 
        

