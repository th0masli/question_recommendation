# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0005_auto_20170911_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galaxy',
            name='question_ids',
            field=models.CharField(max_length=64),
        ),
    ]
