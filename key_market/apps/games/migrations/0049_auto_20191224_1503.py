# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-24 12:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0048_auto_20191223_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='seo_description',
        ),
        migrations.RemoveField(
            model_name='game',
            name='seo_keywords',
        ),
        migrations.RemoveField(
            model_name='game',
            name='seo_title',
        ),
        migrations.RemoveField(
            model_name='game',
            name='slide_text',
        ),
    ]
