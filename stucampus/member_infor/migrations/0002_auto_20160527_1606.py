# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-05-27 08:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member_infor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='deleted',
        ),
        migrations.AlterField(
            model_name='member',
            name='szu_no',
            field=models.CharField(max_length=10, unique=True, verbose_name='\u5b66\u53f7'),
        ),
    ]
