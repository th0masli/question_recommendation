# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0003_auto_20170911_0338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galaxy',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
