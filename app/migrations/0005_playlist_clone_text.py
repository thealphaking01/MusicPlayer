# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-07 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20160407_0604'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='clone_text',
            field=models.TextField(default='', max_length=255),
        ),
    ]
