# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-29 17:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20170529_1733'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='image',
            new_name='Image',
        ),
    ]