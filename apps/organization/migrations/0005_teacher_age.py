# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-08 17:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_teacher_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(default=20, verbose_name='\u8bb2\u5e08\u5e74\u9f84'),
        ),
    ]
