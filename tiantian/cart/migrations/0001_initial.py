# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-16 12:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0001_initial'),
        ('page', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cartinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('goodsinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods_info')),
                ('userInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page.userinfo')),
            ],
        ),
    ]
