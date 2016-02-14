# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-14 15:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='WorkItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, help_text='Unique reference to the item in your ticket tracker (JIRA Key, Story number, etc.)', max_length=255)),
                ('queued_at', models.DateTimeField(help_text='When did the team commit to doing the work item?')),
                ('issue_type', models.CharField(blank=True, db_index=True, help_text='Story, bug, epic, etc.', max_length=255, null=True)),
                ('started_at', models.DateTimeField(blank=True, help_text='When did the team start working on the item?', null=True)),
                ('ended_at', models.DateTimeField(blank=True, help_text='When did the team complete work on the item?', null=True)),
                ('effort_score', models.IntegerField(blank=True, help_text='Story points, estimated hours, etc.', null=True)),
                ('impact_score', models.IntegerField(blank=True, help_text='Dollar value, bug impact, etc.', null=True)),
                ('_cycle_time', models.DurationField(blank=True, db_column='cycle_time', help_text='Time between ended_at and started_at', null=True)),
                ('_lead_time', models.DurationField(blank=True, db_column='lead_time', help_text='Time between ended_at and queued_at', null=True)),
                ('_week_queued_at', models.DateField(blank=True, help_text='The Sunday of the week the team committed to doing the work item?', null=True)),
                ('_week_started_at', models.DateField(blank=True, help_text='The Sunday of the week the team start working on the item', null=True)),
                ('_week_ended_at', models.DateField(blank=True, help_text='The Sunday of the week the team compelted working on the item', null=True)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work.DataSet')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='workitem',
            unique_together=set([('key', 'dataset')]),
        ),
    ]
