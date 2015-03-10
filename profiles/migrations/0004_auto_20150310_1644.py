# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profilepasskeys'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='profilepasskeys',
            unique_together=set([('profile', 'user')]),
        ),
    ]
