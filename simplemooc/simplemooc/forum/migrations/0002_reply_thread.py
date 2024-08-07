# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2024-01-15 01:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='thread',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='forum.Thread', verbose_name='Tópico'),
            preserve_default=False,
        ),
    ]