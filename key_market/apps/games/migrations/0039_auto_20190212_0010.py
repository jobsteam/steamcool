# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-02-11 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0038_remove_game_is_case'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='is_favorite',
        ),
        migrations.AddField(
            model_name='game',
            name='on_main_page',
            field=models.BooleanField(default=False, verbose_name='Показать на главной'),
        ),
    ]