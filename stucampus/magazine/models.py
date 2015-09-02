#-*- coding: utf-8
import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

from stucampus.custom.models_utils import file_save_path
from stucampus.custom.validator import validate_file_extension


def save_path(instance, filename):
    return os.path.join('magazine', instance.name, filename)


class Magazine(models.Model):

    class Meta:
        permissions = (
            ('magazine_add', u'添加杂志'),
            ('magazine_modify', u'编辑杂志'),
        )

    name = models.CharField(max_length=30)
    title = models.CharField(max_length=40)
    issue = models.IntegerField()
    summary = models.CharField(max_length=300, null=True, blank=True)
    pdf_file = models.FileField(upload_to=save_path,
                                validators=[validate_file_extension('pdf')])

    create_date = models.DateField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)


@receiver(post_delete, sender=Magazine)
def Magazine_delete(sender, instance, **kwargs):
    if instance.pdf_file:
        instance.pdf_file.delete(False)