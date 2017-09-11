# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Galaxy',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('ip', models.CharField(max_length=16)),
                ('post_img', models.CharField(max_length=32)),
                ('question_id', models.IntegerField()),
                ('upload_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'user_data',
            },
        ),
    ]
