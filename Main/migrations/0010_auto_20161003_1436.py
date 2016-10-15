# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-03 09:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0009_userdetails_flag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='flag',
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
