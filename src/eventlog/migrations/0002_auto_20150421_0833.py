# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventlog', '0001_squashed_0002_auto_20150419_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='username',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
