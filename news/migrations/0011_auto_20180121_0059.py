# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-20 16:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_auto_20180120_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsindexpage',
            name='intro',
            field=models.CharField(max_length=250),
        ),
    ]