# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-09-07 21:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0033_game_image_banner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='is_special_block',
            new_name='is_special_block_1',
        ),
    ]
