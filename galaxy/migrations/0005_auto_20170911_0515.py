# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0004_auto_20170911_0358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='galaxy',
            old_name='question_id',
            new_name='question_ids',
        ),
    ]
