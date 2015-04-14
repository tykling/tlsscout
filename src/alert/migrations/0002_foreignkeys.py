# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupalert',
            name='group',
            field=models.ForeignKey(related_name='alerts', to='group.Group', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sitealert',
            name='site',
            field=models.ForeignKey(related_name='alerts', to='tlssite.Site', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tagalert',
            name='tag',
            field=models.ForeignKey(related_name='alerts', to='taggit.Tag', null=True),
            preserve_default=True,
        ),
    ]
