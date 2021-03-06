# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-11-01 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('professionId', models.IntegerField()),
                ('courseNum', models.CharField(max_length=50)),
                ('courseName', models.CharField(max_length=200)),
                ('courseNameEN', models.CharField(max_length=200)),
                ('courseType', models.CharField(max_length=50)),
                ('credit', models.FloatField()),
                ('suggestion', models.IntegerField()),
                ('creditType', models.CharField(max_length=10)),
                ('remark', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='MCCourses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseNum', models.CharField(max_length=100)),
                ('courseName', models.CharField(max_length=200)),
                ('credit', models.FloatField()),
                ('creditType', models.CharField(max_length=10)),
                ('remark', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('professionId', models.IntegerField()),
                ('publicRequired', models.FloatField()),
                ('professionalRequired', models.FloatField()),
                ('elective', models.FloatField()),
                ('professionalElective', models.FloatField()),
                ('artsStream', models.FloatField(blank=True, null=True)),
                ('scienceStream', models.FloatField(blank=True, null=True)),
                ('practice', models.FloatField()),
                ('minorRemark', models.CharField(blank=True, max_length=1000, null=True)),
                ('doubleRemark', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Professions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField()),
                ('college', models.CharField(max_length=100)),
                ('profession', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=200)),
            ],
        ),
    ]
