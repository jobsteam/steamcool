# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-17 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0026_auto_20171216_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_special_block_1',
            field=models.BooleanField(default=False, verbose_name='Специальный блок №1'),
        ),
    ]
