# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 07:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('summarizer', '0004_auto_20171030_2344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='summarize',
            name='urlid',
        ),
    ]
