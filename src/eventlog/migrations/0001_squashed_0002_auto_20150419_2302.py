# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [('eventlog', '0001_initial'), ('eventlog', '0002_auto_20150419_2302')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(max_length=50)),
                ('event', models.TextField()),
                ('username', models.CharField(default='homo', max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
