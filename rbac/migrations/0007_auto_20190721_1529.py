# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-07-21 07:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0006_menu_wight'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='wight',
            new_name='weight',
        ),
    ]
