# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-21 01:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('f_wheelsize', models.IntegerField()),
                ('f_width', models.FloatField()),
                ('f_offset', models.IntegerField()),
                ('f_tiresize', models.CharField(max_length=10)),
                ('r_wheelsize', models.IntegerField(null=True)),
                ('r_width', models.FloatField(null=True)),
                ('r_offset', models.IntegerField(null=True)),
                ('r_tiresize', models.CharField(max_length=10, null=True)),
                ('suspension', models.BooleanField()),
                ('suspensionInfo', models.CharField(blank=True, max_length=70)),
                ('spacer', models.BooleanField()),
                ('spacerInfo', models.CharField(blank=True, max_length=70)),
                ('fab', models.BooleanField()),
                ('fabInfo', models.CharField(blank=True, max_length=70)),
                ('date', models.DateField()),
                ('valid', models.BooleanField()),
                ('email', models.EmailField(blank=True, max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='CarImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to=b'images/')),
                ('thumb', models.ImageField(upload_to=b'images/thumbnails/')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drivefitwheelsapp.Car')),
            ],
        ),
    ]
