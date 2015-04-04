# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitecheck', '0001_initial'),
        ('tlssite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitecheck',
            name='site',
            field=models.ForeignKey(related_name='checks', to='tlssite.Site'),
            preserve_default=True,
        ),
    ]
