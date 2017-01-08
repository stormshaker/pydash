# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-08 06:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('roomtemp', models.DecimalField(decimal_places=2, max_digits=4)),
                ('roomhumidity', models.DecimalField(decimal_places=2, max_digits=4)),
                ('watertemp', models.DecimalField(decimal_places=2, max_digits=4)),
                ('ph', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
    ]
