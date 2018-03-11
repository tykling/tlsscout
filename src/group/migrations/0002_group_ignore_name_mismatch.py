# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='ignore_name_mismatch',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
