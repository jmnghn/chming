# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-14 04:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_date']},
        ),
        migrations.RenameField(
            model_name='post',
            old_name='modified_d_date',
            new_name='modified_date',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='img',
            new_name='post_img',
        ),
    ]
