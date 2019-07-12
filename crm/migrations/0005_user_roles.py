# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-07-09 10:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
        ('crm', '0004_auto_20190708_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(to='rbac.Role', verbose_name='用户拥有的角色'),
        ),
    ]