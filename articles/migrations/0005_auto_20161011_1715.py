# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-11 23:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_pressrelease_p_tag_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='pressrelease',
            name='p_tag_text_char_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pressrelease',
            name='p_tag_text_word_count',
            field=models.IntegerField(default=0),
        ),
    ]
