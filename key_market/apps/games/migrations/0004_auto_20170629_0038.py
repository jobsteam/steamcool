# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-28 21:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_game_store_activation'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='method_activation',
            field=models.IntegerField(blank=True, choices=[(1, 'steam gift'), (2, 'origin key'), (3, 'origin key'), (4, 'uplay key')], db_index=True, null=True, verbose_name='способ активации'),
        ),
        migrations.AlterField(
            model_name='game',
            name='language',
            field=models.IntegerField(blank=True, choices=[(1, 'русский'), (2, 'английский')], db_index=True, null=True, verbose_name='Язык'),
        ),
        migrations.AlterField(
            model_name='game',
            name='store_activation',
            field=models.IntegerField(blank=True, choices=[(1, 'steam'), (2, 'origin'), (3, 'uplay')], db_index=True, null=True, verbose_name='активация'),
        ),
    ]
