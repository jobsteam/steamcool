# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-23 14:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0047_auto_20191223_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='partner_title',
            field=models.IntegerField(blank=True, choices=[(1, 'steambuy.com'), (2, 'sfera2002 на plati.ru')], db_index=True, null=True, verbose_name='Название партнера'),
        ),
    ]