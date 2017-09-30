# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-29 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Friendships',
            new_name='Friendship',
        ),
        migrations.RemoveField(
            model_name='member',
            name='friendships',
        ),
        migrations.AddField(
            model_name='member',
            name='friends',
            field=models.ManyToManyField(related_name='friendswith', through='login.Friendship', to='login.Member'),
        ),
    ]
