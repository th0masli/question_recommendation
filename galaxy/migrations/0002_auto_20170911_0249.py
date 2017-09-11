# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galaxy',
            name='post_img',
            field=models.CharField(max_length=128),
        ),
    ]
