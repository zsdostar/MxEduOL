# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-17 11:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='learn_name',
            new_name='learn_time',
        ),
    ]