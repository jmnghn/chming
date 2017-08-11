# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 14:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group', '0007_auto_20170811_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='member',
            field=models.ManyToManyField(related_name='joined_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
