# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 7, 5, 12, 4, 891546, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 7, 5, 12, 10, 742498, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=models.SlugField(default=b'', editable=False),
            preserve_default=True,
        ),
    ]
