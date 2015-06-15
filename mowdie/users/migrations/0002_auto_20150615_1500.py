# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birthday',
            field=models.DateField(null=True, validators=[users.models.validate_date_in_past], blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='url',
            field=models.URLField(null=True, blank=True, verbose_name='Personal URL (homepage/blog)', max_length=255),
        ),
    ]
