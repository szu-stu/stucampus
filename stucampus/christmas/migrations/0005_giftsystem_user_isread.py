# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-12-07 09:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('christmas', '0004_gift_isdelete'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftsystem_user',
            name='isRead',
            field=models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe9\x98\x85\xe8\xaf\xbb\xe5\x85\x8d\xe8\xb4\xa3\xe5\xa3\xb0\xe6\x98\x8e'),
        ),
    ]