# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 20:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookmarks', '0010_auto_20160501_2206'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookmarkComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('bookmark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmark_comments', to='bookmarks.SharedBookmark')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
