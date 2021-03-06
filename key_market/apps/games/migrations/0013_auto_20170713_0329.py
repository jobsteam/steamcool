# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-13 00:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0012_auto_20170708_0218'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='hdd',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='Жесткий диск'),
        ),
        migrations.AddField(
            model_name='game',
            name='os',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='ОС'),
        ),
        migrations.AddField(
            model_name='game',
            name='ozu',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='Оперативная память'),
        ),
        migrations.AddField(
            model_name='game',
            name='processor',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Процессор'),
        ),
        migrations.AddField(
            model_name='game',
            name='video_card',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Видеокарта'),
        ),
    ]
