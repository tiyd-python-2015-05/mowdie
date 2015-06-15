# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150615_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followed',
            field=models.ManyToManyField(related_name='followers', to='users.Profile'),
        ),
    ]
