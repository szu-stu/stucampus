#-*- coding: utf-8
from django.db import models
from django.contrib.auth.models import User

from DjangoUeditor.models import UEditorField

from stucampus.custom.models_utils import file_save_path


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
    content = UEditorField(height=500, width=300, toolbars='mini')
    category = models.ForeignKey(Category, null=True,
                                 on_delete=models.SET_NULL)

    author = models.CharField(max_length=30)
    editor = models.ForeignKey(User)
    source = models.CharField(max_length=50, blank=True, null=True)
    source_link = models.URLField(blank=True, null=True)
    cover = models.CharField(max_length=200, blank=True, null=True)

    create_date = models.DateField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)
    create_ip = models.IPAddressField(editable=False)
    click_count = models.IntegerField(default=0, editable=False)
    deleted = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    publish = models.BooleanField(default=False)

