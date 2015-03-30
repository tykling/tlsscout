# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sitecheck', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiClientState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sleep_until', models.DateTimeField(null=True)),
                ('max_concurrent_assessments', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequestLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('uuid', uuidfield.fields.UUIDField(max_length=32)),
                ('request_url', models.CharField(max_length=1000)),
                ('request_headers', models.TextField()),
                ('request_body', models.TextField(null=True)),
                ('response_code', models.IntegerField(null=True)),
                ('response_headers', models.TextField(null=True)),
                ('response_body', models.TextField(null=True)),
                ('sitecheck', models.ForeignKey(related_name='requestlogs', to='sitecheck.SiteCheck', null=True)),
            ],
            options={
                'ordering': ['-datetime'],
            },
            bases=(models.Model,),
        ),
    ]
