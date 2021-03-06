# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-06 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0023_game_in_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='method_activation',
            field=models.IntegerField(blank=True, choices=[(1, 'steam gift'), (2, 'steam key'), (3, 'origin key'), (4, 'uplay key'), (5, 'rockstar key')], db_index=True, null=True, verbose_name='способ активации'),
        ),
        migrations.AlterField(
            model_name='game',
            name='store_activation',
            field=models.IntegerField(blank=True, choices=[(1, 'steam'), (2, 'origin'), (3, 'uplay'), (4, 'rockstar')], db_index=True, null=True, verbose_name='активация'),
        ),
    ]
