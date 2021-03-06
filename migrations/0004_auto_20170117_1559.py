# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-17 05:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pydash', '0003_auto_20170112_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aquarium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frontlight', models.BooleanField(verbose_name='Front Light On')),
                ('rearlight', models.BooleanField(verbose_name='Rear Light On')),
                ('circpump', models.BooleanField(verbose_name='Circulation Pump On')),
                ('co2', models.BooleanField(verbose_name='CO2 On')),
                ('filter', models.BooleanField(verbose_name='Filter On')),
                ('accent', models.BooleanField(verbose_name='LED Accent Light On')),
            ],
        ),
        migrations.AlterModelOptions(
            name='measurement',
            options={'get_latest_by': 'date'},
        ),
    ]
