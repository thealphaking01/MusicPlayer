# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-07 17:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20160407_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Member')),
            ],
            options={
                'db_table': 'rating',
            },
        ),
        migrations.AlterField(
            model_name='playlist',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='rate',
            name='playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Playlist'),
        ),
    ]