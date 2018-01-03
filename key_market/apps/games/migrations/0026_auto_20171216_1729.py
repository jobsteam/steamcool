# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-16 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0025_auto_20171106_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_soon',
            field=models.BooleanField(default=False, verbose_name='Скоро в продаже'),
        ),
        migrations.AlterField(
            model_name='game',
            name='sa_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Steam-Account id_d'),
        ),
        migrations.AlterField(
            model_name='game',
            name='zz_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Zaka-Zaka id_d'),
        ),
    ]
