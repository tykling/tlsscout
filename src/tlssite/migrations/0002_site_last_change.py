# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tlssite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='last_change',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
