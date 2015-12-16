# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-15 21:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('browsers', '0001_initial'),
        ('partners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=False)),
                ('scheduling_interval', models.PositiveSmallIntegerField()),
                ('browsers', models.ManyToManyField(to='browsers.Browser')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partners.Partner')),
            ],
        ),
    ]