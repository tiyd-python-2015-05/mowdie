# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name_plural': 'statuses'},
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together=set([('user', 'status')]),
        ),
    ]
