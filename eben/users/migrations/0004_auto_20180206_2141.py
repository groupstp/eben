# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-06 13:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180206_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='avatars/%Y/%m/%d/', verbose_name='Picture of User'),
        ),
    ]