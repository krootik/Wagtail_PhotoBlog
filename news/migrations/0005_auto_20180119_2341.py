# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-19 15:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20180119_2317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newspagegalleryimage',
            name='image',
        ),
        migrations.RemoveField(
            model_name='newspagegalleryimage',
            name='page',
        ),
        migrations.DeleteModel(
            name='NewsPageGalleryImage',
        ),
    ]
