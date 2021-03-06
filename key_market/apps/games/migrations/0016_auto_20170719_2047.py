# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-19 17:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0015_auto_20170719_2041'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='screenshot',
            options={'ordering': ['title'], 'verbose_name': 'Скриншот', 'verbose_name_plural': 'Скриншоты'},
        ),
        migrations.AddField(
            model_name='game',
            name='screenshot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='screenshots', to='games.Screenshot', verbose_name='Скриншоты'),
        ),
    ]
