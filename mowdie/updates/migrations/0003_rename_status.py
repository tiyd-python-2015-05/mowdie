# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('updates', '0002_auto_20150610_1434'),
    ]

    operations = [
        migrations.RenameModel('Status', 'Update'),
        migrations.AlterField(
            model_name='favorite',
            name='status',
            field=models.ForeignKey(to='updates.Update'),
        ),
        migrations.RenameField(
            model_name='favorite',
            old_name='status',
            new_name='update'
        ),
    ]
