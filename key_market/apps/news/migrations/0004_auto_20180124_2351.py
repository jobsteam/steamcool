# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-24 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20180124_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(blank=True, max_length=254, verbose_name='slug'),
        ),
    ]
