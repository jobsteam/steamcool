# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-10 17:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0017_auto_20170720_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='slug',
            field=models.SlugField(blank=True, verbose_name='slug'),
        ),
    ]
