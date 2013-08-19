from django.db import models

from stucampus.account.models import Student


class Category(models.Model):
    name = models.CharField(max_length=20)
    url_name = models.CharField(max_length=50)
    link_address = models.URLField(max_length=150)
    parent_category = models.ForeignKey('self')


class Article(models.Model):
    title = models.CharField(max_length=50)
    summary = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, related_name="category_id")
    source_name = models.CharField(max_length=100)
    source_url = models.URLField()
    cover_image = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    creater = models.ForeignKey(Student)
    creater_ip = models.IPAddressField()
    click_count = models.IntegerField()
    is_post = models.BooleanField()
    is_delete = models.BooleanField()
    is_important = models.BooleanField()
