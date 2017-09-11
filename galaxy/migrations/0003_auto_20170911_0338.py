# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0002_auto_20170911_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galaxy',
            name='question_id',
            field=models.CharField(max_length=32),
        ),
    ]
