# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-19 22:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Band',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('musicbrainid', models.CharField(max_length=1000)),
                ('setlistfmwebsite', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='GoogleReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('rating', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('band', models.ManyToManyField(to='venue.Band')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_rating', models.IntegerField()),
                ('how_well_was_the_show_advertised', models.IntegerField(blank=True, null=True)),
                ('did_the_promoter_pay_as_agreed', models.IntegerField(blank=True, null=True)),
                ('manager_and_staff', models.IntegerField(blank=True, null=True)),
                ('sound', models.IntegerField(blank=True, null=True)),
                ('lights', models.IntegerField(blank=True, null=True)),
                ('audience', models.IntegerField(blank=True, null=True)),
                ('green_room', models.IntegerField(blank=True, null=True)),
                ('how_well_did_they_follow_the_rider', models.IntegerField(blank=True, null=True)),
                ('parking', models.IntegerField(blank=True, null=True)),
                ('neighborhood', models.IntegerField(blank=True, null=True)),
                ('comments', models.TextField(max_length=100000)),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('showdate', models.DateField()),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venue.Band')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('city', models.CharField(max_length=1000)),
                ('state', models.CharField(max_length=1000)),
                ('statecode', models.CharField(max_length=1000)),
                ('setlistfmwebsite', models.CharField(max_length=1000)),
                ('setlistfmidcode', models.CharField(max_length=1000)),
                ('fmlat', models.CharField(max_length=1000)),
                ('fmlong', models.CharField(max_length=1000)),
                ('googleid', models.CharField(max_length=1000)),
                ('googlename', models.CharField(max_length=1000)),
                ('googleaddress', models.CharField(max_length=1000)),
                ('googlephone', models.CharField(max_length=1000)),
                ('googlewebsite', models.CharField(max_length=1000)),
                ('googlehours', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='show',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venue.Venue'),
        ),
        migrations.AddField(
            model_name='review',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venue.Venue'),
        ),
        migrations.AddField(
            model_name='googlereview',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venue.Venue'),
        ),
        migrations.AddField(
            model_name='band',
            name='venue',
            field=models.ManyToManyField(through='venue.Show', to='venue.Venue'),
        ),
    ]
