# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-11 17:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('post', '0006_posttagindexpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'verbose_name_plural': 'blog categories',
            },
        ),
        migrations.AddField(
            model_name='postpagetag',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='post.PostCategory'),
        ),
    ]