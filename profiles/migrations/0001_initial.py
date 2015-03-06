# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(default=b'')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(default=b'')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
