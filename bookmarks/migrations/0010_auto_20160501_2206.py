# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 20:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0009_bookmarkcomment_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmarkcomment',
            name='bookmark',
        ),
        migrations.RemoveField(
            model_name='bookmarkcomment',
            name='user',
        ),
        migrations.DeleteModel(
            name='BookmarkComment',
        ),
    ]