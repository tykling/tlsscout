# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group', '0001_initial'),
        ('tlssite', '0002_site_last_change'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('html', models.TextField()),
                ('site', models.ForeignKey(to='tlssite.Site', on_delete=models.PROTECT)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupAlert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.ForeignKey(to='group.Group', null=True, on_delete=models.PROTECT)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteAlert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site', models.ForeignKey(to='tlssite.Site', null=True, on_delete=models.PROTECT)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagAlert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.ForeignKey(to='taggit.Tag', null=True, on_delete=models.PROTECT)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
