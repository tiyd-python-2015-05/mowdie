# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('updates', '0004_auto_20150611_0319'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='favorited_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='favorited_updates', through='updates.Favorite'),
        ),
    ]
