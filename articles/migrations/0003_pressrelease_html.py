# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-09 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20160930_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='pressrelease',
            name='html',
            field=models.TextField(default=b''),
        ),
    ]
