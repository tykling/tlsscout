# -*- coding: utf-8 -*-


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
            field=models.ForeignKey(related_name='checks', to='tlssite.Site', on_delete=models.PROTECT),
            preserve_default=True,
        ),
    ]
