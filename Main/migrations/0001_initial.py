# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-01 09:29
from __future__ import unicode_literals

import Main.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense', models.FloatField(default=0)),
                ('income', models.FloatField(default=0)),
                ('user', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategories', models.CharField(max_length=15)),
                ('source', models.CharField(max_length=15)),
                ('paid_to', models.CharField(max_length=50)),
                ('cost', models.IntegerField()),
                ('tax_details', models.FloatField()),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('bill', models.FileField(blank=True, null=True, upload_to='bills')),
                ('vat', models.CharField(blank=True, max_length=50, null=True)),
                ('ext_ref', models.CharField(blank=True, max_length=10, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('is_recurrent', models.CharField(max_length=10)),
                ('rec_date', models.DateField(default=django.utils.timezone.now)),
                ('rec_year', models.IntegerField(blank=True, null=True)),
                ('rec_month', models.IntegerField(blank=True, null=True)),
                ('rec_day', models.IntegerField(blank=True, null=True)),
                ('option', models.CharField(max_length=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),

        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('dob', models.DateField(null=True)),
                ('address', models.CharField(max_length=100)),
                ('hire_date', models.DateField(null=True)),
                ('phone_no', models.IntegerField()),
                ('photo', models.ImageField(null=True, upload_to='profile')),
                ('occupation', models.CharField(max_length=15)),
                ('yearly_package', models.PositiveIntegerField(null=True)),
                ('pf', models.PositiveIntegerField(default=5)),
                ('res_address', models.CharField(max_length=100)),
                ('user', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
