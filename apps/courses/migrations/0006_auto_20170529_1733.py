# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-29 17:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_course_org'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='Image',
            new_name='image',
        ),
    ]
