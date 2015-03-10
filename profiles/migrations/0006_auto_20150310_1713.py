# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profiles',
            field=models.ManyToManyField(help_text=b'the list of profiles which can be changed by user', to='profiles.Profile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_admin',
            field=models.BooleanField(default=False, help_text=b'define is user can assign profiles to users'),
            preserve_default=True,
        ),
    ]
