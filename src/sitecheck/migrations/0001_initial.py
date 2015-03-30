# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteCheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('urgent', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField(null=True)),
                ('status', models.TextField(null=True)),
                ('finish_time', models.DateTimeField(null=True)),
                ('json_result', models.TextField(null=True)),
                ('status_message', models.TextField(null=True)),
            ],
            options={
                'ordering': ['-finish_time'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteCheckResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('serverip', models.GenericIPAddressField(null=True, unpack_ipv4=True)),
                ('serverhostname', models.TextField(null=True)),
                ('grade', models.CharField(max_length=2, null=True)),
                ('status_message', models.TextField(null=True)),
                ('status_details_message', models.TextField(null=True)),
                ('sitecheck', models.ForeignKey(related_name='results', to='sitecheck.SiteCheck')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
